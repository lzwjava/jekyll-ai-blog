---
audio: false
generated: true
image: false
lang: en
layout: post
title: Lazygit Simple Terminal Git Powerhouse
translated: false
type: note
---

I'll search for comprehensive information about lazygit for you.Now let me search for more specific information about installation and features.---

**Question:** What is a comprehensive introduction to Lazygit, a CLI tool?

**Answer:**

## Overview

Lazygit is a simple terminal UI for git commands, written in Go with the gocui library that enables you to have a feeling of Sourcetree in a terminal-centric environment. It is a lightweight, cli-based UI for Git that has allowed developers to be as fast as they would be using cli commands in a terminal, but using a UI.

## History and Purpose

Lazygit was created in 2018 by Australian developer Jesse Duffield as a side project meant to reduce the friction of remembering and typing long Git commands, and it was open-sourced on GitHub where it quickly gained traction among developers.

## Why Lazygit Was Created

The creator's motivation stemmed from frustration with Git's complexity: interactive rebasing requires editing a TODO file in an editor, staging part of a file needs stepping through each hunk, and simple operations often require complex command sequences.

## Technical Foundation

The tool is written entirely in Go, which makes it fast, portable, and easy to install as a single binary with no dependencies, and provides instant startup time with Go binaries launching in milliseconds.

## Key Features

### Visual Interface and Organization

Lazygit's UI is divided into six panels or sections, with a preview panel that lets you preview unstaged changes, commits, logs, file content, and so on. You can navigate through the TUI panels using arrow keys or vim-style H/J/K/L navigation, with some panels having multiple tabs.

### Keyboard-Driven Workflow

The absolute killer-feature is that it is completely keyboard-driven—you would never have to touch your mouse to work with lazygit. The only keyboard shortcut you need to remember is ? which shows you contextually available operations based on an active panel.

### Core Operations

**Staging and Committing:**
To stage files with lightning speed, use arrow keys to navigate between files and hit the space bar to toggle a file between staged and unstaged.

**Interactive Rebasing:**
You can press i to start an interactive rebase, then squash (s), fixup (f), drop (d), edit (e), move up (ctrl+k) or move down (ctrl+j) any TODO commits before continuing the rebase. In Lazygit, all simple use cases for interactive rebases are supported with their own keybindings, and you're effectively editing that TODO file through Lazygit but everything requires only a single keypress.

**Cherry-Picking:**
You can press shift+c on a commit to copy it and press shift+v to paste (cherry-pick) it.

**Branch Management:**
To create a new branch, press n; to delete a branch, press d and then specify whether you want to delete the branch in a local or remote repository.

**Merge Conflict Resolution:**
To resolve merge conflicts, first merge a branch by pressing M, then choose the merge type and hit Enter; if any merge conflicts occur, the conflicting files appear in the files panel, and you can select the correct merge conflicts and press space to resolve.

### Advanced Features

Lazygit supports custom patch creation from old commits, allowing you to remove the patch from the commit, split out a new commit, apply the patch in reverse to the index, and more. You can create worktrees to have multiple branches going at once without the need for stashing or creating WIP commits when switching between them. You can press b in the commits view to mark a commit as good/bad in order to begin a git bisect.

## Cross-Platform Support

Lazygit can run on Linux, macOS, FreeBSD, and Windows.

## Installation

Lazygit offers multiple installation methods:

**macOS:**
You can easily install lazygit on macOS using brew: brew tap jesseduffield/lazygit && brew install lazygit.

**Windows:**
You can install lazygit using the winget command in the Windows Terminal.

**Linux:**
Lazygit packages for Ubuntu are available via Launchpad PPA through: sudo add-apt-repository ppa:lazygit-team/daily && sudo apt update && sudo apt install lazygit.

**From Source:**
You can use: go get github.com/jesseduffield/lazygit if you have Go installed, then call lazygit in your terminal inside a git repository.

## Configuration

Lazygit is config-as-code: a single YAML file lives at ~/.config/lazygit/config.yml where you can override keybindings, add custom pull-request commands, or pipe output to your preferred pager.

## Target Audience

Lazygit is excellent for beginners as it provides a visual interface that makes Git operations more intuitive without memorizing complex command-line syntax. However, you may not need lazygit if you live in an IDE whose Git panel already gives you most of these features or if you script heavy automation where raw CLI is faster.

## Getting Started

Simply type `lazygit` in your terminal inside a git repository to launch the tool. If you want, you can also add an alias for this with: echo "alias lg='lazygit'" >> ~/.zshrc.

---

## References

- [GitHub - jesseduffield/lazygit: simple terminal UI for git commands](https://github.com/jesseduffield/lazygit)
- [How to Use Lazygit to Skyrocket Your Git Efficiency](https://chishengliu.com/posts/lazygit-tutorial/)
- [How to Use Lazygit to Improve Your Git Workflow](https://www.freecodecamp.org/news/how-to-use-lazygit-to-improve-your-git-workflow/)
- [Level-up Git with lazygit](https://medium.com/@rasmusfangel/level-up-git-with-lazygit-b5e6c923c5d7)
- [What is LazyGit?](https://graphite.com/guides/lazygit)
- [lazygit Keybindings](https://github.com/jesseduffield/lazygit/blob/master/docs/keybindings/Keybindings_en.md)
- [Install and Use lazygit](https://computingforgeeks.com/how-to-install-and-use-lazygit-a-simple-terminal-ui-for-git-commands/)
- [Make advanced Git tasks simple with Lazygit](https://opensource.com/article/20/3/lazygit)
- [Lazygit, the convenience of GUI with the power of git CLI](https://pawelgrzybek.com/lazygit-the-convenience-of-gui-with-the-power-of-git-cli/)
- [The (lazy) Git UI You Didn't Know You Need](https://www.bwplotka.dev/2025/lazygit/)
- [Lazygit: A Simple Terminal UI That Makes Git Human-Friendly](https://www.blog.brightcoding.dev/2025/08/14/lazygit-a-simple-terminal-ui-that-makes-git-human-friendly/)
- [Lazygit: The terminal UI that makes git actually usable](https://www.bytesizego.com/blog/lazygit-the-terminal-ui-that-makes-git-actually-usable)
