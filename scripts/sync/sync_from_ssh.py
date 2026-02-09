import subprocess
import os
import argparse
import sys

# Get the directory of the current script
dir_path = os.path.dirname(os.path.abspath(__file__))

# Target directory for synced files
target_dir = os.path.join(dir_path, "..", "config")

# Ensure target directory exists
os.makedirs(target_dir, exist_ok=True)

# Set up argument parser
parser = argparse.ArgumentParser(
    description="Sync files from remote SSH host to scripts/config/"
)
parser.add_argument("user", help="SSH login username")
parser.add_argument("ip", help="SSH host IP address")
parser.add_argument("remote_path", help="Remote file or directory path to copy")
parser.add_argument(
    "-r", "--recursive",
    action="store_true",
    help="Recursively copy directories"
)
args = parser.parse_args()

# Build SCP command
scp_flags = "-r" if args.recursive else ""
remote_source = f"{args.user}@{args.ip}:{args.remote_path}"
command = f"scp {scp_flags} {remote_source} {target_dir}".strip()

print(f"Copying from {remote_source} to {target_dir}")
result = subprocess.run(command, shell=True, capture_output=True, text=True)

# Check the result
if result.returncode == 0:
    print("Command executed successfully.")
    if result.stdout:
        print("Output:", result.stdout)
else:
    print("Command failed with return code:", result.returncode)
    if result.stderr:
        print("Error:", result.stderr)
    sys.exit(1)
