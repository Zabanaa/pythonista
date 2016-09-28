from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from helpers import send_error, get_missing_fields, hash_user_password
from tornado import escape

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')


db = SQLAlchemy(app)
from models import *


@app.route('/')
def index():
    return "hello this is the index page newwww one brruuuv", 200

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        payload = request.json
        d = payload.get
        try:
            new_company = Company(d('email'), hash_user_password(d('password')), d('name'), d('location'), d('website'), d('twitter'),\
                                                                            d('facebook'), d('linkedin'), d('bio'))
            db.session.add(new_company)
            db.session.commit()
            return jsonify(new_company.serialise()), 201
        except IntegrityError as e:
            cause_of_error = str(e.__dict__['orig'])
            if "violates unique constraint" in cause_of_error:
                return send_error(409, "Bruv, A company is already registered using this email")
            elif "not-null" in cause_of_error:
                missing_fields = get_missing_fields(e.__dict__['params'])
                return send_error(409, missing_fields=missing_fields)
            else:
                return jsonify({"status_code": 400, "message": cause_or_error}), 400
    else:
        return "Whuuuuh ? Just let man register", 200

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        return jsonify(request.get_json()), 200
    else:
        return 'Bruv you want to login ?', 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
