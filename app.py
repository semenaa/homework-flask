from flask import Flask, jsonify, request
from flask.views import MethodView

app = Flask('homework-flask')


@app.route('/')
def hello():
    return 'Hello, World!'
