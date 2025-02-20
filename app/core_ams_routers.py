from flask import Blueprint, jsonify, request
from . import db
from .models import Product
from flask_jwt_extended import jwt_required
from . import api
from flask_restx import Resource

bp = Blueprint('routes', __name__)

from flask import Blueprint, request, jsonify


@bp.route('/', methods=['GET'])
def index():
    return jsonify(message="index"), 200


@bp.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price
    } for product in products])


# Route to add a new product
@bp.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    new_product = Product(
        name=data['name'],
        description=data['description'],
        price=data['price']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product added'}), 201


@api.route('/insert-user-type/')
class InsertUserTypeView(Resource):
    @jwt_required()
    def post(self):
        return "insertUserTypeView"


@api.route('/get-usertypes/')
class GetUserTypes(Resource):
    @jwt_required()
    def post(self):
        return "getUserTypes"


@api.route('/make-superviser/')
class MakeSuperviserView(Resource):
    @jwt_required()
    def post(self):
        return "makeSuperviserView"


@api.route('/insert-site/')
class InsertSiteView(Resource):
    @jwt_required()
    def post(self):
        return "insertSiteView"


@api.route('/apply-leave/')
class ApplyLeaveView(Resource):
    @jwt_required()
    def post(self):
        return "applyLeaveView"


@api.route('/get-sites/')
class GetSitesView(Resource):
    @jwt_required()
    def get(self):
        return "getSitesView"


@api.route('/get-employee/')
class GetEmployeeView(Resource):
    @jwt_required()
    def get(self):
        return "getEmployeeView"


@api.route('/mark-attendance/')
class MarkAttendanceView(Resource):
    @jwt_required()
    def post(self):
        return "markAttendanceView"


@api.route('/insert-country/')
class InsertCountryView(Resource):
    def post(self):
        return "insertCountryView"


@api.route('/insert-state/')
class InsertStateView(Resource):
    def post(self):
        return "insertStateView"


@api.route('/insert-city/')
class InsertCityView(Resource):
    def post(self):
        return "insertCityView"


@api.route('/get-state-by-country/')
class GetStateByCountry(Resource):
    def get(self):
        return "getStateByCountry"


@api.route('/get-city-by-state/')
class GetCityByState(Resource):
    def get(self):
        return "getCityByState"


@api.route('/get-country/')
class GetCountry(Resource):
    def get(self):
        return "GetCountry"
