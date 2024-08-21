from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
import jwt
from jwt.exceptions import DecodeError, ExpiredSignatureError

load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World"

@app.route('/sign-token', methods=['GET'])
def sign_token():
    # Mock user object
    user = {
        "id": 2,
        "username": "test",
        "password": "test"
    }
    
    # Encode the token and ensure it's a string
    token = jwt.encode(user, os.getenv('JWT_SECRET'), algorithm="HS256")
    token_str = token.decode('utf-8') if isinstance(token, bytes) else token

    return jsonify({"token": token_str})

@app.route('/verify-token', methods=['POST'])
def verify_token():
    try:
        # Extract the token from the Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"error": "Authorization header is missing"}), 400
        
        parts = auth_header.split(' ')
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return jsonify({"error": "Invalid Authorization header format"}), 400
        
        token = parts[1]

        # Decode the JWT using the secret key and algorithm
        decoded_token = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=["HS256"])

        # Return the decoded token as a JSON response
        return jsonify({"user": decoded_token})
    except DecodeError:
        return jsonify({"error": "Invalid token"}), 400
    except ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 400
    except Exception as error:
        return jsonify({"error": str(error)}), 500 

if __name__ == "__main__":
    app.run()
