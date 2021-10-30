from marshmallow import Schema, fields, post_dump
from utils import validate_phone_number


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

    @post_dump(pass_many=True)
    def wrap(self, data, many):
        if many:
            return {"contacts": data}

        return {"contact": data}



