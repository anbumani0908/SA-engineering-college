import requests
import json

# API endpoint
url = "https://ollama.com/api/chat"

# Headers
headers = {
    "Authorization": "Bearer 75abea0b9b8d4d329432a2fbb6fcf1c8.dr3IdxNsGm0IMSgpN4pKIdDt",
    "Content-Type": "application/json"
}

# Strict system prompt for JSON output
system_prompt = """
You are an AC control assistant. Always respond ONLY in the following JSON format:
{"action": "<TURN_ON_AC | TURN_OFF_AC | KEEP_STATE>"}

Rules:
- If temperature > 30 → {"action": "TURN_ON_AC"}
- If temperature < 20 → {"action": "TURN_OFF_AC"}
- If 20 <= temperature <= 30 → {"action": "KEEP_STATE"}
"""

while True:
    try:
        # Take temperature input from user
        temperature = input("\nEnter the temperature (or type 'exit' to quit): ")
        if temperature.lower() == "exit":
            print("Exiting AC control assistant.")
            break
        
        # Validate input
        try:
            temperature = float(temperature)
        except ValueError:
            print("⚠️ Please enter a valid number.")
            continue

        # Payload
        payload = {
            "model": "gpt-oss:120b",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"The current temperature is {temperature}°C"}
            ],
            "stream": False
        }

        # Send POST request
        response = requests.post(url, headers=headers, data=json.dumps(payload))

        # Process response
        if response.status_code == 200:
            data = response.json()
            assistant_message = data.get("message", {}).get("content", "")

            try:
                # Convert to Python dict
                action_dict = json.loads(assistant_message)
                print("Assistant says:", action_dict)
            except json.JSONDecodeError:
                # If response is not clean JSON
                print("Assistant says (raw):", assistant_message)

        else:
            print("Error:", response.status_code, response.text)

    except KeyboardInterrupt:
        print("\nExiting AC control assistant.")
        break
