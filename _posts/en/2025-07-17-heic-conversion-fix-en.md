---
audio: false
generated: true
lang: en
layout: post
title: Fixing Pillow HEIC Support Error
translated: false
type: note
---

The error `cannot identify image file` indicates that Pillow is unable to read the HEIC files, likely due to one of the following reasons:
1. **Missing `libheif` library**: Pillow requires `libheif` to handle HEIC files, and it may not be installed or properly configured on your system.
2. **Corrupted or incompatible HEIC files**: The HEIC files may be corrupted or in a format Pillow cannot process.
3. **Pillow version issue**: Although Pillow 9.0.0+ supports HEIC, there could be a configuration issue or an outdated version.

Since you're on macOS (based on your previous output), I'll provide a fixed Python script that includes additional error handling and logging to diagnose the issue. I'll also guide you through installing `libheif` and verifying Pillow's HEIC support. If Pillow continues to fail, the script includes a fallback to use `ImageMagick` (if installed) for HEIC conversion.

### Steps to Fix the Issue

#### 1. Install `libheif`
Pillow relies on `libheif` for HEIC support. Install it using Homebrew:
```bash
brew install libheif
```
After installing, reinstall Pillow to ensure it links with `libheif`:
```bash
pip uninstall pillow
pip install pillow
```

#### 2. Verify Pillow HEIC Support
Check if Pillow can handle HEIC files:
```bash
python -c "from PIL import features; print(features.check_feature('heic'))"
```
- If it outputs `True`, Pillow has HEIC support.
- If it outputs `False` or an error, `libheif` is not properly configured, or Pillow was built without HEIC support.

#### 3. Check File Integrity
Ensure the HEIC files are not corrupted. Try opening one of the files (e.g., `IMG_5988.HEIC`) in a viewer like Preview on macOS. If it doesn't open, the files may be corrupted, and you'll need to re-export or obtain new copies.

#### 4. Updated Python Script
The updated script:
- Uses Pillow for HEIC conversion with improved error handling.
- Falls back to `ImageMagick` (if installed) when Pillow fails to read a HEIC file.
- Logs detailed errors to a file (`conversion_errors.log`) for debugging.
- Supports both `.heic` and `.heif` extensions.
- Compresses output JPGs to ~500KB.

```python
import os
import argparse
import subprocess
import logging
from PIL import Image
from datetime import datetime

# Set up logging
logging.basicConfig(
    filename="conversion_errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Convert HEIC images to JPG and compress to ~500KB.")
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
            ["magick", heic_path, "-quality", "85", jpg_path],
            check=True, capture_output=True, text=True
        )
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"ImageMagick failed for {heic_path}: {e.stderr}")
        return False
    except FileNotFoundError:
        logging.error("ImageMagick not installed. Install it with 'brew install imagemagick'.")
        return False

def convert_heic_to_jpg(heic_path, jpg_path, quality=85):
    """Convert HEIC to JPG and compress to approximate target size."""
    try:
        # Try Pillow first
        image = Image.open(heic_path)
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Save as JPG with initial quality
        image.save(jpg_path, "JPEG", quality=quality)

        # Adjust quality to approach target size
        current_size = get_file_size(jpg_path)
        low, high = 10, 100
        while low <= high and abs(current_size - target_size_kb) > 10:
            quality = (low + high) // 2
            image.save(jpg_path, "JPEG", quality=quality)
            current_size = get_file_size(jpg_path)
            if current_size > target_size_kb:
                high = quality - 1
            else:
                low = quality + 1
        return True
    except Exception as e:
        logging.error(f"Pillow failed for {heic_path}: {e}")
        # Fallback to ImageMagick
        return convert_with_imagemagick(heic_path, jpg_path)

# Process all HEIC files in the input directory
for filename in os.listdir(input_dir):
    if filename.lower().endswith((".heic", ".heif")):
        heic_path = os.path.join(input_dir, filename)
        jpg_filename = os.path.splitext(filename)[0] + ".jpg"
        jpg_path = os.path.join(output_dir, jpg_filename)

        try:
            if convert_heic_to_jpg(heic_path, jpg_path):
                print(f"Converted {filename} to {jpg_filename}, size: {get_file_size(jpg_path):.2f} KB")
            else:
                print(f"Error processing {filename}: Conversion failed (check conversion_errors.log)")
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            logging.error(f"General error for {heic_path}: {e}")

print("Batch conversion complete! Check conversion_errors.log for any issues.")
```

### How to Use
1. **Save the script**:
   Save the code as `photo_compress.py` in your `scripts/media/` directory.

2. **Install dependencies**:
   - Ensure Pillow is installed:
     ```bash
     pip install --upgrade pillow
     ```
   - Install `libheif`:
     ```bash
     brew install libheif
     ```
   - Optionally, install ImageMagick for fallback:
     ```bash
     brew install imagemagick
     ```

3. **Run the script**:
   ```bash
   python scripts/media/photo_compress.py ./assets/images/yuebei
   ```
   - This processes all `.heic` and `.heif` files in `assets/images/yuebei`.
   - Output JPGs are saved in `assets/images/yuebei_compressed`.
   - Errors are logged to `conversion_errors.log` in the current directory.

4. **Check the log**:
   If any files fail to convert, check `conversion_errors.log` for detailed error messages.

### Additional Troubleshooting
- **If Pillow still fails**:
  - Verify `libheif` is correctly installed and linked:
    ```bash
    pkg-config --modversion libheif
    ```
    If this fails, reinstall `libheif` and Pillow.
  - Test a single file manually:
    ```python
    from PIL import Image
    img = Image.open("./assets/images/yuebei/IMG_5988.HEIC")
    print("Image opened successfully")
    ```
    If this fails, the file may be corrupted or in an unsupported HEIC variant.

- **Corrupted files**:
  - Try converting one file with ImageMagick manually:
    ```bash
    magick ./assets/images/yuebei/IMG_5988.HEIC test.jpg
    ```
    If this fails, the file is likely corrupted.

- **ImageMagick fallback**:
  - If Pillow consistently fails, the script will attempt to use ImageMagick (if installed).
  - Install `jpegoptim` for better compression control:
    ```bash
    brew install jpegoptim
    ```
    Then, after running the script, compress the output:
    ```bash
    for i in ./assets/images/yuebei_compressed/*.jpg; do jpegoptim --size=500k "$i"; done
    ```

### References
- [Pillow Documentation](https://pillow.readthedocs.io/en/stable/)
- [ImageMagick](https://imagemagick.org/)
- [libheif](https://github.com/strukturag/libheif)
- [jpegoptim](https://github.com/tjko/jpegoptim)

If you still encounter issues, share the contents of `conversion_errors.log` or any new error messages, and I can provide further assistance!
