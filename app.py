from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from helpers import send_error, get_missing_fields

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')


db = SQLAlchemy(app)
from models import * 


@app.route('/')
def index():
    return "hello this is the index page newwww one brruuuv"

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        payload = request.json
        d = payload.get
        try:
            new_company = Company(d('email'), d('password'), d('name'), d('location'), d('website'), d('twitter'),\
                                                                            d('facebook'), d('linkedin'), d('bio'))
            db.session.add(new_company)
            db.session.commit()
            return jsonify(new_company.serialise()), 201
        except IntegrityError as e:
            cause_of_error = str(e.__dict__['orig'])
            if "violates unique constraint" in cause_of_error:
                return jsonify({"code": 400, "message": "A company is already registered using this email"}), 400
            elif "not-null" in cause_of_error:
                missing_fields = get_missing_fields(e.__dict__['params'])
                return jsonify({"code": "400", "missing_fields": missing_fields, "message": "wagwaan bruv, you missed\
                some fields", "reason": cause_of_error}), 400
            else:
                return jsonify({"code": "400", "message": cause_or_error}), 400
    else:
        return "Whuuuuh ? Just let man register"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
