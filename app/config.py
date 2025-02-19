class Config:
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@db:5432/ecommerce'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/mac/Documents/ams-flask/ams-flask/ecommerce.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your-secret-key'
    JWT_SECRET_KEY = 'your-secret-key'  # Change this to something more secure

