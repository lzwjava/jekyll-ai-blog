#!/usr/bin/env python3

import os
import sys
import argparse
import subprocess


def run_translation_batch(batch_end):
    """Run translation for a specific batch end number."""
    cmd = [
        sys.executable,
        "scripts/translation/update_lang_notes.py",
        "--n",
        str(batch_end),
    ]

    print(f"Running translation batch up to {batch_end} files...")
    result = subprocess.run(
        cmd, cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    )

    if result.returncode != 0:
        print(f"Translation batch failed for --n {batch_end}")
        return False

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Run notes translation batches locally, similar to the GitHub workflow."
    )
    parser.add_argument(
        "--total",
        type=int,
        default=3700,
        help="Total number of recent posts to process (default: 3700)",
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        default=10,
        help="Batch size for processing (default: 10, matching workflow)",
    )
    parser.add_argument(
        "--start_batch",
        type=int,
        default=10,
        help="Starting batch end number (default: 10, matching workflow)",
    )

    args = parser.parse_args()

    total_posts = args.total
    batch_size = args.batch_size
    start_batch = args.start_batch

    # Validate total_posts similar to the workflow
    if total_posts <= 0:
        print("TOTAL_POSTS must be a positive integer. Skipping translation batch job.")
        sys.exit(0)

    print(
        f"Starting local translation of {total_posts} recent notes in batches of {batch_size}"
    )

    for batch_end in range(start_batch, total_posts + 1, batch_size):
        if batch_end > total_posts:
            batch_end = total_posts

        print(f"\n--- Processing batch ending at {batch_end} ---")

        success = run_translation_batch(batch_end)
        if not success:
            print(f"Batch {batch_end} failed, stopping...")
            sys.exit(1)

        # Always commit changes after each batch
        try:
            # Add changes
            subprocess.run(["git", "add", "_posts/**/**"], check=True)

            # Check if there are changes to commit
            result = subprocess.run(["git", "diff", "--cached", "--quiet"])
            if result.returncode != 0:  # There are changes
                # Commit
                subprocess.run(
                    ["git", "commit", "-m", "docs(notes) Add translated notes"],
                    check=True,
                )
                print(f"Committed changes for batch {batch_end}")

                # Try to push, pull first if push fails
                try:
                    subprocess.run(["git", "push"], check=True)
                    print(f"Pushed changes for batch {batch_end}")
                except subprocess.CalledProcessError:
                    print(
                        f"Push failed for batch {batch_end}, pulling latest changes..."
                    )
                    subprocess.run(["git", "pull", "--rebase"], check=True)
                    subprocess.run(["git", "push"], check=True)
                    print(f"Pulled, rebased, and pushed changes for batch {batch_end}")
            else:
                print(f"No changes for batch {batch_end}, skipping commit and push")

        except subprocess.CalledProcessError as e:
            print(f"Git operation failed for batch {batch_end}: {e}")
            sys.exit(1)

    print("All batches processed successfully!")


if __name__ == "__main__":
    main()
