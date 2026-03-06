#!/usr/bin/env python3
import os
import sys
import requests
import json

token = os.environ.get("CLOUDFLARE_API_KEY")
if not token:
    print("Error: Set CLOUDFLARE_API_KEY", file=sys.stderr)
    sys.exit(1)

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
}

query = """
query {
  __type(name: "Account") {
    fields {
      name
      description
    }
  }
}
"""

response = requests.post(
    "https://api.cloudflare.com/client/v4/graphql",
    headers=headers,
    json={"query": query},
)
data = response.json()

if "errors" in data:
    print(json.dumps(data["errors"], indent=2), file=sys.stderr)
    sys.exit(1)

print("Account fields:")
analytics_fields = []
for field in data["data"]["__type"]["fields"]:
    name = field["name"]
    desc = field.get("description", "")
    print(f"  {name}: {desc}")
    if any(
        kw in name.lower() for kw in ["analytics", "dataset", "web", "metric", "visit"]
    ):
        analytics_fields.append(field)

print("\\nAnalytics-related fields:")
for field in analytics_fields:
    print(f"  {field['name']}: {field.get('description', 'no desc')}")
