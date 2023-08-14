import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

DB_NAME = "database.db"

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(12).hex()
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Task

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
