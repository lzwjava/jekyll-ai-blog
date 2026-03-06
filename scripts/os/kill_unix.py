#!/usr/bin/env python3

import subprocess
import re


def find_process_on_port(port):
    """Find the process ID using the specified port on Unix systems (macOS/Linux)."""
    try:
        # For macOS and Linux, use lsof
        result = subprocess.run(
            ["lsof", "-i", f":{port}"], capture_output=True, text=True, check=False
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            if len(lines) > 1:  # Skip header
                parts = lines[1].split()
                if len(parts) >= 2:
                    return parts[1], f"{parts[0]} ({parts[1]})"  # PID and command
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    return None, None


def find_processes_by_pattern(pattern):
    """Find all process IDs matching the specified pattern on Unix systems (macOS/Linux)."""
    processes = []
    try:
        # Use ps aux and grep to find processes containing the pattern
        result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            for line in lines[1:]:  # Skip header
                if pattern.lower() in line.lower():
                    parts = line.split()
                    if (
                        len(parts) >= 11
                    ):  # ps aux format: USER PID %CPU %MEM VSZ RSS TTY STAT START TIME COMMAND
                        pid = parts[1]
                        command = " ".join(parts[10:])
                        processes.append((pid, f"{command} ({pid})"))
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    return processes


def get_process_details(pid):
    """Get detailed information about a process on Unix systems (macOS/Linux)."""
    try:
        # For macOS and Linux, use ps
        ps_result = subprocess.run(
            ["ps", "-p", pid, "-o", "pid,ppid,lstart,etime,command"],
            capture_output=True,
            text=True,
        )
        if ps_result.returncode == 0:
            lines = ps_result.stdout.strip().split("\n")
            if len(lines) > 1:
                # Skip header and find data line
                data_line = None
                for line in lines[1:]:
                    line = line.strip()
                    if line.startswith(pid):
                        data_line = line
                        break

                if data_line:
                    # Parse the ps output carefully
                    # Format: PID PPID STARTED ELAPSED COMMAND
                    # Where STARTED can have multiple spaces: "Mon Sep 29 23:40:03 2025"
                    # ELAPSED can be formats: dd-hh:mm:ss, hh:mm:ss, mm:ss
                    match = re.match(
                        r"(\d+)\s+(\d+)\s+(.*?)\s+([0-9-]+:[0-9:]+)\s+(.+)", data_line
                    )
                    if match:
                        pid_val, ppid_val, lstart_val, etime_val, command_val = (
                            match.groups()
                        )

                        return {
                            "name": command_val.split()[0],
                            "pid": pid_val,
                            "ppid": ppid_val,
                            "started": lstart_val,
                            "elapsed": etime_val,
                            "command": command_val,
                            "app_info": None,
                        }
    except (subprocess.CalledProcessError, FileNotFoundError, IndexError):
        pass

    return None


def kill_process(pid):
    """Kill the process with the specified PID on Unix systems (macOS/Linux)."""
    try:
        # First check if process exists
        check_result = subprocess.run(["ps", "-p", pid], capture_output=True, text=True)
        if check_result.returncode != 0:
            print(f"Process {pid} does not exist or has already terminated")
            return True  # Consider it successful if process is already gone

        # Try to kill the process
        result = subprocess.run(
            ["kill", "-9", pid], capture_output=True, text=True, check=False
        )

        # Check if kill was successful by verifying process is gone
        verify_result = subprocess.run(
            ["ps", "-p", pid], capture_output=True, text=True
        )
        if verify_result.returncode != 0:
            print(f"Successfully killed process {pid}")
            return True
        else:
            print(f"Failed to kill process {pid} - process still running")
            print(f"Kill command exit code: {result.returncode}")
            if result.stdout:
                print(f"Kill stdout: {result.stdout.strip()}")
            if result.stderr:
                print(f"Kill stderr: {result.stderr.strip()}")

            # Check if it's a system process or requires higher privileges
            try:
                # Get process owner
                owner_result = subprocess.run(
                    ["ps", "-p", pid, "-o", "user="], capture_output=True, text=True
                )
                if owner_result.returncode == 0:
                    owner = owner_result.stdout.strip()
                    current_user = subprocess.run(
                        ["whoami"], capture_output=True, text=True
                    ).stdout.strip()
                    if owner != current_user:
                        print(
                            f"Process {pid} is owned by '{owner}', you are '{current_user}' - may need sudo"
                        )
                    else:
                        print(
                            f"Process {pid} is owned by you but may be a protected system process"
                        )
            except:
                pass

            return False

    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Failed to kill process {pid}: {e}")
        print("This may be due to:")
        print("  - Process already terminated")
        print("  - Insufficient permissions (try with sudo)")
        print("  - Process is a critical system process")
        print("  - kill command not found")
        return False
