from functools import wraps
from flask import request, jsonify
from auth.jwt_utils import decode_token

def auth_required(required_role=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                auth_header = request.headers.get("Authorization")

                if not auth_header or not auth_header.startswith("Bearer "):
                    return jsonify({"message": "Authorization token missing"}), 401

                token = auth_header.split(" ")[1]
                payload = decode_token(token)

                if not payload:
                    return jsonify({"message": "Invalid or expired token"}), 401

                if required_role and payload.get("role") != required_role:
                    return jsonify({"message": "Forbidden: insufficient permissions"}), 403

                # attach user info for later use
                request.user = payload

                return f(*args, **kwargs)

            except Exception as e:
                print("JWT ERROR:", e)
                return jsonify({"message": "Authentication failed"}), 500

        return wrapper
    return decorator
