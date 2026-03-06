import argparse
import subprocess
from pathlib import Path

#!/usr/bin/env python3
"""
git_commit_filter.py
List all files NOT matching a given extension touched by a commit.

Usage:
    python git_commit_filter.py /path/to/repo abc123 --exclude-ext py
"""


def list_files_excluding_ext(repo: Path, commit: str, exclude_ext: str) -> list[str]:
    """
    Return a list of file paths changed in the given commit
    whose extension is NOT `exclude_ext`.
    """
    cmd = [
        "git",
        "-C",
        str(repo),
        "diff-tree",
        "--no-commit-id",
        "--name-only",
        "-r",
        commit,
    ]
    try:
        output = subprocess.check_output(cmd, text=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"git diff-tree failed: {e}") from e

    files = output.strip().splitlines()
    if exclude_ext.startswith("."):
        exclude_ext = exclude_ext[1:]
    exclude_ext = exclude_ext.lower()
    filtered_files = [f for f in files if not f.lower().endswith(f".{exclude_ext}")]
    return filtered_files


def main() -> None:
    parser = argparse.ArgumentParser(
        description="List files changed by a specific git commit, excluding a given extension.",
        usage="%(prog)s repo_path commit_hash [--exclude-ext EXT]",
    )
    parser.add_argument("repo", type=Path, help="Path to the git repository.")
    parser.add_argument("commit", help="Commit hash to inspect.")
    parser.add_argument(
        "--exclude-ext",
        default="py",
        help="File extension to exclude (default: py). Do NOT include the leading dot.",
    )

    args = parser.parse_args()

    try:
        files = list_files_excluding_ext(args.repo, args.commit, args.exclude_ext)
    except RuntimeError as e:
        print(e)
        return

    if files:
        print(f"Files changed (excluding .{args.exclude_ext}):")
        for f in files:
            print(f)
    else:
        print(f"No files changed (excluding .{args.exclude_ext}) in this commit.")


if __name__ == "__main__":
    main()
