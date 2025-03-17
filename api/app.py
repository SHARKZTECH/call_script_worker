import traceback
from flask import Flask, jsonify
from flask_restful import Api
from api.call_script.resources import CallScriptResource
from api.health.resource import Health
from werkzeug.exceptions import default_exceptions, HTTPException

HEALTH_ROUTE = "/health"
CALL_SCRIPT_ROUTE = "/"


def create_app():
    app = Flask(__name__)
    api = Api(app, catch_all_404s=True)

    api.add_resource(Health, HEALTH_ROUTE)
    api.add_resource(CallScriptResource, CALL_SCRIPT_ROUTE)

    app = _setup_json_error_handling(app)

    return app


def _setup_json_error_handling(app):
    """Setup JSON error handling for Flask application."""

    def make_json_error(ex):
        """Generate JSON error response."""
        message = f"{type(ex).__name__}: {str(ex)}"
        traceback_string = traceback.format_exc()

        data = {
            "error": 1,
            "message": message,
            "traceback": traceback_string,
            "type": ex.__class__.__name__,
        }

        if isinstance(ex, HTTPException):
            data["code"] = ex.code
            response = jsonify(data)
            response.status_code = ex.code
        else:
            response = jsonify(data)
            response.status_code = 500  # Internal Server Error

        return response

    # Register error handlers **ONLY for valid HTTP status codes**
    for code in list(default_exceptions.keys()):  # Only standard HTTP error codes
        app.register_error_handler(code, make_json_error)

    app.register_error_handler(Exception, make_json_error)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8000, debug=True)
