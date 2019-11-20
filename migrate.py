from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import app
from app import create_app
from config import app_config, app_active


config = app_config[app_active]
config.APP = create_app(app_active)

config = app_config[app_active]

migrate = Migrate(config.APP, app.db_config)
manager = Manager(config.APP)
manager.add_command('db', MigrateCommand)

#importa os models apos carregar a base
from model import User, Role, Product, Category



if __name__ == '__main__':
    manager.run()
