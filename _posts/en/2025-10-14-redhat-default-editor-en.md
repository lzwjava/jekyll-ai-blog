---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Red Hat Enterprise Linux Default Text Editor
translated: false
type: note
---

### Default Text Editor in Red Hat Enterprise Linux

In Red Hat Enterprise Linux (RHEL), the default text editor is **Vi** (often aliased to **Vim**, which stands for "Vi IMproved"). Vi is a modal, command-line text editor that's been the standard on Unix-like systems since the 1970s. It's lightweight, ubiquitous, and pre-installed on most RHEL systems via the `vim-minimal` or `vim-enhanced` package.

#### Why Vi/Vim?

- It's efficient for server environments where GUI editors aren't practical.
- Commands are keyboard-based: Insert mode for typing (`i`), and command mode for editing (e.g., `dd` to delete a line, `:wq` to save and quit).
- If you're new to it, it has a learning curve but is powerful once mastered.

#### Checking and Using It

- Run `vi filename.txt` (or `vim filename.txt`) to open a file.
- To check your current default editor: `echo $EDITOR` (usually outputs `/usr/bin/vi`).
- If you prefer something else (like Emacs from your previous query), set it with `export EDITOR=emacs` in your `~/.bashrc`.

For a quick start, type `vimtutor` to launch an interactive tutorial.

[How to get started with the Vi editor - Red Hat](https://www.redhat.com/en/blog/get-started-vi-editor)
[Linux skills: 9 tutorials to get more from your text editor - Red Hat](https://www.redhat.com/en/blog/text-editor-roundup-2022)
