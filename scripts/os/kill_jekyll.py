#!/usr/bin/env python3
"""
Script to kill Jekyll server processes running on port 4000 (default Jekyll port)
"""

import subprocess
import sys


def get_jekyll_processes():
    """Get list of PIDs for Ruby processes listening on port 4000"""
    try:
        # Run lsof to find processes on port 4000
        result = subprocess.run(
            ["lsof", "-i", ":4000"], capture_output=True, text=True, check=False
        )

        # lsof returns exit code 1 when no processes are found, which is not an error for us
        if result.returncode != 0 and result.returncode != 1:
            print(f"Error running lsof: exit code {result.returncode}")
            return set()

        if not result.stdout.strip():
            return set()

        pids = set()
        for line in result.stdout.strip().split("\n"):
            if line.startswith("ruby"):
                # Extract PID from the line
                parts = line.split()
                if len(parts) >= 2 and parts[1].isdigit():
                    pids.add(int(parts[1]))

        return pids

    except FileNotFoundError:
        print("Error: lsof command not found. Please install lsof.")
        return set()
    except Exception as e:
        print(f"Error running lsof: {e}")
        return set()


def kill_processes(pids):
    """Kill the specified processes"""
    if not pids:
        print("No Jekyll processes found on port 4000")
        return False

    print(f"Found Jekyll processes: {', '.join(map(str, pids))}")

    for pid in pids:
        try:
            print(f"Killing process {pid}...")
            subprocess.run(["kill", "-9", str(pid)], check=True)
        except subprocess.CalledProcessError:
            print(f"Error killing process {pid}")

    # Verify processes are dead
    import time

    time.sleep(0.5)

    remaining_pids = get_jekyll_processes()
    if not remaining_pids:
        print("All Jekyll processes killed successfully!")
        return True
    else:
        print(
            f"Some processes may still be running: {', '.join(map(str, remaining_pids))}"
        )
        return False


def main():
    """Main function"""
    print("Killing Jekyll server processes on port 4000...")

    pids = get_jekyll_processes()
    success = kill_processes(pids)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
