from marshmallow import Schema, fields

class LoginSchema(Schema):
    username = fields.Str(required=True, error_messages={"required": "Username is required."})
    password = fields.Str(required=True, error_messages={"required": "Password is required."})

class RegisterSchema(Schema):
    username = fields.Str(required=True, error_messages={"required": "Username is required."})
    password = fields.Str(required=True, error_messages={"required": "Password is required."})
    email = fields.Str(required=True, error_messages={"required": "Email is required."})
