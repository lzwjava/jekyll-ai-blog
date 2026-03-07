import os
import argparse
import subprocess
import logging

# Set up logging
logging.basicConfig(
    filename="conversion_errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Parse command-line arguments
parser = argparse.ArgumentParser(
    description="Convert HEIC images to JPG and compress to ~500KB."
)
parser.add_argument("input_dir", help="Directory containing HEIC files")
args = parser.parse_args()

# Define input and output directories
input_dir = args.input_dir.rstrip(os.sep)
output_dir = input_dir + "_compressed"
target_size_kb = 500  # Target file size in KB

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


def get_file_size(file_path):
    """Return file size in KB."""
    return os.path.getsize(file_path) / 1024


def convert_with_imagemagick(heic_path, jpg_path):
    """Fallback to ImageMagick for HEIC to JPG conversion."""
    try:
        subprocess.run(
            ["magick", heic_path, "-quality", "30", jpg_path],
            check=True,
            capture_output=True,
            text=True,
        )
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"ImageMagick failed for {heic_path}: {e.stderr}")
        return False
    except FileNotFoundError:
        logging.error(
            "ImageMagick not installed. Install it with 'brew install imagemagick'."
        )
        return False


def convert_heic_to_jpg(heic_path, jpg_path, quality=80):
    """Convert HEIC to JPG and compress to approximate target size."""
    return convert_with_imagemagick(heic_path, jpg_path)


# Process all HEIC files in the input directory
for filename in os.listdir(input_dir):
    if filename.lower().endswith((".heic", ".heif")):
        heic_path = os.path.join(input_dir, filename)
        jpg_filename = os.path.splitext(filename)[0] + ".jpg"
        jpg_path = os.path.join(output_dir, jpg_filename)

        try:
            if convert_heic_to_jpg(heic_path, jpg_path):
                print(
                    f"Converted {filename} to {jpg_filename}, size: {get_file_size(jpg_path):.2f} KB"
                )
            else:
                print(
                    f"Error processing {filename}: Conversion failed (check conversion_errors.log)"
                )
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            logging.error(f"General error for {heic_path}: {e}")

print("Batch conversion complete! Check conversion_errors.log for any issues.")
