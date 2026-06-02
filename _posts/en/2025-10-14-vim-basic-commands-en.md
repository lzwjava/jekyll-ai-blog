---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Vim Basic Commands Tutorial
translated: false
type: note
---

Vim (short for Vi IMproved) is a powerful, modal text editor that's the default on many Linux systems like Red Hat. It's keyboard-driven and efficient once you learn the basics. Vim has three main modes: **Normal** (for navigation and commands, default), **Insert** (for typing text), and **Visual** (for selecting text). Press `Esc` to return to Normal mode from anywhere.

The best way to learn hands-on is to run `vimtutor` in your terminal—it launches an interactive tutorial.

## 1. Opening and Closing Vim
- Open or create a file: `vim filename.txt` (e.g., `vim notes.txt`).
- Quit without saving: In Normal mode, type `:q!` and press Enter.
- Exit Vim: See saving section below.

## 2. Modes
- **Normal mode**: Default—use for commands. Press `Esc` to enter.
- **Insert mode**: Press `i` (insert before cursor) or `a` (append after cursor) to enter. You'll see `-- INSERT --` at the bottom.
- **Visual mode**: Press `v` to select text.
- **Command-line mode**: Press `:` to enter (for save, quit, search).

## 3. Navigation (in Normal Mode)
Use these instead of arrow keys for efficiency:
- `h`: Left one character
- `j`: Down one line
- `k`: Up one line
- `l`: Right one character
- `w`: Forward to start of next word
- `b`: Backward to start of previous word
- `0`: Start of line
- `$`: End of line
- `gg`: Top of file
- `G`: Bottom of file
- `:n`: Jump to line n (e.g., `:5`)
- Prefix with numbers: `5j` (down 5 lines)

Enable line numbers: `:set number`

## 4. Inserting and Editing Text
- Enter Insert mode:
  - `i`: Insert before cursor
  - `I`: Insert at start of line
  - `a`: Append after cursor
  - `A`: Append at end of line
  - `o`: New line below (enters Insert mode)
  - `O`: New line above (enters Insert mode)
- Exit Insert mode: `Esc`
- Replace single character: `r` (then type the new char)
- Undo: `u`
- Redo: `Ctrl + r`
- Repeat last command: `.`

## 5. Deleting, Copying, and Pasting
- Delete character: `x`
- Delete line: `dd`
- Delete range: `:3,5d` (lines 3 to 5)
- Copy (yank) line: `yy`
- Copy selected text: In Visual mode (`v`), highlight with arrows, then `y`
- Paste after cursor: `p`
- Paste before cursor: `P`
- Select text: `v` (character-wise), then move cursor; `Esc` to exit Visual.

## 6. Saving and Quitting
- Save: `:w`
- Save and quit: `:wq` or `:x` or `ZZ` (capital Z twice)
- Force save and quit: `:wq!`
- Quit without saving: `:q!` or `ZQ`

## 7. Searching
- Search forward: `/pattern` (e.g., `/hello`), then Enter; `n` for next.
- Search backward: `?pattern`
- Replace: `:%s/old/new/g` (replace all "old" with "new")

## Quick Tips
- Help: `:help` or `:h keyword`
- Split screen: `:split filename` (horizontal) or `:vsplit filename` (vertical); `Ctrl + w w` to switch.
- Practice in a test file to avoid mistakes.
- Syntax highlighting: `:syntax on`

This covers the essentials to get you editing files quickly. For more, explore `:help` in Vim or the resources below.

[Getting started with Vim: The basics](https://opensource.com/article/19/3/getting-started-vim)
[Basic Vim Commands](https://www.geeksforgeeks.org/linux-unix/basic-vim-commands/)
[Vim Cheat Sheet](https://vim.rtorr.com/)
