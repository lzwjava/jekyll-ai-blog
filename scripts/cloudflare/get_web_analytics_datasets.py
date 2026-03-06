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

    account_id = (
        os.environ.get("CLOUDFLARE_ACCOUNT_ID") or "4c073cd42000b12a4d61bb679c0043d4"
    )

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    query = (
        """
    query {
      viewer {
        accounts(filter: {accountTag: "%s"}) {
          analyticsEngineDatasets {
            name
          }
        }
      }
    }
    """
        % account_id
    )

    response = requests.post(
        "https://api.cloudflare.com/client/v4/graphql",
        headers=headers,
        json={"query": query},
    )
    if response.status_code != 200:
        print(f"Error: {response.status_code} {response.text}", file=sys.stderr)
        sys.exit(1)

    data = response.json()
    if "errors" in data:
        print(
            f"GraphQL errors: {json.dumps(data['errors'], indent=2)}", file=sys.stderr
        )
        sys.exit(1)

    try:
        datasets = data["data"]["viewer"]["accounts"][0]["analyticsEngineDatasets"]
        print("Web Analytics datasets:")
        for d in datasets:
            print(f"  {d['name']}")
    except (KeyError, IndexError):
        print("No datasets found or error parsing.")


if __name__ == "__main__":
    main()
