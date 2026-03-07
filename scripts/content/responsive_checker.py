import os
import re
from PIL import Image


def check_images_in_markdown(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

        # Extract image paths from markdown
        image_pattern = r"!\[.*?\]\((.*?)\)"
        images = re.findall(image_pattern, content)

        for img_path in images:
            # Construct full path to image
            base_path = os.path.dirname(file_path)
            full_img_path = os.path.join(base_path, img_path)

            try:
                # Open and read image dimensions
                with Image.open(full_img_path) as img:
                    width, height = img.size
                    if width < height:
                        print(
                            f"Image {img_path} in {file_path} should be responsive. Dimensions: {width}x{height}"
                        )
                        # Here you can add logic to modify the markdown or store the info
            except Exception as e:
                print(f"Error reading image {img_path}: {e}")


def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                check_images_in_markdown(file_path)


if __name__ == "__main__":
    directory = (
        "/Users/lzwjava/projects/lzwjava.github.io/_posts"  # Adjust this path as needed
    )
    process_directory(directory)
