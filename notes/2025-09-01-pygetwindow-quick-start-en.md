---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: PyGetWindow Quick Start Guide
translated: false
type: note
---

### Installation
PyGetWindow is a Python library for manipulating and querying windows on multiple platforms (Windows, macOS, and Linux). Install it via pip:

```bash
pip install pygetwindow
```

### Importing the Module
Start by importing the module in your Python script:

```python
import pygetwindow as gw
```

### Getting Window Objects
PyGetWindow represents windows as `Window` objects. You can retrieve windows by title, process, or other attributes.

- **Get all window objects**:
  Use `gw.getAllWindows()` to return a list of all open windows.

- **Get windows by title**:
  Use `gw.getWindowsWithTitle(title)` or `gw.getFirstWindowWithTitle(title)` for partial or exact matches.

- **Get active window**:
  Use `gw.getActiveWindow()` to get the currently focused window.

Example:
```python
windows = gw.getAllWindows()
active = gw.getActiveWindow()
notepad = gw.getWindowsWithTitle('Notepad')  # List of windows with 'Notepad' in title
```

### Common Methods on Window Objects
Once you have a `Window` object, you can access properties and methods like:

- **Properties**: `title`, `left`, `top`, `width`, `height`, `isMinimized`, `isMaximized`, `isActive`.
- **Methods**:
  - `activate()`: Bring the window to the front and make it active.
  - `maximize()` / `minimize()` / `restore()` / `close()`: Control window state.
  - `resize() / move()`: Adjust size and position.

Example:
```python
if notepad:
    win = notepad[0]
    print(win.title)  # Output: e.g., 'Untitled - Notepad'
    win.activate()
    win.maximize()
    win.move(100, 100)  # Move to position (100, 100)
    win.resize(800, 600)  # Resize to 800x600
```

### Handling Multiple Platforms
- On Windows and macOS, it uses native APIs.
- On Linux, it relies on X11 or Wayland support; ensure your system has it installed (e.g., `x11-utils` on Ubuntu).
- If a method isn't supported on your OS, it may raise a `NotImplementedError`.

### Examples
Here are a few practical code snippets:

1. **Print all window titles**:
   ```python
   for win in gw.getAllWindows():
       print(win.title)
   ```

2. **Close a specific window**:
   ```python
   firefox_wins = gw.getWindowsWithTitle('Mozilla Firefox')
   if firefox_wins:
       firefox_wins[0].close()
   ```

3. **Move and resize multiple windows**:
   ```python
   windows = gw.getAllWindows()
   for i, win in enumerate(windows[:3]):  # First 3 windows
       win.move(50 * i, 50 * i)
       win.resize(400, 400)
   ```

For advanced usage, refer to the [official documentation](https://pygetwindow.readthedocs.io/). If you encounter platform-specific issues, check system permissions or dependencies like `xdotool` on Linux.
