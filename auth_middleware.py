from functools import wraps
from flask import request, jsonify, g
import jwt
import os

# auth_middleware
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        authorization_header = request.headers.get('Authorization')
        # check if there is a header before attempting to decode it
        if authorization_header is None:
            return jsonify({"error": "Unauthorized"}), 401
        try:
            # remove the 'Bearer' portion of the Auth header string
            token = authorization_header.split(' ')[1]
            #decode will throw an error if hte token is invalid, triggering the except block automatically
            token_data = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=["HS256"])
            g.user = token_data
        except Exception as error:
            return jsonify({"error": str(error)}), 500
        return f(*args, **kwargs)
    return decorated_function