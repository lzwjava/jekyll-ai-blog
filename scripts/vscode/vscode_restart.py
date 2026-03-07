import sys
import time
import subprocess


def restart_vscode():
    """Restart VSCode gracefully to prevent accidental re-creation of draft files."""
    print(
        "Restarting VSCode gracefully to prevent accidental re-creation of draft files..."
    )
    try:
        if sys.platform == "win32":
            # Graceful close without /f
            subprocess.run(["taskkill", "/im", "Code.exe", "/t"], check=False)
            time.sleep(3)  # Delay for cleanup
            subprocess.Popen(["code", "."])  # Reopen
        elif sys.platform == "darwin":
            # Use AppleScript for graceful quit
            subprocess.run(
                ["osascript", "-e", 'quit app "Visual Studio Code"'], check=False
            )
            time.sleep(3)
            subprocess.call(["open", "-a", "Visual Studio Code", "."])
        elif sys.platform.startswith("linux"):
            # SIGTERM for graceful termination
            subprocess.run(["killall", "code"], check=False)
            time.sleep(3)
            subprocess.Popen(["code", "."])
        else:
            print("Unsupported platform for restarting VSCode.")
    except Exception as e:
        print(f"Error during restart: {e}. Please manually restart VSCode.")


if __name__ == "__main__":
    restart_vscode()
