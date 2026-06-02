---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Using the Subl Command Line Tool
translated: false
type: note
---

### Using the `subl` Command in Sublime Text

Great news—your `subl` CLI is already installed and working (as shown by the `--help` output)! This is Sublime Text build 4200 (a recent version), and `subl` is the official command-line interface for opening files, directories, and more. It's super versatile for developers and power users.

I'll break it down with practical examples. Run these from any directory in your terminal. The core syntax is:

```
subl [arguments] [files or directories]
```

#### 1. **Basic Usage: Open Files or Directories**

- **Open the current directory** (loads it as a project/folder in Sublime):

  ```
  subl .
  ```

  - This opens a new window with the current folder's contents.

- **Open a specific file**:

  ```
  subl myfile.txt
  ```

  - Opens `myfile.txt` in the default window (or a new one if you want).

- **Open multiple files/directories**:

  ```
  subl file1.txt file2.js ~/Documents/myproject/
  ```

  - Opens all of them in Sublime.

- **Open at a specific line/column** (useful for jumping to errors):

  ```
  subl myfile.py:42          # Opens at line 42
  subl myfile.py:42:5        # Opens at line 42, column 5
  ```

#### 2. **Common Arguments (From the Help)**

Here are the most useful flags with examples. Combine them as needed (e.g., `subl -n file.txt`).

- **`-n` or `--new-window`**: Always open in a fresh window.

  ```
  subl -n myfile.txt
  ```

  - Handy if you want to keep your existing Sublime sessions separate.

- **`-a` or `--add`**: Add files/folders to your *current* Sublime window (if it's already open).

  ```
  subl -a newfolder/
  ```

  - This doesn't create a new window—great for building up a workspace.

- **`-w` or `--wait`**: Wait for you to close the file(s) in Sublime before the terminal command finishes.

  ```
  subl -w myfile.txt
  ```

  - Useful in scripts (e.g., after running a build, open and wait for review). Implied when reading from stdin.

- **`-b` or `--background`**: Open without bringing Sublime to the foreground (keeps your terminal focused).

  ```
  subl -b myfile.txt
  ```

- **`-s` or `--stay`**: Keep Sublime in focus after you close the file (only relevant with `-w`).

  ```
  subl -w -s myfile.txt
  ```

  - Prevents it from switching back to the terminal automatically.

- **`--project <project>`**: Open a specific Sublime project file (`.sublime-project`).

  ```
  subl --project MyProject.sublime-project
  ```

  - Projects save workspaces, settings, etc. Create one via File > Save Project in Sublime.

- **`--command <command>`**: Run a Sublime command (e.g., a plugin action) without opening files.

  ```
  subl --command "build"    # Triggers the build command if you have a build system set up
  ```

  - Check Sublime's console (View > Show Console) for available commands.

- **`--launch-or-new-window`**: Only open a new window if Sublime isn't already running.

  ```
  subl --launch-or-new-window .
  ```

  - Efficient for quick checks without cluttering your screen.

- **Stdin Support** (edit piped input):

  ```
  echo "Hello World" | subl -   # Opens stdin in Sublime for editing
  subl - > output.txt          # Edit stdin and save changes to output.txt
  ```

  - After editing in Sublime, save and close to continue.

- **`--safe-mode`**: Launch Sublime without plugins or custom settings (for troubleshooting).

  ```
  subl --safe-mode myfile.txt
  ```

- **Other Flags**:
  - `-h` or `--help`: Shows the help you already saw.
  - `-v` or `--version`: Prints the version (e.g., `subl -v`).

#### 3. **Tips for Everyday Use**

- **Files starting with `-`**: If a filename looks like a flag (e.g., `-config`), use `--` to separate:

  ```
  subl -- -config.json
  ```

- **Aliases for Convenience**: Add shortcuts to your shell profile (`~/.zshrc` for zsh, or `~/.bash_profile` for bash):

  ```
  alias st='subl'     # Shorter alias
  alias stt='subl -n' # For new tabs/windows
  ```

  Reload with `source ~/.zshrc`.
- **In Scripts/GIT**: Use it in hooks or aliases, e.g., `git diff | subl -` to review changes.
- **Vs. `open`**: Now that `subl` is set up, it's better than `open -a "Sublime Text"` because it supports lines, projects, and more advanced features.
- **Troubleshooting**:
  - If `subl` stops working, re-run the symlink install from my previous response.
  - For large projects, use `-a` to avoid multiple windows.
  - On macOS, if focus issues arise, try without `-b` first.

This covers 90% of what you'll need! Start with `subl .` in a project folder and experiment. If you have a specific workflow or error, share more details for tailored advice.
