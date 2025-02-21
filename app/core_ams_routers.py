from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from . import api
from flask_restx import Resource
from .core_ams_serializers import *
from flask import make_response
from .models import Employee, Leave
from .cuatom_auth_serializers import CheckAdminUserIdentitySerializer
from pdb import set_trace

bp = Blueprint('routes', __name__)


@bp.route('/index/', methods=['GET'])
def index():
    return jsonify(message="index"), 200


@api.route('/insert-user-type/')
class InsertUserTypeView(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        user_serializer = ValidateInsertUsertypeSerializer()
        try:
            user_type_data = user_serializer.load(data)
            new_user_type = UserType(
                typename=user_type_data.get("typename"),
                description=user_type_data.get("description"),
            )
            db.session.add(new_user_type)
            db.session.commit()

        except ValidationError as err:
            return make_response(jsonify({"error": err.messages}), 400)

        return make_response(jsonify({"message": "User type added successfully"}), 200)


@api.route('/get-usertypes/')
class GetUserTypes(Resource):
    @jwt_required()
    def get(self):
        user_types = UserType.query.all()
        return jsonify([{
            'id': type.id,
            'name': type.typename,
            'description': type.description,
        } for type in user_types])


@api.route('/insert-site/')
class InsertSiteView(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        site_serializer = ValidateSiteDetailsSerializers()
        try:
            site_data = site_serializer.load(data)
            new_user_type = Site(
                owner_user_id=site_data.get("owner_user_id"),
                sitename=site_data.get("sitename"),
                address=site_data.get("address"),
                country=site_data.get("country"),
                state=site_data.get("state"),
                city=site_data.get("city"),
                latitude=site_data.get("latitude"),
                longitude=site_data.get("longitude")
            )
            db.session.add(new_user_type)
            db.session.commit()

        except ValidationError as err:
            return make_response(jsonify({"error": err.messages}), 400)

        return make_response(jsonify({"message": "Site name added successfully"}), 200)


@api.route('/get-sites/')
class GetSitesView(Resource):
    @jwt_required()
    def get(self):
        data = request.get_json()
        site_serializer = GetSitesSerializer()
        try:
            site_data = site_serializer.load(data)
            admin_sites = site_data.get("admin_sites")
            employee_sites = site_data.get("employee_sites")
            if admin_sites:
                return jsonify([{
                    'id': type.id,
                    'sitename': type.sitename,
                    'address': type.address,
                } for type in admin_sites])
            else:
                return jsonify([{
                    'id': type.id,
                    'sitename': type.sitename,
                    'address': type.address,
                } for type in employee_sites])
        except ValidationError as err:
            return make_response(jsonify({"error": err.messages}), 400)


@api.route('/get-employee/')
class GetEmployeeView(Resource):
    @jwt_required()
    def get(self):
        data = request.get_json()
        site_serializer = GetEmployeeSerializer()
        try:
            site_data = site_serializer.load(data)
            result = Employee.query.filter_by(site_info_id=site_data.get("site_info_id"))
            return jsonify([{
                'id': type.id,
                'user_id': type.user_id,
                'site_info_id': type.site_info_id,
            } for type in result])

        except ValidationError as err:
            return make_response(jsonify({"error": err.messages}), 400)


@api.route('/apply-leave/')
class ApplyLeaveView(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        site_serializer = ApplyLeaveSerializers()
        try:
            user_type_data = site_serializer.load(data)
            new_user_type = Leave(
                employee_id=user_type_data.get("employee_id"),
                site_info_id=user_type_data.get("site_info_id"),
                start_date=user_type_data.get("start_date"),
                end_date=user_type_data.get("end_date"),
                reason=user_type_data.get("reason")
            )
            db.session.add(new_user_type)
            db.session.commit()
        except ValidationError as err:
            return make_response(jsonify({"error": err.messages}), 400)


@api.route('/insert-country/')
class InsertCountryView(Resource):
    def post(self):
        all_errors = {}
        data = request.get_json()
        auth_serializer = CheckAdminUserIdentitySerializer()
        other_serializer = InsertCountrySerializer()
        try:
            auth_data = auth_serializer.load(data)
        except ValidationError as err:
            all_errors.update({"auth_errors": err.messages})

        try:
            other_data = other_serializer.load(data)
            new_user_type = Country(
                countryname=other_data.get("countryname"),
                sortname=other_data.get("sortname"),
                countrycode=other_data.get("countrycode"),
            )
            db.session.add(new_user_type)
            db.session.commit()

        except ValidationError as err:
            all_errors.update({"other_errors": err.messages})

        if all_errors:
            return make_response(jsonify({"errors": all_errors}), 400)

        return make_response(jsonify({"message": "Country inserted successfully"}), 201)


@api.route('/insert-state/')
class InsertStateView(Resource):
    def post(self):
        all_errors = {}
        data = request.get_json()
        auth_serializer = CheckAdminUserIdentitySerializer()
        other_serializer = InsertStateSerializer()
        try:
            auth_data = auth_serializer.load(data)
        except ValidationError as err:
            all_errors.update({"auth_errors": err.messages})

        try:
            other_data = other_serializer.load(data)
            new_user_type = State(
                countryid=other_data.get("countryid_id"),
                statename=other_data.get("statename")
            )
            db.session.add(new_user_type)
            db.session.commit()

        except ValidationError as err:
            all_errors.update({"other_errors": err.messages})

        if all_errors:
            return make_response(jsonify({"errors": all_errors}), 400)

        return make_response(jsonify({"message": "Country inserted successfully"}), 201)


@api.route('/insert-city/')
class InsertCityView(Resource):
    def post(self):
        all_errors = {}
        data = request.get_json()
        auth_serializer = CheckAdminUserIdentitySerializer()
        other_serializer = InsertCitySerializer()
        try:
            auth_data = auth_serializer.load(data)
        except ValidationError as err:
            all_errors.update({"auth_errors": err.messages})

        try:
            other_data = other_serializer.load(data)
            new_user_type = City(
                stateid=other_data.get("stateid_id"),
                cityname=other_data.get("cityname")
            )
            db.session.add(new_user_type)
            db.session.commit()

        except ValidationError as err:
            all_errors.update({"other_errors": err.messages})

        if all_errors:
            return make_response(jsonify({"errors": all_errors}), 400)

        return make_response(jsonify({"message": "Country inserted successfully"}), 201)


@api.route('/make-superviser/')
class MakeSuperviserView(Resource):
    @jwt_required()
    def post(self):
        return "makeSuperviserView"


@api.route('/mark-attendance/')
class MarkAttendanceView(Resource):
    @jwt_required()
    def post(self):
        return "markAttendanceView"


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
