from extension import db
from flask_restful import Resource
from flask import request
from models.user import User
from http import HTTPStatus
from flask_expects_json import expects_json
from schemas import create_user_schema, login_schema, patch_schema
from utils import generate_hash,verify_password
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from models.token_blocklist import TokenBlockList


class CreateUserResource(Resource):
    @expects_json(create_user_schema)
    def post(self):
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        phone_number = data.get("phone_number")
        password = data.get("password")

        if User.get_by_username(username):
            return {"message": "username already exists"}, HTTPStatus.BAD_REQUEST

        if User.get_by_email(email):
            return {"message": "email address already registered to a different user"}, HTTPStatus.BAD_REQUEST

        if User.get_by_phone_number(phone_number):
            return {"message": "phone number already registered to a different user"}, HTTPStatus.BAD_REQUEST
        password_hash = generate_hash(password)
        try:
            user = User(username=username,
                        email=email,
                        phone_number=phone_number,
                        password=password_hash
                        )

        except Exception as err:
            return {"message": err}, HTTPStatus.BAD_REQUEST

        db.session.add(user)
        db.session.commit()
        access_token = create_access_token(identity=user.id)
        return {"access_token": access_token}, HTTPStatus.CREATED


class LoginResource(Resource):
    @expects_json(login_schema)
    def post(self):
        json_data = request.get_json()
        username = json_data.get("username")
        password = json_data.get("password")
        user = User.get_by_username(username)
        if (not user) or (not user.status):
            return {"error": "User not found"}, HTTPStatus.NOT_FOUND
        if not verify_password(password, user.password):
            return {"error": "Incorrect password and username"}, HTTPStatus.BAD_REQUEST
        access_token = create_access_token(identity=user.id)
        return {"access_token": access_token}, HTTPStatus.OK


class UserResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        user = User.get_by_id(current_user_id)
        return user.data, HTTPStatus.OK

    @jwt_required()
    @expects_json(patch_schema)
    def put(self):
        json_data = request.get_json()
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        username = json_data.get("username")
        email = json_data.get("email")
        phone_number = json_data.get("phone_number")
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

        return user.data, HTTPStatus.OK

    @jwt_required()
    def delete(self):
        current_user_id = get_jwt_identity()
        user = User.get_by_id(id=current_user_id)
        user.status = False
        jti = get_jwt()["jti"]
        db.session.add(TokenBlockList(jti=jti, user=user.username, description="User profile deleted"))
        db.session.commit()

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








