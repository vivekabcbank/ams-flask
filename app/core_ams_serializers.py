from idlelib.iomenu import errors

from marshmallow import Schema, fields, validate, post_load, ValidationError, EXCLUDE
from .allfunctions import *
from . import db
from sqlalchemy import func, or_
from .models import UserType, Site, Employee, Country, City, State, User
from sqlalchemy.orm import joinedload


class ValidateInsertUsertypeSerializer(Schema):
    typename = fields.String(required=True, validate=validate.Length(min=1))
    description = fields.String(required=True, validate=validate.Length(min=1))

    class Meta:
        unknown = EXCLUDE

    @post_load
    def process_data(self, data, **kwargs):
        errors = {}
        typename = data.get('typename')
        existing_user_type = UserType.query.filter_by(typename=typename,
                                                      isdeleted=False).first()
        if existing_user_type:
            errors["typename"] = 'Type name already exists'

        if errors:
            raise ValidationError(errors)

        return data


class ValidateSiteDetailsSerializers(Schema):
    owner_user_id = fields.String(required=True, validate=validate.Length(min=1))
    sitename = fields.String(required=True, validate=validate.Length(min=1))
    address = fields.String(required=True, validate=validate.Length(min=1))
    country = fields.String(required=True, validate=validate.Length(min=1))
    state = fields.String(required=True, validate=validate.Length(min=1))
    city = fields.String(required=True, validate=validate.Length(min=1))
    latitude = fields.String(required=True, validate=validate.Length(min=1))
    longitude = fields.String(required=True, validate=validate.Length(min=1))

    class Meta:
        unknown = EXCLUDE

    @post_load
    def process_data(self, data, **kwargs):
        errors = {}

        sitename = data.get("sitename")

        try:
            data["owner_user_id"] = owner_user_id = int(decode_id(data.get("owner_user_id")))
        except Exception:
            errors["owner_user_id"] = "Invalid owner id"

        existing_owner_site = Site.query.filter_by(owner_user_id=owner_user_id,
                                                   sitename=sitename,
                                                   isdeleted=False).first()
        if existing_owner_site:
            errors["sitename"] = 'Site name already exists'

        if errors:
            raise ValidationError(errors)

        return data


class GetSitesSerializer(Schema):
    owner_user_id = fields.String(required=True, validate=validate.Length(min=1))
    usertype_id = fields.String(required=True, validate=validate.Length(min=1))

    class Meta:
        unknown = EXCLUDE

    @post_load
    def process_data(self, data, **kwargs):
        errors = {}
        try:
            data["owner_user_id"] = owner_user_id = int(decode_id(data.get("owner_user_id")))
        except Exception:
            errors["owner_user_id"] = "Invalid owner id"

        try:
            data["usertype_id"] = usertype_id = int(decode_id(data.get("usertype_id")))
        except Exception:
            errors["usertype_id"] = "Invalid usertype_id"

        try:
            if usertype_id == User_Type_id.ADMIN.value:
                data["admin_sites"] = Site.query.filter_by(owner_user_id=owner_user_id,
                                                           isdeleted=False)
            else:
                employee = db.session.query(Employee).filter_by(id=owner_user_id).first()
                # employee = db.session.query(Employee).options(joinedload(Employee.site_info)).filter_by(
                #     id=owner_user_id).first()
                # This would fetch the Employee and the related Site in a singlequery.

                data["employee_sites"] = employee.site_info
        except Exception as e:
            errors["error"] = "failed to process request"

        if errors:
            raise ValidationError(errors)

        return data


class GetEmployeeSerializer(Schema):
    site_info_id = fields.String(required=True, validate=validate.Length(min=1))

    class Meta:
        unknown = EXCLUDE

    @post_load
    def process_data(self, data, **kwargs):
        errors = {}
        try:
            data["site_info_id"] = int(decode_id(data.get("site_info_id")))
        except Exception as e:
            errors["site_info_id"] = "Site name not valid"

        if errors:
            raise ValidationError(errors)

        return data


