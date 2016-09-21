from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from helpers import send_error

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')


db = SQLAlchemy(app)
from models import Company

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

        except Exception as e:
            if "violates unique constraint" in str(e.__dict__['orig']):
                return jsonify({"code": 400, "message": "A company is already registered using this email"})
    else:
        return "Whuuuuh ? Just let man register"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
