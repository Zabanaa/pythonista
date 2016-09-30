from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from tornado import escape
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')


db = SQLAlchemy(app)
from models import *
from helpers import send_json, get_missing_fields, hash_user_password, register_company


@app.route('/')
def index():
    if 'company' in session:
        return "Hello %s, and welcome back home" % session['company']
    else:
        return "Hello and welcome to pythonista.io, please login", 200

@app.route('/register', methods=['GET'])
def load_register_page():
    return "Plase fill out the form to register an account for your company", 200

@app.route("/register", methods=['POST'])
def register_user():
    form = request.get_json()
    try:
        new_company = register_company(form)
        return send_json(201, resource=new_company.serialise())
    except IntegrityError as e:
        cause_of_error = str(e.__dict__['orig'])
        if "violates unique constraint" in cause_of_error:
            return send_json(409, "sorry, it seems like a company is already registered using this email")
        elif "not-null" in cause_of_error:
            missing_fields = get_missing_fields(e.__dict__['params'])
            return send_json(409, missing_fields=missing_fields)
        else:
            return send_json(400, cause_or_error)

@app.route('/login', methods=['GET'])
def load_login_page():
    return "Hello, please submit your credentials to log in", 200


@app.route('/login', methods=["POST"])
def login():

    login_credentials = request.get_json()
    value = login_credentials.get
    email = value('email')
    password = value('password')
    company = Company.query.filter_by(email=email).first()

    if company is not None:
        if check_password_hash(company.password, password) == True:
            session['company'] = company.name
            welcome_message = "Hello %s, welcome back" % session['company']
            return send_json(200, welcome_message) # Add redirect url
        else:
            return send_json(401, "Sorry, the password you provided is incorrect")
    else:
        return send_json(401, "Sorry, there is no company registered at this address")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
