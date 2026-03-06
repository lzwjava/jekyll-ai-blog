from PIL import Image
import os
import sys


def crop_center(image_path, top_percent=0):
    img = Image.open(image_path)
    w, h = img.size

    # Use full width as the size
    size = w

    # Calculate top position based on percentage
    top = int(h * top_percent / 100)

    # Crop square from top position
    left = 0
    right = w
    bottom = top + size

    # Ensure we don't go beyond image bounds
    if bottom > h:
        bottom = h
        top = h - size
        if top < 0:
            top = 0

    return img.crop((left, top, right, bottom))


def process_crop(input_path, top_percent=0):
    cropped = crop_center(input_path, top_percent)

    # Get directory and filename without extension
    dir_path = os.path.dirname(input_path)
    filename = os.path.splitext(os.path.basename(input_path))[0]

    # Create output path with _crop suffix
    output_path = os.path.join(dir_path, f"{filename}_crop.jpg")

    cropped.save(output_path)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python crop.py <input_jpg_path> [top_percent]")
        sys.exit(1)

    input_path = sys.argv[1]
    top_percent = float(sys.argv[2]) if len(sys.argv) == 3 else 0
    process_crop(input_path, top_percent)
