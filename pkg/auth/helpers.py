from pkg import db
from ..helpers import *
from ..models import Company
from sqlalchemy.exc import IntegrityError

def register_company(payload):

    try:
        new_company = Company(payload)
        db.session.add(new_company)
        db.session.commit()
        return 201, {"message" : "Registration successful"}, {"Location": new_company.get_url()}

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

def logout_company():
    return logout_successful()
