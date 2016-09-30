from flask import jsonify
from app import db
from models import Company
from werkzeug.security import generate_password_hash

def hash_user_password(password):

    '''
        Takes a plain text password and encrypts it
    '''

    if password is not None:
        hashed_password = generate_password_hash(password)
        return hashed_password

def register_company(company_obj):

    '''
    Accepts a request dictionary and saves it as a Company 
    instance in the database
    '''

    if 'password' in company_obj:
        company_obj['password'] = hash_user_password(company_obj['password'])

    new_company = Company(company_obj)
    db.session.add(new_company)
    db.session.commit()

    return new_company


def send_response(status_code, response_object):
    return jsonify(response_object), status_code

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
