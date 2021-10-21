from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.contact import Contact
from models.user import User
from flask_expects_json import expects_json
from schemas import contact_schema
from flask import request
from extension import db
from http import HTTPStatus


class ContactListResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        contacts = Contact.query.filter_by(user_id=current_user_id).all()
        return {"contacts": [{"id": contact.id, "name": contact.name}
                             for contact in contacts if contact.status is True]}

    @jwt_required()
    @expects_json(contact_schema)
    def post(self):
        user_id = get_jwt_identity()
        user = User.get_by_id(user_id)
        json_data = request.get_json()
        name = json_data.get("name")
        email = json_data.get("email")
        phone_number = json_data.get("phone_number")
        address = json_data.get("address")
        image_url = json_data.get("image_url")

        contacts = Contact.query.filter_by(user_id=user_id).all()
        check_phone_number = next((contact for contact in contacts
                                   if contact.phone_number == phone_number if contact.status), None)

        if check_phone_number:
            return {"message": "phone number has been previously added"}
        new_contact = Contact(
            name=name,
            email=email,
            phone_number=phone_number,
            address=address,
            image_url=image_url
        )
        user.contacts.append(new_contact)
        db.session.commit()
        return new_contact.data, HTTPStatus.CREATED


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

        return contact.data, HTTPStatus.OK

    @jwt_required()
    @expects_json(contact_schema)
    def put(self, contact_id):
        current_user_id = get_jwt_identity()
        contact = Contact.get_by_contact_id(contact_id)
        if not contact or not contact.status:
            return {"message": f"There is no contact associated with the contact_id {contact_id}"}, \
                   HTTPStatus.NOT_FOUND

        if contact.user_id != current_user_id:
            return {"message": "UNAUTHORIZED ACCESS"}, HTTPStatus.UNAUTHORIZED

        json_data = request.get_json()
        name = json_data.get("name")
        email = json_data.get("email")
        phone_number = json_data.get("phone_number")
        address = json_data.get("address")
        image_url = json_data.get("image_url")

        contacts = Contact.query.filter_by(user_id=current_user_id).all()
        check_phone_number = next((contact for contact in contacts if contact.phone_number == phone_number), None)

        if (check_phone_number is not None) and (contact.id != check_phone_number.id) and \
                (check_phone_number.status is True):
            return {"message": "phone number has been registered with another contact"}

        contact.name = name
        contact.email = email
        contact.phone_number = phone_number
        if address is not None:
            contact.address = address

        if image_url is not None:
            contact.image_url = image_url

        db.session.commit()
        return contact.data, HTTPStatus.OK

    @jwt_required()
    def delete(self):
        current_user_id = get_jwt_identity()
        user = User.get_by_id(id=current_user_id)
        user.status = False
        db.session.commit()
        return "", HTTPStatus.NO_CONTENT


