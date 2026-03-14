import json
import os
import sys


def reverse_sync_config():
    print("Starting reverse Claude Code config sync...")

    # Source: sanitized config in your project
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    source_path = os.path.join(project_dir, "config", "claude_code_settings.json")
    print(f"Source config path: {source_path}")

    # Target: original config location
    target_dir = os.path.expanduser("~/.claude")
    target_path = os.path.join(target_dir, "settings.json")
    print(f"Target config path: {target_path}")

    # Check if source exists
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"Source config not found: {source_path}")

    # Create target directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)

    # Read the sanitized config
    with open(source_path, "r") as f:
        config = json.load(f)

    # Restore sensitive env vars from environment variables
    restored = False
    if "env" in config:
        for key in config["env"]:
            if config["env"][key] == "":
                env_val = os.getenv(key)
                if env_val:
                    config["env"][key] = env_val
                    print(f"Restored {key}.")
                    restored = True
                else:
                    print(f"Warning: {key} environment variable not set.")

    if not restored:
        print("No keys needed restoration (already set or no match).")

    # Write the restored config back to the original location
    print("Writing config back to original location...")
    with open(target_path, "w") as f:
        json.dump(config, f, indent=2)
        f.write("\n")

    print("Reverse Claude Code config sync completed successfully.")

    # Print the complete config for verification
    print("\nComplete config:")
    print(json.dumps(config, indent=2))


if __name__ == "__main__":
    reverse_sync_config()
