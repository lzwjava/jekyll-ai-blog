#!/usr/bin/env python3
"""
Save WiFi List Script
Scans WiFi networks and saves the parsed list to tmp/wifi_list.json.
"""

import os
import json
from get_wifi_list import get_wifi_list

# Ensure @tmp directory exists
TMP_DIR = "tmp"
os.makedirs(TMP_DIR, exist_ok=True)


def prepare_networks_for_save(networks):
    """
    Prepare the networks list for saving, ensuring BSSID format and adding full_line.
    """
    prepared = []
    for net in networks:
        # Create a copy
        network_data = net.copy()

        # Create full_line for compatibility
        full_line = (
            f"SSID: {net.get('ssid', 'N/A')}, BSSID: {net.get('bssid', 'N/A')}, "
            f"Mode: {net.get('mode', 'N/A')}, Channel: {net.get('channel', 'N/A')}, "
            f"Frequency: {net.get('frequency', 'N/A')}, Rate: {net.get('rate', 'N/A')}, "
            f"Bandwidth: {net.get('bandwidth', 'N/A')}, Signal: {net.get('signal', '0')}%, "
            f"Bars: {net.get('bars', 'N/A')}, Security: {net.get('security', 'N/A')}, "
            f"Active: {net.get('active', 'N/A')}, In-Use: {net.get('in_use', 'N/A')}"
        )

        network_data["full_line"] = full_line
        prepared.append(network_data)

    return prepared


def main():
    print("=== Save WiFi List ===")
    print()

    # Get WiFi list
    print("Scanning for available WiFi networks...")
    networks = get_wifi_list()
    if not networks:
        print("No WiFi networks found.")
        return

    # Prepare for saving
    prepared_networks = prepare_networks_for_save(networks)
    if not prepared_networks:
        print("No networks found.")
        return

    # Save to JSON
    filename = os.path.join(TMP_DIR, "wifi_list.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(prepared_networks, f, ensure_ascii=False, indent=2)
    print(f"WiFi list saved to: {filename}")
    print(f"Found {len(prepared_networks)} networks.")


if __name__ == "__main__":
    main()
