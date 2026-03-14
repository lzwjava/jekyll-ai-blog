import json
import os
import subprocess
import sys


def reverse_sync_config(restart=True):
    print("Starting reverse config sync...")

    # Source: sanitized config in your project
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    source_path = os.path.join(project_dir, "config", "claude_code_config.json")
    print(f"Source config path: {source_path}")

    # Target: original config location on macOS
    target_dir = os.path.expanduser("~/.claude-code-router")
    target_path = os.path.join(target_dir, "config.json")
    print(f"Target config path: {target_path}")

    # Check if source exists
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"Source config not found: {source_path}")

    # Create target directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)

    # Read the sanitized config
    with open(source_path, "r") as f:
        config = json.load(f)

    # Restore API keys from environment variables
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    if not openrouter_api_key:
        print("Warning: OPENROUTER_API_KEY environment variable not set.")
        # Optionally fail fast if key is required
        # raise EnvironmentError("Missing OPENROUTER_API_KEY environment variable")

    # Replace empty or placeholder API keys
    if "Providers" in config:
        restored = False
        for provider in config["Providers"]:
            if "api_key" in provider and (
                not provider["api_key"]
                or provider["api_key"] == "REPLACE_WITH_OPENROUTER_API_KEY"
            ):
                provider["api_key"] = openrouter_api_key
                if openrouter_api_key:
                    print("Restored API key for provider.")
                    restored = True
                else:
                    print("No valid API key to restore.")
        if not restored:
            print("No API key needed restoration (already set or no match).")

    # Write the restored config back to the original location
    print("Writing config back to original location...")
    with open(target_path, "w") as f:
        json.dump(config, f, indent=2)

    print("Reverse config sync completed successfully.")

    # Print the complete config for verification
    print("\nComplete config:")
    print(json.dumps(config, indent=2))

    # Restart ccr if requested
    if restart:
        print("\nRestarting Claude Code Router...")
        try:
            subprocess.run(["ccr", "restart"], check=True)
            print("Claude Code Router restarted successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to restart Claude Code Router: {e}")
        except FileNotFoundError:
            print(
                "Warning: 'ccr' command not found. Is Claude Code Router installed and in PATH?"
            )


if __name__ == "__main__":
    no_restart = "--no-restart" in sys.argv
    restart_flag = not no_restart
    reverse_sync_config(restart=restart_flag)
