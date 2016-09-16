from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

db = SQLAlchemy(app)

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
