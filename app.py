from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from helpers import send_error

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

db = SQLAlchemy(app)
import models

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    payload = request.json
    d = payload.get
    if payload:
        try:
            new_company = models.Company(d('email'), d('password'), d('name'), d('location'), d('website'), d('twitter'),\
                                     d('facebook'), d('linkedin'), d('bio'))
            db.session.add(new_company)
            db.session.commit()
            return jsonify(new_company.serialise()), 201
        except Exception as e:
            if "violates unique constraint" in str(e.__dict__['orig']):
                return send_error(400, "A company is already registered using this email") 

    return "<h1> Registration Page Bruuuuv </h1>"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
