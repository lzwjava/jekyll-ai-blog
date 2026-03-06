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


def process_avatar(input_path, output_dir, top_percent=0):
    cropped = crop_center(input_path, top_percent)
    os.makedirs(output_dir, exist_ok=True)
    out1 = os.path.join(output_dir, "avatar.jpg")
    out2 = os.path.join(output_dir, "avatar_dark.jpg")
    cropped.save(out1)
    cropped.save(out2)
    print(f"Saved: {out1}, {out2}")


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python avatar.py <input_jpg_path> [top_percent]")
        sys.exit(1)

    input_path = sys.argv[1]
    top_percent = float(sys.argv[2]) if len(sys.argv) == 3 else 0
    output_dir = "assets/images/"
    process_avatar(input_path, output_dir, top_percent)
