from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_object('pythonista.config.DevelopmentConfig')
mail = Mail(app)

from pythonista.api.routes import api
from pythonista.auth.routes import auth

app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(auth)


@app.route('/')
def index():
    '''
        Controller for the index page, will eventually return a static html page
        for things like angular, react etc
    '''
    return "Hello, please log in", 200
