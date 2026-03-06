#!/usr/bin/env python3
"""
WiFi Password Generator Script
Loads WiFi list from tmp/wifi_list.json, lets user select one, generates suggested passwords using LLM, and saves to @tmp dir.
This script requires online access for LLM. Use a separate offline script to attempt connections with saved passwords.
"""

import os
import sys
import argparse
import json
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from scripts.llm.openrouter_client import call_openrouter_api

# Ensure @tmp directory exists
TMP_DIR = "tmp"
os.makedirs(TMP_DIR, exist_ok=True)


def load_wifi_list():
    """
    Load the WiFi list from tmp/wifi_list.json.
    Returns a list of dicts with 'ssid', 'bssid', 'full_line'.
    """
    filename = os.path.join(TMP_DIR, "wifi_list.json")
    if not os.path.exists(filename):
        print(f"WiFi list not found: {filename}")
        print("Run save_wifi_list.py first.")
        sys.exit(1)
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_passwords(ssid, num_suggestions=10, model="deepseek-v3.2"):
    """
    Use OpenRouter LLM to generate suggested passwords for the given SSID.
    """
    prompt = f"""You are generating WiFi passwords for a network in Guangzhou, China. Consider local preferences: Chinese people often like the number 8 (lucky), so include passwords with many 8's like 88888888 or 12345678. Also use number sequences like 123456, 1-6, or 8-8 patterns. Include some alphabetic sequences like abcdef or qwerty. Mix in general common passwords like password, admin, 1234567890, not just based on the SSID name '{ssid}'. Make them diverse and plausible for Chinese WiFi defaults. Use only English letters, numbers, and symbols. No Chinese characters. Aim for 8-12 characters.

Output only a valid JSON array of {num_suggestions} unique strings, like: ["password1", "password2", ...]"""
    try:
        response = call_openrouter_api(prompt, model=model)
        # Try to parse as JSON
        cleaned_response = re.sub(
            r"```json\s*|\s*```", "", response.strip(), flags=re.IGNORECASE
        )
        passwords = json.loads(cleaned_response)
        if isinstance(passwords, list):
            # Filter to ensure no Chinese characters (simple check) and limit to num_suggestions
            passwords = [
                pwd
                for pwd in passwords[:num_suggestions]
                if isinstance(pwd, str)
                and not any(0x4E00 <= ord(c) <= 0x9FFF for c in pwd)
            ]
            return passwords[:num_suggestions]
        else:
            raise ValueError("Response is not a list")
    except (json.JSONDecodeError, ValueError, Exception) as e:
        print(f"Error generating or parsing passwords: {e}")
        # Fallback: try old parsing method
        lines = [
            line.strip()
            for line in response.split("\n")
            if line.strip() and line[0].isdigit()
        ]
        fallback_passwords = [
            line.split(".", 1)[1].strip() if "." in line else line
            for line in lines[:num_suggestions]
        ]
        fallback_passwords = [
            pwd
            for pwd in fallback_passwords
            if not any(0x4E00 <= ord(c) <= 0x9FFF for c in pwd)
        ]
        if fallback_passwords:
            return fallback_passwords[:num_suggestions]
        return []


def save_passwords_to_file(bssid, passwords):
    """
    Save the list of passwords to a file in @tmp dir using BSSID.
    """
    safe_bssid = bssid.replace(":", "_")
    filename = os.path.join(TMP_DIR, f"{safe_bssid}_passwords.txt")
    with open(filename, "w") as f:
        for pwd in passwords:
            f.write(f"{pwd}\n")
    print(f"Passwords saved to: {filename}")
    return filename


def main():
    parser = argparse.ArgumentParser(description="WiFi Password Generator")
    parser.add_argument(
        "-n",
        type=int,
        default=10,
        help="Number of password suggestions to generate (default: 10)",
    )
    args = parser.parse_args()

    print("=== WiFi Password Generator ===")
    print()

    # Load WiFi list
    networks = load_wifi_list()
    if not networks:
        print("No networks loaded.")
        sys.exit(1)

    print("Available WiFi Networks:")
    for i, net in enumerate(networks, 1):
        print(f"{i}. {net['full_line']}")

    # User input
    try:
        choice = int(input(f"\nSelect a network (1-{len(networks)}): "))
        if 1 <= choice <= len(networks):
            selected = networks[choice - 1]
            ssid = selected["ssid"]
            bssid = selected["bssid"]
            print(f"\nSelected: {ssid} (BSSID: {bssid})")
        else:
            print("Invalid choice.")
            sys.exit(1)
    except ValueError:
        print("Invalid input.")
        sys.exit(1)

    # Generate passwords
    print(f"\nGenerating {args.n} password suggestions for '{ssid}'...")
    passwords = generate_passwords(ssid, num_suggestions=args.n)

    if passwords:
        print("Suggested passwords:")
        for i, pwd in enumerate(passwords, 1):
            print(f"{i}. {pwd}")
        # Save to file using BSSID
        save_passwords_to_file(bssid, passwords)
    else:
        print("Failed to generate passwords.")

    print("\nUse a separate offline script to read this file and attempt connections.")


if __name__ == "__main__":
    main()
