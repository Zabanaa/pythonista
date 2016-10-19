from flask import jsonify, session, request
from .errors import *
from .models import *
import functools

def login_required(f):

    '''
        Checks if the session contains a key called company
        And that it matches the email of the actual company
        If it does, it proceeds to the function called by the controller
        else it returns a 403 Unauthorised response
    '''

    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if 'company' in session:
            company = Company.query.filter_by(email=session['company']).first()

            if session['company'] == company.email:
                return f(*args, **kwargs)
        else:
            return unauthorised()
    return wrapped

# Serialise Json
def serialise_json(f):
    '''
        Takes the return value (aka the response) from the
        controller and jsonifies it
        (Only works if the response is a tuple)
        (This decorator is dependent on the order by which the elemnts are returned)
    '''
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        return_value = f(*args, **kwargs)
        status_code = None
        headers = None

        if isinstance(return_value, tuple): # The response is a tuple
            status_code, data, headers = return_value # unpack the tuple
            return_value = jsonify(data) # jsonify the response object
            return_value.status_code = status_code

            if headers is not None:
                return_value.headers.extend(headers)
        return return_value

    return wrapped

