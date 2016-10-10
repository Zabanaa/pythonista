from pythonista import db
from flask import session, url_for
from ..models import Company
from sqlalchemy.exc import IntegrityError

def login_successful(company_email=None):
    session['company'] = company_email
    return 302, {"message": "Login successful"}, {"Location": url_for('index')}

def logout_successful():
    session.clear()
    return 302, {"message": "You have been logged out"}, {"Location": url_for('index')}

def logout_company():
    return logout_successful()

def wrong_password():
    return 401, {"error": "The password you provided is incorrect", "status_code": 401}, {}

def wrong_email():
    return 401, {"error": "No company is registered using this email address", "status_code": 401}, {}

def incomplete_request(missing_fields=None):
    return 409, {"error": "Incomplete request, Missing required fields.", "status_code": 409,\
                 "missing_fields": missing_fields}, {}

def unauthorised():
    return 403, {"error": "Unauthorised", "status_code": 403}, {"Location": url_for('auth.login')}

def bad_request(reason=None):
    return 400, {"error": "Something went wrong", "status_code": 400, "reason": reason}, {}

def not_found():
    return 404, {"error": "Not found", "status_code": 404}, {}

def login_company(payload):

    email, password = (payload['email'], payload['password'])
    company = Company.query.filter_by(email=email).first()

    if company is not None:
        if company.verify_password(password) == True:
            return login_successful(company_email=company.email)
        else:
            return wrong_password()
    else:
        return wrong_email()

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
