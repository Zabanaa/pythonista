from app import *
from flask import jsonify, session, url_for
from models import *

def wrong_password():
    return 401, {"error": "The password you provided is incorrect", "status_code": 401}, {}

def email_already_registered():
    return 409, {"error": "A company is already registered using this email", "status_code": 409}, {}

def wrong_email():
    return 401, {"error": "No company is registered using this email address", "status_code": 401}, {}

def incomplete_request(missing_fields=None):
    return 409, {"error": "Incomplete request, Missing required fields.", "status_code": 409,\
                    "missing_fields": missing_fields}, {}

def bad_request(reason=None):
    return 400, {"error": "Something went wrong", "status_code": 400, "reason": reason}, {}

def not_found():
    return 404, {"error": "Not found", "status_code": 404}, {}

def login_successful(company_email=None):
    session['company'] = company_email
    return 302, {"message": "Login successful"}, {"Location": url_for('index')}

def logout_successful():
    session.clear()
    return 302, {"message": "You have been logged out"}, {"Location": url_for('index')}

def get_missing_fields(response_body):

    '''
    Accepts a dict containing the payload.
    Loops through that dict
    Appends the keys with a value of None to a list
    returns that list
    '''

    missing_fields = []
    for key, value in response_body.items():
        if response_body[key] == None:
            missing_fields.append(key)
    return missing_fields
