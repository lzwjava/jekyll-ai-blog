#!/usr/bin/env python3
"""
WiFi Scanner Script for Linux Systems
Scans and displays available WiFi networks with signal strength, security information, and other details.
"""

import os
import sys
import time

# Add the parent directory to the Python path
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from scripts.network.get_wifi_list_util import (
    get_wifi_list,
    check_current_connection,
    test_wifi_connection,
    save_successful_connections,
)


def main():
    """Main function to scan and display WiFi networks."""
    print("=== WiFi Network Scanner with Password Testing ===")
    print()

    # Check current connection
    current = check_current_connection()
    if current:
        print(current)
        print()

    # Scan available networks
    print("Scanning for available WiFi networks...")
    networks = get_wifi_list()

    print("Available WiFi Networks:")
    if not networks:
        print("  No WiFi networks found or scanning method available")
        return

    # Filter out empty SSIDs
    available_networks = [
        net
        for net in networks
        if net["ssid"] and net["ssid"] != "N/A" and net["ssid"].strip()
    ]

    print(f"Found {len(available_networks)} networks to test...")
    print()

    successful_connections = []

    for i, net in enumerate(available_networks, 1):
        print(
            f"[{i}/{len(available_networks)}] Testing: {net['ssid']} (Security: {net['security']}, Signal: {net['signal']}%)"
        )

        # Skip if network is already connected
        if net.get("active") == "yes" or net.get("in_use") == "yes":
            print(f"  Skipping - already connected")
            continue

        # Test connection with password 88888888
        success, error = test_wifi_connection(net["ssid"])
        if success:
            print(f"  ✓ SUCCESS! Password 88888888 works for {net['ssid']}")
            successful_connections.append(net)
        else:
            print(f"  ✗ Failed - {error}")

        # Small delay between tests
        time.sleep(1)

    print()
    print(
        f"Testing complete. Found {len(successful_connections)} network(s) with password 88888888."
    )

    if successful_connections:
        save_successful_connections(successful_connections)
        print(f"Results saved to tmp/wifi.csv")
        print()
        print("Successful connections:")
        for net in successful_connections:
            print(
                f"  - {net['ssid']} (Signal: {net['signal']}%, Security: {net['security']})"
            )
    else:
        print("No networks accepted the password 88888888.")

    print()


if __name__ == "__main__":
    main()
