import os
import argparse
from type_flag_util import update_front_matter


def main():
    parser = argparse.ArgumentParser(
        description="Update front matter in blog notes files"
    )
    parser.add_argument("-n", type=int, help="Maximum number of files to update")
    parser.add_argument(
        "--type",
        default="note",
        help="Type value to set in front matter (default: note)",
    )
    args = parser.parse_args()

    notes_dir = "notes"
    count = 0

    # Process files in notes directory
    if not args.n or count < args.n:
        for filename in os.listdir(notes_dir):
            if filename.endswith(".md") and (not args.n or count < args.n):
                file_path = os.path.join(notes_dir, filename)
                update_front_matter(file_path, args.type)
                count += 1


if __name__ == "__main__":
    main()
