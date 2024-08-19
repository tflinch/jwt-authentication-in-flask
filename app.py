from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World"

@app.route('/sign-token', methods=['GET'])
def sign_token():
    #mock user object
    user = {"id":2,
     "username": "test",
     "password": "test"
    }
    return jsonify(user)

app.run()