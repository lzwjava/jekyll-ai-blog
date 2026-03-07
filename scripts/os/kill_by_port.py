#!/usr/bin/env python3

import argparse
import platform

# Import platform-specific modules
if platform.system().lower() == "windows":
    import kill_windows as platform_module
else:
    import kill_unix as platform_module


def find_process_on_port(port):
    """Find the process ID using the specified port."""
    return platform_module.find_process_on_port(port)


def get_process_details(pid):
    """Get detailed information about a process."""
    return platform_module.get_process_details(pid)


def kill_process(pid):
    """Kill the process with the specified PID."""
    return platform_module.kill_process(pid)


def main():
    parser = argparse.ArgumentParser(
        description="Kill process running on a specific port"
    )
    parser.add_argument(
        "--port",
        "-p",
        type=int,
        default=8080,
        help="Port number to kill process on (default: 8080)",
    )
    args = parser.parse_args()

    port = args.port
    pid, process_info = find_process_on_port(port)

    if not pid:
        print(f"No process found running on port {port}")
        return

    # Get detailed process information
    details = get_process_details(pid)

    print(f"Found process running on port {port}:")
    print(f"  Name: {process_info}")

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

    print("")
    print("Do you want to kill this process? (Press Enter to kill, or 'no' to exit)")

    try:
        response = input().strip().lower()
        if response == "no" or response == "n":
            print("Process not killed. Exiting.")
            return
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        return

    if kill_process(pid):
        print(f"Successfully killed process {pid}")
    else:
        print(f"Failed to kill process {pid}")
        print(
            "You may need administrator privileges or the process may have already terminated."
        )


if __name__ == "__main__":
    main()
