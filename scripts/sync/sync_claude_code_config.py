import json
import os


def sync_config():
    print("Starting Claude Code config sync...")
    source_path = os.path.expanduser("~/.claude/settings.json")
    print(f"Source config path: {source_path}")
    target_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config"
    )
    target_path = os.path.join(target_dir, "claude_code_settings.json")
    print(f"Target config path: {target_path}")

    # Read source config
    with open(source_path, "r") as f:
        config = json.load(f)

    # Replace sensitive info
    if "env" in config:
        for key in list(config["env"].keys()):
            if any(s in key.lower() for s in ["token", "key", "secret", "password"]):
                config["env"][key] = ""

    # Write sanitized config
    print("Writing sanitized config...")
    with open(target_path, "w") as f:
        json.dump(config, f, indent=2)
        f.write("\n")
    print("Claude Code config sync completed successfully")


if __name__ == "__main__":
    sync_config()
