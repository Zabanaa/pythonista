from flask import jsonify

def send_error(code, message):
    error = {
        'code': code,
        'message': message
    }
    return jsonify(error)
