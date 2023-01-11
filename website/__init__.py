#This is used to make our website a python package, allowing us import the folder and use functions inside this folder
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
#from flask_migrate import Migrate

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'flsafklasfjl;asjfl;as'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    #migrate = Migrate(app,db)
    db.init_app(app)

    from .general import mod
    app.register_blueprint(mod, url_prefix = '/')
 
    from .db_models import User, Stock

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "general.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    with app.app_context():
        if not path.exists('website/' + DB_NAME):
            db.create_all()
            print('db created')
        else:
            print('database on website/' + DB_NAME + 'exists')