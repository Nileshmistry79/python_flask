from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from datetime import timedelta

db = SQLAlchemy()
DB_NAME = "users.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'mysecreatwebapp'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['PERMANENT_SESSION_LIFETIME'] = 60

    db.init_app(app)

    from .invoatemr import invoatemr
    from .auth import auth
    from .gen import gen
    from .purespec import purespec

    app.register_blueprint(invoatemr)
    app.register_blueprint(auth)
    app.register_blueprint(gen)
    app.register_blueprint(purespec)

    from .models import User, Note
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app


def create_database(app):
    # if not path.exists('website/' + DB_NAME):
    #     db.create_all(app=app)
    #     print('Created Database!')
    with app.app_context():
        db.create_all()