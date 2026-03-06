#!/usr/bin/env python3

import argparse
import sys
import platform

# Import platform-specific modules
if platform.system().lower() == "windows":
    import kill_windows as platform_module
else:
    import kill_unix as platform_module


def find_processes_by_pattern(pattern):
    """Find all process IDs matching the specified pattern."""
    return platform_module.find_processes_by_pattern(pattern)


def get_process_details(pid):
    """Get detailed information about a process."""
    return platform_module.get_process_details(pid)


def kill_process(pid):
    """Kill the process with the specified PID."""
    return platform_module.kill_process(pid)


def main():
    parser = argparse.ArgumentParser(description="Kill processes matching a pattern")
    parser.add_argument(
        "pattern",
        type=str,
        help='Pattern to match process names/commands (e.g., "clash")',
    )
    args = parser.parse_args()

    pattern = args.pattern
    processes = find_processes_by_pattern(pattern)

    if not processes:
        print(f"No processes found matching pattern '{pattern}'")
        return

    print(f"Found {len(processes)} process(es) matching pattern '{pattern}':\n")

    # Show details for each process found
    for i, (pid, process_info) in enumerate(processes, 1):
        print(f"[{i}] Process:")
        print(f"  Name: {process_info}")

        # Get detailed process information
        details = get_process_details(pid)

        if details:
            if details.get("app_info"):
                print(f"  Application: {details['app_info']}")
            if details.get("started"):
                print(f"  Started: {details['started']}")
            if details.get("elapsed"):
                print(f"  Running for: {details['elapsed']}")
            if details.get("ppid"):
                print(f"  Parent PID: {details['ppid']}")

            # Show full command for Java processes
            if details.get("name") == "java" and details.get("command"):
                print(f"  Command: {details['command']}")
        else:
            print("  (Unable to retrieve detailed process information)")

        print()

    print(
        f"Do you want to kill all {len(processes)} process(es)? (Press Enter to kill, or 'no' to exit)"
    )

    try:
        response = input().strip().lower()
        if response == "no" or response == "n":
            print("Processes not killed. Exiting.")
            return
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        return

    # Kill all found processes
    killed_count = 0
    failed_count = 0
    failed_pids = []

    for pid, _ in processes:
        if kill_process(pid):
            killed_count += 1
            print(f"Successfully killed process {pid}")
        else:
            failed_count += 1
            failed_pids.append(pid)
            print(f"Failed to kill process {pid}")

    if failed_pids:
        print(f"\nFailed to kill {failed_count} process(es): {', '.join(failed_pids)}")
        print(
            "You may need administrator privileges or the processes may have already terminated."
        )
    else:
        print(f"\nSuccessfully killed all {killed_count} process(es)")


if __name__ == "__main__":
    main()
