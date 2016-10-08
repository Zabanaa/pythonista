from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

from pkg.api.routes import api
from pkg.auth.routes import auth

app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(auth)

app.config.from_object('pkg.config.DevelopmentConfig')

@app.route('/')
def index():
    return "Hello, please log in", 200
