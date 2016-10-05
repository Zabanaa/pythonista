from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from decorators import serialise_json

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

db = SQLAlchemy(app)
from models import * 
from auth import *
from api_helpers import *


@app.route('/')
def index():
    if 'company' in session:
        return "Hello %s, and welcome back home" % session['company'], 200
    else:
        return "Hello and welcome to pythonista.io, please login", 200

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
def get_companies():
    companies = [c.serialise() for c in Company.query.all()]
    return 200, {"status_code": 200, "companies": companies}, {}


# get company (accepts company_id as a parameter)
# get_job_by_id (accepts job_id as a parameter)
# get_company_jobs (accepts company_id as a parameter and queries the db to get all the jobs related to that company)



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
