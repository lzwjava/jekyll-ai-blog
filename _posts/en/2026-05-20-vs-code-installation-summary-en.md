---
audio: false
generated: true
image: false
lang: en
layout: post
title: VS Code Installation Summary
translated: false
type: note
---

Here's the full picture of what was done:
    
    
    
    VS Code Installation — Complete Summary
    
    How it was installed
    Added Microsoft's official apt repository, then installed via apt. This means VS Code will receive automatic updates through your system's package manager.
    
    Installation path
    - Binary: /usr/bin/code
    - Version: 1.121.0 (latest stable)
    - Architecture: x64
    - Deb size: 158 MB download, ~726 MB on disk
    
    Display environment
    - Display: X11 (:0)
    - Session type: X11 (not Wayland)
    - code . will open in your current desktop session
    
    Pre-installed extensions (54 found)
    VS Code came with an existing extension set already installed in your home directory (~/.vscode/extensions/). Highlights:
    
    Core language support:
    - Python: ms-python.python, ms-python.vscode-pylance, ms-python.debugpy, ms-python.autopep8
    - C/C++: ms-vscode.cpptools, ms-vscode.cpptools-extension-pack, ms-vscode.cmake-tools, twxs.cmake
    - Rust: rust-lang.rust-analyzer
    - Go: golang.go
    - Java: full pack — redhat.java, vscjava.vscode-java-pack, vscjava.vscode-java-debug, vscjava.vscode-java-test, vscjava.vscode-maven, vscjava.vscode-gradle, vscjava.vscode-lombok
    - Kotlin: mathiasfrohlich.kotlin
    - Nix: bbenoist.nix
    - PHP: xdebug.php-pack
    - TOML: bungcip.better-toml
    - YAML/XML: redhat.vscode-yaml, redhat.vscode-xml
    
    Embedded & MCU development:
    - marus25.cortex-debug, mcu-debug.debug-tracker-vscode, mcu-debug.memory-view, mcu-debug.peripheral-viewer
    - raspberry-pi.raspberry-pi-pico, paulober.pico-w-go
    - ms-vscode.vscode-serial-monitor, moozzyk.arduino
    
    Remote development:
    - ms-vscode-remote.remote-ssh, ms-vscode-remote.remote-containers, ms-vscode.remote-explorer
    
    Other notable:
    - github.vscode-github-actions — GitHub Actions support
    - editorconfig.editorconfig — EditorConfig compliance
    - akamud.vscode-theme-onedark, azemoh.one-monokai — themes
    - ms-vscode.css, octref.vetur — web/styling
    
    ww package — also installed globally
    Alongside VS Code, ww was installed earlier as an editable global package (~/.local/bin/ww) with system Python 3.12, ready to use from any terminal.