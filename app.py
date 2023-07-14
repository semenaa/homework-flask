from flask import Flask, jsonify, request
from flask.views import MethodView

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run()
