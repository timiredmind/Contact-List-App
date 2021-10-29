from marshmallow import Schema, fields
from utils import generate_hash, validate_phone_number


class UserSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Method(deserialize="hash_password", required=True)
    email = fields.Email(required=True)
    phone_number = fields.Str(validate=validate_phone_number, required=True)
    date_created = fields.DateTime(dump_only=True)

    def hash_password(self, password):
        return generate_hash(password)




