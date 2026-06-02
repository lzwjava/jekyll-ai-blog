---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Automated WiFi Connection Testing Script
translated: false
type: note
---

import subprocess
import time
import os

def get_wifi_interfaces():
    """Helper to find WiFi interfaces."""
    try:
        result = subprocess.run("nmcli dev status | grep wifi | awk '{print $1}'", shell=True, capture_output=True, text=True)
        interfaces = [iface.strip() for iface in result.stdout.split('\n') if iface.strip()]
        return interfaces
    except:
        return []

def test_wifi_connection(ssid, password="88888888", timeout=30):
    """Test WiFi connection non-interactively. Returns tuple(success: bool, error: str)."""
    interfaces = get_wifi_interfaces()
    if not interfaces:
        return False, "No WiFi interface available"
    interface = interfaces[0]  # Use first available interface
    con_name = f"test-{ssid}"  # Unique name for the test profile

    # Commands
    delete_cmd = f"nmcli connection delete '{con_name}'"
    add_cmd = (
        f"nmcli connection add type wifi con-name '{con_name}' "
        f"ifname {interface} ssid '{ssid}' "
        f"wifi-sec.key-mgmt wpa-psk wifi-sec.psk '{password}' "
        f"-- autoconnect no"
    )
    up_cmd = f"nmcli connection up '{con_name}'"
    disconnect_cmd = f"nmcli device disconnect {interface}"

    try:
        # Delete any existing profile (suppress errors if missing)
        subprocess.run(delete_cmd, shell=True, capture_output=True, timeout=5)
        time.sleep(1)

        # Create new profile with embedded password (non-interactive)
        add_result = subprocess.run(add_cmd, shell=True, capture_output=True, text=True, timeout=10)
        if add_result.returncode != 0:
            error = add_result.stderr.strip() or add_result.stdout.strip() or "Failed to create connection profile"
            return False, f"Profile creation error: {error}"

        # Activate the profile (non-interactive)
        up_result = subprocess.run(up_cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        if up_result.returncode != 0:
            error = up_result.stderr.strip() or up_result.stdout.strip() or "Activation failed"
            if "secrets were required" in error.lower():
                error = "Wrong password or authentication failed"
            elif "activation failed" in error.lower():
                error = f"Connection activation failed: {error}"
            return False, f"nmcli error: {error}"

        # Wait for stabilization
        time.sleep(2)

        # Test internet with ping
        ping_test = subprocess.run("ping -c 1 -W 3 8.8.8.8", shell=True, capture_output=True, text=True, timeout=5)
        if ping_test.returncode == 0:
            return True, None
        else:
            error = ping_test.stderr.strip() or "Ping failed"
            return False, f"Connected but no internet: {error}"

    except subprocess.TimeoutExpired:
        return False, f"Operation timeout after {timeout} seconds"
    except subprocess.SubprocessError as e:
        return False, f"Command error: {str(e)}"
    finally:
        # Cleanup: Down the connection and delete profile
        try:
            subprocess.run(f"nmcli connection down '{con_name}'", shell=True, capture_output=True, timeout=5)
            subprocess.run(delete_cmd, shell=True, capture_output=True, timeout=5)
            subprocess.run(disconnect_cmd, shell=True, capture_output=True, timeout=5)
        except subprocess.SubprocessError:
            pass  # Ignore cleanup issues
