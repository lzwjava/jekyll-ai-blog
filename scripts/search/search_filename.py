import subprocess
import argparse
import sys
import os
import shutil


def check_ack():
    """Check if ack is installed."""
    if not shutil.which("ack"):
        print("Error: ack is not installed.")
        print("Please install it first:")
        print("  macOS: brew install ack")
        print("  Ubuntu/Debian: sudo apt-get install ack")
        print("  Windows: scoop install ack")
        sys.exit(1)


def search_filenames(query, ignore_case=False, delete=False):
    """Search markdown filenames using ack."""
    try:
        check_ack()

        cmd = [shutil.which("ack")]
        if ignore_case:
            cmd.append("-i")

        # Search only filenames, not file contents
        cmd.append("-g")

        # Only search markdown files
        cmd.append("--type-add=md=.md,.markdown")
        cmd.append("--md")

        # Add search pattern
        cmd.append(query)

        # Specify directories to search
        cmd.append("notes")

        # Execute search
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode not in [0, 1]:  # 1 means no matches found
            print("Error executing search command")
            print(result.stderr)
            return

        if not result.stdout.strip():
            print("No matching filenames found")
            return

        matches = [line.strip() for line in result.stdout.splitlines() if line.strip()]

        if delete:
            deleted_files = []
            missing_files = []

            for match in matches:
                path = (
                    match if os.path.isabs(match) else os.path.join(os.getcwd(), match)
                )

                if os.path.exists(path):
                    try:
                        os.remove(path)
                        deleted_files.append(match)
                    except OSError as exc:
                        print(f"Failed to delete {match}: {exc}")
                else:
                    missing_files.append(match)

            if deleted_files:
                print("Deleted files:")
                print("\n".join(deleted_files))

            if missing_files:
                print("Files not found (skipped):")
                print("\n".join(missing_files))
        else:
            print("\n".join(matches))

    except subprocess.CalledProcessError as e:
        print(f"Error executing search: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Search markdown filenames in the repository"
    )
    parser.add_argument("query", help="Search pattern to look for in filenames")
    parser.add_argument(
        "-i", "--ignore-case", action="store_true", help="Case insensitive search"
    )
    parser.add_argument(
        "--del",
        dest="delete",
        action="store_true",
        help="Delete all files that match the search results",
    )

    args = parser.parse_args()
    search_filenames(args.query, args.ignore_case, args.delete)
