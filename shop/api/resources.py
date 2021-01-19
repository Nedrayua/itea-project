
from marshmallow.exceptions import ValidationError
from flask_restful import Resource
from flask import request

from shop.models.shop_models import User, Category, Product, Order
from shop.models import extra_models
from shop.bot import sending_news
from . schemas import UserSchema, CategorySchemaRead, CategorySchemaWrite, ProductSchemaRead, ProductSchemaWrite
from . schemas import OrderSchema, NewsSchema


class UserResource(Resource):
    def get(self, id=None):
        if id:
            return UserSchema().dump(User.objects.get(telegram_id=id))
        else:
            return UserSchema().dump(User.objects(), many=True)

    def post(self):
        try:
            UserSchema().load(request.json)
        except ValidationError as e:
            return str(e)
        user = User(**request.json)
        user.save()
        return UserSchema().dump(user)

    def put(self, id):
        try:
            UserSchema().load(request.json)
        except ValidationError as e:
            return str(e)
        user = User.objects.get(telegram_id=id)
        user.update(**request.json)
        user.reload()
        return UserSchema().dump(user)

    def delete(self, id):
        User.objects.get(telegram_id=id).delete()
        return str({"status": "deleted"})


class CategoryResource(Resource):
    def get(self, id=None):
        if id:
            return CategorySchemaRead().dump(Category.objects.get(id=id))
        else:
            return CategorySchemaRead().dump(Category.objects(), many=True)

    def post(self):
        try:
            CategorySchemaWrite().load(request.json)
        except ValidationError as e:
            return str(e)
        category = Category(**request.json)
        category.save()
        return CategorySchemaRead().dump(category)

    def put(self, id):
        try:
            CategorySchemaWrite().load(request.json)
        except ValidationError as e:
            return str(e)

        if request.json['parent']:
            request.json['parent'] = Category.objects.get(id=request.json['parent'])

        if request.json['subcategories']:
            for i in range(len(request.json['subcategories'])):
                request.json['subcategories'][i] = Category.objects.get(id=request.json['subcategories'][i])

        category = Category.objects.get(id=id)
        category.update(**request.json)
        category.reload()
        return CategorySchemaRead().dump(category)

    def delete(self, id):
        Category.objects.get(id=id).delete()
        return str({"status": "deleted"})


class ProductResource(Resource):
    def get(self, id=None):
        if id:
            return ProductSchemaRead().dump(Product.objects.get(id=id))
        else:
            return ProductSchemaRead().dump(Product.objects(), many=True)

    def post(self):
        img = None
        try:
            if request.json['image']:
                img = request.json.pop('image')
            ProductSchemaWrite().load(request.json)
        except ValidationError as e:
            return str(e)

        product = Product(**request.json)
        if img:
            with open(img, 'rb') as file:
                product.image.put(file, content_type='image/jpg')
        product.save()
        return ProductSchemaRead().dump(product)

    def put(self, id):
        try:
            ProductSchemaWrite().load(request.json)
        except ValidationError as e:
            return str(e)
        if request.json['category']:
            request.json['category'] = Category.objects.get(id=request.json['category'])
        product = Product.objects.get(id=id)
        if request.json['image']:
            with open(request.json['image'], 'rb') as file:
                product.image.put(file, content_type='image/jpg')
                product.save()
                request.json.pop('image')
        product.update(**request.json)
        product.reload()
        return ProductSchemaRead().dump(product)

    def delete(self, id):
        Product.objects.get(id=id).delete()
        return str({"status": "deleted"})


class OrderResource(Resource):
    def get(self, id=None):
        if id:
            return OrderSchema().dump(Order.objects.get(id=id))
        else:
            return OrderSchema().dump(Order.objects(), many=True)


class NewsResource(Resource):
    def get(self, id=None):
        if id:
            return NewsSchema().dump(extra_models.News.objects.get(id=id))
        else:
            return NewsSchema().dump(extra_models.News.objects(), many=True)

    def post(self):
        try:
            NewsSchema().load(request.json)
        except ValidationError as e:
            return str(e)
        news = extra_models.News(**request.json)
        news.save()
        s = sending_news.Sender(User.objects(), text=news)
        s.send_message()
        return NewsSchema().dump(news)

    def put(self, id):
        try:
            NewsSchema().load(request.json)
        except ValidationError as e:
            return str(e)
        news = extra_models.News.objects.get(id=id)
        news.update(**request.json)
        news.reload()
        return NewsSchema().damp(news)

    def delete(self, id):
        extra_models.News.objects.get(id=id).delete()
        return str({"status": "deleted"})
