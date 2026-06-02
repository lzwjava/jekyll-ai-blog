---
audio: false
generated: true
image: false
lang: en
layout: post
title: PIL vs PyAutoGUI Screenshot Comparison
translated: false
type: note
---

Both **PIL’s `ImageGrab`** and **PyAutoGUI’s screenshot tools** let you capture the screen, but they differ in usage, features, and cross-platform support.

---

## 1. PIL (Pillow) – `ImageGrab`

`ImageGrab` is part of **Pillow (the modern PIL fork)**. It allows you to capture the screen or part of it.

### How it works

* On **Windows and macOS**, it uses native APIs (GDI on Windows, Quartz on macOS) to capture pixels.
* On **Linux**, it’s not supported by default (needs extra libraries like `xwd`).

### Example usage

```python
from PIL import ImageGrab

# Capture full screen
screenshot = ImageGrab.grab()
screenshot.save("screenshot.png")

# Capture a region (left, top, right, bottom)
region = (100, 100, 500, 500)
cropped_screenshot = ImageGrab.grab(bbox=region)
cropped_screenshot.show()
```

### Pros

* Simple, part of Pillow (no extra dependency).
* Good when you’re already working with Pillow for image processing.

### Cons

* No Linux support by default.
* Less flexibility (no multi-monitor awareness).

---

## 2. PyAutoGUI – `screenshot()`

PyAutoGUI is more general-purpose for automation (mouse/keyboard + screen capture).

### How it works

* Wraps **Pillow internally**.
* Uses OS APIs (cross-platform: Windows, macOS, Linux).
* Can return a Pillow `Image` directly or save to file.

### Example usage

```python
import pyautogui

# Capture full screen
screenshot = pyautogui.screenshot()
screenshot.save("screenshot.png")

# Capture a region (left, top, width, height)
region_screenshot = pyautogui.screenshot(region=(100, 100, 400, 400))
region_screenshot.show()
```

### Pros

* Cross-platform (Windows, macOS, Linux).
* Easy to integrate with automation scripts (mouse/keyboard control).
* Can capture specific regions directly.

### Cons

* Slightly slower than `ImageGrab` since it abstracts more.
* Extra dependency (`pip install pyautogui`).

---

## Which should you use?

* **If you only need screenshots and you’re on Windows/macOS** → `ImageGrab` is lightweight and fast.
* **If you also need automation or Linux support** → `pyautogui` is better.

---

👉 Do you want me to also show you **how to benchmark** the performance difference between `ImageGrab` and `pyautogui.screenshot()` with Python code?
