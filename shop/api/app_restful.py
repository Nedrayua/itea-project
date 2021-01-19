from flask import Flask
from flask_restful import Api

from . resources import UserResource, CategoryResource, ProductResource, OrderResource, NewsResource

app = Flask(__name__)
api = Api(app)

api.add_resource(UserResource, '/user', '/user/<string:id>')
api.add_resource(ProductResource, '/product', '/product/<string:id>')
api.add_resource(CategoryResource, '/category', '/category/<string:id>')
api.add_resource(OrderResource, '/order', '/order/<string:id>')
api.add_resource(NewsResource, '/news', '/news/<string:id>')

