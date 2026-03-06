#!/usr/bin/env python3
import subprocess
import sys

# Use gpg to decrypt a file
if len(sys.argv) < 2:
    print("Usage: python3 gpg_decrypt.py <input_file> [output_file]")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2] if len(sys.argv) > 2 else None

# Use gpg to decrypt
cmd = ["gpg", "--decrypt"]
if output_file:
    cmd.extend(["--output", output_file])
cmd.append(input_file)

result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode == 0:
    if output_file:
        print(f"File decrypted successfully and saved to {output_file}")
    else:
        print("Decrypted message:")
        print(result.stdout)
else:
    print(f"Error decrypting file: {result.stderr}")
