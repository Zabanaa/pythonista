from flask import jsonify

def send_error(code, message):
    error = {
        'code': code,
        'message': message
    }
    return jsonify(error)

def get_missing_fields(response_body):
    missing_fields = []
    for key, value in response_body.items():
        if response_body[key] == None:
            missing_fields.append(key)
    return missing_fields
