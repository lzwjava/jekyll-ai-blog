#!/usr/bin/env python3
import subprocess
import sys
import re


def get_commits_with_deletions(n):
    """Get the last n commits with their stats."""
    try:
        # Get commit hashes in reverse chronological order (latest first)
        cmd = ["git", "log", "--oneline", "-n", str(n), "--format=%H"]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=".")
        if result.returncode != 0:
            print(f"Error getting commits: {result.stderr}", file=sys.stderr)
            return []

        commits = result.stdout.strip().split("\n")
        return [commit for commit in commits if commit]
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return []


def get_changed_files_count(commit_hash):
    """Get the number of files changed (with deletions) in a commit."""
    try:
        cmd = ["git", "show", "--stat", commit_hash]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=".")

        if result.returncode != 0:
            return 0

        # Parse the output to find files that have been changed (had deletions)
        lines = result.stdout.split("\n")
        files_changed = 0

        # Look for the summary line like "n files changed, ..."
        for line in lines:
            if "files changed" in line:
                # Extract the file count using regex
                match = re.search(r"(\d+)\s+files? changed", line)
                if match:
                    files_changed = int(match.group(1))
                    break

        return files_changed
    except Exception as e:
        print(f"Error getting deletion count for {commit_hash}: {e}", file=sys.stderr)
        return 0


def main():
    if len(sys.argv) != 3:
        print("Usage: python git_delete_commit.py <n> <m>", file=sys.stderr)
        print("  n: number of recent commits to check", file=sys.stderr)
        print("  m: minimum number of files with deletions required", file=sys.stderr)
        sys.exit(1)

    try:
        n = int(sys.argv[1])
        m = int(sys.argv[2])
    except ValueError:
        print("Error: n and m must be integers", file=sys.stderr)
        sys.exit(1)

    if n <= 0 or m < 0:
        print("Error: n must be > 0 and m must be >= 0", file=sys.stderr)
        sys.exit(1)

    commits = get_commits_with_deletions(n)

    for commit_hash in commits:
        changed_files_count = get_changed_files_count(commit_hash)
        if changed_files_count > m:
            print(f"{commit_hash}: {changed_files_count}")
            sys.exit(0)

    print("none")


if __name__ == "__main__":
    main()
