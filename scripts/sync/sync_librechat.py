import os
import argparse
from typing import Iterable, Tuple

SENSITIVE_ENV_SUBSTRINGS: Tuple[str, ...] = (
    "API_KEY",
    "API-TOKEN",
    "TOKEN",
    "SECRET",
    "PASSWORD",
    "ACCESS_TOKEN",
    "REFRESH_TOKEN",
    "BEARER",
    "OPENAI_KEY",
    "ANTHROPIC_KEY",
    "GOOGLE_KEY",
    "AZURE_KEY",
)

SENSITIVE_YAML_KEYS: Tuple[str, ...] = (
    "apiKey",
    "api_key",
    "key",
    "token",
    "secret",
    "password",
    "accessToken",
    "refreshToken",
    "bearer",
)


# Recover mapping: sanitized key -> environment variable to populate on reverse
ENV_RECOVERY_MAP = {
    "OPENROUTER_KEY": "OPENROUTER_API_KEY",
    "SERPER_API_KEY": "SERPER_API_KEY",
    "FIRECRAWL_API_KEY": "FIRECRAWL_API_KEY",
    "JINA_API_KEY": "JINA_API_KEY",
}


def ensure_target_dir() -> str:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_dir = os.path.join(base_dir, "config")
    os.makedirs(target_dir, exist_ok=True)
    return target_dir


def is_sensitive_env_key(key: str) -> bool:
    upper_key = key.upper()
    # Special case: Treat JWT secrets as non-sensitive
    if upper_key in ("JWT_SECRET", "JWT_REFRESH_SECRET"):
        return False
    if upper_key.endswith("_KEY") or upper_key.endswith("-KEY"):
        return True
    return any(part in upper_key for part in SENSITIVE_ENV_SUBSTRINGS)


def sanitize_env(lines: Iterable[str]) -> str:
    out_lines = []
    for line in lines:
        raw = line.rstrip("\n")
        if not raw or raw.lstrip().startswith("#"):
            out_lines.append(raw)
            continue
        if "=" not in raw:
            out_lines.append(raw)
            continue
        k, v = raw.split("=", 1)
        if is_sensitive_env_key(k.strip()):
            out_lines.append(f"{k}=")
        else:
            out_lines.append(raw)
    return "\n".join(out_lines) + "\n"


def sanitize_yaml_lines(lines: Iterable[str]) -> str:
    out_lines = []
    for line in lines:
        s = line.rstrip("\n")
        # Skip comments and empty
        if not s.strip() or s.lstrip().startswith("#"):
            out_lines.append(s)
            continue

        # Try to match simple key: value pairs, preserving indentation
        stripped = s.lstrip()
        indent_len = len(s) - len(stripped)
        indent = s[:indent_len]

        # Handle list item key: value (e.g., "- apiKey: abc")
        if stripped.startswith("- "):
            dash, rest = stripped.split(" ", 1)
            # rest might be "apiKey: value"; try to split once on ':'
            if ":" in rest:
                key, after = rest.split(":", 1)
                key_name = key.strip()
                if key_name in SENSITIVE_YAML_KEYS:
                    out_lines.append(f'{indent}- {key_name}: ""')
                    continue
        else:
            if ":" in stripped:
                key, after = stripped.split(":", 1)
                key_name = key.strip()
                if key_name in SENSITIVE_YAML_KEYS:
                    out_lines.append(f'{indent}{key_name}: ""')
                    continue

        out_lines.append(s)
    return "\n".join(out_lines) + "\n"


def sync_librechat(librechat_dir: str | None = None) -> None:
    print("Syncing LibreChat config...")
    lc_dir = (
        os.path.expanduser(librechat_dir)
        if librechat_dir
        else os.path.expanduser("~/projects/LibreChat")
    )
    env_src = os.path.join(lc_dir, ".env")
    yaml_src = os.path.join(lc_dir, "librechat.yaml")
    docker_compose_src = os.path.join(lc_dir, "docker-compose.override.yml")

    target_dir = ensure_target_dir()
    env_dst = os.path.join(target_dir, "librechat.env")
    yaml_dst = os.path.join(target_dir, "librechat.yaml")
    docker_compose_dst = os.path.join(target_dir, "docker-compose.override.yml")

    found_any = False

    if os.path.exists(env_src):
        print(f"Reading: {env_src}")
        with open(env_src, "r", encoding="utf-8") as f:
            sanitized = sanitize_env(f.readlines())
        with open(env_dst, "w", encoding="utf-8") as f:
            f.write(sanitized)
        print(f"Wrote sanitized .env to {env_dst}")
        found_any = True
    else:
        print(f"Warning: .env not found at {env_src}")

    if os.path.exists(yaml_src):
        print(f"Reading: {yaml_src}")
        # Copy librechat.yaml verbatim; do NOT sanitize.
        with open(yaml_src, "r", encoding="utf-8") as f:
            yaml_raw = f.read()
        with open(yaml_dst, "w", encoding="utf-8") as f:
            f.write(yaml_raw)
        print(f"Wrote YAML to {yaml_dst}")
        found_any = True
    else:
        print(f"Warning: librechat.yaml not found at {yaml_src}")

    if os.path.exists(docker_compose_src):
        print(f"Reading: {docker_compose_src}")
        # Copy docker-compose.override.yml verbatim; do NOT sanitize.
        with open(docker_compose_src, "r", encoding="utf-8") as f:
            docker_raw = f.read()
        with open(docker_compose_dst, "w", encoding="utf-8") as f:
            f.write(docker_raw)
        print(f"Wrote docker-compose.override.yml to {docker_compose_dst}")
        found_any = True
    else:
        print(f"Warning: docker-compose.override.yml not found at {docker_compose_src}")

    if not found_any:
        print("Nothing to sync. Provide LIBRECHAT_DIR or ensure default path exists.")


