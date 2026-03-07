import subprocess
import os


def main():
    # Get the local file path
    local_file = "/Users/lzwjava/.config/clash/clash_config.yaml"

    # Define remote host and file
    remote_host = "lzw@192.168.1.16"
    remote_file = os.path.join(".config", "clash", "clash_config.yaml")
    remote_path = os.path.join("~", remote_file)

    # Construct the scp command
    command = ["scp", local_file, remote_host + ":" + remote_path]

    # Execute the command using subprocess.run
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("File successfully synced to", remote_host, remote_path)
    except subprocess.CalledProcessError as e:
        print("Error syncing file. SCP command returned:", e.returncode)
        print("Error message:", e.stderr)


if __name__ == "__main__":
    main()
