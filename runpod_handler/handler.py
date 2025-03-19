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
    user_name = event['input']["user_name"]
    call_reason = event['input']["call_reason"]
    user_company = event['input']["user_company"]
    job_title = event['input']["job_title"]
    tone = event['input'].get("tone", "Formal")

    call_script = service.get_call_script(
        user_name, call_reason, user_company, job_title, tone)
    return {
        "call_script": call_script
    }


if __name__ == "__main__":
    runpod.serverless.start({
        "handler": handler
    })
