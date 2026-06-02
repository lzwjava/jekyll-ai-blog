---
audio: false
generated: true
lang: en
layout: post
title: VSCode Wrap Lines
translated: false
type: note
---

To make VSCode wrap lines so you can easily see when lines are too long, you can configure the word wrap settings to wrap lines at a specific column. Here's how to do it:

### Steps to Enable Line Wrapping at a Specific Column

1. **Open Settings in VSCode**:
   - Press `Ctrl + ,` (or `Cmd + ,` on macOS) to open the Settings panel.
   - Alternatively, go to `File` > `Preferences` > `Settings`.

2. **Search for Word Wrap Settings**:
   - In the Settings panel, type "word wrap" in the search bar.
   - Locate the setting labeled **Editor: Word Wrap**.

3. **Set Word Wrap to "wordWrapColumn"**:
   - Change the **Editor: Word Wrap** setting to `"wordWrapColumn"`.
   - This option allows lines to wrap at a specific column.

4. **Specify the Column Limit**:
   - Look for the **Editor: Word Wrap Column** setting (it appears when "wordWrapColumn" is selected).
   - Set this to your preferred column limit, for example, `80`.
   - This means any line longer than 80 characters will be wrapped.

5. **(Optional) Add a Vertical Ruler for Visual Guidance**:
   - Search for "rulers" in the Settings search bar.
   - Find the **Editor: Rulers** setting.
   - Add your preferred column to the list, for example, `[80]`.
   - This will display a vertical line at column 80, providing a visual cue for the line length limit.

6. **(Optional) Adjust Wrapping Indent for Clarity**:
   - Search for "wrapping indent" in the Settings search bar.
   - Find the **Editor: Wrapping Indent** setting.
   - Set it to `"indent"` (or another option like `"deepIndent"`) to indent wrapped lines.
   - This helps distinguish wrapped lines from new lines, making it clearer that they are continuations.

### How It Works

- After configuring these settings, any line exceeding the specified column (e.g., 80 characters) will be wrapped and displayed on multiple visual lines.
- The wrapped lines are indented (if you adjusted the wrapping indent), making it easy to see that they are part of the same logical line.
- The vertical ruler (if enabled) shows a line at the specified column, reinforcing the visual limit.
- By noticing that a line is wrapped, you can quickly tell that it is too long, as it exceeds your column limit.

### Example

Suppose you have a line of code that is 100 characters long:

- With **Editor: Word Wrap** set to `"wordWrapColumn"` and **Editor: Word Wrap Column** set to `80`, the line will wrap at the 80th character.
- The wrapped portion will be indented, and the ruler (if enabled) will show where the 80th column is.
- This setup eliminates the need for horizontal scrolling and makes it clear that the line exceeds 80 characters.

### Additional Notes

- The wrapping is purely visual; the actual code remains one logical line, so it won't affect how your code runs or is formatted.
- If you want to enforce strict line length limits, consider using linters or formatters alongside these visual settings.
- For quick checks, you can also refer to the status bar in VSCode, which shows the current line and column number, but the wrapping and ruler should suffice for visual identification.

By following these steps, you can easily see when lines are too long in VSCode without horizontal scrolling, as they will be wrapped at your specified column limit.
