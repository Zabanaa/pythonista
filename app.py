from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from helpers import send_json, get_missing_fields, hash_user_password
from tornado import escape
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')


db = SQLAlchemy(app)
from models import *


@app.route('/')
def index():
    return "Hello and welcome to pythonista.io", 200

@app.route('/register', methods=['GET'])
def load_register_page():
    return "Plase fill out the form to register an account for your company", 200

@app.route("/register", methods=['POST'])
def register_user():
    form = request.get_json()
    value = form.get
    try:
        new_company = Company(
            value('email'),
            hash_user_password(value('password')),
            value('name'),
            value('location'),
            value('website'),
            value('twitter'),
            value('facebook'),
            value('linkedin'),
            value('bio')
        )
        db.session.add(new_company)
        db.session.commit()
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

    # Check if the email corresponds to a company in the db
        # if so,
            # check the password they provided with the password hash related to that company
            # if they match
                # they get a 200 ok
                # and a redirection url to use on the front end
                # also, we set the session for that user
            #else
                # return a 401 with a message about the passwd
    # else
        # we return a 401 unauthorised because the password they provided did not match the hash in the db

    if company is not None:
        if check_password_hash(company.password, password) == True:
            session['company'] = email
            return send_json(200, "you are logged in") # send a redirection url along with the message
        else:
            return send_json(401, "Sorry, the password you provided is incorrect")
    else:
        return send_json(401, "The company does not exist bruv whuh you doin ?")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
