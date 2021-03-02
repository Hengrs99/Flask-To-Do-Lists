from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    """ construct the core application """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'supersecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # IMPORTS
    from .views import views
    from .auth import auth
    from .api import api
    from . import models

    create_database(app)

    # LOGIN MANAGER SETUP
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return models.User.query.get(int(id))

    # REGISTER ROUTES
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(api, url_prefix='/')

    return app


def create_database(app):
    """ initialize database """
    if not path.exists(f'website/{DB_NAME}'):
        db.create_all(app=app)
        print('Database Created!')
