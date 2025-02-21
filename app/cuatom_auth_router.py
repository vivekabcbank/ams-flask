from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from flask_restx import Resource
from . import app, api
from flask import make_response
from .cuatom_auth_serializers import *
from marshmallow import ValidationError


@api.route('/signup-user/', methods=['POST'])
class UserSignUpView(Resource):
    def post(self):
        data = request.get_json()
        user_serializer = ValidateUserDetailsSerializer()

        try:
            user_data = user_serializer.load(data)
            new_user = User(
                company_name=user_data.get("company_name"),
                username=user_data.get("username"),
                email=user_data.get("email"),
                first_name=user_data.get("first_name"),
                last_name=user_data.get("last_name"),
                gender=user_data.get("gender"),
                dob=user_data.get("dob"),
                calling_code=user_data.get("calling_code"),
                phone=user_data.get("phone"),
                address=user_data.get("address"),
                pincode=user_data.get("pincode"),
                country=user_data.get("country"),
                state=user_data.get("state"),
                city=user_data.get("city"),
                usertype_id=user_data.get("usertype_id")
                # usertype=usertype => like this we can connect usertype instance
            )
            new_user.set_password(user_data.get("password"))
            db.session.add(new_user)
            db.session.commit()

        except ValidationError as err:
            return make_response(jsonify({"error": err.messages}), 400)

        return make_response(jsonify(user_data), 200)


@api.route('/signin-user/', methods=['POST'])
class UserSigninView(Resource):
    def post(self):
        data = request.get_json()
        user_serializer = ValidateLoginUserSerializer()
        try:
            user_data = user_serializer.load(data)
            user = user_data["user"]
            access_token = create_access_token(identity=str(user.id))
        except ValidationError as err:
            return make_response(jsonify({"error": err.messages}), 400)

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
