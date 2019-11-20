from flask import Blueprint
from utils.controllers_util import json_response

email = Blueprint('email', __name__)


@email.route('/')
def index():
    return json_response(200, 'Funcionou', ['Teste'])
