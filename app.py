from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

db = SQLAlchemy(app)
from models import *
from auth import *
from api_helpers import *
from decorators import serialise_json, login_required

@app.route('/')
def index():
    return "Hello, please log in"

@app.route('/register', methods=['GET'])
def load_register_page():
    return "Plase fill out the form to register an account for your company", 200

@app.route("/register", methods=['POST'])
@serialise_json
def register_user():
    form = request.get_json()
    return register_company(form)

@app.route('/login', methods=['GET'])
def load_login_page():
    return "Hello, please submit your credentials to log in", 200

@app.route('/login', methods=["POST"])
@serialise_json
def login():
    form = request.get_json()
    return login_company(form)

@app.route('/logout', methods=['GET'])
@serialise_json
def logout():
    return logout_company()

@app.route('/api/companies', methods=['GET'])
@serialise_json
def companies():
    return get_companies()

@app.route('/api/companies/<int:company_id>', methods=['GET'])
@serialise_json
def company(company_id):
    return get_company(company_id)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
