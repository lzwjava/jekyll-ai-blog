import subprocess


def scan_wifi():
    """Scans for available Wi-Fi networks and their details using system_profiler."""
    try:
        output = subprocess.check_output(
            ["system_profiler", "SPAirPortDataType"], universal_newlines=True
        )
        return output
    except subprocess.CalledProcessError as e:
        print(f"Error scanning Wi-Fi: {e}")
        return None


def parse_wifi_scan(scan_output):
    """Parses the output of the Wi-Fi scan to extract network names (SSIDs)."""
    if not scan_output:
        return []

    ssids = []
    lines = scan_output.splitlines()

    ssids = []
    start_parsing = False
    for line in lines:
        if "Other Local Wi-Fi Networks:" in line:
            start_parsing = True
            continue
        if start_parsing and ":" in line:
            ssid = line.split(":")[1].strip()
            ssids.append(ssid)

    return ssids


def attempt_connect(ssid, password=""):
    """Attempts to connect to a Wi-Fi network with a given SSID and password."""
    try:
        if password:
            command = ["networksetup", "-setairportnetwork", "en0", ssid, password]
        else:
            command = ["networksetup", "-setairportnetwork", "en0", ssid]

        subprocess.check_call(command, timeout=10)  # Added timeout
        print(f"Successfully connected to {ssid}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to connect to {ssid}: {e}")
        return False
    except subprocess.TimeoutExpired:
        print(f"Connection to {ssid} timed out.")
        return False


if __name__ == "__main__":
    print("Scanning for Wi-Fi networks...")
    scan_result = scan_wifi()

    if scan_result:
        ssids = parse_wifi_scan(scan_result)
        print("\nAvailable Wi-Fi Networks:")
        for ssid in ssids:
            print(f"- {ssid}")

        print("\nAttempting to connect to available networks (no password)...")
        if not ssids:
            print("No networks found to connect to.")

        else:
            for ssid in ssids:
                print(f"Attempting to connect to {ssid}...")  # Added feedback
                if attempt_connect(ssid):
                    print(f"Connected to {ssid} successfully!")
                    break  # Stop after the first successful connection
                else:
                    print(f"Could not connect to {ssid}.")
    else:
        print("Wi-Fi scan failed.")
