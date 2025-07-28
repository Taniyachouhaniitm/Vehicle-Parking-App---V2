from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from celery import Celery
from werkzeug.security import generate_password_hash

from config import Config  
from models import db, Role, User
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.user_routes import user_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    
    db.init_app(app)
    jwt = JWTManager(app)
    CORS(app, supports_credentials=True)

  
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)

  
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(user_bp, url_prefix='/user')
    with app.app_context():
        db.create_all()

    
        if not Role.query.first():
            admin_role = Role(name='admin')
            user_role = Role(name='user')
            db.session.add_all([admin_role, user_role])
            db.session.commit()

    
        if not User.query.filter_by(username='admin').first():
            admin_role = Role.query.filter_by(name='admin').first()
            admin_user = User(
                username='admin',
                email='admin@abc.com',
                fname='Admin',
                lname='User',
                password=generate_password_hash('admin'),
                role=admin_role
            )
            db.session.add(admin_user)
            db.session.commit()

    return app, celery


app, celery = create_app()

@app.route('/')
def home():
    return 'Vehicle Parking app'



if __name__ == '__main__':
    app.run(debug=True)
