from flask import Blueprint, request, jsonify
from auth.jwt_utils import generate_token

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")

# TEMP users (later DB)
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "user": {"password": "user123", "role": "user"}
}

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or "username" not in data or "password" not in data:
        return jsonify({"message": "Invalid credentials"}), 400

    user = USERS.get(data["username"])
    if not user or user["password"] != data["password"]:
        return jsonify({"message": "Unauthorized"}), 401

    token = generate_token(data["username"], user["role"])

    return jsonify({
        "success": True,
        "token": token
    })
