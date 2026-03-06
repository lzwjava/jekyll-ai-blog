#!/usr/bin/env python3
"""Cross-platform script to get the current browser tab title."""

import sys
import platform
import subprocess


def get_linux_firefox_title():
    """Get the current Firefox tab title on Linux."""
    try:
        # First check if xdotool is available
        if subprocess.run(["which", "xdotool"], capture_output=True).returncode != 0:
            print("DEBUG: xdotool not found in PATH", file=sys.stderr)
            return None

        # Use xdotool to get the active window title
        print("DEBUG: Running xdotool to get active window title", file=sys.stderr)
        result = subprocess.run(
            ["xdotool", "getactivewindow", "getwindowname"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        print(
            f"DEBUG: xdotool result: returncode={result.returncode}, stdout='{result.stdout.strip()}', stderr='{result.stderr.strip()}'",
            file=sys.stderr,
        )

        if result.returncode == 0:
            title = result.stdout.strip()
            print(f"DEBUG: Raw window title: '{title}'", file=sys.stderr)

            # Firefox titles typically include the page title followed by " - Mozilla Firefox"
            if " - Mozilla Firefox" in title:
                clean_title = title.split(" - Mozilla Firefox")[0]
                print(f"DEBUG: Cleaned Firefox title: '{clean_title}'", file=sys.stderr)
                return clean_title
            return title
        else:
            print("DEBUG: xdotool command failed", file=sys.stderr)
    except subprocess.TimeoutExpired:
        print("DEBUG: xdotool command timed out", file=sys.stderr)
    except subprocess.SubprocessError as e:
        print(f"DEBUG: Subprocess error: {e}", file=sys.stderr)
    except Exception as e:
        print(f"DEBUG: Unexpected error: {e}", file=sys.stderr)
    return None


def get_macos_safari_title():
    """Get the current Safari tab title on macOS."""
    try:
        # Use AppleScript to get the current Safari tab title
        script = """
        tell application "Safari"
            set currentTab to current tab of window 1
            return name of currentTab
        end tell
        """
        result = subprocess.run(
            ["osascript", "-e", script], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, subprocess.SubprocessError):
        pass
    return None


def get_windows_edge_title():
    """Get the current Edge tab title on Windows."""
    try:
        # Use PowerShell to get Microsoft Edge window title
        ps_script = """
        $edge = Get-Process | Where-Object { $_.ProcessName -eq "msedge" } | Select-Object -First 1
        if ($edge) {
            Add-Type -AssemblyName Microsoft.VisualBasic
            [Microsoft.VisualBasic.Interaction]::AppActivate($edge.Id) | Out-Null
            $title = Get-Process -Id $edge.Id | Select-Object -ExpandProperty MainWindowTitle
            Write-Output $title
        }
        """
        result = subprocess.run(
            ["powershell.exe", "-Command", ps_script],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0 and result.stdout.strip():
            title = result.stdout.strip()
            # Edge titles may include " - Microsoft Edge" suffix
            if " - Microsoft Edge" in title:
                return title.split(" - Microsoft Edge")[0]
            return title
    except (subprocess.TimeoutExpired, subprocess.SubprocessError):
        pass
    return None


def main():
    """Main function to get browser title based on platform."""
    system = platform.system().lower()
    print(f"DEBUG: Detected platform: {system}", file=sys.stderr)

    title = None

    if system == "linux":
        print("DEBUG: Using Linux Firefox detection", file=sys.stderr)
        title = get_linux_firefox_title()
    elif system == "darwin":  # macOS
        print("DEBUG: Using macOS Safari detection", file=sys.stderr)
        title = get_macos_safari_title()
    elif system == "windows":
        print("DEBUG: Using Windows Edge detection", file=sys.stderr)
        title = get_windows_edge_title()
    else:
        print(f"Unsupported platform: {system}", file=sys.stderr)
        sys.exit(1)

    print(f"DEBUG: Retrieved title: '{title}'", file=sys.stderr)
    if title:
        print(title)
    else:
        print("Could not retrieve browser title", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
