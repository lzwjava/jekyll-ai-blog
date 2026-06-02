---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Vi Editor Basics for Red Hat Linux
translated: false
type: note
---

Vi is a powerful, keyboard-driven text editor that's standard on Linux systems, including Red Hat Enterprise Linux (RHEL). It's lightweight and efficient for editing configuration files, scripts, and more. In Red Hat, the `vi` command typically points to `vim` (Vi IMproved), which adds features like syntax highlighting. This guide covers the basics for beginners.

## Installation
Vi is pre-installed on most Red Hat systems. If you need the full `vim` package (or it's missing), install it via the package manager:

- For RHEL 7/8:
  ```
  sudo yum install vim
  ```

- For RHEL 9+:
  ```
  sudo dnf install vim
  ```

After installation, you can use `vi` or `vim` interchangeably.

## Starting Vi
1. Open a terminal.
2. Run `vi filename.txt` (replace `filename.txt` with your file path).
   - If the file exists, it opens for editing.
   - If not, a new empty file is created.
3. To open without a file (for practice): `vi`.
Vi starts in **command mode** (the default). You'll see a blank screen or file contents with a cursor at the top-left.

## Understanding Modes
Vi has three main modes—switching between them is key:
- **Command Mode**: Default for navigation, deletion, and most actions. Press `Esc` to enter/return here from other modes.
- **Insert Mode**: For typing/editing text. Enter from command mode (e.g., press `i`).
- **Ex Mode**: For advanced commands like saving. Enter by typing `:` in command mode.

Commands are case-sensitive. Prefix numbers to repeat actions (e.g., `3dd` deletes 3 lines).

## Basic Navigation (in Command Mode)
Use the home-row keys for cursor movement—no mouse needed:
- `h`: Left one character
- `j`: Down one line
- `k`: Up one line
- `l`: Right one character
- `w`: Forward one word
- `b`: Backward one word
- `0` (zero): Start of line
- `$`: End of line
- `gg`: Top of file
- `G`: Bottom of file
- `Ctrl + F`: Page down
- `Ctrl + B`: Page up

## Entering Insert Mode and Editing
From command mode, press one of these to switch to insert mode and start typing:
- `i`: Insert before cursor
- `I`: Insert at start of line
- `a`: Append after cursor
- `A`: Append at end of line
- `o`: New line below
- `O`: New line above

To exit insert mode: Press `Esc` (return to command mode).

Common editing commands (in command mode):
- **Delete**:
  - `x`: Delete character under cursor
  - `X`: Delete character before cursor
  - `dd`: Delete current line
  - `dw`: Delete current word
  - `D`: Delete to end of line
- **Copy (Yank)**:
  - `yy`: Copy current line
  - `y`: Copy selection (after `v` to select)
- **Paste**:
  - `p`: Paste after cursor
  - `P`: Paste before cursor
- **Undo**:
  - `u`: Undo last change
  - `U`: Undo all changes to current line
- **Repeat**: `.` (repeats last command)

## Saving and Exiting
These are **Ex commands**—type `:` in command mode, then the command, and press `Enter`:
- `:w`: Save (write) changes
- `:q`: Quit (if no changes)
- `:wq` or `ZZ` (in command mode): Save and quit
- `:q!`: Quit without saving (force discard changes)
- `:w filename`: Save as new file

If you're stuck, `:q!` gets you out safely.

## Searching and Replacing
- Search forward: `/pattern` (e.g., `/error`), then `n` for next match, `N` for previous.
- Search backward: `?pattern`.
- Replace all: `:%s/old/new/g` (global replace; add `c` for confirmation, e.g., `:%s/old/new/gc`).

## Tips for Red Hat Users
- Customize in `~/.vimrc` (create if needed):
  ```
  set number          # Show line numbers
  syntax on           # Syntax highlighting
  set tabstop=4       # Tab width
  set autoindent      # Auto-indent
  ```
  Edit with `vi ~/.vimrc`, add lines, then `:wq`.
- For multiple files: `vi file1.txt file2.txt`, switch with `:n` (next) or `:prev` (previous).
- Practice in a test file to avoid mistakes in system files.

Vi takes practice but becomes intuitive. Start simple and use `Esc` often!

## References
[How to get started with the Vi editor - Red Hat](https://www.redhat.com/en/blog/get-started-vi-editor)
[LFCS #2: How to Install and Use Vi/Vim as a Full Text Editor in Linux](https://www.tecmint.com/vi-editor-usage/)
[vi Editor in Linux - GeeksforGeeks](https://www.geeksforgeeks.org/linux-unix/vi-editor-unix/)
