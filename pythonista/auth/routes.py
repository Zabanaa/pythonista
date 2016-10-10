from flask import Blueprint
from .helpers import *
from ..errors import *
from ..decorators import *

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET'])
def load_register_page():
    return "Plase fill out the form to register an account for your company", 200

@auth.route("/register", methods=['POST'])
@serialise_json
def register_user():
    form = request.get_json()
    return register_company(form)

@auth.route('/login', methods=['GET'])
def load_login_page():
    return "Hello, please submit your credentials to log in", 200

@auth.route('/login', methods=["POST"])
@serialise_json
def login():
    form = request.get_json()
    return login_company(form)

@auth.route('/logout', methods=['GET'])
@serialise_json
def logout():
    return logout_company()
