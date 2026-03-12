---
audio: false
generated: true
image: false
lang: en
layout: post
title: Yazi Terminal File Manager Guide
translated: false
type: note
---

I'll search for comprehensive information about Yazi to give you a detailed introduction to this file manager tool.Let me search for more information about Yazi's plugins and use cases.---

## Question:

What is a comprehensive introduction to Yazi, a file manager tool?

## Answer:

### Overview

Yazi is a terminal file manager written in Rust, based on non-blocking async I/O, designed to provide an efficient, user-friendly, and customizable file management experience. The name "Yazi" means "duck" in Chinese. The tool is currently in public beta and can be used as a daily driver, though it is under heavy development with expected breaking changes.

### Core Performance Features

**Asynchronous Architecture:**
Yazi features full asynchronous support where all I/O operations are asynchronous and CPU tasks are spread across multiple threads, making the most of available resources. The tool internally uses Tokio as its asynchronous runtime to handle tasks in a non-blocking (event-driven) manner, ensuring high efficiency and quick response times.

**Task Management:**
The tool provides powerful async task scheduling and management with real-time progress updates, task cancellation, and internal task priority assignment.

**Preview Capabilities:**
Combined with the pre-caching mechanism, it greatly accelerates image and normal file loading. Yazi supports previewing text files, PDF files, images, videos, and includes built-in syntax highlighting.

### Key Features

**Image and Media Support:**
Yazi includes built-in support for multiple image protocols, also integrated with Überzug++ and Chafa, covering almost all terminals.

**Plugin System:**
The tool features a concurrent plugin system with UI plugins (rewriting most of the UI), functional plugins, custom previewer/preloader/spotter/fetcher capabilities, requiring just Lua scripts. Users can extend Yazi's functionality through Lua plugins, which need to be placed in the plugins subdirectory of Yazi's configuration directory.

**User Interface and Functionality:**
Additional features include bulk renaming, archive extraction, visual mode, file chooser, git integration, and mount manager. The tool supports multi-tab support, cross-directory selection, scrollable preview (for videos, PDFs, archives, code, directories), theme system, mouse support, trash bin, and custom layouts.

### Customization and Configuration

**Configuration System:**
Yazi uses TOML-based configuration files with options that override default settings. The configuration directory is located at `~/.config/yazi/` on Unix-like systems and `%AppData%\yazi\config\` on Windows.

**Keybindings:**
The tool adopts a more modern UI interface similar to Vim in key design, supporting batch operations and mouse scrolling, and integrating with multiple commonly used tools such as fd, rg, fzf.

**Theming:**
Yazi's theming system provides comprehensive visual customization for all interface components, file types, and icons through a flexible three-layer configuration structure: preset themes (dark/light), flavor overrides, and user customizations.

### Available Plugins and Extensions

The Yazi ecosystem includes a rich collection of plugins for various purposes:

- **File Operations:** Smart-enter (open files or enter directories with one key), full-border (add borders for fancier appearance), toggle-pane (toggle different panes), chmod (change file permissions), smart-paste (paste files intelligently)
- **Navigation:** Jump-to-char (vim-like character jumping), smart-filter (continuous filtering), bookmarks
- **Version Control:** Git integration for showing file change status, lazygit integration
- **Media Preview:** mediainfo (preview multiple media types), audio-preview (spectrogram visualization)
- **Data Viewing:** duckdb (preview CSV/TSV/JSON/Parquet files with analysis)
- **System Integration:** mount-manager, sshfs (remote directory mounting), sudo operations, trash management

### Installation and Integration

Installation is straightforward on macOS using Homebrew and on Linux with package managers, though the process is longer for Windows. A shell wrapper function allows users to automatically move into the directory they were in when exiting Yazi.

### Comparison with Other Tools

Yazi compares favorably to other terminal file managers. While Ranger is the tried and true classic favorite with its first stable release in 2009, it has been noted as somewhat slow and requiring vim commands for basic operations like creating files. Yazi offers faster performance with more intuitive hotkey-based operations and integration with modern command-line tools.

### Use Cases

Yazi is particularly valuable for developers and terminal enthusiasts who want to boost productivity through a modern, customizable file manager that avoids the overhead of GUI file explorers while providing powerful preview and plugin capabilities within the terminal environment.

---

## References:

- [https://github.com/sxyazi/yazi](https://github.com/sxyazi/yazi)
- [https://yazi-rs.github.io/](https://yazi-rs.github.io/)
- [https://yazi-rs.github.io/docs/quick-start/](https://yazi-rs.github.io/docs/quick-start/)
- [https://terminaltrove.com/yazi/](https://terminaltrove.com/yazi/)
- [https://medium.com/@pthapa1/yazi-the-best-terminal-file-manager-to-boost-your-productivity-bf13f244756a](https://medium.com/@pthapa1/yazi-the-best-terminal-file-manager-to-boost-your-productivity-bf13f244756a)
- [https://www.x-cmd.com/pkg/yazi/](https://www.x-cmd.com/pkg/yazi/)
- [https://snapcraft.io/yazi](https://snapcraft.io/yazi)
- [https://www.markpitblado.me/blog/setting-up-the-yazi-file-manager](https://www.markpitblado.me/blog/setting-up-the-yazi-file-manager)
- [https://www.josean.com/posts/how-to-use-yazi-file-manager](https://www.josean.com/posts/how-to-use-yazi-file-manager)
- [https://wiki.nixos.org/wiki/Yazi](https://wiki.nixos.org/wiki/Yazi)
- [https://yazi-rs.github.io/docs/configuration/overview/](https://yazi-rs.github.io/docs/configuration/overview/)
- [https://github.com/yazi-rs/plugins](https://github.com/yazi-rs/plugins)
- [https://yazi-rs.github.io/docs/plugins/overview/](https://yazi-rs.github.io/docs/plugins/overview/)
- [https://yazi-rs.github.io/docs/resources/](https://yazi-rs.github.io/docs/resources/)
- [https://yazi-rs.github.io/docs/installation/](https://yazi-rs.github.io/docs/installation/)
- [https://github.com/AnirudhG07/awesome-yazi](https://github.com/AnirudhG07/awesome-yazi)