def reverse_sync_librechat(librechat_dir: str | None = None) -> None:
    print("Reverse syncing into LibreChat directory...")
    lc_dir = (
        os.path.expanduser(librechat_dir)
        if librechat_dir
        else os.path.expanduser("~/projects/LibreChat")
    )

    src_dir = ensure_target_dir()
    env_src = os.path.join(src_dir, "librechat.env")
    yaml_src = os.path.join(src_dir, "librechat.yaml")
    docker_compose_src = os.path.join(src_dir, "docker-compose.override.yml")

    env_dst = os.path.join(lc_dir, ".env")
    yaml_dst = os.path.join(lc_dir, "librechat.yaml")
    docker_compose_dst = os.path.join(lc_dir, "docker-compose.override.yml")

    wrote_any = False

    if os.path.exists(env_src):
        print(f"Reading: {env_src}")
        with open(env_src, "r", encoding="utf-8") as f:
            in_lines = f.readlines()

        # Try to recover sensitive values from environment variables if blank
        out_lines: list[str] = []
        for line in in_lines:
            raw = line.rstrip("\n")
            if not raw or raw.lstrip().startswith("#") or "=" not in raw:
                out_lines.append(raw)
                continue
            k, v = raw.split("=", 1)
            key = k.strip()
            val = v.strip()

            recovered_env_name = ENV_RECOVERY_MAP.get(key)
            recovered_value = (
                os.environ.get(recovered_env_name) if recovered_env_name else None
            )

            if recovered_value and (val == "" or val == '""' or val == "''"):
                out_lines.append(f'{key}="{recovered_value}"')
            else:
                out_lines.append(raw)

        data = "\n".join(out_lines) + "\n"

        # Note: this operation will overwrite target .env
        try:
            with open(env_dst, "w", encoding="utf-8") as f:
                f.write(data)
            print(f"Wrote .env to {env_dst}")
            wrote_any = True
        except PermissionError:
            print(
                f"Permission denied writing {env_dst}. Run with appropriate permissions."
            )
    else:
        print(f"Warning: sanitized env not found at {env_src}")

    if os.path.exists(yaml_src):
        print(f"Reading: {yaml_src}")
        with open(yaml_src, "r", encoding="utf-8") as f:
            data = f.read()
        try:
            with open(yaml_dst, "w", encoding="utf-8") as f:
                f.write(data)
            print(f"Wrote YAML to {yaml_dst}")
            wrote_any = True
        except PermissionError:
            print(
                f"Permission denied writing {yaml_dst}. Run with appropriate permissions."
            )
    else:
        print(f"Warning: sanitized yaml not found at {yaml_src}")

    if os.path.exists(docker_compose_src):
        print(f"Reading: {docker_compose_src}")
        with open(docker_compose_src, "r", encoding="utf-8") as f:
            data = f.read()
        try:
            with open(docker_compose_dst, "w", encoding="utf-8") as f:
                f.write(data)
            print(f"Wrote docker-compose.override.yml to {docker_compose_dst}")
            wrote_any = True
        except PermissionError:
            print(
                f"Permission denied writing {docker_compose_dst}. Run with appropriate permissions."
            )
    else:
        print(f"Warning: docker-compose.override.yml not found at {docker_compose_src}")

    if not wrote_any:
        print("Nothing written. Ensure sanitized files exist in scripts/config.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync LibreChat config <-> repo config"
    )
    parser.add_argument(
        "--reverse",
        action="store_true",
        help="Copy from scripts/config back to LibreChat directory",
    )
    parser.add_argument(
        "--dir",
        dest="directory",
        default=os.environ.get("LIBRECHAT_DIR"),
        help="LibreChat directory (default: ~/projects/LibreChat or LIBRECHAT_DIR)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.reverse:
        reverse_sync_librechat(args.directory)
    else:
        sync_librechat(args.directory)
