from flask import Blueprint, render_template, redirect, request
from utils.controllers_util import json_response
from model.User import User
from exceptions.ValidationException import ValidationException


login = Blueprint('login', __name__)


@login.route('/login/', methods=['GET'])
def go_login():
    return render_template('login.html')


@login.route('/do-login/', methods=['POST'])
def do_login():
    user = User()
    user.email = request.form['email']
    password = request.form['password']
    result = user.get_user_by_email()

    if result is not None:
        res = user.verify_password(password_no_hash=password, password_database=result.password)
        if res:
            return json_response(200, 'Usuário autenticado.',result.as_dict())
    exception = ValidationException('login', 'Usuário ou senha inválidos')
    raise exception


@login.route('/recovery-password/')
def recovery_password():
    return 'To do...'


@login.route('/profile/<int:id>/')
def profile(id):
    return 'O id desse usuário é %d' % id