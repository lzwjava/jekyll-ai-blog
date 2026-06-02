---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Ghostty 安装全面评测
translated: true
type: note
---

以下是完整的回顾：

Ghostty 安装 —— 全面评测

版本与来源
- Ghostty 1.3.1（稳定版通道，最新）
- 从 mkasberg/ghostty-ubuntu PPA 安装（社区维护，维护者同时参与 Ghostty 项目）
- 添加的 PPA：ppa:mkasberg/ghostty-ubuntu → 固定为 Ubuntu Noble（24.04）—— 正确映射到 Linux Mint 22.3

安装方法

sudo add-apt-repository ppa:mkasberg/ghostty-ubuntu
sudo apt-get install ghostty

后续通过 apt 自动更新。

包内容

区域：二进制
详情：/usr/bin/ghostty（27 MB，GTK4 + OpenGL 渲染器，GPU 加速）
────────────────────────────────────────
区域：共享库
详情：libghostty-vt.so（VT 终端 API 库，C 头文件位于 /usr/include/ghostty/）
────────────────────────────────────────
区域：依赖项
详情：GTK4、libadwaita、libfontconfig、freetype、harfbuzz、oniguruma、libwayland、X11
────────────────────────────────────────
区域：主题
详情：350+ 内置主题位于 /usr/share/ghostty/themes/（Catppuccin、Nord、TokyoNight、Gruvbox、Dracula、Solarized 等）
────────────────────────────────────────
区域：Shell 集成
详情：bash、zsh、fish、elvish、nushell —— preexec 钩子、集成脚本
────────────────────────────────────────
区域：编辑器支持
详情：vim、neovim（compiler、ftdetect、ftplugin、syntax）、bat 语法高亮
────────────────────────────────────────
区域：补全
详情：bash、fish、zsh
────────────────────────────────────────
区域：DBus
详情：D-Bus 激活的服务文件
────────────────────────────────────────
区域：systemd
详情：用户服务：app-com.mitchellh.ghostty.service
────────────────────────────────────────
区域：桌面入口
详情：com.mitchellh.ghostty.desktop —— 应用菜单启动器
────────────────────────────────────────
区域：Nautilus
详情：Python 扩展，用于右键菜单“Open in Ghostty”
────────────────────────────────────────
区域：KIO
详情：KDE 服务菜单集成
────────────────────────────────────────
区域：图标
详情：16×16 至 1024×1024，包括 HiDPI 变体
────────────────────────────────────────
区域：手册页
详情：ghostty.1（用户命令）、ghostty.5（配置文件格式）
────────────────────────────────────────
区域：语言
详情：25+ 种语言翻译
────────────────────────────────────────
区域：terminfo
详情：ghostty 和 xterm-ghostty 条目（正确的终端类型检测）
────────────────────────────────────────
区域：Appstream
详情：com.mitchellh.ghostty.metainfo.xml —— 软件中心元数据

构建详情
- Zig 0.15.2 编译器（ReleaseFast）
- GTK 4.14.5（构建与运行时）
- libadwaita 1.5.0（已启用）
- libX11 + libwayland（均已启用，双协议）
- 字体引擎：fontconfig + freetype
- 渲染器：通过通用渲染器使用 OpenGL
- 检测到内核 io_uring 支持

配置文件
Ghostty 使用 INI 风格的配置文件，位于 ~/.config/ghostty/config（首次启动时自动创建，若不存在）。关键配置模式：

ini
theme = Catppuccin Mocha
font-size = 13
font-family = JetBrains Mono
background-opacity = 0.92
window-padding-x = 4
window-padding-y = 4


备注
- PPA 还会安装 libgtk4-layer-shell0 和 libonig5 作为依赖项
- Shell 集成自动加载（bash：/usr/share/ghostty/shell-integration/bash/）
- Nautilus 扩展在右键菜单中添加“Open in Ghostty”
- 更新通过 apt update && apt upgrade 进行，与其他系统包一样
