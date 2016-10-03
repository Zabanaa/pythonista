from flask import Flask, request, jsonify, session, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from tornado import escape
from werkzeug.security import check_password_hash
from decorators import serialise_json

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

db = SQLAlchemy(app)
from models import *
from helpers import get_missing_fields, register_company, send_response, wrong_email, email_already_registered,\
incomplete_request, bad_request, wrong_password


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
        return send_response(201, {"status_code": 201, "company": new_company.serialise()})

    except IntegrityError as e:
        cause_of_error = str(e.__dict__['orig'])
        if "violates unique constraint" in cause_of_error:
            return email_already_registered()
        elif "not-null" in cause_of_error:
            missing_fields = get_missing_fields(e.__dict__['params'])
            return incomplete_request(missing_fields=missing_fields)
        else:
            return bad_request()

@app.route('/login', methods=['GET'])
def load_login_page():
    return "Hello, please submit your credentials to log in", 200

@app.route('/login', methods=["POST"])
def login():

    form = request.get_json()
    login_creds = (form['email'], form['password'])
    company = Company.query.filter_by(email=login_creds[0]).first()
    # login_user(company)
    if company is not None:
        if check_password_hash(company.password, login_creds[1]) == True:
            session['company'] = company.name
            return send_response(200, {
                "status_code": 200,
                "message": "Hello %s, welcome back" % session['company'],
                "redirect_to": "/"
            })
        else:
            wrong_password()
    else:
        wrong_email()

@app.route('/logout', methods=['GET'])
def logout_user():
    session.clear()
    return send_response(200, {
        "status_code": 200,
        "message": "You are now logged out",
        "redirect_to": url_for("index") 
    })

# get company (accepts company_id as a parameter)
# get_job_by_id (accepts job_id as a parameter)
# get_company_jobs (accepts company_id as a parameter and queries the db to get all the jobs related to that company)



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
