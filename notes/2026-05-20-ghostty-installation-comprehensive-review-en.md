---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ghostty Installation Comprehensive Review
translated: false
type: note
---

Here's the full rundown:
    
    
    
    Ghostty Installation — Comprehensive Review
    
    Version & Source
    - Ghostty 1.3.1 (stable channel, latest)
    - Installed from mkasberg/ghostty-ubuntu PPA (community-maintained, same maintainer who works with the Ghostty project)
    - PPA added: ppa:mkasberg/ghostty-ubuntu → pinned to Ubuntu Noble (24.04) — maps correctly to Linux Mint 22.3
    
    Installation Method
    
    sudo add-apt-repository ppa:mkasberg/ghostty-ubuntu
    sudo apt-get install ghostty
    
    Updates are automatic through apt going forward.
    
    Package Contents
    
    Area: Binary
    Details: /usr/bin/ghostty (27 MB, GTK4 + OpenGL renderer, GPU-accelerated)
    ────────────────────────────────────────
    Area: Shared libs
    Details: libghostty-vt.so (VT terminal API library, C headers under /usr/include/ghostty/)
    ────────────────────────────────────────
    Area: Dependencies
    Details: GTK4, libadwaita, libfontconfig, freetype, harfbuzz, oniguruma, libwayland, X11
    ────────────────────────────────────────
    Area: Themes
    Details: 350+ built-in themes at /usr/share/ghostty/themes/ (Catppuccin, Nord, TokyoNight, Gruvbox, Dracula,
      Solarized, etc.)
    ────────────────────────────────────────
    Area: Shell integrations
    Details: bash, zsh, fish, elvish, nushell — preexec hooks, integration scripts
    ────────────────────────────────────────
    Area: Editor support
    Details: vim, neovim (compiler, ftdetect, ftplugin, syntax), bat syntax highlighting
    ────────────────────────────────────────
    Area: Completions
    Details: bash, fish, zsh
    ────────────────────────────────────────
    Area: DBus
    Details: Service file for D-Bus activation
    ────────────────────────────────────────
    Area: systemd
    Details: User service: app-com.mitchellh.ghostty.service
    ────────────────────────────────────────
    Area: Desktop entry
    Details: com.mitchellh.ghostty.desktop — app menu launcher
    ────────────────────────────────────────
    Area: Nautilus
    Details: Python extension for right-click "Open in Ghostty"
    ────────────────────────────────────────
    Area: KIO
    Details: KDE service menu integration
    ────────────────────────────────────────
    Area: Icons
    Details: 16×16 through 1024×1024, including HiDPI variants
    ────────────────────────────────────────
    Area: Man pages
    Details: ghostty.1 (user command), ghostty.5 (config file format)
    ────────────────────────────────────────
    Area: Locale
    Details: 25+ language translations
    ────────────────────────────────────────
    Area: terminfo
    Details: ghostty and xterm-ghostty entries (proper terminal type detection)
    ────────────────────────────────────────
    Area: Appstream
    Details: com.mitchellh.ghostty.metainfo.xml — software center metadata
    
    Build Details
    - Zig 0.15.2 compiler (ReleaseFast)
    - GTK 4.14.5 (build & runtime)
    - libadwaita 1.5.0 (enabled)
    - libX11 + libwayland (both enabled, dual-protocol)
    - Font engine: fontconfig + freetype
    - Renderer: OpenGL via generic renderer
    - Kernel io_uring support detected
    
    Config File
    Ghostty uses an INI-style config at ~/.config/ghostty/config (auto-created on first launch if absent). Key config patterns:
    
    ini
    theme = Catppuccin Mocha
    font-size = 13
    font-family = JetBrains Mono
    background-opacity = 0.92
    window-padding-x = 4
    window-padding-y = 4
    
    
    Notes
    - The PPA also installs libgtk4-layer-shell0 and libonig5 as dependencies
    - Shell integration is auto-loaded (bash: /usr/share/ghostty/shell-integration/bash/)
    - The Nautilus extension adds "Open in Ghostty" to right-click context menus
    - Updates come through apt update && apt upgrade like any other system package