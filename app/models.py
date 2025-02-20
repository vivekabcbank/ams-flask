from . import db
from flask_bcrypt import Bcrypt
from datetime import datetime

bcrypt = Bcrypt()


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String(200), nullable=True)
    price = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f"<Product {self.name}>"


class UserType(db.Model):
    __tablename__ = 'usertype'  # Equivalent to db_table in Django
    id = db.Column(db.Integer, primary_key=True)  # You need a primary key
    typename = db.Column(db.String(200), nullable=True)  # Equivalent to CharField(max_length=200)
    description = db.Column(db.Text, nullable=True)  # Equivalent to TextField
    isdeleted = db.Column(db.Boolean, default=False)  # Equivalent to BooleanField(default=False)
    createddate = db.Column(db.DateTime, default=datetime.utcnow,nullable=False)  # Equivalent to DateTimeField(default=timezone.now)
    updateddate = db.Column(db.DateTime, nullable=True)  # Equivalent to DateTimeField(null=True)

    def __str__(self):
        return f"{self.typename}"


class Country(db.Model):
    __tablename__ = 'country'

    id = db.Column(db.Integer, primary_key=True)  # Primary key
    countryname = db.Column(db.String(200), default="")
    sortname = db.Column(db.String(200), default="")
    countrycode = db.Column(db.String(200), default="")
    isdeleted = db.Column(db.Boolean, default=False)
    createddate = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updateddate = db.Column(db.DateTime, nullable=True)

    def __str__(self):
        return f"{self.countryname}"


class State(db.Model):
    __tablename__ = 'state'

    id = db.Column(db.Integer, primary_key=True)  # Primary key
    countryid = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=True)  # ForeignKey to Country
    statename = db.Column(db.String(200))
    isdeleted = db.Column(db.Boolean, default=False)
    createddate = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updateddate = db.Column(db.DateTime, nullable=True)

    # Relationship with Country
    country = db.relationship('Country', backref=db.backref('states', lazy=True))

    def __str__(self):
        return f"{self.statename}"


class City(db.Model):
    __tablename__ = 'city'

    id = db.Column(db.Integer, primary_key=True)  # Primary key
    stateid = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=True)  # ForeignKey to State
    cityname = db.Column(db.String(200))
    isdeleted = db.Column(db.Boolean, default=False)
    createddate = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updateddate = db.Column(db.DateTime, nullable=True)

    # Relationship with State
    state = db.relationship('State', backref=db.backref('cities', lazy=True))

    def __str__(self):
        return f"{self.cityname}"


