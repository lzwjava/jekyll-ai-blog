import os
import sys
import tomlkit
import subprocess


def reverse_sync_config(restart=True):
    print("Starting reverse codex config sync...")

    # Source: sanitized config in your project
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    source_path = os.path.join(project_dir, "config", "codex_config.toml")
    print(f"Source config path: {source_path}")

    # Target: original config location
    target_dir = os.path.expanduser("~/.codex")
    target_path = os.path.join(target_dir, "config.toml")
    print(f"Target config path: {target_path}")

    # Check if source exists
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"Source config not found: {source_path}")

    # Create target directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)

    # Read the sanitized config
    with open(source_path, "r") as f:
        config = tomlkit.load(f)

    # Restore API keys from environment variables
    codex_api_key = os.getenv("CODEX_API_KEY")
    codex_token = os.getenv("CODEX_TOKEN")

    if not codex_api_key:
        print("Warning: CODEX_API_KEY environment variable not set.")
    if not codex_token:
        print("Warning: CODEX_TOKEN environment variable not set.")

    # Replace empty API keys
    restored = False
    if "api_key" in config and (not config["api_key"] or config["api_key"] == ""):
        if codex_api_key:
            config["api_key"] = codex_api_key
            print("Restored API key.")
            restored = True
        else:
            print("No valid API key to restore.")

    if "token" in config and (not config["token"] or config["token"] == ""):
        if codex_token:
            config["token"] = codex_token
            print("Restored token.")
            restored = True
        else:
            print("No valid token to restore.")

    if not restored:
        print("No keys needed restoration (already set or no match).")

    # Write the restored config back to the original location
    print("Writing config back to original location...")
    with open(target_path, "w") as f:
        tomlkit.dump(config, f)

    print("Reverse codex config sync completed successfully.")

    # Print the complete config for verification
    print("\nComplete config:")
    print(tomlkit.dumps(config))


if __name__ == "__main__":
    no_restart = "--no-restart" in sys.argv
    restart_flag = not no_restart
    reverse_sync_config(restart=restart_flag)
