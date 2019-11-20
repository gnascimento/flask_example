#	-*-	coding:	utf-8	-*-
from flask import Flask, request, render_template, redirect
#	config	import
from config import app_config, app_active
# import config
from flask_sqlalchemy import SQLAlchemy
import wtforms_json

config = app_config[app_active]

db_config: SQLAlchemy


def create_app(config_name):
    app = Flask(__name__, template_folder='templates')
    app.secret_key = config.SECRET
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    global db_config
    db_config = SQLAlchemy(config.APP)
    db_config.init_app(app)

    #compatibilidade com wtforms json
    wtforms_json.init()

    from controller import email_controller, user_controller, login_controller
    from handlers import error_handler
    app.register_blueprint(email_controller.email, url_prefix='/email')
    app.register_blueprint(user_controller.user, url_prefix='/user')
    app.register_blueprint(login_controller.login, url_prefix='/')
    app.register_blueprint(error_handler.errors, url_prefix='/error')


    @app.route('/')
    def index():
        return 'Hello World!'

    return app
