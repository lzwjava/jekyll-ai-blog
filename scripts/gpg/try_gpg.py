#!/usr/bin/env python3
import subprocess

# Use gpg to list keys
result = subprocess.run(["gpg", "--list-keys"], capture_output=True, text=True)
print(result.stdout)