class ApplyLeaveSerializers(Schema):
    employee_id = fields.String(required=True, validate=validate.Length(min=1))
    site_info_id = fields.String(required=True, validate=validate.Length(min=1))
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    reason = fields.String(required=True, validate=validate.Length(min=1))

    class Meta:
        unknown = EXCLUDE

    @post_load
    def process_data(self, data, **kwargs):
        errors = {}
        try:
            data["employee_id"] = employee_id = int(decode_id(data.get("employee_id")))
        except Exception:
            errors["employee_id"] = "Invalid employee_id"

        try:
            data["site_info_id"] = site_info_id = int(decode_id(data.get("site_info_id")))
        except Exception:
            errors["site_info_id"] = "Invalid site_info_id"

        start_date = data.get("start_date")
        end_date = data.get("end_date")

        if start_date >= end_date:
            errors['date mismatch'] = "End date shoule be grater than start date"

        try:
            if employee_id is not None and site_info_id is not None:
                if not Employee.query.filter_by(id=employee_id,
                                                site_info_id=site_info_id,
                                                isdeleted=False).first():
                    errors['mismatch_data'] = "employee_id, site not matched"

        except Exception as e:
            errors['mismatch_data'] = "employee_id, site not matchedee"

        if errors:
            raise ValidationError(errors)

        return data


class InsertCountrySerializer(Schema):
    countryname = fields.String(required=True, validate=validate.Length(min=1))
    sortname = fields.String(required=True, validate=validate.Length(min=1))
    countrycode = fields.String(required=True, validate=validate.Length(min=1))

    class Meta:
        unknown = EXCLUDE

    @post_load
    def process_data(self, data, **kwargs):
        errors = {}
        countryname = data.get("countryname", "")
        sortname = data.get("sortname", "")
        countrycode = data.get("countrycode", "")

        country = Country.query.filter_by(countryname=countryname,
                                          sortname=sortname,
                                          countrycode=countrycode).first()
        if country:
            errors["typename"] = "Country name already exists"

        if errors:
            raise ValidationError(errors)

        return data


class InsertStateSerializer(Schema):
    countryid_id = fields.String(required=True, validate=validate.Length(min=1))
    statename = fields.String(required=True, validate=validate.Length(min=1))

    class Meta:
        unknown = EXCLUDE

    @post_load
    def process_data(self, data, **kwargs):
        errors = {}
        statename = data.get("statename")

        try:
            data["countryid_id"] = countryid_id = int(decode_str(data.get("countryid_id")))
            if not Country.query.filter_by(id=countryid_id,
                                           isdeleted=False
                                           ).first():
                errors["countryid_id"] = "Country Identity doesn't valid."
        except Exception as e:
            errors["countryid_id"] = "Country Identity doesn't valid."

        state = State.query.filter_by(statename=statename,
                                      isdeleted=False
                                      ).first()
        if state:
            errors["statename"] = "State name already exists"

        if errors:
            raise ValidationError(errors)

        return data


class InsertCitySerializer(Schema):
    stateid_id = fields.String(required=True, validate=validate.Length(min=1))
    cityname = fields.String(required=True, validate=validate.Length(min=1))

    class Meta:
        unknown = EXCLUDE

    @post_load
    def process_data(self, data, **kwargs):
        errors = {}
        cityname = data.get("cityname")

        try:
            data["stateid_id"] = stateid_id = int(decode_str(data.get("stateid_id")))
            if not State.query.filter_by(id=stateid_id,
                                         isdeleted=False
                                         ).first():
                errors["stateid_id"] = "State Identity doesn't valid."
        except Exception as e:
            errors["stateid_id"] = "State Identity doesn't valid."

        city = City.query.filter_by(cityname=cityname,
                                    isdeleted=False
                                    ).first()
        if city:
            errors["cityname"] = "City name already exists"

        if errors:
            raise ValidationError(errors)

        return data


class MakeSuperviserSerializer(Schema):
    employee_id = fields.String(required=True, validate=validate.Length(min=1))
    password = fields.String(required=True, validate=validate.Length(min=1))

    class Meta:
        unknown = EXCLUDE

    @post_load
    def process_data(self, data, **kwargs):
        errors = {}
        try:
            data["employee_id"] = employee_id = int(decode_id(data.get("employee_id")))
            employee = Employee.query.filter_by(pk=employee_id,
                                                isdeleted=False).first()
            user = User.query.filter_by(pk=employee.user.id,
                                        isdeleted=False).first()
            data["user"] = user
        except Exception as e:
            errors['user_id'] = "Invalid employee id"

        if errors:
            raise ValidationError(errors)

        return data
