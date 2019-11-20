from flask import Blueprint, request, redirect, render_template
from model.User import User
from wtforms import Form, BooleanField, StringField, PasswordField, IntegerField, validators
from exceptions.ValidationException import ValidationException
from utils.controllers_util import json_response


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=40, message='O campo "username" precisa ter entre 4 e 40 caracteres')])
    email = StringField('E-mail', [validators.Length(min=6, max=250, message='O campo "e-mail" precisa ter entre 6 e 250 caracteres'), validators.Email(message= 'O e-mail informado é inválido')])
    password = PasswordField('Senha', [
        validators.DataRequired(message= 'O campo "senha" é requerido'),
        validators.EqualTo('confirm', message='A confirmação de senha não é igual a senha informada')
    ])
    confirm = PasswordField('Repeat Password')
    active = BooleanField('Ativo', false_values=['false', False, '0', 0])
    role_id = IntegerField('Grupo', [validators.DataRequired(message='O campo "grupo" é requerido')])

user = Blueprint('user', __name__)


@user.route('/', methods=['POST'])
def create():
    # form = RegistrationForm(request.form)
    form = RegistrationForm.from_json(request.json)
    if form.validate():
        user = User()
        user.username = form.username.data
        user.email = form.email.data
        user.password = user.hash_password(form.password.data)
        user.active = form.active.data
        user.role_id = form.role_id.data
        user.persist()
        return json_response(201, "Usuário criado com sucesso", user.as_dict())
    else:
        raise ValidationException.from_wt_forms(form)


@user.route('/<int:id>', methods=['PUT'])
def update(id):
    # form = RegistrationForm(request.form)
    form = RegistrationForm.from_json(request.json)
    if form.validate():
        user = User()
        user.id = id
        user.username = form.username.data
        user.email = form.email.data
        user.password = user.hash_password(form.password.data)
        user.active = form.active.data
        user.role_id = form.role_id.data
        user.update()
        return json_response(200, "Usuário atualizado com sucesso", user.as_dict())
    else:
        raise ValidationException.from_wt_forms(form)


@user.route('/<int:id>', methods=['DELETE'])
def delete(id):
    user = User.find(id)
    if user is not None:
        user.delete()
        return json_response(200, "Usuário excluído com sucesso", None)
    else:
        raise ValidationException('id', 'Não existe usuário com o id %d informado' % id)