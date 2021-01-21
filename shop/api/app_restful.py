from flask import Blueprint
from flask_restful import Api

from . resources import UserResource, CategoryResource, ProductResource, OrderResource, NewsResource


app_api = Blueprint('app_api', __name__)
api = Api(app_api)
api.init_app(app_api)

api.add_resource(UserResource, '/api/user', '/api/user/<string:id>')
api.add_resource(ProductResource, '/api/product', '/api/product/<string:id>')
api.add_resource(CategoryResource, '/api/category', '/api/category/<string:id>')
api.add_resource(OrderResource, '/api/order', '/api/order/<string:id>')
api.add_resource(NewsResource, '/api/news', '/api/news/<string:id>')


