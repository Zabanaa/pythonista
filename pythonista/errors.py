from flask import jsonify, session, url_for

def incomplete_request(missing_fields=None):
    '''
        Accepts a list of missing fields returned by the IntegrityError exception thrown by sqlAlchemy
        Returns a 409 conflict along with the list.
    '''
    return 409, {"error": "Incomplete request, Missing required fields.", "status_code": 409,\
                    "missing_fields": missing_fields}, {}
def forbidden():

    '''
        Returns a 403 Forbidden along with a url to the login page in the location header.
    '''

    return 403, {"error": "Forbidden", "status_code": 403}, {"Location": url_for('auth.login')}

def bad_request(reason=None):

    '''
        Returns a 400 bad request response along with an optional reason.
    '''
    return 400, {"error": "Something went wrong", "status_code": 400, "reason": reason}, {}

def not_found():
    '''
        Returns a 404 not found.
    '''
    return 404, {"error": "Not found", "status_code": 404}, {}

def invalid_token():
    '''
        Returns a 404 not found if the token provided by the client is invalid.
    '''
    return 404, {"error": "Invalid Token", "status_code": 404}, {}

def email_already_registered():
    '''
        Will return a 409 Conflict if the user tries to register with an already existing email.
    '''
    return 409, {"error": "A company is already registered using this email", "status_code": 409}, {}

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
