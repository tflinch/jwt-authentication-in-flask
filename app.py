from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
import jwt
import bcrypt
import psycopg2, psycopg2.extras
from jwt.exceptions import DecodeError, ExpiredSignatureError

load_dotenv()

password = b"super secret password"
# Hash a password for the first time, with a randomly-generated salt
hashed = bcrypt.hashpw(password, bcrypt.gensalt())
# Check that an unhashed password matches one that has previously been
# hashed
if bcrypt.checkpw(password, hashed):
    print("It Matches!")
else:
    print("It Does not Match :(")


def get_db_connection():
    connection = psycopg2.connect(host='localhost',
                            database='flask_auth_db',
                            user=os.getenv('POSTGRES_USERNAME'),
                            password=os.getenv('POSTGRES_PASSWORD'))
    return connection

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

@app.route('/auth/signup', methods=['POST'])
def signup():
    try:
        new_user_data = request.get_json()
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT * FROM users WHERE username = %s;", (new_user_data["username"],))
        existing_user = cursor.fetchone()
        if existing_user:
            cursor.close()
            return jsonify({"error": "Username already taken"}), 400
        hashed_password = bcrypt.hashpw(bytes(new_user_data["password"], 'utf-8'), bcrypt.gensalt())
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s) RETURNING username", (new_user_data["username"], hashed_password.decode('utf-8')))
        created_user = cursor.fetchone()
        connection.commit()
        connection.close()
        return jsonify(created_user), 201
    except Exception as error:
        return jsonify({"error": str(error)}), 401

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
