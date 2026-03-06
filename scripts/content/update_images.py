import os
import re
import sys
import argparse


def update_post_images(post_path):
    """Update post images by removing existing ones and adding all images from the directory in alphabetical order."""

    # Read the post file
    try:
        with open(post_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file {post_path}: {e}")
        return False

    # Find existing image references to detect the directory
    image_pattern = r"!\[.*?\]\(/assets/images/([^/]+)/[^)]+\)"
    matches = re.findall(image_pattern, content)

    if not matches:
        print("No image directory found in the post")
        return False

    # Use the first image directory found
    image_dir = matches[0]
    assets_path = os.path.join(
        os.path.dirname(os.path.dirname(post_path)), "assets", "images", image_dir
    )

    if not os.path.exists(assets_path):
        print(f"Image directory not found: {assets_path}")
        return False

    # Get all image files in the directory
    image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"}
    image_files = []

    for file in os.listdir(assets_path):
        if any(file.lower().endswith(ext) for ext in image_extensions):
            image_files.append(file)

    # Sort alphabetically
    image_files.sort()

    if not image_files:
        print(f"No image files found in {assets_path}")
        return False

    # Remove all existing image references
    content = re.sub(r"!\[.*?\]\(/assets/images/[^)]+\)\s*\n?", "", content)

    # Add new images at the end
    new_images = []
    for image_file in image_files:
        new_images.append(f"![img](/assets/images/{image_dir}/{image_file})")

    # Ensure content ends with newline before adding images
    if not content.endswith("\n"):
        content += "\n"

    # Add images with proper spacing
    content += "\n" + "\n\n".join(new_images) + "\n"

    # Write back to file
    try:
        with open(post_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Successfully updated images in {post_path}")
        print(f"Added {len(image_files)} images from /assets/images/{image_dir}/")
        return True
    except Exception as e:
        print(f"Error writing file {post_path}: {e}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Update post images by removing existing ones and adding all images from the directory in alphabetical order."
    )
    parser.add_argument("post_path", help="Path to the post file")

    args = parser.parse_args()
    update_post_images(args.post_path)
