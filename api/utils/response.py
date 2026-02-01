from flask import jsonify


def success_response(message, data=None, status_code=200):
    return jsonify({
        "success": True,
        "message": message,
        "data": data,
        "errors": None
    }), status_code


def error_response(message, errors=None, status_code=400):
    return jsonify({
        "success": False,
        "message": message,
        "data": None,
        "errors": errors
    }), status_code
