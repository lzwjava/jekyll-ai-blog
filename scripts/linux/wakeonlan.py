#!/usr/bin/env python3
import os
import subprocess
import sys

mac_address = os.environ.get("MAG_MAC_ADDRESS")
if not mac_address:
    print("Error: MAG_MAC_ADDRESS environment variable is not set.", file=sys.stderr)
    sys.exit(1)

try:
    subprocess.run(["wakeonlan", mac_address], check=True)
    print(f"Wake-on-LAN packet sent to {mac_address}")
except subprocess.CalledProcessError as e:
    print(f"Error running wakeonlan: {e}", file=sys.stderr)
    sys.exit(1)