class User(db.Model):
    __tablename__ = 'auth_user'  # Defining table name (equivalent to Meta db_table)

    id = db.Column(db.Integer, primary_key=True)  # Primary key field (auto-generated in Django)
    company_name = db.Column(db.String(250))
    first_name = db.Column(db.String(250))
    last_name = db.Column(db.String(250))
    username = db.Column(db.String(120), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password_hash = db.Column(db.String(128), nullable=True)
    usertype_id = db.Column(db.Integer, db.ForeignKey('usertype.id'), nullable=True)  # Foreign Key to UserType
    image = db.Column(db.Text, default='', nullable=True)
    gender = db.Column(db.String(1), nullable=True)
    dob = db.Column(db.Date, nullable=True)
    calling_code = db.Column(db.String(10), nullable=True)
    phone = db.Column(db.String(20), default='', nullable=True)
    address = db.Column(db.Text, default='', nullable=True)
    pincode = db.Column(db.String(20), default='', nullable=True)
    country = db.Column(db.String(50), default='', nullable=True)
    state = db.Column(db.String(50), default='', nullable=True)
    city = db.Column(db.String(50), default='', nullable=True)
    isdeleted = db.Column(db.Boolean, default=False)
    createddate = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updateddate = db.Column(db.DateTime, nullable=True)

    # Relationship with UserType
    usertype = db.relationship('UserType', backref=db.backref('users', lazy=True))

    def __repr__(self):
        return f'<User {self.username}>'

    def check_password(self, password: str) -> bool:
        """Check if the given password matches the stored password hash."""
        return bcrypt.check_password_hash(self.password_hash, password)

    def set_password(self, password: str) -> None:
        """Hash and set the password."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def get_name(self):
        name = ""
        if self.first_name:
            name = f"{self.first_name}"
        if self.last_name:
            name = f"{name} {self.last_name}" if name else self.last_name
        return name

    def __str__(self):
        return f"{self.username}"


class Site(db.Model):
    __tablename__ = 'site'  # Define the table name

    id = db.Column(db.Integer, primary_key=True)
    owner_user_id = db.Column(db.Integer, db.ForeignKey('auth_user.id'))  # Foreign key to Users model
    sitename = db.Column(db.String(200))
    address = db.Column(db.Text, default='', nullable=True)
    country = db.Column(db.String(50), default='', nullable=True)
    state = db.Column(db.String(50), default='', nullable=True)
    city = db.Column(db.String(50), default='', nullable=True)
    latitude = db.Column(db.String(20), default='', nullable=True)
    longitude = db.Column(db.String(20), default='', nullable=True)
    isdeleted = db.Column(db.Boolean, default=False)
    createddate = db.Column(db.DateTime, default=datetime.utcnow)
    updateddate = db.Column(db.DateTime, nullable=True)

    # Relationship with Users model (Owner of the site)
    owner_user = db.relationship('User', backref=db.backref('sites', lazy=True))

    def __str__(self):
        return self.sitename


class Employee(db.Model):
    __tablename__ = 'employee'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('auth_user.id'), nullable=True)  # Foreign Key to User
    site_info_id = db.Column(db.Integer, db.ForeignKey('site.id'), nullable=True)  # Foreign Key to Site
    joiningdate = db.Column(db.Date, nullable=True)
    min_wages = db.Column(db.Float, default=0.0)
    qualification = db.Column(db.String(250), default='')
    is_on_leave = db.Column(db.Boolean, default=False)
    isdeleted = db.Column(db.Boolean, default=False)
    createddate = db.Column(db.DateTime, default=datetime.utcnow)
    updateddate = db.Column(db.DateTime, nullable=True)

    # Relationships
    user = db.relationship('User', backref=db.backref('employee', uselist=False))
    site_info = db.relationship('Site', backref=db.backref('employees', lazy=True))

    def __str__(self):
        return f"{self.user.username}"


class Attendance(db.Model):
    __tablename__ = 'attendance'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=True)  # ForeignKey to Employee
    site_info_id = db.Column(db.Integer, db.ForeignKey('site.id'), nullable=True)  # ForeignKey to Site
    attendance = db.Column(db.String(2), nullable=True)  # Choices: 'P', 'A', 'HD', 'OT'
    date = db.Column(db.Date, nullable=True)
    isdeleted = db.Column(db.Boolean, default=False)
    createddate = db.Column(db.DateTime, default=datetime.utcnow)
    updateddate = db.Column(db.DateTime, nullable=True)

    # Relationships
    employee = db.relationship('Employee', backref=db.backref('attendances', lazy=True))
    site_info = db.relationship('Site', backref=db.backref('attendances', lazy=True))

    def __str__(self):
        return f"{self.employee}"


class Leave(db.Model):
    __tablename__ = 'leave'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=True)  # ForeignKey to Employee
    site_info_id = db.Column(db.Integer, db.ForeignKey('site.id'), nullable=True)  # ForeignKey to Site
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    reason = db.Column(db.Text, nullable=True)
    isdeleted = db.Column(db.Boolean, default=False)
    createddate = db.Column(db.DateTime, default=datetime.utcnow)
    updateddate = db.Column(db.DateTime, nullable=True)

    # Relationships
    employee = db.relationship('Employee', backref=db.backref('leaves', lazy=True))
    site_info = db.relationship('Site', backref=db.backref('leaves', lazy=True))

    def __str__(self):
        return f"{self.employee.id}"
