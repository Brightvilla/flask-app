from marshmallow import Schema, fields, validate

class RegisterSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=3, max=80))
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True, validate=validate.Length(min=6))

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.String(dump_only=True)
    email = fields.Email(dump_only=True)
    role = fields.String(dump_only=True)
