from flask import Flask, request
from main import info, handler

app = Flask(__name__)


@app.route("/")
def get_info():
    return info(None, None)['body']


@app.route("/start", methods=['POST'])
def start():
    return handler({'path': '/start'}, None)['body']


@app.route("/end", methods=['POST'])
def end():
    return handler({'path': '/end'}, None)['body']


@app.route("/move", methods=['POST'])
def move():
    return handler({'path': '/move', 'body': request.data}, None)['body']
