---
audio: false
generated: true
lang: en
layout: post
title: Enable Soft Wrap in Zed
translated: false
type: note
---

Zed, like many modern text editors, uses the concept of "soft wrap" to wrap lines. This means that lines will appear wrapped in the editor, but no actual newline characters are inserted into your file.

Here's how to enable line wrapping in Zed:

1.  **Open Zed's Settings:**

      * Press `Command + Shift + P` (macOS) or `Ctrl + Shift + P` (Windows/Linux) to open the Command Palette.
      * Type "local" and select "zed: Open Local Settings". This will open your `settings.json` file.

2.  **Add the `soft_wrap` setting:**

      * In your `settings.json` file, add or modify the `"soft_wrap"` setting. You have a few options:

          * **`"editor_width"`:** This is the most common and generally recommended option. It will wrap lines to fit the current width of your editor window.
            ```json
            {
              "soft_wrap": "editor_width"
            }
            ```
          * **`"preferred_line_length"`:** This will wrap lines based on a specified `preferred_line_length` (e.g., 80 characters). You'll also need to define `preferred_line_length`.
            ```json
            {
              "soft_wrap": "preferred_line_length",
              "preferred_line_length": 80
            }
            ```
          * **`"bounded"`:** This option provides a more advanced wrapping behavior, though `editor_width` or `preferred_line_length` are usually sufficient for most users.
          * **`"none"`:** This disables line wrapping.

3.  **Save the file:**

      * Press `Command + S` (macOS) or `Ctrl + S` (Windows/Linux) to save the `settings.json` file.

Zed should now wrap lines according to your chosen setting.

**Important Notes:**

  * **Project-level settings:** You can also enable word wrap at the project level by creating a `.zed` folder in your project directory and placing a `settings.json` file inside it with the desired `soft_wrap` configuration. This will override your global settings for that specific project.
  * **Language-specific settings:** You can even configure `soft_wrap` for specific languages. For example, to set soft wrap for Markdown files:
    ```json
    {
      "languages": {
        "Markdown": {
          "soft_wrap": "editor_width"
        }
      }
    }
    ```
  * **"Rewrap" command:** If you're looking for a command to "hard wrap" text (insert actual newlines) rather than just visually wrapping, Zed also has a "Rewrap" command (often bound to `Alt-Q` or `Alt-W`). This is useful for formatting comments or long lines of prose.
