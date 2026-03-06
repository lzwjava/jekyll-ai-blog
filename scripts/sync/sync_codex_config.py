import os
import tomlkit


def sync_config():
    print("Starting codex config sync...")
    source_path = os.path.expanduser("~/.codex/config.toml")
    print(f"Source config path: {source_path}")
    target_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config"
    )
    target_path = os.path.join(target_dir, "codex_config.toml")
    print(f"Target config path: {target_path}")

    # Read source config
    with open(source_path, "r") as f:
        config = tomlkit.load(f)

    # Replace sensitive info (assume api_key similar to JSON version)
    if "api_key" in config:
        config["api_key"] = ""

    # Write sanitized config
    print("Writing sanitized config...")
    with open(target_path, "w") as f:
        tomlkit.dump(config, f)
    print("Codex config sync completed successfully")


if __name__ == "__main__":
    sync_config()
