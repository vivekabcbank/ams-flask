from marshmallow import Schema, fields, validate, post_load, ValidationError, EXCLUDE
from .allfunctions import *
from .models import User
from . import db
from sqlalchemy import func, or_


class CheckAdminUserIdentitySerializer(Schema):
    userauth = fields.String(required=True, validate=validate.Length(min=1))

    class Meta:
        unknown = EXCLUDE

    @post_load
    def process_data(self, data, **kwargs):
        errors = {}
        try:
            data["userauth"] = userauth = int(decode_id(data.get("userauth")))
            user = db.session.query(User).filter(
                or_(
                    User.usertype_id == User_Type_id.ADMIN.value,
                    User.is_superuser == True
                ),
                User.id == userauth,
                User.isdeleted == False
            ).first()

            if not user:
                errors["userauth"] = "Admin Identity doesn't valid1."
        except Exception as e:
            errors["userauth"] = "Admin Identity doesn't valid2."

        if errors:
            raise ValidationError(errors)

        return data


class ValidateUserDetailsSerializer(Schema):
    company_name = fields.String(required=True, validate=validate.Length(min=1))
    first_name = fields.String(required=True, validate=validate.Length(min=1))
    last_name = fields.String(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=False)
    usertype_id = fields.String(required=True, validate=validate.Length(min=1))
    gender = fields.String(validate=validate.OneOf(['M', 'F', 'O']))
    dob = fields.Date(required=False)
    calling_code = fields.String(required=True, validate=validate.Length(min=1))
    phone = fields.String(validate=validate.Length(min=10, max=15), required=True)
    address = fields.String(required=True, validate=validate.Length(min=1))
    pincode = fields.String(required=True, validate=validate.Length(min=1))
    country = fields.String(required=True, validate=validate.Length(min=1))
    state = fields.String(required=True, validate=validate.Length(min=1))
    city = fields.String(required=True, validate=validate.Length(min=1))
    password = fields.String(required=True, validate=validate.Length(min=1))

    class Meta:
        unknown = EXCLUDE

    @post_load
    def process_email(self, data, **kwargs):
        email = data.get('email')
        existing_user = User.query.filter_by(isdeleted=False,
                                             email=email).first()
        if existing_user:
            raise ValidationError(f'Email {email} is already in use.')
        return data

    @post_load
    def process_data(self, data, **kwargs):
        errors = {}

        calling_code = data.get('calling_code')
        phone = data.get('phone')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        data['username'] = set_username(first_name, last_name)

        try:
            data["usertype_id"] = int(decode_id(data.get("usertype_id")))
        except Exception as e:
            errors["usertype_id"] = "Invalid usertype_id"

        existing_user = User.query.filter_by(isdeleted=False,
                                             calling_code=calling_code,
                                             phone=phone
                                             ).first()
        if existing_user:
            errors["invalid_phone"] = f'Phone {calling_code}{phone} is already in use.'

        if errors:
            raise ValidationError(errors)
        return data


class ValidateLoginUserSerializer(Schema):
    username = fields.String(required=True, validate=validate.Length(min=1))
    password = fields.String(required=True, validate=validate.Length(min=1))

    class Meta:
        unknown = EXCLUDE

    @post_load
    def process_data(self, data, **kwargs):
        errors = {}
        username = data.get('username')
        password = data.get('password')

        user = db.session.query(User).filter(
            or_(
                User.username == username,
                func.concat(User.calling_code, User.phone) == username
            ),
            User.isdeleted == False
        ).first()

        data["user"] = user

        if not user or not user.check_password(password):
            errors["invalid credentials"] = "Invalid credentials"

        if errors:
            raise ValidationError(errors)

        return data
