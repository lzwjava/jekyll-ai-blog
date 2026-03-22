import os
import json
import subprocess
import sys
import argparse
from typing import Any

REMOTE_USER = "lzw"
REMOTE_HOST = "192.168.1.36"
REMOTE_PATH = "~/.openclaw/openclaw.json"

SENSITIVE_KEY_SUBSTRINGS = (
    "key",
    "token",
    "secret",
    "password",
    "apikey",
    "api_key",
    "accesstoken",
    "refreshtoken",
    "bearer",
    "credential",
    "auth",
    "integrity",
)


def is_sensitive_key(key: str) -> bool:
    lower = key.lower()
    return any(part in lower for part in SENSITIVE_KEY_SUBSTRINGS)


def sanitize_value(value: Any) -> Any:
    if isinstance(value, str):
        return ""
    if isinstance(value, dict):
        return sanitize_json(value)
    if isinstance(value, list):
        return [sanitize_value(item) for item in value]
    return value


def sanitize_json(data: dict) -> dict:
    result = {}
    for k, v in data.items():
        if is_sensitive_key(k):
            result[k] = sanitize_value(v)
        else:
            result[k] = sanitize_nested(v)
    return result


def sanitize_nested(value: Any) -> Any:
    if isinstance(value, dict):
        return sanitize_json(value)
    if isinstance(value, list):
        return [sanitize_nested(item) for item in value]
    return value


def target_dir() -> str:
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base, "config")
    os.makedirs(path, exist_ok=True)
    return path


def fetch_remote(user: str, host: str, remote_path: str, local_path: str) -> bool:
    src = f"{user}@{host}:{remote_path}"
    cmd = ["scp", src, local_path]
    print(f"Fetching {src} ...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"scp failed: {result.stderr.strip()}", file=sys.stderr)
        return False
    return True


def sync_openclaw(user: str, host: str) -> None:
    dst_dir = target_dir()
    tmp_path = os.path.join(dst_dir, "openclaw_raw.json")
    out_path = os.path.join(dst_dir, "openclaw.json")

    if not fetch_remote(user, host, REMOTE_PATH, tmp_path):
        sys.exit(1)

    with open(tmp_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    os.remove(tmp_path)

    sanitized = sanitize_json(data)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(sanitized, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Wrote sanitized config to {out_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch and sanitize openclaw.json from remote host"
    )
    parser.add_argument("--user", default=REMOTE_USER, help="SSH username")
    parser.add_argument("--host", default=REMOTE_HOST, help="Remote host IP")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    sync_openclaw(args.user, args.host)
