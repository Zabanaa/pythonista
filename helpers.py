from flask import jsonify
from werkzeug.security import generate_password_hash

def hash_user_password(password):
    if password is not None:
        hashed_password = generate_password_hash(password)
        return hashed_password

def send_error(status_code, message=None, missing_fields=None):

    if missing_fields is not None:

        error = {
            'status_code': status_code,
            'message': "Incomplete request. Missing required fields".lower(),
            'missing_fields': missing_fields,
        }

    else:
        error = {
            'status_code': status_code,
            'message': message.lower()
        }

    return jsonify(error), status_code

def get_missing_fields(response_body):
    missing_fields = []
    for key, value in response_body.items():
        if response_body[key] == None:
            missing_fields.append(key)
    return missing_fields
