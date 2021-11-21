from extension import db, cache
from flask_restful import Resource
from flask import request
from models.user import User
from http import HTTPStatus
from marshmallow import ValidationError
from utils import verify_password, clear_cache
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from models.token_blocklist import TokenBlockList
from schema.user import UserSchema


class CreateUserResource(Resource):
    def post(self):
        json_data = request.get_json()
        try:
            data = UserSchema().load(json_data)
        except ValidationError as error:
            return {
                "message": "Validation Error",
                "errors": error.messages
            }, HTTPStatus.BAD_REQUEST

        if User.get_by_username(data["username"]):
            return {"message": "username already exists"}, HTTPStatus.BAD_REQUEST

        if User.get_by_email(data["email"]):
            return {"message": "email address already registered to a different user"}, HTTPStatus.BAD_REQUEST

        if User.get_by_phone_number(data["phone_number"]):
            return {"message": "phone number already registered to a different user"}, HTTPStatus.BAD_REQUEST

        user = User(**data)

        db.session.add(user)
        db.session.commit()
        access_token = create_access_token(identity=user.id)
        return {"access_token": access_token}, HTTPStatus.CREATED


class LoginResource(Resource):
    def post(self):
        json_data = request.get_json()
        try:
            UserSchema(exclude=("email", "phone_number",)).load(json_data)
        except ValidationError as err:
            return {
                "message": "Validation Error",
                "error": err.messages
            }, HTTPStatus.BAD_REQUEST

        username = json_data.get("username")
        password = json_data.get("password")
        user = User.get_by_username(username)
        if (not user) or (not user.status):
            return {"error": "User not found"}, HTTPStatus.NOT_FOUND
        if not verify_password(password, user.password):
            return {"error": "Incorrect password or username"}, HTTPStatus.BAD_REQUEST
        access_token = create_access_token(identity=user.id)
        return {"access_token": access_token}, HTTPStatus.OK


class UserResource(Resource):
    @jwt_required()
    @cache.cached(timeout=300)
    def get(self):
        current_user_id = get_jwt_identity()
        user = User.get_by_id(id=current_user_id)
        return UserSchema(exclude=("id",)).dump(user), HTTPStatus.OK

    @jwt_required()
    def patch(self):
        json_data = request.get_json()
        try:
            data = UserSchema(partial=True, exclude=("password", )).load(json_data)
        except ValidationError as err:
            return {
                "message": "Validation Error",
                "error": err.messages
            }

        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        username = data.get("username") or user.username
        email = data.get("email") or user.email
        phone_number = data.get("phone_number") or user.phone_number
        if user.username == username is False and User.get_by_username(username):
            return {"message": "username already registered to a different user"}, HTTPStatus.BAD_REQUEST
        if user.email == email is False and User.get_by_email(email):
            return {"message": "email address already registered to a different user"}, HTTPStatus.BAD_REQUEST
        if user.phone_number == phone_number is False and User.get_by_phone_number(phone_number):
            return {"message": "phone number already registered to a different user"}, HTTPStatus.BAD_REQUEST

        user.username = username
        user.email = email
        user.phone_number = phone_number
        db.session.commit()
        clear_cache("view//users/info")
        return UserSchema(exclude=("id", )).dump(user), HTTPStatus.OK

    @jwt_required()
    def delete(self):
        current_user_id = get_jwt_identity()
        user = User.get_by_id(id=current_user_id)
        user.status = False
        jti = get_jwt()["jti"]
        db.session.add(TokenBlockList(jti=jti, user=user.username, description="User profile deleted"))
        db.session.commit()
        clear_cache("user")
        return "", HTTPStatus.NO_CONTENT


class UserLogOutResource(Resource):
    @jwt_required()
    def delete(self):
        jti = get_jwt()["jti"]
        user = User.get_by_id(id=get_jwt_identity())
        revoked_token = TokenBlockList(jti=jti, user=user.username, description="User logged out")
        db.session.add(revoked_token)
        db.session.commit()

        return "", HTTPStatus.NO_CONTENT
