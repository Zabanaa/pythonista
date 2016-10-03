from flask import jsonify
from app import db
from models import Company

# Login required decorator

# check if company is in the session
# check that the session value is equal to the actual company name
# if so execute the function
# else return a 403 unauthorised and redirect the user

def wrong_password():
    response = jsonify({"error": "The password you provided is incorrect", "status_code": 401})
    response.status_code = 401
    return response

def email_already_registered():
    response = jsonify({"error": "A company is already registered using this email", "status_code": 409})
    response.status_code = 409
    return response

def wrong_email():
    response = jsonify({"error": "No company is registered using this email address", "status_code": 401})
    response.status_code = 401
    return response

def incomplete_request(missing_fields=None):
    response = jsonify({"error": "Incomplete request, missing required fields", "status_code": 409,\
                    "missing_fields": missing_fields})
    response.status_code = 409
    return response

def bad_request(reason=None):
    response = jsonify({"error": "Something went wrong", "status_code": 400, "reason": reason})
    response.status_code = 400
    return response

def register_company(company_obj):

    '''
    Accepts a request dictionary and saves it as a Company 
    instance in the database
    '''

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
