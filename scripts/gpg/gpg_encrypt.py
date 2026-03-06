#!/usr/bin/env python3
import subprocess
import sys

# Use gpg to encrypt a message
if len(sys.argv) < 3:
    print("Usage: python3 gpg_encrypt.py <recipient> <message> [output_file]")
    sys.exit(1)

recipient = sys.argv[1]
message = sys.argv[2]
output_file = sys.argv[3] if len(sys.argv) > 3 else "message.gpg"

# Use gpg to encrypt
result = subprocess.run(
    ["gpg", "--encrypt", "--recipient", recipient, "--output", output_file],
    input=message,
    capture_output=True,
    text=True,
)
if result.returncode == 0:
    print(f"Message encrypted successfully and saved to {output_file}")
else:
    print(f"Error encrypting message: {result.stderr}")
