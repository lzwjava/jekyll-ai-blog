import subprocess
import argparse
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from llm.openrouter_client import call_openrouter_api


def check_git_status():
    result = subprocess.run(
        ["git", "status", "--porcelain"], capture_output=True, text=True
    )
    if result.stdout.strip():
        raise Exception(
            "Cannot rebase: You have unstaged changes. Please commit or stash them first."
        )


def generate_squash_message(rebase_todo):
    commits = []
    for line in rebase_todo.split("\n"):
        if line.startswith("pick") or line.startswith("squash"):
            parts = line.split(" ", 3)  # Split into: action, hash, [message]
            if len(parts) > 2:
                commits.append(parts[2])

    prompt = f"""Here are the commits to be squashed:

{' '.join(commits)}

Generate a concise, descriptive commit message that summarizes all these changes.
Follow conventional commit format (e.g., feat:, fix:, docs:, etc.).
Make it clear and informative in one line."""

    try:
        message = call_openrouter_api(prompt, model="claude-sonnet")
        return message.strip()
    except Exception as e:
        print(f"Error generating commit message: {e}")
        return " + ".join(commits)


def main():
    parser = argparse.ArgumentParser(description="Interactive git squash helper")
    parser.add_argument("n", type=int, help="Number of commits to squash")
    args = parser.parse_args()

    # Check for unstaged changes first
    check_git_status()

    # Print git rebase command for user to run
    print(f"\nRun this command to start the interactive rebase:")
    print(f"git rebase -i HEAD~{args.n}")

    print(
        "\nNow copy the contents of the git-rebase-todo file here (Ctrl+D when done):"
    )
    rebase_todo = sys.stdin.read().strip()

    # Modify rebase todo - keep first pick, change rest to squash
    modified_todo = []
    first_pick = True
    for line in rebase_todo.split("\n"):
        if line.startswith("#") or not line.strip():
            modified_todo.append(line)
        elif line.startswith("pick") and first_pick:
            modified_todo.append(line)
            first_pick = False
        elif line.startswith("pick"):
            modified_todo.append(line.replace("pick", "squash"))
        else:
            modified_todo.append(line)

    # Generate commit message
    commit_message = generate_squash_message(rebase_todo)

    print("\nReplace the rebase-todo content with:")
    print("=" * 50)
    print("\n".join(modified_todo))
    print("=" * 50)

    print("\nWhen prompted for the commit message, use:")
    print("=" * 50)
    print(commit_message)
    print("=" * 50)


if __name__ == "__main__":
    main()
