import subprocess
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def check_git_status():
    result = subprocess.run(
        ["git", "status", "--porcelain"], capture_output=True, text=True
    )
    if result.stdout.strip():
        raise Exception(
            "Cannot force push: You have unstaged changes. Please commit or stash them first."
        )


def get_current_branch():
    result = subprocess.run(
        ["git", "branch", "--show-current"], capture_output=True, text=True
    )
    return result.stdout.strip()


def main():
    check_git_status()
    current_branch = get_current_branch()
    subprocess.run(["git", "push", "--force-with-lease", "origin", current_branch])


if __name__ == "__main__":
    main()
