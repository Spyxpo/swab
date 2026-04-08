from flask import Blueprint, request
from api.utils.response import success_response, error_response

example_bp = Blueprint(
    "example_bp",
    __name__,
    url_prefix="/api/v1/examples"
)

@example_bp.route("/", methods=["POST"])
def create_example():
    try:
        print("API HIT")  # debug marker

        data = request.get_json()
        print("DATA:", data)

        if not data or "name" not in data:
            return error_response(
                message="Validation failed",
                errors={"name": "This field is required"},
                status_code=400
            )

        return success_response(
            message="Example created successfully",
            data=data,
            status_code=201
        )

    except Exception as e:
        print("ERROR:", e)
        return error_response(
            message="Internal server error",
            errors=str(e),
            status_code=500
        )
