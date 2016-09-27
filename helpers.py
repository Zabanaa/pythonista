from flask import jsonify

def send_error(status_code, message=None, missing_fields=None):

    if missing_fields is not None:

        error = {
            'status_code': status_code,
            'message': "Incomplete request. Missing required fields",
            'missing_fields': missing_fields,
        }

    else:
        error = {
            'status_code': status_code,
            'message': message
        }

    return jsonify(error), status_code

def get_missing_fields(response_body):
    missing_fields = []
    for key, value in response_body.items():
        if response_body[key] == None:
            missing_fields.append(key)
    return missing_fields
