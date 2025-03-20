import requests
import json

endpoint_id = "ud7kgi0v1yvtlm"
api_key = "4V6LMT65ASH1HCAV6GFVPUQJX75PYG8EOPBMC2GV"

url = f"https://api.runpod.ai/v2/{endpoint_id}/runsync"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}

json_data = {
    "input": {
        "user_name": ["Jack Davis"],
        "call_reason": ["Discuss partnership"],
        "user_company": ["TechCorp"],
        "job_title": ["CTO"],
        "speed_multiplier": "1"
    }
}

try:
    response = requests.post(url, json=json_data, headers=headers)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"API request failed: {e}")
    exit()

result = response.json()

call_script = result.get("output", {}).get("call_script")

if call_script:
    print("API Response Received")
    print("Call Script Generated Successfully:")
    print(call_script)
else:
    print("No call script found in API response")
