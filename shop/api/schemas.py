from marshmallow import Schema, fields
from marshmallow.validate import Range, Length


class UserSchema(Schema):
    id = fields.String()
    telegram_id = fields.String()
    username = fields.String(validate=Length(min=2, max=128))
    first_name = fields.String(validate=Length(min=2, max=128))
    phone_number = fields.String(validate=Length(max=13))
    email = fields.Email()
    user_address = fields.String(validate=Length(min=12, max=128))
    is_block = fields.Boolean()


class CategorySchemaRead(Schema):
    id = fields.String()
    title = fields.String(validate=Length(min=2, max=128))
    description = fields.String(validate=Length(min=0, max=512))
    parent = fields.Nested('CategorySchemaRead', only=('id', "title",))
    subcategories = fields.List(fields.Nested('CategorySchemaRead', only=('id', "title",)))


class CategorySchemaWrite(CategorySchemaRead):
    parent = fields.String()
    subcategories = fields.List(fields.String())


class ParametersSchema(Schema):
    id = fields.String()
    height = fields.Float()
    width = fields.Float()
    weight = fields.Float()
    additional_description = fields.String()


class ProductSchemaRead(Schema):
    id = fields.String()
    title = fields.String(validate=Length(max=256), required=True)
    description = fields.String(validate=Length(min=0, max=512))
    in_stock = fields.Boolean()
    discount = fields.Integer(validate=Range(min=0, max=100), default=0)
    price = fields.Integer()
    #image = fields.Raw(load_only=True) # В АПИ функцонал привязки есть, но настроить отображение не успел (((
    category = fields.Nested(CategorySchemaRead, only=('id', 'title',))
    parameters = fields.Nested('ParametersSchema')


class ProductSchemaWrite(ProductSchemaRead):
    category = fields.String()
    parameters = fields.Dict()
    image = fields.String()


class OrderSchema(Schema):
    id = fields.String()
    user = fields.Nested('UserSchema')
    products = fields.List(fields.Nested('ProductSchemaRead', only=("id", "title",)))
    delivery_data = fields.Dict()
    in_work_status = fields.Boolean()
    sent_to_client = fields.Boolean()


class NewsSchema(Schema):
    id = fields.String()
    title = fields.String(validate=Length(min=2, max=128), required=True)
    body = fields.String(validate=Length(min=2, max=2048), required=True)
