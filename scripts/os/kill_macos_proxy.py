#!/usr/bin/env python3

import argparse
import subprocess


def find_clash_processes():
    """Find all Clash-related processes on macOS."""
    processes = []

    # Specific patterns to match Clash processes
    clash_patterns = ["clash-darwin-amd64", "clash.py", "clash"]

    try:
        # Use ps aux to find all processes
        result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            for line in lines[1:]:  # Skip header
                # Check if line contains any clash pattern (case insensitive)
                line_lower = line.lower()
                if any(pattern in line_lower for pattern in clash_patterns):
                    parts = line.split()
                    if len(parts) >= 11:
                        pid = parts[1]
                        user = parts[0]
                        command = " ".join(parts[10:])

                        # Filter out grep command and focus on user processes
                        if "grep" not in command and user != "root":
                            # More specific filtering for the actual Clash processes
                            if (
                                "clash-darwin-amd64" in command
                                or "clash.py" in command
                                or ("/python" in command and "clash" in command)
                            ):
                                processes.append((pid, f"{command} ({pid})"))
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    return processes


def get_process_details(pid):
    """Get detailed information about a process."""
    try:
        ps_result = subprocess.run(
            ["ps", "-p", pid, "-o", "pid,ppid,lstart,etime,command"],
            capture_output=True,
            text=True,
        )
        if ps_result.returncode == 0:
            lines = ps_result.stdout.strip().split("\n")
            if len(lines) > 1:
                data_line = None
                for line in lines[1:]:
                    line = line.strip()
                    if line.startswith(pid):
                        data_line = line
                        break

                if data_line:
                    import re

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
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    return None


def kill_process(pid):
    """Kill the process with the specified PID."""
    try:
        # First check if process exists
        check_result = subprocess.run(["ps", "-p", pid], capture_output=True, text=True)
        if check_result.returncode != 0:
            print(f"Process {pid} does not exist or has already terminated")
            return True

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
            return False

    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Failed to kill process {pid}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Kill Clash processes on macOS")
    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Kill processes without asking for confirmation",
    )
    args = parser.parse_args()

    processes = find_clash_processes()

    if not processes:
        print("No Clash processes found")
        return

    print(f"Found {len(processes)} Clash process(es):\n")

    # Show details for each process found
    for i, (pid, process_info) in enumerate(processes, 1):
        print(f"[{i}] Process:")
        print(f"  PID: {pid}")
        print(f"  Command: {process_info}")

        # Get detailed process information
        details = get_process_details(pid)

        if details:
            if details.get("started"):
                print(f"  Started: {details['started']}")
            if details.get("elapsed"):
                print(f"  Running for: {details['elapsed']}")
            if details.get("ppid"):
                print(f"  Parent PID: {details['ppid']}")

        print()

    # Ask for confirmation unless --force is used
    if not args.force:
        print(
            f"Do you want to kill all {len(processes)} Clash process(es)? (Press Enter to kill, or 'no' to exit)"
        )

        try:
            response = input().strip().lower()
            if response == "no" or response == "n":
                print("Clash processes not killed. Exiting.")
                return
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return
    else:
        print("Force mode enabled - proceeding to kill all Clash processes")

    # Kill all found processes
    killed_count = 0
    failed_count = 0
    failed_pids = []

    for pid, _ in processes:
        if kill_process(pid):
            killed_count += 1
        else:
            failed_count += 1
            failed_pids.append(pid)

    if failed_pids:
        print(f"\nFailed to kill {failed_count} process(es): {', '.join(failed_pids)}")
        print(
            "You may need administrator privileges or the processes may have already terminated."
        )
    else:
        print(f"\nSuccessfully killed all {killed_count} Clash process(es)")


if __name__ == "__main__":
    main()
