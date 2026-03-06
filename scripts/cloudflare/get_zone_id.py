#!/usr/bin/env python3
import os
import sys
import requests
import json


def main():
    token = os.environ.get("CLOUDFLARE_API_KEY")
    if not token:
        print("Error: Set CLOUDFLARE_API_KEY environment variable", file=sys.stderr)
        sys.exit(1)

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    response = requests.get(
        "https://api.cloudflare.com/client/v4/zones", headers=headers
    )
    if response.status_code != 200:
        print(f"Error: {response.status_code} {response.text}", file=sys.stderr)
        sys.exit(1)

    data = response.json()
    if not data.get("success"):
        print(f"API error: {json.dumps(data, indent=2)}", file=sys.stderr)
        sys.exit(1)

    print("Available zones:")
    for zone in data["result"]:
        print(f"  Zone ID: {zone['id']}")
        print(f"  Name: {zone['name']}")
        print(f"  Status: {zone['status']}")
        print()


if __name__ == "__main__":
    main()
