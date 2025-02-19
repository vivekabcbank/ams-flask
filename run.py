from app import create_app, db
from flask_jwt_extended import JWTManager
app = create_app()

jwt = JWTManager(app)

@app.before_first_request
def create_tables():
    print("Creating tables...")
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
