---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: Windows Toast Notifications with Python
translated: false
type: note
---

### What is win10toast?
win10toast is a lightweight Python library that enables you to send toast notifications (pop-up alerts) on Windows 10 from your Python scripts. It's useful for user notifications in desktop applications or scripts, similar to native Windows toasts.

### Prerequisites
- Python 3.x installed.
- Windows 10 (it relies on Windows-specific APIs).
- No additional dependencies beyond Python.

### Installation
Install the library via pip (the Python package installer):

```
pip install win10toast
```

If you're using a virtual environment, activate it first.

### Basic Usage
1. Import the module:
   ```python
   from win10toast import ToastNotifier
   ```

2. Create a `ToastNotifier` instance and call its `show_toast` method to display a notification:
   ```python
   toaster = ToastNotifier()
   toaster.show_toast("Title", "Message", icon_path=None, duration=5)
   ```
   - **Title**: A string for the notification headline.
   - **Message**: A string for the notification body.
   - **icon_path**: Optional path to a .ico or .png file for the notification icon (e.g., `"path/to/icon.ico"`). Omit for no icon.
   - **duration**: Time in seconds for the toast to appear (default is 5; Windows may override this).

The notification will appear in the Action Center and as a pop-up.

### Advanced Usage
- **Customizing Icon**: Use an image file (128x128 pixels recommended for best quality).
- **Handling Click Events**: Pass a callback function (limited support; mainly for on-click behavior is basic).
- **Multiple Notifications**: Instantiate `ToastNotifier` once and reuse it to send multiple toasts.
- **Error Handling**: Wrap in try-except to handle potential Windows API issues, e.g., if notifications are disabled.

Example with icon and error handling:
```python
from win10toast import ToastNotifier
import os

try:
    toaster = ToastNotifier()
    icon = "C:\\path\\to\\icon.ico"  # Replace with actual path
    toaster.show_toast("Alert!", "Your script has finished.", icon_path=icon, duration=10)
except Exception as e:
    print(f"Notification failed: {e}")
```

### Limitations and Tips
- Notifications require Windows 10's Action Center to be enabled (Settings > System > Notifications & actions).
- For more complex features (e.g., actions or images), consider alternatives like plyer or winrt (part of modern Windows SDK).
- If notifications don't appear, check Windows focus assist settings or try running the script as an administrator.

For full documentation, check the [win10toast GitHub repository](https://github.com/Charnelx/win10toast). If you run into issues, provide error details for tailored help.
