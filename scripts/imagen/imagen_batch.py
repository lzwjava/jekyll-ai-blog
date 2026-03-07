#!/usr/bin/env python3
"""
Batch Image Generator for Latest Blog Posts
Generates OG images for the latest 10 blog posts.
"""

import sys
import argparse
from pathlib import Path
from imagen_prompt import imagen_prompt
from imagen_og import generate_image_with_imagen


def process_file_custom(file_path, output_path, debug=False):
    """Process a single Jekyll post file with custom output path."""
    print(f"\n=== Processing file: {file_path} ===")

    # Check if output file already exists
    if Path(output_path).exists():
        print(f"⏭️  Skipping - image already exists: {output_path}")
        return "skipped"

    try:
        print("Generating image prompt from content...")
        # Get image prompt using the imported function
        prompt = imagen_prompt(file_path, debug=debug)

        if prompt is None:
            print("❌ Failed to generate image prompt")
            return None

        print(f"✓ Generated prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")

        print(f"Creating output directory: {Path(output_path).parent}")
        # Ensure output directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        # Generate image
        success = generate_image_with_imagen(prompt, output_path)

        if success:
            print(f"✓ Successfully processed {file_path}")
        else:
            print(f"❌ Failed to process {file_path}")

        return prompt if success else None

    except Exception as e:
        print(f"Error processing {file_path}: {e}", file=sys.stderr)
        return None


def imagen_og_files_custom(files, output_dir="assets/images/og", debug=False):
    """Process multiple files to generate OG images with custom output directory.

    Args:
        files: List of file paths to process
        output_dir: Directory to save generated images
        debug: Enable debug output

    Returns:
        Number of successfully processed files
    """
    print(f"\nProcessing {len(files)} files...")
    print(f"Output directory: {output_dir}")
    success_count = 0
    skipped_count = 0

    for i, file_path in enumerate(files, 1):
        print(f"\n[{i}/{len(files)}] Processing: {file_path}")
        output_path = f"{output_dir}/og{i}.jpg"
        result = process_file_custom(file_path, output_path, debug)
        if result == "skipped":
            skipped_count += 1
        elif result:
            success_count += 1

    print("\n=== Summary ===")
    print(f"Processed: {len(files)} files")
    print(f"Successful: {success_count} files")
    print(f"Skipped: {skipped_count} files")
    print(f"Failed: {len(files) - success_count - skipped_count} files")

    return success_count


def main():
    parser = argparse.ArgumentParser(
        description="Generate OG images for latest blog posts"
    )
    parser.add_argument(
        "-n",
        "--number",
        type=int,
        default=10,
        help="Number of latest files to process (default: 10)",
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug output")

    args = parser.parse_args()

    print("Batch OG Image Generator")
    print("========================")

    # Find latest n markdown files in original directory
    print(f"Finding latest {args.number} markdown files...")
    original_dir = Path("original")

    if not original_dir.exists():
        print("❌ Original directory not found!")
        sys.exit(1)

    # Get all markdown files and sort by filename (date) descending
    md_files = sorted(original_dir.glob("*.md"), key=lambda x: x.name, reverse=True)

    if not md_files:
        print("❌ No markdown files found in original directory!")
        sys.exit(1)

    # Take latest n files
    latest_files = md_files[: args.number]

    print(f"Found {len(md_files)} total files, processing latest {len(latest_files)}")
    for i, file_path in enumerate(latest_files, 1):
        print(f"  {i:2d}. {file_path.name}")

    # Generate images
    success_count = imagen_og_files_custom(
        files=[str(f) for f in latest_files],
        output_dir="assets/images/og",
        debug=args.debug,
    )

    if success_count == len(latest_files):
        print(f"\n✅ All {success_count} images generated successfully!")
    else:
        print(f"\n⚠️ {success_count}/{len(latest_files)} images generated successfully")

    return success_count


if __name__ == "__main__":
    main()
