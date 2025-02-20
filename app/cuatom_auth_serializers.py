from marshmallow import Schema, fields, validate, post_load, ValidationError
from .allfunctions import *
from .models import User
from . import db
from sqlalchemy import func, or_

class ValidateUserDetailsSerializer(Schema):
    company_name = fields.String(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.Email(required=False)
    usertype_id = fields.String(required=True)
    gender = fields.String(validate=validate.OneOf(['M', 'F', 'O']))
    dob = fields.Date(required=False)
    calling_code = fields.String(required=True)
    phone = fields.String(validate=validate.Length(min=10, max=15), required=True)
    address = fields.String(required=True)
    pincode = fields.String(required=True)
    country = fields.String(required=True)
    state = fields.String(required=True)
    city = fields.String(required=True)
    password = fields.String(required=True)

    @post_load
    def process_email(self, data, **kwargs):
        email = data.get('email')
        existing_user = User.query.filter_by(isdeleted= False,
                                             email=email).first()
        if existing_user:
            raise ValidationError(f'Email {email} is already in use.')
        return data

    @post_load
    def process_data(self, data, **kwargs):
        data["usertype_id"] = int(decode_id(data.get("usertype_id")))
        calling_code = data.get('calling_code')
        phone = data.get('phone')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        data['username'] = set_username(first_name, last_name)
        existing_user = User.query.filter_by(isdeleted= False,
                                             calling_code=calling_code,
                                             phone=phone
                                             ).first()
        if existing_user:
            raise ValidationError(f'Phone {calling_code}{phone} is already in use.')
        return data


class ValidateLoginUserSerializer(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)

    @post_load
    def process_data(self, data, **kwargs):
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
            raise ValidationError('Invalid credentials')

        return data