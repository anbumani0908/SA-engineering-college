import requests
import json
import re

# API endpoint
url = "https://ollama.com/api/chat"

# Headers
headers = {
    "Authorization": "Bearer 75abea0b9b8d4d329432a2fbb6fcf1c8.dr3IdxNsGm0IMSgpN4pKIdDt",
    "Content-Type": "application/json"
}

# Payload
payload = {
    "model": "gpt-oss:120b",
    "messages": [
        {"role": "user", "content": "Hello"}
    ],
    "stream": False
}

# Send POST request
response = requests.post(url, headers=headers, data=json.dumps(payload))

if response.status_code == 200:
    response_text = response.text  # Get raw JSON string

    # Regex pattern to extract the assistant's content
    match = re.search(r'"content"\s*:\s*"([^"]+)"', response_text)
    if match:
        assistant_message = match.group(1)
        print("Assistant says:\n")
        print(assistant_message)
    else:
        print("Assistant message not found.")
else:
    print("Error:", response.status_code, response.text)
