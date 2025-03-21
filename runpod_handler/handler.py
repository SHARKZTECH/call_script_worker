import runpod
from typing import Dict

from api.call_script.service import CallScriptService
from api.app import create_app

print("Starting RunPod handler...")
app = create_app()
service: CallScriptService = app.injector.get(CallScriptService)
print("Handler loaded")


def handler(event: Dict):
    print(f"Running inference on {event}")
    input_data = event['input']

    def unwrap(value):
        return value[0] if isinstance(value, list) else value

    user_name = unwrap(input_data.get("user_name", ""))
    call_reason = unwrap(input_data.get("call_reason", ""))
    user_company = unwrap(input_data.get("user_company", ""))
    job_title = unwrap(input_data.get("job_title", ""))
    tone = unwrap(input_data.get("tone", "Formal"))
    language = unwrap(input_data.get("language", "english"))

    call_script = service.get_call_script(
        user_name, call_reason, user_company, job_title, tone, language)

    return {
        "call_script": call_script
    }


if __name__ == "__main__":
    runpod.serverless.start({
        "handler": handler
    })
