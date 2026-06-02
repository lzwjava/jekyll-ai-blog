---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: PIL ImageGrab Screenshot Guide
translated: false
type: note
---

### Prerequisites

To use `ImageGrab` from the PIL (Pillow) library, ensure you have Pillow installed. On Windows, install it via pip:

```
pip install Pillow
```

No additional setup is typically needed for Windows, as `ImageGrab` uses native Windows APIs.

### Basic Usage

`ImageGrab.grab()` captures the entire screen (all monitors) as a PIL Image object. Here's a simple example to take a screenshot and save it as a PNG file:

```python
from PIL import ImageGrab

# Capture the entire screen
screenshot = ImageGrab.grab()

# Save the image to a file
screenshot.save("screenshot.png")
```

This will save a file named `screenshot.png` in your current working directory.

### Additional Options

- **Capture a specific region**: Specify a bounding box (left, top, right, bottom) as a tuple of pixel coordinates.

  ```python
  # Capture a 300x300 pixel area starting at (100, 100)
  region = (100, 100, 400, 400)  # Adjust coordinates as needed
  screenshot = ImageGrab.grab(bbox=region)
  screenshot.save("region_screenshot.png")
  ```

- **Include the mouse cursor** (if supported; check Pillow documentation for version details):

  ```python
  # Note: This may require include_layered_windows=True on some systems
  screenshot = ImageGrab.grab(include_layered_windows=True)
  ```

- **Show the image**: Use `screenshot.show()` to open it in your default image viewer (for testing).

### Notes

- Coordinates are in pixels, with (0, 0) at the top-left of the primary monitor.
- For multi-monitor setups, `grab()` captures all screens as one composite image.
- If you encounter issues (e.g., permission errors on newer Windows versions), ensure your script has screen capture permissions or try running it with administrator privileges.
- Full documentation: [Pillow ImageGrab docs](https://pillow.readthedocs.io/en/stable/reference/ImageGrab.html). For Windows-specific quirks, check GitHub issues if needed.
