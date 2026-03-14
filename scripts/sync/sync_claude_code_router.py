import json
import os


def sync_config():
    print("Starting config sync...")
    source_path = os.path.expanduser("~/.claude-code-router/config.json")
    print(f"Source config path: {source_path}")
    target_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config"
    )
    target_path = os.path.join(target_dir, "claude_code_config.json")
    print(f"Target config path: {target_path}")

    # Read source config
    with open(source_path) as f:
        config = json.load(f)

    # Replace sensitive info
    if "Providers" in config:
        for provider in config["Providers"]:
            if "api_key" in provider:
                provider["api_key"] = ""

    # Write sanitized config
    print("Writing sanitized config...")
    with open(target_path, "w") as f:
        json.dump(config, f, indent=2)
    print("Config sync completed successfully")


if __name__ == "__main__":
    sync_config()
