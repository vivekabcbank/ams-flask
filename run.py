from app import create_app, db
from flask_jwt_extended import JWTManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.models import  UserType, Country, State, City, User, Site, Employee, Attendance, Leave

app = create_app()

jwt = JWTManager(app)

@app.before_first_request
def create_tables():
    print("Creating tables...")
    db.create_all()


admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')

admin.add_view(ModelView(UserType, db.session))
admin.add_view(ModelView(Country, db.session))
admin.add_view(ModelView(State, db.session))
admin.add_view(ModelView(City, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Site, db.session))
admin.add_view(ModelView(Employee, db.session))
admin.add_view(ModelView(Attendance, db.session))
admin.add_view(ModelView(Leave, db.session))

if __name__ == '__main__':
    app.run(debug=True)
