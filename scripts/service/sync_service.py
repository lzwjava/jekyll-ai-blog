#!/usr/bin/env python3
"""
Sync Service Files Script

This script copies systemd service files from /etc/systemd/system to
scripts/service directory for backup and version control purposes.

Usage:
    python scripts/service/sync_service.py
    python scripts/service/sync_service.py clash ollama llama openwebui
"""

import shutil
import os
import sys

# Default service files to copy
DEFAULT_SERVICES = [
    "clash.service",
    "ollama.service",
    "llama.service",
    "openwebui.service",
]

# Source and destination directories
SYSTEMD_DIR = "/etc/systemd/system"
DESTINATION_DIR = os.path.join(os.path.dirname(__file__), "..", "service")


def copy_service_file(service_name):
    """Copy a single service file from systemd directory."""
    source_path = os.path.join(SYSTEMD_DIR, service_name)
    destination_path = os.path.join(DESTINATION_DIR, service_name)

    try:
        if os.path.exists(source_path):
            shutil.copy2(source_path, destination_path)
            print("[OK] Copied: " + service_name)
            return True
        else:
            print("[ERROR] Service file not found: " + source_path)
            return False
    except PermissionError:
        print("[ERROR] Permission denied reading: " + source_path)
        return False
    except Exception as e:
        print("[ERROR] Copying " + service_name + ": " + str(e))
        return False


def copy_all_services(services=None):
    """Copy specified service files or default services."""
    if services is None:
        services = DEFAULT_SERVICES

    success_count = 0
    fail_count = 0

    print("Copying service files from " + SYSTEMD_DIR + " to " + DESTINATION_DIR)
    print("=" * 60)

    # Ensure destination directory exists
    os.makedirs(DESTINATION_DIR, exist_ok=True)

    for service in services:
        if copy_service_file(service):
            success_count += 1
        else:
            fail_count += 1

    print("=" * 60)
    print("Copied " + str(success_count) + " files, " + str(fail_count) + " failures")

    return success_count, fail_count


def main():
    """Main function."""
    if len(sys.argv) > 1:
        # If arguments provided, use them as service names
        services = sys.argv[1:]
    else:
        # Use default services
        services = DEFAULT_SERVICES

    success, fail = copy_all_services(services)

    if fail == 0:
        print("\nAll services copied successfully!")
    else:
        print("\n" + str(fail) + " services failed to copy")

    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
