from flask import Blueprint, jsonify, request
from . import db
from .models import Product

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