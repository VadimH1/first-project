from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    phone_number = fields.String(required=True)
    first_name = fields.String()
    second_name = fields.String()
    password = fields.String()


class CommentsSchema(Schema):
    id = fields.Integer(dump_only=True)
    author_id = fields.Integer(required=True)
    post_id = fields.Integer(required=True)
    text = fields.String(required=True, validate=[validate.Length(max=100)])
    created = fields.DateTime()
    is_deleted = fields.Boolean()


class PostSchema(Schema):
    id = fields.Integer(dump_only=True)
    author_id = fields.Integer(required=True)
    title = fields.String(required=True, validate=[validate.Length(max=100)])
    body = fields.String(required=True, validate=[validate.Length(max=100)])
    is_deleted = fields.Boolean()
    comments = fields.Nested(
        CommentsSchema, many=True
    )
    created = fields.DateTime()

class UploadSchema(Schema):
    id = fields.Integer(dump_only=True)    
    url = fields.String(required=True, validate=[validate.Length(max=200)])
