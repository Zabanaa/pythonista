from helpers import send_response, wrong_password, wrong_email, get_missing_fields, incomplete_request, bad_request,\
email_already_registered
from sqlalchemy.exc import IntegrityError
from flask import session, url_for
from models import Company
from app import * 

def register_company(payload):

    try:
        new_company = Company(payload)
        db.session.add(new_company)
        db.session.commit()
        return 201, {"message" : "Registration successful"}, {"Location": "bruvjjj"}

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
            session['company'] = company.email
            return 302, {"message": "Login successful"}, {"Location": url_for('index')}
        else:
            return wrong_password()
    else:
        return wrong_email()

def logout_company():
    session.clear()
    return 302, {"message": "You have been logged out"}, {"Location": url_for('index')}
