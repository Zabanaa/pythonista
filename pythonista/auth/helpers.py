from pythonista import db
from flask import session, url_for
from ..models import Company
from sqlalchemy.exc import IntegrityError

def login_successful(company_email=None):
    '''
        Takes an email as a param.
        Sets the session's company key to the previously passed email
        returns a 302 along with a full url to the index page in the location header (used for redirection)
    '''
    session['company'] = company_email
    return 302, {"message": "Login successful"}, {"Location": url_for('index')}

def logout_successful():
    '''
        Clears the session
        Sends a 302 along with a full url to the index page in the location header (used for redirection)
    '''
    session.clear()
    return 302, {"message": "You have been logged out"}, {"Location": url_for('index')}

def logout_company():
    ''' calls the above function '''
    return logout_successful()

def wrong_password():
    '''
        returns a 401 unauthorised
    '''
    return 401, {"error": "The password you provided is incorrect", "status_code": 401}, {}

def wrong_email():
    '''
        returns a 401 unauthorised if a user attempts to login using a non existant email address
    '''
    return 401, {"error": "No company is registered using this email address", "status_code": 401}, {}

def login_company(payload):

    '''
        Takes a JSON payload in the form of a dict
        We extract the email and password
        Lookup the company by email in the DB
        If there's a match
        We check that the password matches the hash of that company
        We then log them in
        else we return a 401 error
        and if the company does not exist we return a wrong email error

    '''

    email, password = (payload['email'], payload['password'])
    company = Company.query.filter_by(email=email).first()

    if company is not None:
        if company.confirmed:
            if company.verify_password(password) == True:
                return login_successful(company_email=company.email)
            else:
                return wrong_password()
    else:
        return wrong_email()
