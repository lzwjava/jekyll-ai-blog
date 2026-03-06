import subprocess
import re

#!/usr/bin/env python3
import matplotlib.pyplot as plt


def get_disk_usage():
    """Run df -h and parse the output"""
    result = subprocess.run(["df", "-h"], capture_output=True, text=True)
    lines = result.stdout.strip().split("\n")[1:]  # Skip header

    filesystems = []
    used_percentages = []
    mount_points = []

    for line in lines:
        parts = line.split()
        if len(parts) >= 6 and parts[4].endswith("%"):
            filesystem = parts[0]
            used_percent = int(parts[4].rstrip("%"))
            mount_point = parts[5]

            # Skip special filesystems
            if not filesystem.startswith(("/dev/loop", "tmpfs", "udev")):
                filesystems.append(filesystem)
                used_percentages.append(used_percent)
                mount_points.append(mount_point)

    return filesystems, used_percentages, mount_points


def create_disk_usage_chart():
    """Create a bar chart of disk usage"""
    filesystems, used_percentages, mount_points = get_disk_usage()

    plt.figure(figsize=(12, 6))
    bars = plt.bar(
        range(len(filesystems)),
        used_percentages,
        color=[
            "red" if x > 80 else "orange" if x > 60 else "green"
            for x in used_percentages
        ],
    )

    plt.xlabel("Filesystems")
    plt.ylabel("Used Space (%)")
    plt.title("Disk Usage by Filesystem")
    plt.xticks(
        range(len(filesystems)),
        [f"{fs}\n{mp}" for fs, mp in zip(filesystems, mount_points)],
        rotation=45,
        ha="right",
    )
    plt.ylim(0, 100)

    # Add percentage labels on bars
    for bar, percentage in zip(bars, used_percentages):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1,
            f"{percentage}%",
            ha="center",
            va="bottom",
        )

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    create_disk_usage_chart()
