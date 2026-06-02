---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Python Script for Nexus NPM Downloads
translated: false
type: note
---

Here's a Python script to download an npm package from your internal Nexus registry:

```python
import os
import requests
import sys
import json

def download_npm_package(registry_url, package_name, version=None, output_dir="."):
    """
    Download an npm package from an internal Nexus registry.

    Args:
        registry_url: Base URL of the Nexus npm registry (e.g., https://company.com/npm/group)
        package_name: Name of the package (e.g., 'lodash' or '@scope/package-name')
        version: Specific version to download (optional, defaults to latest)
        output_dir: Directory to save the downloaded package
    """

    # Get auth token from environment variable
    auth_token = os.getenv('NPM_AUTH_TOKEN')
    if not auth_token:
        print("Error: NPM_AUTH_TOKEN environment variable not set")
        sys.exit(1)

    # Set up headers with authentication
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Accept': 'application/json'
    }

    # Construct package metadata URL
    # Handle scoped packages (e.g., @scope/package-name)
    encoded_package_name = package_name.replace('/', '%2F')
    metadata_url = f"{registry_url.rstrip('/')}/{encoded_package_name}"

    try:
        # Get package metadata
        print(f"Fetching package metadata for {package_name}...")
        response = requests.get(metadata_url, headers=headers)
        response.raise_for_status()

        metadata = response.json()

        # Determine which version to download
        if version is None:
            version = metadata.get('dist-tags', {}).get('latest')
            if not version:
                print("Error: Could not determine latest version")
                sys.exit(1)
            print(f"Latest version: {version}")

        # Get the tarball URL for the specified version
        if version not in metadata.get('versions', {}):
            print(f"Error: Version {version} not found")
            print(f"Available versions: {list(metadata.get('versions', {}).keys())}")
            sys.exit(1)

        tarball_url = metadata['versions'][version]['dist']['tarball']

        # Download the tarball
        print(f"Downloading {package_name}@{version}...")
        tarball_response = requests.get(tarball_url, headers=headers, stream=True)
        tarball_response.raise_for_status()

        # Save the tarball
        os.makedirs(output_dir, exist_ok=True)
        safe_package_name = package_name.replace('@', '').replace('/', '-')
        output_file = os.path.join(output_dir, f"{safe_package_name}-{version}.tgz")

        with open(output_file, 'wb') as f:
            for chunk in tarball_response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Successfully downloaded to {output_file}")
        return output_file

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Response: {e.response.text}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Example usage
    REGISTRY_URL = "https://company.com/npm/group"

    # Example: Download a specific package
    # download_npm_package(REGISTRY_URL, "lodash", version="4.17.21")

    # Example: Download latest version
    # download_npm_package(REGISTRY_URL, "express")

    # Example: Download scoped package
    # download_npm_package(REGISTRY_URL, "@babel/core", version="7.23.0")

    # Interactive mode
    if len(sys.argv) < 2:
        print("Usage: python script.py <package-name> [version]")
        print("Example: python script.py lodash 4.17.21")
        print("Example: python script.py @babel/core")
        sys.exit(1)

    package = sys.argv[1]
    ver = sys.argv[2] if len(sys.argv) > 2 else None

    download_npm_package(REGISTRY_URL, package, version=ver)
```

**Usage:**

1. **Set your auth token:**

   ```bash
   export NPM_AUTH_TOKEN="your-token-here"
   ```

2. **Run the script:**

   ```bash
   # Download latest version
   python script.py lodash

   # Download specific version
   python script.py lodash 4.17.21

   # Download scoped package
   python script.py @babel/core 7.23.0
   ```

**Key features:**

- Uses `NPM_AUTH_TOKEN` environment variable for authentication
- Supports both regular and scoped packages
- Downloads latest version by default or specific version if provided
- Saves the `.tgz` file with a clean filename
- Includes error handling and progress messages
- Streams large downloads efficiently

**Note:** Some Nexus configurations might use `_auth` (base64) instead of bearer tokens. If your setup uses basic auth, modify the headers to:

```python
headers = {
    'Authorization': f'Basic {auth_token}',  # token should be base64 encoded
    'Accept': 'application/json'
}
```
