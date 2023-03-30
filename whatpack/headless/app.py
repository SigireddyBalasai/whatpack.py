"""This is the flask module we will write get the request and send the response"""

from flask import Flask, request, current_app, send_file
from .whats import WhatsApp

app = Flask(__name__)


@app.route('/')
def hello_world():
    """A hello world method for testing if the webserver works"""
    return 'Hello, World!'


@app.route('/send_message')
def send_message_to_number():
    """This is the method to send message to a number"""
    print(request.args)
    phone = request.args.get('phone')
    current_app.config['ok'].send_user_message(phone, request.args.get('message'))
    return 'done'


@app.route('/send_user_image')
def send_user_image():
    """This will send an image to the user"""
    current_app.config['ok'].send_image(request.args.get('phone'), request.args.get('filename'))
    return 'done'


@app.route("/send_user_document")
def send_user_document():
    """THid will send a document to the user"""
    filename = request.args.get('filename')
    phone = request.args.get('phone')
    current_app.config['ok'].send_document(phone, filename=filename)
    return 'done'


@app.route("/login")
def send_login_image():
    """"Login to whatsapp web by scanning the QR code Send the image to the user"""
    app.config['ok'] = WhatsApp()
    return send_file('hello.png')


def create_app():
    """This will return the app"""
    return app
