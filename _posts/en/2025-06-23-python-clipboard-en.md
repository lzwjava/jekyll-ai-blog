---
audio: false
generated: true
lang: en
layout: post
title: Python Clipboard Access on Ubuntu
translated: false
type: note
---

To read from the clipboard (pasteboard) in Ubuntu using Python, you can use libraries like `pyperclip` or interact with system clipboard utilities like `xclip` or `xsel`. Below are two common approaches:

### Approach 1: Using `pyperclip`
`pyperclip` is a cross-platform Python library for accessing the clipboard.

1. **Install pyperclip**:
   ```bash
   pip install pyperclip
   ```

2. **Python code to read from clipboard**:
   ```python
   import pyperclip

   # Read the contents of the clipboard
   clipboard_content = pyperclip.paste()
   print(clipboard_content)
   ```

3. **Notes**:
   - Ensure `xclip` or `xsel` is installed on Ubuntu, as `pyperclip` relies on them:
     ```bash
     sudo apt update
     sudo apt install xclip xsel
     ```
   - This method is simple and works across platforms.

### Approach 2: Using `xclip` Directly
If you prefer to interact with the system clipboard directly, you can use `xclip`.

1. **Install xclip**:
   ```bash
   sudo apt update
   sudo apt install xclip
   ```

2. **Python**

System: Python code to read from clipboard using `xclip`:
   ```python
   import subprocess

   # Read the contents of the clipboard
   process = subprocess.run(['xclip', '-selection', 'clipboard', '-o'], capture_output=True, text=True)
   clipboard_content = process.stdout
   print(clipboard_content)
   ```

3. **Notes**:
   - This approach directly calls the `xclip` command-line tool.
   - Use `-selection clipboard` for the modern clipboard (Ctrl+C/Ctrl+V) or `-selection primary` for the mouse-selection clipboard.
   - Ensure `xclip` is installed.

### Recommendations
- **Use `pyperclip`** for simplicity and portability unless you have specific reasons to use `xclip` or `xsel`.
- Both methods require `xclip` or `xsel` to be installed for clipboard access on Ubuntu.
- If the clipboard content is not text (e.g., an image), these methods may not work as expected, and you’d need a library like `pyclip` or additional handling for non-text data.

Tested on Ubuntu 22.04 with Python 3.10. If you encounter issues, ensure the required tools (`xclip` or `xsel`) are installed and the clipboard contains text data.
