#!/usr/bin/env python3

import subprocess


def find_process_on_port(port):
    """Find the process ID using the specified port on Windows."""
    try:
        # For Windows, use netstat and tasklist
        result = subprocess.run(
            ["netstat", "-ano"], capture_output=True, text=True, check=True
        )
        for line in result.stdout.split("\n"):
            if f":{port}" in line and ("LISTENING" in line or "ESTABLISHED" in line):
                parts = line.strip().split()
                if len(parts) >= 5:
                    pid = parts[-1]
                    # Get process name
                    task_result = subprocess.run(
                        ["tasklist", "/FI", f"PID eq {pid}"],
                        capture_output=True,
                        text=True,
                    )
                    for task_line in task_result.stdout.split("\n"):
                        if pid in task_line and ".exe" in task_line:
                            parts_task = task_line.split()
                            if len(parts_task) >= 2:
                                return pid, parts_task[0]
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    return None, None


def find_processes_by_pattern(pattern):
    """Find all process IDs matching the specified pattern on Windows."""
    processes = []
    try:
        # Use tasklist to find processes by name
        result = subprocess.run(
            ["tasklist", "/FI", f"IMAGENAME eq {pattern}", "/FO", "CSV"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            for line in lines[1:]:  # Skip header
                parts = line.replace('"', "").split(",")
                if len(parts) >= 2:
                    image_name = parts[0]
                    pid = parts[1]
                    if (
                        image_name.lower().startswith(pattern.lower())
                        or pattern.lower() in image_name.lower()
                    ):
                        processes.append((pid, f"{image_name} ({pid})"))

        # Also try with wildcard pattern
        if not processes:
            result2 = subprocess.run(
                ["tasklist", "/FI", f"IMAGENAME eq {pattern}*", "/FO", "CSV"],
                capture_output=True,
                text=True,
            )
            if result2.returncode == 0:
                lines = result2.stdout.strip().split("\n")
                for line in lines[1:]:  # Skip header
                    parts = line.replace('"', "").split(",")
                    if len(parts) >= 2:
                        image_name = parts[0]
                        pid = parts[1]
                        processes.append((pid, f"{image_name} ({pid})"))
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    return processes


def get_process_details(pid):
    """Get detailed information about a process on Windows."""
    try:
        # For Windows, use tasklist and wmic for more details
        task_result = subprocess.run(
            ["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV"],
            capture_output=True,
            text=True,
        )
        if task_result.returncode == 0:
            lines = task_result.stdout.strip().split("\n")
            if len(lines) > 1:
                parts = lines[1].replace('"', "").split(",")
                return {
                    "name": parts[0],
                    "pid": parts[1],
                    "started": None,  # Windows tasklist doesn't easily show start time
                    "command": f"{parts[0]} (PID: {parts[1]})",
                }
    except (subprocess.CalledProcessError, FileNotFoundError, IndexError):
        pass

    return None


def kill_process(pid):
    """Kill the process with the specified PID on Windows."""
    try:
        subprocess.run(["taskkill", "/F", "/PID", pid], check=True)
        return True
    except subprocess.CalledProcessError:
        return False
