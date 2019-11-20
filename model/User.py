# from flask_sqlalchemy import SQLAlchemy
# from config import app_config, app_active
import model.Role
import app
from passlib.hash import pbkdf2_sha256
from model.SerializableModel import SerializableModel, db


# config = app_config[app_active]
# db = SQLAlchemy(config.APP)


class User(db.Model, SerializableModel):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column('username', db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime(6), default=db.func.current_timestamp(), nullable=False)
    last_update = db.Column(db.DateTime(6), onupdate=db.func.current_timestamp(), nullable=True)
    recovery_code = db.Column(db.String(200), nullable=True)
    active = db.Column(db.Boolean(), default=1, nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey(model.Role.Role.id), nullable=False)
    role = db.relationship('Role', lazy=False)

    def get_user_by_email(self):
        try:
            user = db.session.query(User).filter(User.email == self.email).first()
            return user
        except Exception as e:
            raise e
        finally:
            db.session.close()

    def get_user_by_id(self):
        """
            Construiremos	essa	função	capítulos	depois
        """
        return ''

    def update(self):
        db.session.merge(self)
        db.session.commit()
        return self

    def persist(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def find(id):
        user = User.query.filter_by(id= id).first()
        return user

    def hash_password(self, password):
        try:
            return pbkdf2_sha256.hash(password)
        except    Exception    as    e:
            print("Erro	ao	criptografar	senha	%s" % e)

    def set_password(self, password):
        self.password = pbkdf2_sha256.hash(password)

    def verify_password(self, password_no_hash, password_database):
        try:
            return pbkdf2_sha256.verify(password_no_hash, password_database)
        except    ValueError:
            return False
