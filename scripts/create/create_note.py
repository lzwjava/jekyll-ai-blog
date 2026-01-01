import sys
import os
import random
import subprocess
import argparse
from datetime import datetime, timedelta
from typing import Optional
from gpa import gpa
from create_note_from_clipboard import create_note

# Ensure repository root is on sys.path for importing scripts.* packages
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from scripts.llm.openrouter_client import MODEL_MAPPING
from scripts.content.fix_mathjax import fix_mathjax_in_file
from scripts.content.fix_table import process_tables_in_file

def check_uncommitted_changes() -> None:
    """Check if there are any uncommitted changes in the repository.

    Raises an exception if uncommitted changes are found to prevent conflicts.
    """
    try:
        toplevel = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], text=True
        ).strip()
        result = subprocess.run(
            ["git", "-C", toplevel, "status", "--porcelain"],
            capture_output=True, text=True, check=True
        )
        if result.stdout.strip():
            print("[error] Uncommitted changes detected. Please commit or stash your changes before running this script.")
            raise RuntimeError("Uncommitted changes found")
    except subprocess.CalledProcessError as e:
        print(f"[error] Failed to check git status: {e}")
        raise


def git_pull_rebase() -> None:
    """Run 'git pull --rebase' at the repository root.

    This is helpful when creating notes from multiple machines to avoid conflicts.
    If not in a git repo or git is unavailable, fail gracefully.
    """
    try:
        toplevel = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], text=True
        ).strip()
        print(f"[info] Running 'git pull --rebase' in {toplevel}...")
        subprocess.run(["git", "-C", toplevel, "pull", "--rebase"], check=True)
    except Exception as e:
        print(f"[error] git pull --rebase failed: {e}")
        raise


def _repo_root() -> str:
    """Return the repository root derived from this file's location."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def open_note_in_browser(note_path: Optional[str]) -> None:
    """Open the GitHub page for the created note in the system default browser."""
    if not note_path:
        return

    abs_note_path = os.path.abspath(note_path)
    root = _repo_root()

    try:
        rel_path = os.path.relpath(abs_note_path, root)
    except ValueError as exc:
        print(f"[warn] Unable to compute relative path for {abs_note_path}: {exc}")
        return

    github_url = "https://github.com/lzwjava/blog-source/blob/main/" + rel_path.replace(os.sep, "/")

    if sys.platform.startswith("darwin"):
        command = ["open", github_url]
    elif sys.platform.startswith("linux"):
        command = ["env", "NO_AT_BRIDGE=1", "xdg-open", github_url]
    else:
        try:
            import webbrowser

            if not webbrowser.open(github_url):
                print(f"[warn] webbrowser module could not launch {github_url}")
        except Exception as exc:  # pragma: no cover - defensive fallback
            print(f"[warn] Unable to launch browser for {github_url}: {exc}")
        return

    try:
        subprocess.run(command, check=False)
    except FileNotFoundError:
        print(f"[warn] Launch command not found when opening {github_url}")
    except Exception as exc:  # pragma: no cover - defensive fallback
        print(f"[warn] Failed to open browser for {github_url}: {exc}")

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Create a note; first positional arg is the model key."
    )
    # Add 'unknown' to the available choices
    all_choices = sorted(list(MODEL_MAPPING.keys()) + ["unknown"])

    parser.add_argument(
        "model",
        choices=all_choices,
        default="unknown",
        help=(
            "Model key to annotate in frontmatter; choices shown above."
        ),
    )
    parser.add_argument(
        "--random",
        action="store_true",
        help="Use a random date within last 180 days",
    )
    parser.add_argument(
        "--without-math",
        action="store_true",
        help="Skip fixing MathJax delimiters in the created file before git add",
    )
    parser.add_argument(
        "--open",
        action="store_true",
        help="Open the note in browser after creating",
    )
    parser.add_argument(
        "--no-push",
        action="store_true",
        help="Skip the gpa git push step",
    )
    return parser.parse_args()

def generate_random_date():
    """Generate a random date within the last 180 days"""
    # Seed the random number generator with current timestamp for better randomness
    random.seed(datetime.now().timestamp())

    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)

    random_days = random.randint(0, 180)
    random_date = start_date + timedelta(days=random_days)

    return random_date.strftime('%Y-%m-%d')

if __name__ == "__main__":
    # Check for uncommitted changes before proceeding
    check_uncommitted_changes()

    # Ensure we are up to date to avoid conflicts across machines
    git_pull_rebase()

    args = parse_args()
    random_date = generate_random_date() if args.random else None
    print(f"[debug] random_date: {random_date}")  # Debug output

    created_path = create_note(date=random_date, note_model_key=args.model)

    # Fix MathJax before invoking GPT-assisted git add/commit (unless --without-math is specified)
    if not args.without_math and created_path and os.path.exists(created_path):
        try:
            # Check if model contains "gemini" and pass gemini=True if so
            is_gemini_model = "gemini" in args.model.lower()
            fix_mathjax_in_file(created_path, gemini=is_gemini_model)
            process_tables_in_file(created_path, fix_tables=True)
        except Exception as e:
            print(f"[warn] MathJax fix failed for {created_path}: {e}")

    # Only run gpa if --no-push is not specified
    if not args.no_push:
        gpa()

    # Open browser if --open flag is specified
    if args.open:
        try:
            open_note_in_browser(created_path)
        except Exception as e:
            print(f"[warn] Failed to open browser: {e}")

    print(f"[info] Note created at {created_path}")
