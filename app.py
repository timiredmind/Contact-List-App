from extension import db, migrate, jwt
from flask import Flask, make_response, jsonify
from config import Config
from jsonschema import ValidationError
from resources.user import CreateUserResource, LoginResource, UserResource, UserLogOutResource
from flask_restful import Api
from resources.contact import ContactListResource, ContactResource
from models.token_blocklist import TokenBlockList


def register_extension(app):
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)


def register_resource(app):
    api = Api(app)
    api.add_resource(CreateUserResource, "/users/register")
    api.add_resource(LoginResource, "/users/login")
    api.add_resource(UserResource, "/users/info")
    api.add_resource(ContactListResource, "/users/contacts")
    api.add_resource(ContactResource, "/users/contacts/<int:contact_id>")
    api.add_resource(UserLogOutResource, "/users/logout")


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_extension(app)
    register_resource(app)

    @app.errorhandler(400)
    def bad_request(error):
        if isinstance(error.description, ValidationError):
            original_error = error.description
            return make_response(jsonify({"error": original_error.message}), 400)
        return error


    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        token = db.session.query(TokenBlockList.id).filter_by(jti=jti).scalar()
        return token is not None

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
