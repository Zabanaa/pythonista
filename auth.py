from helpers import send_response, wrong_password, wrong_email, get_missing_fields, incomplete_request, bad_request,\
email_already_registered
from sqlalchemy.exc import IntegrityError
from flask import session
from models import Company
from app import db

def register_company(payload):

    try:
        new_company = Company(payload)
        db.session.add(new_company)
        db.session.commit()
        return send_response(201, {
                "status_code": 201,
                "resource": new_company.serialise()
        })
    # return the resources url in the location response header ('location' = newcompany.get_url)
    except IntegrityError as e:
        cause_of_error = str(e.__dict__['orig'])
        if "violates unique constraint" in cause_of_error:
            return email_already_registered()
        elif "not-null" in cause_of_error:
            missing_fields = get_missing_fields(e.__dict__['params'])
            return incomplete_request(missing_fields=missing_fields)
        else:
            return bad_request()

# decorate with serialise_json to avoid having to return send_response
def login_company(payload):

    email, password = (payload['email'], payload['password'])
    company = Company.query.filter_by(email=email).first()

    if company is not None:
        if company.verify_password(password) == True:
            session['company'] = company.email
            return send_response(200, {
                "status_code": 200,
                "message": "Hello %s, welcome back" % company.name,
                "redirect_to": "/"
            })
            # add redirect to location header
            # return 302
        else:
            return wrong_password()
    else:
        return wrong_email()

# decorate with serialise_json to avoid having to return send_response
def logout_company():
    session.clear()
    # add redirect url to location header
    return send_response(200, {"status_code": 302,
                               "message": "You have been logged out", 
                               "redirect_to": "/"
                               })
