---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Opening Sublime Text from CLI
translated: false
type: note
---

### Opening Sublime Text from the Command Line (CLI)

Sublime Text doesn't include a built-in `sublime` (or `subl`) command by default on macOS (which it sounds like you're using, based on the `open -a` reference). However, there's an official and straightforward way to add it using Sublime's bundled `subl` script. This is cleaner than relying on the `open` command. I'll walk you through the options below, starting with the recommended approach.

#### 1. **Install the Official `subl` CLI Command (Recommended)**
Sublime Text includes a `subl` executable in its app bundle that you can symlink to a directory in your PATH (like `/usr/local/bin`). This lets you run `subl .` (to open the current directory) or `subl file.txt` from anywhere in the terminal.

**Steps for macOS (Sublime Text 3 or 4):**
- Open Terminal.
- Run this command to create the symlink (it requires admin privileges, so you'll be prompted for your password):
  ```
  sudo ln -s "/Applications/Sublime Text.app/Contents/SharedSupport/bin/subl" /usr/local/bin/subl
  ```
  - If you're using Sublime Text 3, the path might be slightly different: `"/Applications/Sublime Text 2.app/Contents/SharedSupport/bin/subl"` (adjust the version number as needed).
  - If `/usr/local/bin` isn't in your PATH, add it to your shell profile (e.g., `~/.zshrc` or `~/.bash_profile`):
    ```
    echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

- Test it: Navigate to a directory (e.g., `cd ~/Desktop`) and run:
  ```
  subl .
  ```
  This should open Sublime Text with the current folder loaded.

If the symlink path doesn't work (e.g., due to version differences), check the exact location:
- Run `find /Applications/Sublime\ Text.app -name subl` to locate the binary.

**Why this is nice:**
- It's official and lightweight—no third-party tools needed.
- Works system-wide, like a real CLI.
- Sublime Text 4 even has an option in the console (View > Show Console) to run `sublime_installation` or similar, but the symlink is the most reliable.

**If you're on Linux or Windows:**
- Linux: Similar symlink process—e.g., `sudo ln -s /opt/sublime_text/sublime_text /usr/local/bin/subl`.
- Windows: Add `C:\Program Files\Sublime Text\sublime_text.exe` to your PATH, or use a batch file for `subl`.

#### 2. **Fallback: Use the `open` Command (No Installation Needed)**
If you don't want to mess with symlinks or PATH, macOS's built-in `open` command works great for basic use. It's already available everywhere.

- To open the current directory in Sublime:
  ```
  open -a "Sublime Text" .
  ```
  - Note: Use `"Sublime Text"` (with space) if that's your app name. If it's just "Sublime.app", adjust accordingly. You can check the exact name in `/Applications/`.

- To open a specific file:
  ```
  open -a "Sublime Text" filename.txt
  ```

- Alias it for convenience: Add this to your shell profile (`~/.zshrc` or `~/.bash_profile`) to mimic `subl`:
  ```
  alias subl='open -a "Sublime Text"'
  ```
  Then reload with `source ~/.zshrc` and use `subl .` as usual.

**Pros/Cons:**
- Super simple and no setup.
- But it's macOS-only and less flexible (e.g., no easy way to specify lines or projects like with `subl`).

#### Troubleshooting
- **Command not found?** Ensure your PATH includes `/usr/local/bin` (run `echo $PATH` to check).
- **App not found?** Verify Sublime is in `/Applications/`. If it's elsewhere (e.g., via Homebrew: `brew install --cask sublime-text`), adjust paths.
- **Permissions issues?** The symlink needs sudo, but once set, it's fine.
- If you're using a package manager like Homebrew, you can install Sublime via `brew install --cask sublime-text`, and it might handle the CLI for you.

This should get you up and running nicely! If you run into errors or specify your OS/version, I can refine the steps.
