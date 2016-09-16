from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

@app.route('/')
def index():
    return "What's going on bruv"


if __name__ == "__main__":
    app.run(debug=True)
