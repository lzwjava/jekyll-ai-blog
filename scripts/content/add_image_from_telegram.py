import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def get_next_number(target_dir, dir_name, image_ext):
    """Get the next available number for the image filename."""
    if not target_dir.exists():
        return 1

    existing_files = list(target_dir.glob(f"{dir_name}*.{image_ext}"))
    if not existing_files:
        return 1

    # Extract numbers from existing files
    numbers = []
    for file in existing_files:
        stem = file.stem
        if stem.startswith(dir_name):
            try:
                # Extract number after dir_name
                number_part = stem[len(dir_name) :]
                if number_part.isdigit():
                    numbers.append(int(number_part))
                elif number_part == "":
                    numbers.append(1)  # Handle case where file is just dir_name
            except ValueError:
                continue

    return max(numbers) + 1 if numbers else 1


def copy_to_clipboard(text):
    """Copy text to clipboard using pbcopy (macOS)."""
    try:
        subprocess.run(["pbcopy"], input=text.encode(), check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def get_source_options():
    """Get the list of available source options."""
    return [
        "self-screenshot",
        "self-captured",
        "walmart",
        "pinduoduo",
        "amazon",
        "chatgpt",
    ]


def get_source_mapping():
    """Get the mapping from simplified names to full names."""
    return {
        "self-screenshot": "Self-screenshot",
        "self-captured": "Self-captured",
        "walmart": "walmart.com",
        "pinduoduo": "pinduoduo.com",
        "amazon": "amazon.com",
        "chatgpt": "chatgpt.com",
    }


def parse_arguments():
    """Parse command line arguments."""
    source_options = get_source_options()

    parser = argparse.ArgumentParser(
        description="Copy images to assets/images directory with organized naming"
    )
    parser.add_argument("image_path", help="Path to the source image file")
    parser.add_argument(
        "dir_name",
        help="Directory name under assets/images/ (will be created if it doesn't exist)",
    )
    parser.add_argument(
        "source",
        choices=source_options,
        help=f"Source attribution for the image. Options: {', '.join(source_options)}",
    )

    return parser.parse_args()


def validate_source_image(image_path):
    """Validate that the source image exists and is a valid file."""
    source_path = Path(image_path)

    if not source_path.exists():
        print(f"Error: Source image '{image_path}' does not exist.")
        sys.exit(1)

    if not source_path.is_file():
        print(f"Error: '{image_path}' is not a file.")
        sys.exit(1)

    # Get image extension
    image_ext = source_path.suffix.lstrip(".")
    if not image_ext:
        print("Error: Source file has no extension.")
        sys.exit(1)

    return source_path, image_ext


def setup_target_directory(dir_name):
    """Set up and create the target directory for the image."""
    script_dir = Path(__file__).parent
    assets_dir = script_dir.parent.parent / "assets" / "images" / dir_name

    # Create target directory if it doesn't exist
    assets_dir.mkdir(parents=True, exist_ok=True)

    return assets_dir


def copy_image_file(source_path, target_path):
    """Copy the image file to the target location."""
    try:
        shutil.copy2(source_path, target_path)
        print("✅ Image copied successfully!")
        print(f"   Source: {source_path}")
        print(f"   Target: {target_path}")
        return True
    except Exception as e:
        print(f"❌ Error copying file: {e}")
        return False


def generate_markdown_content(relative_path, source):
    """Generate the formatted markdown content."""
    return f"""{{: .centered }}
![]({relative_path}){{: .responsive }}
*Source: {source}*{{: .caption }}"""


def handle_clipboard_and_output(markdown_content, relative_path):
    """Handle clipboard copying and display output information."""
    if copy_to_clipboard(markdown_content):
        print("📋 Markdown content copied to clipboard!")
        print(f"   Image path: {relative_path}")
    else:
        print(f"⚠️  Could not copy to clipboard. Path: {relative_path}")

    print("\n📝 Next steps:")
    print("   1. The formatted markdown is now in your clipboard")
    print("   2. Paste it directly into your markdown file")
    print("   3. Update the caption text if needed")
    print("\n📄 Clipboard content:")
    print(markdown_content)


def main():
    """Main function to orchestrate the image copying process."""
    # Parse command line arguments
    args = parse_arguments()

    # Get source mapping
    source_mapping = get_source_mapping()
    full_source_name = source_mapping.get(args.source, args.source)

    # Validate source image
    source_path, image_ext = validate_source_image(args.image_path)

    # Set up target directory
    assets_dir = setup_target_directory(args.dir_name)

    # Get next available number and create target filename
    next_number = get_next_number(assets_dir, args.dir_name, image_ext)
    target_filename = f"{args.dir_name}{next_number}.{image_ext}"
    target_path = assets_dir / target_filename

    # Copy the image file
    if not copy_image_file(source_path, target_path):
        sys.exit(1)

    # Generate markdown content and handle clipboard
    relative_path = f"assets/images/{args.dir_name}/{target_filename}"
    markdown_content = generate_markdown_content(relative_path, full_source_name)
    handle_clipboard_and_output(markdown_content, relative_path)


if __name__ == "__main__":
    main()
