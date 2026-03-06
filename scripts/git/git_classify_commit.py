#!/usr/bin/env python3
"""
git_commit_type.py
Count commits by type: code (py, html, js, etc.), markdown (md), or others.
If multiple types are present, the one with the most files wins.
"""

import argparse
import subprocess
from pathlib import Path
from collections import Counter

# Extensions considered as "code"
CODE_EXTS = {
    "py",
    "js",
    "ts",
    "jsx",
    "tsx",
    "html",
    "css",
    "scss",
    "sass",
    "java",
    "c",
    "cpp",
    "cxx",
    "h",
    "hpp",
    "go",
    "rs",
    "php",
    "rb",
    "swift",
    "kt",
    "scala",
    "clj",
    "erl",
    "ex",
    "dart",
}
# Extensions considered as "markdown"
MD_EXTS = {"md", "markdown"}


def classify_commit(repo: Path, commit: str) -> str | None:
    """
    Return 'code', 'md', 'others', or None depending on the files changed in the commit.
    If multiple types are present, the one with the most files wins.
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
    if not files:
        return None

    counts = Counter()
    for f in files:
        ext = f.rsplit(".", 1)[-1].lower()
        if ext in CODE_EXTS:
            counts["code"] += 1
        elif ext in MD_EXTS:
            counts["md"] += 1
        else:
            counts["others"] += 1

    if not counts:
        return None
    # Return the type with the highest count
    return counts.most_common(1)[0][0]


def list_commits(repo: Path, rev_range: str) -> list[str]:
    """Return list of commit hashes in the given revision range."""
    cmd = ["git", "-C", str(repo), "rev-list", rev_range]
    try:
        output = subprocess.check_output(cmd, text=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"git rev-list failed: {e}") from e
    return output.strip().splitlines()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Count commits by type: code vs markdown vs others."
    )
    parser.add_argument("repo", type=Path, help="Path to the git repository.")
    parser.add_argument(
        "rev_range",
        nargs="?",
        default="HEAD",
        help="Git revision range to inspect (default: HEAD).",
    )

    args = parser.parse_args()

    try:
        commits = list_commits(args.repo, args.rev_range)
    except RuntimeError as e:
        print(e)
        return

    total = len(commits)
    print(f"Found {total} commits to analyze.\n")

    stats = Counter()
    for idx, commit in enumerate(commits, 1):
        ctype = classify_commit(args.repo, commit)
        if ctype:
            stats[ctype] += 1
        # Print progress every 10% or every commit if < 50
        if total < 50 or idx % max(1, total // 10) == 0 or idx == total:
            print(
                f"[{idx:>{len(str(total))}}/{total}] {commit[:8]} -> {ctype or 'skip'}"
            )

    print("\nCommit type counts:")
    for t in ("code", "md", "others"):
        print(f"{t}: {stats[t]}")


if __name__ == "__main__":
    main()
