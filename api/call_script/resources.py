from flask import request
from flask_restful import Resource
from api.call_script.service import CallScriptService


class CallScriptResource(Resource):
    """REST API Endpoint for Call Script Generation."""

    def post(self):
        """Handle API requests to generate a call script."""
        data = request.get_json()

        required_fields = ["user_name", "call_reason",
                           "user_company", "job_title"]
        for field in required_fields:
            if field not in data:
                return {"error": f"Missing required field: {field}"}, 400

        user_name = data["user_name"]
        call_reason = data["call_reason"]
        user_company = data["user_company"]
        job_title = data["job_title"]
        tone = data.get("tone", "Formal")

        call_script = CallScriptService.get_call_script(
            user_name, call_reason, user_company, job_title, tone)

        if call_script:
            return {"call_script": call_script}, 200
        else:
            return {"error": "Failed to generate call script"}, 500
