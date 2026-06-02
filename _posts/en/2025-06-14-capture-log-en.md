---
audio: false
generated: true
lang: en
layout: post
title: Capture Log
translated: false
type: note
---

In GNOME Terminal, the "Select All" option (usually accessed via `Edit > Select All` or `Ctrl+Shift+A`) only selects the text currently visible on the screen. To select **all text** in the terminal, including content in the scrollback buffer (beyond what's visible), you can use one of these methods:

### Method 1: Increase Scrollback Buffer and Manual Selection
1. **Ensure Scrollback is Enabled**:
   - Go to `Edit > Profile Preferences` in GNOME Terminal.
   - Under the "Scrolling" tab, ensure the scrollback buffer is set to a high number or "Unlimited" to capture all terminal output.
2. **Manual Selection**:
   - Scroll to the top of the terminal output using the mouse or `Shift+Page Up`.
   - Click and drag from the top to the bottom to select all text manually.
   - Alternatively, use `Shift+Home` to jump to the start of the buffer, then click and drag or use `Shift+End` to select to the end.

### Method 2: Use a Command to Capture All Output
If you want to capture all terminal output (including scrollback), you can redirect or copy the output using a command:
1. **Redirect Output to a File**:
   - If you know the command generating the output, rerun it with redirection:
     ```bash
     command > output.txt
     ```
     This saves all output to `output.txt`, which you can then open and select.
2. **Use `script` to Record Terminal Session**:
   - Start a recording session with:
     ```bash
     script output.log
     ```
   - Run your commands, then type `exit` to stop recording.
   - Open `output.log` to select all text.

### Method 3: Copy Scrollback Buffer via Terminal Command
1. Use the `tee` command or similar to capture output while running commands:
   ```bash
   command | tee output.txt
   ```
   This displays the output in the terminal and saves it to `output.txt`.
2. Open the file in a text editor to select all text easily.

### Method 4: Use `tmux` or `screen` for Advanced Control
If you frequently need to capture all terminal output:
1. **Install and Use `tmux`**:
   - Install `tmux`:
     ```bash
     sudo apt install tmux  # On Debian/Ubuntu
     ```
   - Start a `tmux` session:
     ```bash
     tmux
     ```
   - Run your commands.
   - Enter scroll mode with `Ctrl+b, [`, then press `Ctrl+a, Ctrl+e` to select all text in the buffer.
   - Copy with `Ctrl+b, ]` (after configuring `tmux` to enable copying).
2. **Save tmux Buffer**:
   - Save the entire buffer to a file:
     ```bash
     tmux capture-pane -S - -E - -b 0 -J > output.txt
     ```
   - Open `output.txt` to select all text.

### Limitations
- GNOME Terminal itself doesn’t have a built-in "select all scrollback" feature via the GUI.
- The scrollback buffer size may limit how much text is available if not set to unlimited.
- For very large outputs, using `tmux`, `screen`, or redirecting to a file is more reliable.

If you need further clarification or help with a specific command, let me know!
