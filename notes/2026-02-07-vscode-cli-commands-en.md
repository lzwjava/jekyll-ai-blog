---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Master VS Code CLI Commands
translated: false
type: note
---

**Question:** Provide a comprehensive introduction to VS Code's `code` command line options.

**Answer:**

The `code` command is the **command-line interface (CLI)** for Visual Studio Code. It allows you to launch VS Code, open files/folders, install extensions, compare files, set preferences, and more — all from the terminal or scripts.

### First Step: Make `code` Available in Your Terminal

- On **macOS** and **Linux**: Open VS Code → press `Ctrl+Shift+P` (or `Cmd+Shift+P`) → type "shell command" → run **Shell Command: Install 'code' command in PATH**.
- On **Windows**: The installer usually adds it to PATH automatically. If not, add the VS Code bin folder manually (typically `C:\Users\<YourUser>\AppData\Local\Programs\Microsoft VS Code\bin`).

After this step you can simply type `code` in any terminal.

Check it works:

```bash
code --version
# or
code -v
```

### Get the Full List of Options

The most up-to-date list is always available by running:

```bash
code --help
```

This shows version, usage examples, and all current flags (new options appear in new VS Code releases).

### Most Commonly Used Options (Core CLI Flags)

| Flag / Short | Long form                  | Description / Typical Use Case                                                                 |
|--------------|----------------------------|------------------------------------------------------------------------------------------------|
| `-h`         | `--help`                   | Show all available options                                                                     |
| `-v`         | `--version`                | Show VS Code version + commit ID                                                               |
| `.`          | (no flag)                  | `code .` → open current directory                                                              |
| `file.txt`   | (no flag)                  | `code README.md` → open specific file(s)                                                       |
| `-n`         | `--new-window`             | Force new window (even if VS Code is already open)                                             |
| `-r`         | `--reuse-window`           | Force open in the last active window (most common when you already have VS Code open)         |
| `-g`         | `--goto`                   | Open file at specific location: `code -g file.py:42:10` (line 42, column 10)                   |
| `--diff`     | `--diff file1 file2`       | Open diff editor between two files                                                             |
| `-w`         | `--wait`                   | Wait until the opened files are closed before returning to terminal (useful in git editors)   |
| `--locale`   | `--locale=es`              | Force display language (en, es, zh-cn, etc.)                                                   |
| `--user-data-dir` | `--user-data-dir <path>` | Use custom user data folder (great for testing / portable setups / multiple instances)       |
| `--extensions-dir` | `--extensions-dir <path>` | Custom extensions folder                                                                       |
| `--disable-extensions` | —                       | Start without any extensions (very useful for troubleshooting)                                 |
| `--disable-gpu` | —                       | Disable hardware acceleration (helps with some graphics/driver issues)                        |
| `--status`   | `--status`                 | Print detailed status information                                                              |

### Opening Files at Specific Locations

```bash
# Open file and jump to line 15
code main.py:15

# Line 30, column 5
code src/App.tsx:30:5

# Multiple files + goto
code -g index.html:10 src/styles.css
```

### Useful Everyday Examples

```bash
# Open current folder in new window
code . -n

# Open project in already open VS Code window
code ~/projects/my-app -r

# Compare two files
code --diff old-version.py new-version.py

# Open file from stdin (very powerful with pipes)
echo "Hello" | code -

# Wait for file to be closed (great for git commit message editor)
git config --global core.editor "code --wait"

# Open folder with specific profile
code ~/work/project --profile "Work"

# Troubleshoot: start clean
code --disable-extensions --user-data-dir=/tmp/vscode-test
```

### Extension Management from CLI

```bash
# Install extension
code --install-extension ms-python.python

# Uninstall
code --uninstall-extension ms-python.python

# List installed extensions
code --list-extensions

# List with versions
code --list-extensions --show-versions
```

### Advanced / Less Common Flags (from --help)

- `--max-memory=...` — set memory limit
- `--telemetry` / `--disable-telemetry`
- `--verbose` — more logging
- `--log debug|info|warn|error`
- `--profile <name>` — use named profile
- `--folder-uri` / `--file-uri` — open using URI scheme
- Subcommands like `code tunnel` (for remote tunnels)

For the absolute latest and complete list (including any new flags added after 2025), always run:

```bash
code --help
```

The official documentation page is continuously updated:

**References:**

- [Command Line Interface (CLI) - Visual Studio Code](https://code.visualstudio.com/docs/editor/command-line)
- [Getting Started: Tips and Tricks (includes CLI examples)](https://code.visualstudio.com/docs/getstarted/tips-and-tricks)