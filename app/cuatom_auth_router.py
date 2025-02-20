from . import db
from flask import Blueprint, request, jsonify
from .models import User
from flask_jwt_extended import create_access_token, jwt_required
from flask_restx import Resource
from . import app, api
from flask import make_response


@api.route('/signup-user/', methods=['POST'])
class UserSignUpView(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return make_response(jsonify({"msg": "Missing fields"}), 400)

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return make_response(jsonify({"msg": "User already exists"}), 400)

        new_user = User(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return make_response(jsonify({"msg": "User created successfully"}), 201)


@api.route('/signin-user/', methods=['POST'])
class UserSigninView(Resource):
    def post(self):

        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return make_response(jsonify({"msg": "Missing fields"}), 400)

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            return make_response(jsonify({"msg": "Invalid credentials"}), 401)

        # Create access token
        access_token = create_access_token(identity=str(user.id))
        return make_response(jsonify(access_token=access_token), 200)


@api.route('/insert-employee/')
class InsertEmployeeView(Resource):
    @jwt_required()
    def post(self):
        return "insertEmployeeView"


auth = Blueprint('auth', __name__)


# http://127.0.0.1:5000/auth/protected
@auth.route('/protected/', methods=['GET'])
@jwt_required()
def protected():
    return jsonify(message="This is a protected resource, accessible only with a valid JWT.")


# http://127.0.0.1:5000/protected_app
@app.route('/protected_app/', methods=['GET'])
def protected_app():
    return jsonify(message="This is a protected resource, accessible only with a valid JWT.")
