import requests
import json
import os

# Load captured data
with open("scripts/try/captured_request.json", "r") as f:
    captured = json.load(f)

url = "https://v2-as.pincc.ai/v1/messages?beta=true"  # Note the ?beta=true parameter
headers = captured["headers"]
data = json.loads(captured["body"])

# Remove headers that are usually set by requests or are specific to the capture session
forbidden = ["Host", "Connection", "Content-Length", "Accept-Encoding"]
for h in forbidden:
    if h in headers:
        del headers[h]

print(f"URL: {url}")
print(f"Data keys: {list(data.keys())}")
print(f"Messages count: {len(data.get('messages', []))}")

response = requests.post(url, headers=headers, json=data)
print(f"Status Code: {response.status_code}")
try:
    print(json.dumps(response.json(), indent=2))
except:
    print(response.text)
