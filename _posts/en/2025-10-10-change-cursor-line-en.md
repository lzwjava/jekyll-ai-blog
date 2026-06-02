---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Change VS Code Cursor to Line
translated: false
type: note
---

### Fixing the Block (Rectangle) Cursor in VS Code

Got it—sounds like your cursor has switched to a block/rectangle style (common in overwrite mode or default settings), but you want the thin vertical **line** style for easier editing. This is a quick settings tweak. Follow these steps exactly:

#### Via the Settings UI (Easiest)

1. Open VS Code.
2. Press `Ctrl + ,` (Windows/Linux) or `Cmd + ,` (macOS) to open Settings.
3. In the search box at the top, type: **cursor style**.
4. Look for **Editor: Cursor Style** (under Text Editor > Cursor).
5. Click the dropdown and select **Line** (it might currently say "Block").
6. The change happens instantly—try typing in a file to see the thin line cursor.

If it's still not updating, close and reopen VS Code, or restart it fully.

#### Via settings.json (For Precision)

1. Open the Command Palette: `Ctrl + Shift + P` (or `Cmd + Shift + P` on macOS).
2. Type and select: **Preferences: Open User Settings (JSON)**.
3. Add or update this line inside the `{}` (create it if empty):

   ```json:disable-run
   "editor.cursorStyle": "line"
   ```

4. Save the file (`Ctrl + S` or `Cmd + S`).

#### Extra Tips

- **Overwrite Mode?** If you're accidentally in "overwrite" (where it blocks characters), press the **Insert** key on your keyboard to toggle back to insert mode.
- **Blinking Issue?** If the line looks choppy, search for **cursor blinking** in settings and set it to **Blink** or **Smooth**.
- **Extensions Interfering?** Disable extensions like Vim temporarily (Extensions view > right-click > Disable) to test.

This should get you that clean line cursor right away. If it's still rectangle-shaped after this, share your OS or a screenshot for more targeted help!

[VS Code Cursor Documentation](https://code.visualstudio.com/docs/editor/codebasics#_cursor-style)

```
