from marshmallow import Schema, fields, validate, post_load, ValidationError, EXCLUDE
from .allfunctions import *
from . import db
from sqlalchemy import func, or_
from .models import UserType, Site, Employee, Country, City, State
from pdb import set_trace
from sqlalchemy.orm import joinedload


class ValidateInsertUsertypeSerializer(Schema):
    typename = fields.String(required=True)
    description = fields.String(required=True)

    @post_load
    def process_data(self, data, **kwargs):
        typename = data.get('typename')
        existing_user_type = UserType.query.filter_by(typename=typename,
                                                      isdeleted=False).first()
        if existing_user_type:
            raise ValidationError('Type name already exists')

        return data


class ValidateSiteDetailsSerializers(Schema):
    owner_user_id = fields.String(required=True)
    sitename = fields.String(required=True)
    address = fields.String(required=True)
    country = fields.String(required=True)
    state = fields.String(required=True)
    city = fields.String(required=True)
    latitude = fields.String(required=True)
    longitude = fields.String(required=True)

    @post_load
    def process_data(self, data, **kwargs):
        data["owner_user_id"] = owner_user_id = int(decode_id(data.get("owner_user_id")))
        sitename = data.get("sitename")

        existing_owner_site = Site.query.filter_by(owner_user_id=owner_user_id,
                                                   sitename=sitename,
                                                   isdeleted=False).first()
        # set_trace()
        if existing_owner_site:
            raise ValidationError('Site name already exists')

        return data


class GetSitesSerializer(Schema):
    owner_user_id = fields.String(required=True)
    usertype_id = fields.String(required=True)

    @post_load
    def process_data(self, data, **kwargs):
        data["owner_user_id"] = owner_user_id = int(decode_id(data.get("owner_user_id")))
        data["usertype_id"] = usertype_id = int(decode_id(data.get("usertype_id")))

        if usertype_id == User_Type_id.ADMIN.value:
            data["admin_sites"] = Site.query.filter_by(owner_user_id=owner_user_id,
                                                       isdeleted=False)
        else:
            employee = db.session.query(Employee).filter_by(id=owner_user_id).first()
            # employee = db.session.query(Employee).options(joinedload(Employee.site_info)).filter_by(
            #     id=owner_user_id).first()
            # This would fetch the Employee and the related Site in a singlequery.

            data["employee_sites"] = employee.site_info

        return data


class GetEmployeeSerializer(Schema):
    site_info_id = fields.String(required=True)

    @post_load
    def process_data(self, data, **kwargs):
        try:
            data["site_info_id"] = int(decode_id(data.get("site_info_id")))
        except Exception as e:
            raise ValidationError("Site name not valid")

        return data


class ApplyLeaveSerializers(Schema):
    employee_id = fields.String(required=True, validate=validate.Length(min=1))
    site_info_id = fields.String(required=True, validate=validate.Length(min=1))
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    reason = fields.String(required=True, validate=validate.Length(min=1))

    @post_load
    def process_data(self, data, **kwargs):
        errors = {}
        data["employee_id"] = employee_id = int(decode_id(data.get("employee_id")))
        data["site_info_id"] = site_info_id = int(decode_id(data.get("site_info_id")))

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
        countryid_id = data.get("countryid_id")
        statename = data.get("statename")

        try:
            countryid_id = int(decode_str(countryid_id))
            data["countryid_id"] = countryid_id
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
        stateid_id = data.get("stateid_id")
        cityname = data.get("cityname")

        try:
            stateid_id = int(decode_str(stateid_id))
            data["stateid_id"] = stateid_id
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
