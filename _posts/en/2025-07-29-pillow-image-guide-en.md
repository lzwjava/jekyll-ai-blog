---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: PIL Pillow Image Processing Guide
translated: false
type: note
---

### What is PIL/Pillow?
PIL originally stood for Python Imaging Library, but it's now maintained as the Pillow package (a modern fork). You import it as `PIL` in code, but you need to install Pillow via pip. It's used for opening, manipulating, and saving image files in Python. Supports formats like JPEG, PNG, GIF, BMP, and more.

### Installation
To use PIL, install Pillow:
```bash
pip install pillow
```

### Basic Import and Usage
After installing, import it like this in your Python script:
```python
from PIL import Image
```
No need for `import PIL.Image`—this directly imports the Image module.

### Common Image Operations
Here's how to perform basic tasks. Assume you have an image file named `example.jpg` in your directory.

#### 1. Opening an Image
```python
image = Image.open('example.jpg')  # Opens the image file
image.show()  # Displays it (works on systems with an image viewer)
```

#### 2. Getting Image Info
```python
print(image.format)  # e.g., 'JPEG'
print(image.size)    # Tuple: (width, height)
print(image.mode)    # e.g., 'RGB' for color images
```

#### 3. Resizing an Image
```python
resized = image.resize((800, 600))  # Resize to 800x600 pixels
resized.save('resized_example.jpg')  # Save the resized image
```

#### 4. Converting Formats
```python
image.convert('L').save('grayscale_example.png')  # Convert to grayscale and save as PNG
```

#### 5. Rotating an Image
```python
rotated = image.rotate(90)  # Rotate 90 degrees clockwise
rotated.save('rotated_example.jpg')
```

#### 6. Cropping an Image
```python
left, top, right, bottom = 100, 100, 300, 300  # Define crop box (x1, y1, x2, y2)
cropped = image.crop((left, top, right, bottom))
cropped.save('cropped_example.jpg')
```

#### 7. Applying Filters (Requires Extra Imports)
For filters, import `ImageFilter`:
```python
from PIL import ImageFilter
blurred = image.filter(ImageFilter.BLUR)  # Apply blur filter
blurred.save('blurred_example.jpg')
```

### Advanced Example: Batch Processing Multiple Images
```python
import os
from PIL import Image

# Resize all JPEG images in a folder to 200x200
input_folder = 'images/'
output_folder = 'resized_images/'
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.endswith('.jpg'):
        image = Image.open(os.path.join(input_folder, filename))
        resized = image.resize((200, 200))
        resized.save(os.path.join(output_folder, filename))
```

### Tips and Notes
- **Error Handling**: Use try-except for invalid files, e.g., `try: image = Image.open('file.jpg')`.
- **Memory Efficiency**: For large images, use `image.close()` after operations to free memory.
- **Documentation**: Check Pillow's full docs at [pillow.readthedocs.io](https://pillow.readthedocs.io/en/stable/) for more functions like drawing, text addition, or EXIF data handling.
- **Dependencies**: Pillow might need system libraries (e.g., libjpeg) on some setups; see the installation guide if issues arise.

If you have a specific task or error, provide more details for tailored help!
