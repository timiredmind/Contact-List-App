from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.contact import Contact
from models.user import User
from flask import request
from extension import db
from http import HTTPStatus
from schema.contact import ContactSchema
from marshmallow import ValidationError


class ContactListResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        data = Contact.query.filter_by(user_id=current_user_id).all()
        contacts = [contact for contact in data if contact.status]
        return ContactSchema(many=True, only=("id", "name", "phone_number")).dump(contacts), HTTPStatus.OK

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = User.get_by_id(user_id)
        json_data = request.get_json()
        try:
            data = ContactSchema().load(json_data)
        except ValidationError as err:
            return {
                "message": "Validation Error",
                "error": err.messages
            }, HTTPStatus.BAD_REQUEST

        phone_number = data.get("phone_number")

        contacts = Contact.query.filter_by(user_id=user_id).all()
        check_phone_number = next((contact for contact in contacts
                                   if contact.phone_number == phone_number if contact.status), None)

        if check_phone_number:
            return {"message": "phone number has been previously added"}, HTTPStatus.BAD_REQUEST
        new_contact = Contact(**data)

        user.contacts.append(new_contact)
        db.session.commit()
        return ContactSchema().dump(new_contact), HTTPStatus.CREATED


class ContactResource(Resource):
    @jwt_required()
    def get(self, contact_id):
        current_user_id = get_jwt_identity()
        contact = Contact.get_by_contact_id(contact_id)
        if not contact or not contact.status:
            return {"message": f"There is no contact associated with the contact_id {contact_id}"},\
                   HTTPStatus.NOT_FOUND

        if contact.user_id != current_user_id:
            return {"message": "UNAUTHORIZED ACCESS"}, HTTPStatus.UNAUTHORIZED

        return ContactSchema().dump(contact), HTTPStatus.OK

    @jwt_required()
    def patch(self, contact_id):
        current_user_id = get_jwt_identity()
        contact = Contact.get_by_contact_id(contact_id)
        if not contact or not contact.status:
            return {"message": f"There is no contact associated with the contact_id {contact_id}"}, \
                   HTTPStatus.NOT_FOUND

        if contact.user_id != current_user_id:
            return {"message": "UNAUTHORIZED ACCESS"}, HTTPStatus.UNAUTHORIZED

        json_data = request.get_json()
        try:
            data = ContactSchema(partial=True).load(json_data)
        except ValidationError as err:
            return {
                "message": "Validation Error",
                "error": err.messages
            }

        phone_number = json_data.get("phone_number")

        contacts = Contact.query.filter_by(user_id=current_user_id).all()
        check_phone_number = next((contact for contact in contacts if contact.phone_number == phone_number), None)

        if (check_phone_number is not None) and (contact.id != check_phone_number.id) and \
                (check_phone_number.status is True):
            return {"message": "phone number has been registered with another contact"}, HTTPStatus.BAD_REQUEST

        contact.name = data.get("name") or contact.name
        contact.email = data.get("email") or contact.email
        contact.phone_number = data.get("phone_number") or contact.phone_number
        contact.address = data.get("address") or contact.address
        contact.image_url = data.get("image_url") or contact.address

        db.session.commit()
        return ContactSchema().dump(contact), HTTPStatus.OK

    @jwt_required()
    def delete(self, contact_id):
        current_user_id = get_jwt_identity()
        contact = Contact.get_by_contact_id(contact_id)
        if current_user_id != contact.user_id:
            return {"message": "UNAUTHORIZED ACCESS"}, HTTPStatus.UNAUTHORIZED
        contact.status = False
        db.session.commit()
        return "", HTTPStatus.NO_CONTENT
