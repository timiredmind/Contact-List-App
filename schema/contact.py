from marshmallow import Schema, fields
from utils import validate_phone_number
from schema.pagination import PaginationSchema


class ContactSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    phone_number = fields.Str(required=True, validate=validate_phone_number)
    address = fields.Str()
    image_url = fields.Str()
    date_created = fields.DateTime(dump_only=True)


class ContactPaginationSchema(PaginationSchema):
    contacts = fields.Nested(ContactSchema, attribute="items", many=True)


