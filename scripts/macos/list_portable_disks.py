#!/usr/bin/env python3
"""
Script to list portable disks on macOS
"""

import subprocess
import sys


def run_command(cmd):
    """Run a command and return its output, or None if it fails."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else None
    except Exception:
        return None


def get_disk_info(disk_id):
    """Get detailed information about a disk."""
    disk_info = run_command(f'diskutil info "{disk_id}" 2>/dev/null')
    if not disk_info:
        return None

    info = {}
    for line in disk_info.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()

            if key == "Volume Name":
                info["volume_name"] = value
            elif key == "Mount Point":
                info["mount_point"] = value
            elif key == "Total Size":
                # Extract the size part before the parenthesis
                info["total_size"] = value.split("(")[0].strip()
            elif key == "Disk Size":
                # For disks without file system
                info["disk_size"] = value.split("(")[0].strip()
            elif key == "Volume Free Space":
                # Extract just the readable part (e.g., "1.5 TB" from "1.5 TB (...Bytes...) (%)")
                parts = value.split("(")
                info["available_space"] = parts[0].strip() if parts else value.strip()

    return info


def main():
    print("Listing portable disks on macOS:")
    print("=================================")
    print()

    # Get list of external disks
    external_disks_cmd = (
        "diskutil list | grep external | grep '^/dev/disk' | cut -d' ' -f1"
    )
    external_disks_output = run_command(external_disks_cmd)

    if not external_disks_output:
        print("ℹ️  No external portable disks currently detected.")
        print()
        print("💡 Tips:")
        print(
            "   • Make sure your USB drive, external HDD, or SD card is properly inserted"
        )
        print("   • Check if the device appears in Finder or Disk Utility")
        print("   • Some devices may require formatting or mounting")
        print()
        print("💻 For more details, use: diskutil list")
        sys.exit(0)

    portable_count = 0
    output_lines = []

    # Process each external disk
    for disk_id in external_disks_output.strip().split("\n"):
        disk_id = disk_id.strip()
        if not disk_id:
            continue

        # Check the whole disk and its primary partition (most common for USB drives)
        devices_to_check = [disk_id, f"{disk_id}s1"]

        # Process each device (whole disk and partitions)
        for device in devices_to_check:
            portable_count += 1

            # Get detailed info about this device
            device_id = device.replace("/dev/", "")
            disk_info = get_disk_info(device)
            if disk_info:
                if device == disk_id:
                    output_lines.append(f"📀 Device: {device_id}")
                else:
                    output_lines.append(f"📁 Volume: {device_id}")

                volume_name = disk_info.get("volume_name")
                if volume_name and volume_name != "Not applicable (no file system)":
                    output_lines.append(f"   Name: {volume_name}")

                total_size = disk_info.get("total_size")
                disk_size = disk_info.get("disk_size")
                if total_size:
                    output_lines.append(f"   Total: {total_size}")
                elif disk_size:
                    output_lines.append(f"   Total: {disk_size}")

                mount_point = disk_info.get("mount_point")
                if mount_point and mount_point != "Not applicable (no file system)":
                    output_lines.append(f"   Mounted at: {mount_point}")

                available_space = disk_info.get("available_space")
                if available_space:
                    output_lines.append(f"   Available: {available_space}")

                output_lines.append("")  # Empty line for spacing

    # Print the output
    print("\n".join(output_lines))

    print(f"Found {portable_count} external portable disk(s).")
    print()
    print("💻 For more details, use: diskutil list")


if __name__ == "__main__":
    main()
