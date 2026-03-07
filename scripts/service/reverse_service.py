#!/usr/bin/env python3
"""
Reverse Service Files Script

This script copies systemd service files from scripts/service directory
back to /etc/systemd/system directory. It also provides options to reload
the systemd daemon and start/enable services.

This typically requires sudo privileges.

Usage:
    python scripts/service/reverse_service.py
    python scripts/service/reverse_service.py clash ollama llama openwebui
    python scripts/service/reverse_service.py --reload
    python scripts/service/reverse_service.py --enable clash ollama
"""

import shutil
import os
import sys
import subprocess

# Default service files to copy (from your scripts/service directory)
DEFAULT_SERVICES = [
    "clash.service",
    "ollama.service",
    "llama.service",
    "openwebui.service",
]

# Source and destination directories
SOURCE_DIR = os.path.join(os.path.dirname(__file__), "..", "service")
SYSTEMD_DIR = "/etc/systemd/system"


def copy_service_file(
    service_name, reload_daemon=False, enable_service=False, start_service=False
):
    """Copy a single service file from scripts/service to systemd."""
    source_path = os.path.join(SOURCE_DIR, service_name)
    destination_path = os.path.join(SYSTEMD_DIR, service_name)

    if not os.path.exists(source_path):
        print("[ERROR] Service file not found: " + source_path)
        return False

    try:
        shutil.copy2(source_path, destination_path)
        print("[OK] Copied: " + service_name)

        if reload_daemon:
            os.chmod(destination_path, 0o644)
            reload_systemd()

        if enable_service:
            enable_systemd_service(service_name)

        if start_service:
            start_systemd_service(service_name)

        return True

    except PermissionError:
        print("[ERROR] Permission denied writing to: " + destination_path)
        print(
            "[INFO] Try running with sudo: sudo python3 scripts/service/reverse_service.py"
        )
        return False
    except Exception as e:
        print("[ERROR] Copying " + service_name + ": " + str(e))
        return False


def reload_systemd():
    """Reload the systemd daemon to recognize new/updated services."""
    try:
        subprocess.run(
            ["systemctl", "daemon-reload"], check=True, capture_output=True, text=True
        )
        print("[OK] systemd daemon reloaded")
        return True
    except subprocess.CalledProcessError as e:
        print("[ERROR] Failed to reload systemd: " + str(e))
        return False


def enable_systemd_service(service_name):
    """Enable a systemd service to start on boot."""
    try:
        subprocess.run(
            ["systemctl", "enable", service_name],
            check=True,
            capture_output=True,
            text=True,
        )
        print("[OK] Enabled service: " + service_name)
        return True
    except subprocess.CalledProcessError as e:
        print("[ERROR] Failed to enable " + service_name + ": " + str(e))
        return False


def start_systemd_service(service_name):
    """Start a systemd service immediately."""
    try:
        subprocess.run(
            ["systemctl", "start", service_name],
            check=True,
            capture_output=True,
            text=True,
        )
        print("[OK] Started service: " + service_name)
        return True
    except subprocess.CalledProcessError as e:
        print("[ERROR] Failed to start " + service_name + ": " + str(e))
        return False


def list_available_services():
    """List available service files in scripts/service directory."""
    services = []
    try:
        for file in os.listdir(SOURCE_DIR):
            if file.endswith(".service"):
                services.append(file)
        return sorted(services)
    except FileNotFoundError:
        return []


def main():
    """Main function."""
    services = []
    reload_daemon = False
    enable_services = False
    start_services = False

    # Parse command line arguments
    for arg in sys.argv[1:]:
        if arg == "--reload":
            reload_daemon = True
        elif arg == "--enable":
            enable_services = True
        elif arg == "--start":
            start_services = True
        elif arg == "--restart":
            reload_daemon = True
            start_services = True
        elif arg == "--list":
            available = list_available_services()
            print("Available service files in scripts/service:")
            for service in available:
                print("  - " + service)
            return 0
        else:
            services.append(arg)

    if not services:
        services = DEFAULT_SERVICES

    available_services = list_available_services()
    if not available_services:
        print("No .service files found in " + SOURCE_DIR)
        return 1

    print("Copying service files from " + SOURCE_DIR + " to " + SYSTEMD_DIR)
    print("=" * 70)

    success_count = 0
    fail_count = 0

    for service in services:
        if service in available_services:
            if copy_service_file(
                service, reload_daemon, enable_services, start_services
            ):
                success_count += 1
            else:
                fail_count += 1
        else:
            print("[ERROR] Service not available: " + service)
            print("[INFO] Run with --list to see available services")
            fail_count += 1

    print("=" * 70)
    print("Copied " + str(success_count) + " files, " + str(fail_count) + " failures")

    if success_count > 0 and require_sudo():
        print("\n[INFO] Some operations may require sudo privileges")
        print("       Try: sudo python3 scripts/service/reverse_service.py")

    return 0 if fail_count == 0 else 1


def require_sudo():
    """Check if the current user has permissions to write to systemd directory."""
    return not os.access(SYSTEMD_DIR, os.W_OK)


if __name__ == "__main__":
    sys.exit(main())
