---
audio: false
generated: true
lang: en
layout: post
title: WebP to JPG Conversion in Ubuntu
translated: false
type: note
---

You have several excellent options for converting WebP to JPG in Ubuntu, both from the command line and with GUI tools.

## Command Line Tools

These are generally the most flexible and efficient for single files or batch conversions.

### 1\. ImageMagick

ImageMagick is a powerful suite of command-line tools for image manipulation, and it's widely available.

* **Installation:**

    ```bash
    sudo apt update
    sudo apt install imagemagick
    ```

* **Convert a single file:**

    ```bash
    convert input.webp output.jpg
    ```

    Or, using `magick` for ImageMagick v7+:

    ```bash
    magick input.webp output.jpg
    ```

* **Convert multiple files (batch conversion) in the current directory:**

    ```bash
    mogrify -format JPEG *.webp
    ```

    This will convert all `.webp` files in the current directory to `.jpeg` (or `.jpg`) with the same filename. If you want the converted files in a separate directory:

    ```bash
    mkdir output_jpgs # Create a directory for output
    mogrify -format JPEG -path output_jpgs *.webp
    ```

### 2\. `dwebp` (from `libwebp` package)

`dwebp` is a dedicated tool for decoding WebP images.

* **Installation:**

    ```bash
    sudo apt update
    sudo apt install webp
    ```

* **Convert a single file:**

    ```bash
    dwebp input.webp -o output.jpg
    ```

    While you specify `.jpg` as the output, `dwebp` often outputs to PPM format and requires another tool like ImageMagick to convert to a proper JPEG. However, some sources suggest directly using `.jpg` as the output works for simple cases. If you encounter issues, convert to PNG first, then to JPG:

    ```bash
    dwebp input.webp -o output.png
    convert output.png output.jpg
    ```

### 3\. `ffmpeg`

`ffmpeg` is primarily for video and audio, but it's also very capable with image formats.

* **Installation:**

    ```bash
    sudo apt update
    sudo apt install ffmpeg
    ```

* **Convert a single file:**

    ```bash
    ffmpeg -i input.webp output.jpg
    ```

* **Convert multiple files (batch conversion):**

    ```bash
    for file in *.webp; do ffmpeg -i "$file" "${file%.*}.jpg"; done
    ```

    This command iterates through all `.webp` files in the current directory and converts them to `.jpg` with the same name (e.g., `image.webp` becomes `image.jpg`).

## GUI Tools

If you prefer a graphical interface, here are a couple of options:

### 1\. GIMP (GNU Image Manipulation Program)

GIMP is a powerful open-source image editor that supports WebP.

* **Installation:**

    ```bash
    sudo apt update
    sudo apt install gimp
    ```

* **How to convert:**
    1. Open the WebP image in GIMP (File \> Open).
    2. Go to File \> Export As.
    3. In the "Export Image" dialog, choose "JPEG image" from the "Select File Type (By Extension)" dropdown.
    4. Click "Export" and adjust quality settings if desired.

### 2\. XnView MP / XnConvert

These are cross-platform image viewers and batch converters with comprehensive format support, including WebP.

* **Installation:**
    You might need to download the `.deb` package from their official website and install it using `sudo dpkg -i <package_name.deb>` or through a graphical package installer.
* **How to convert (generally):**
    1. Open XnView MP or XnConvert.
    2. Add the WebP images you want to convert.
    3. Choose JPG as the output format.
    4. Adjust any settings (quality, resize, etc.).
    5. Start the conversion.

### 3\. Converseen

Converseen is a free batch image converter that supports WebP.

* **Installation:** You can usually find it in the Ubuntu Software Center or install it via apt if available in your repositories.
* **How to convert:** It has a straightforward GUI for adding images, selecting output format, and converting.

## Which method to choose?

* **For quick, single-file conversions or scripting automated tasks:** Use `ffmpeg` or `ImageMagick` from the command line. They are very efficient.
* **For occasional conversions where you want a visual interface and more control over image editing:** GIMP is a great choice.
* **For batch converting many images with a GUI and various options:** XnView MP/XnConvert or Converseen are excellent.

No matter which method you choose, make sure to install the necessary packages first.
