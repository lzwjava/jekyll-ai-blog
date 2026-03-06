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


def search_code(query, ignore_case=False):
    """Search code files using ack."""
    try:
        check_ack()

        cmd = [shutil.which("ack")]
        if ignore_case:
            cmd.append("-i")

        # No context lines, only show matching lines

        # Search code files
        cmd.append(
            "--type-add=code=.py,.js,.ts,.rs,.c,.cpp,.cc,.h,.hpp,.java,.go,.rb,.php,.sh,.kt,.swift,.scala"
        )
        cmd.append("--code")

        # Enable color output
        cmd.append("--color")
        cmd.append("--color-match=red")

        # Add search pattern
        cmd.append(query)

        # Search all directories for code files
        cmd.append(".")

        # Execute search with environment variable to force color output
        env = os.environ.copy()
        env["CLICOLOR_FORCE"] = "1"
        result = subprocess.run(cmd, capture_output=True, text=True, env=env)

        if result.returncode not in [0, 1]:  # 1 means no matches found
            print("Error executing search command")
            print(result.stderr)
            return

        if result.stdout:
            # Process output to show file:line_range format
            lines = result.stdout.strip().split("\n")

            for line in lines:
                print()
                if line.startswith("--"):
                    print()  # Add blank line for separators
                    continue

                # Check if line has file:line_number: or file-line_number- format
                if ":" in line:
                    parts = line.split(":", 1)
                    if len(parts) >= 2:
                        file_part = parts[0]
                        content = parts[1]

                        # Extract line number from file-line_number format
                        if "-" in file_part and file_part.split("-")[-1].isdigit():
                            file_name = "-".join(file_part.split("-")[:-1])
                            line_num = file_part.split("-")[-1]
                            print(f"{file_name}:{line_num}:{content}")
                        else:
                            print(line)
                    else:
                        print(line)
                elif "-" in line and not line.startswith("-"):
                    # Handle context lines like file-line_number-content
                    parts = line.split("-")
                    if len(parts) >= 3 and parts[-2].isdigit():
                        file_name = "-".join(parts[:-2])
                        line_num = parts[-2]
                        content = parts[-1]
                        print(f"{file_name}:{line_num}:{content}")
                    else:
                        print(line)
                else:
                    print(line)

            print()  # Add newline after output
        else:
            print("No matches found")

    except subprocess.CalledProcessError as e:
        print(f"Error executing search: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search code files in the repository")
    parser.add_argument("query", help="Search pattern to look for")
    parser.add_argument(
        "-i", "--ignore-case", action="store_true", help="Case insensitive search"
    )

    args = parser.parse_args()
    search_code(args.query, args.ignore_case)
