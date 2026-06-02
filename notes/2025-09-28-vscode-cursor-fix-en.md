---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-sonnet-4
title: Fixing VSCode Cross Cursor Problems
translated: false
type: note
---

The mouse cursor changing to a cross/plus symbol (十字架) in VSCode usually indicates that VSCode is in a special mode or there's a configuration issue. Here are the most common causes and solutions:

## Common Causes:

1. **Column Selection Mode**: You might have accidentally activated column/block selection mode
   - Try pressing `Alt + Shift + I` or `Ctrl + Shift + Alt + Arrow keys` to exit this mode

2. **Extension Conflict**: Some extensions can change cursor behavior
   - Try disabling extensions temporarily: `Ctrl + Shift + P` → "Developer: Reload Window"
   - Or start VSCode in safe mode: `code --disable-extensions`

3. **Zoom/Selection Tools**: You might have activated a zoom or selection tool
   - Press `Escape` key several times
   - Try `Ctrl + Z` to undo recent actions

4. **Terminal Focus Issue**: If the terminal is focused, it can change cursor behavior
   - Click in the editor area to refocus
   - Try `Ctrl + 1` to focus on the editor

## Quick Fixes:

1. **Restart VSCode**: Simple but often effective
   - `Ctrl + Shift + P` → "Developer: Reload Window"

2. **Check Mouse Settings**:
   - Go to File → Preferences → Settings
   - Search for "cursor" and check cursor-related settings

3. **Reset Workspace**:
   - Close VSCode
   - Delete `.vscode` folder in your project (if present)
   - Reopen the project

4. **System-wide Issue Check**:
   - Test if the cursor issue appears in other applications
   - If yes, it might be a GNOME/system setting issue

Try pressing `Escape` a few times first, then restart VSCode. This usually resolves the cross cursor issue.
