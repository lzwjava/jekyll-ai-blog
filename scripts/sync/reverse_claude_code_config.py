import argparse
import json
import os

CHANNEL_ENV_VARS = {
    "pincc": {
        "ANTHROPIC_AUTH_TOKEN": "PINCC_API_KEY",
        "ANTHROPIC_BASE_URL": "PINCC_API_ENDPOINT",
    },
    "sssaicode": {
        "ANTHROPIC_AUTH_TOKEN": "SSSAICODE_API_KEY",
        "ANTHROPIC_BASE_URL": "SSSAICODE_API_ENDPOINT",
    },
}

KNOWN_TOKEN_VARS = [
    v for mapping in CHANNEL_ENV_VARS.values() for v in mapping.values()
]


def reverse_sync_config(channel: str):
    print(f"Starting reverse Claude Code config sync (channel: {channel})...")

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

    # Apply channel selection: update env var references in config
    config["channel"] = channel
    env_mapping = CHANNEL_ENV_VARS[channel]
    if "env" not in config:
        config["env"] = {}
    for claude_key, named_var in env_mapping.items():
        config["env"][claude_key] = named_var
        print(f"Set {claude_key} -> {named_var} (channel: {channel})")

    # Persist channel selection back to source settings.json
    with open(source_path, "w") as f:
        json.dump(config, f, indent=2)
        f.write("\n")
    print(f"Saved channel '{channel}' to source config.")

    # Restore sensitive env vars from environment variables
    restored = False
    deploy_config = json.loads(json.dumps(config))  # deep copy for deployment
    if "env" in deploy_config:
        for key in deploy_config["env"]:
            val = deploy_config["env"][key]
            if val in KNOWN_TOKEN_VARS:
                env_val = os.getenv(val)
                if env_val:
                    deploy_config["env"][key] = env_val
                    print(f"Restored {key} from {val}.")
                    restored = True
                else:
                    print(f"Warning: {val} environment variable not set.")
            elif val == "":
                env_val = os.getenv(key)
                if env_val:
                    deploy_config["env"][key] = env_val
                    print(f"Restored {key}.")
                    restored = True
                else:
                    print(f"Warning: {key} environment variable not set.")

    if not restored:
        print("No keys needed restoration (already set or no match).")

    # Remove internal 'channel' key before writing to ~/.claude/settings.json
    deploy_config.pop("channel", None)

    # Write the restored config back to the original location
    print("Writing config back to original location...")
    with open(target_path, "w") as f:
        json.dump(deploy_config, f, indent=2)
        f.write("\n")

    print("Reverse Claude Code config sync completed successfully.")

    # Print the complete config for verification
    print("\nComplete config:")
    print(json.dumps(deploy_config, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reverse sync Claude Code config.")
    parser.add_argument(
        "channel",
        choices=list(CHANNEL_ENV_VARS.keys()),
        nargs="?",
        default="pincc",
        help="API channel to use (default: pincc)",
    )
    args = parser.parse_args()
    reverse_sync_config(args.channel)
