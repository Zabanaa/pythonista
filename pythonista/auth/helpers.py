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

def email_already_registered():
    return 409, {"error": "A company is already registered using this email", "status_code": 409}, {}

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

def register_company(payload):

    try:
        new_company = Company(payload)
        db.session.add(new_company)
        db.session.commit()
        return 201, {"status_code": 201, "message" : "Registration successful"}, {"Location": new_company.get_url()}

    except IntegrityError as e:
        cause_of_error = str(e.__dict__['orig'])
        if "violates unique constraint" in cause_of_error:
            return email_already_registered()
        elif "not-null" in cause_of_error:
            missing_fields = get_missing_fields(e.__dict__['params'])
            return incomplete_request(missing_fields=missing_fields)
        else:
            return bad_request()

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

