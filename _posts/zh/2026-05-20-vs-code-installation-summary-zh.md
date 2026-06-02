---
audio: false
generated: true
image: false
lang: zh
layout: post
title: VS Code 安装摘要
translated: true
type: note
---

以下是所做工作的完整概况：

VS Code 安装 — 完整总结

安装方式
已添加微软官方 apt 仓库，并通过 apt 进行安装。这意味着 VS Code 将可通过系统包管理器接收自动更新。

安装路径
- 二进制文件：/usr/bin/code
- 版本：1.121.0（最新稳定版）
- 架构：x64
- 安装包大小：下载 158 MB，磁盘占用约 726 MB

显示环境
- 显示：X11 (:0)
- 会话类型：X11（非 Wayland）
- 在终端中执行 `code .` 将在当前桌面会话中打开

预装扩展（共发现 54 个）
VS Code 自带了已安装在用户主目录（~/.vscode/extensions/）的扩展集。重点内容如下：

核心语言支持：
- Python：ms-python.python、ms-python.vscode-pylance、ms-python.debugpy、ms-python.autopep8
- C/C++：ms-vscode.cpptools、ms-vscode.cpptools-extension-pack、ms-vscode.cmake-tools、twxs.cmake
- Rust：rust-lang.rust-analyzer
- Go：golang.go
- Java：完整套件 — redhat.java、vscjava.vscode-java-pack、vscjava.vscode-java-debug、vscjava.vscode-java-test、vscjava.vscode-maven、vscjava.vscode-gradle、vscjava.vscode-lombok
- Kotlin：mathiasfrohlich.kotlin
- Nix：bbenois.nix
- PHP：xdebug.php-pack
- TOML：bungcip.better-toml
- YAML/XML：redhat.vscode-yaml、redhat.vscode-xml

嵌入式与 MCU 开发：
- marus25.cortex-debug、mcu-debug.debug-tracker-vscode、mcu-debug.memory-view、mcu-debug.peripheral-viewer
- raspberry-pi.raspberry-pi-pico、paulober.pico-w-go
- ms-vscode.vscode-serial-monitor、moozzyk.arduino

远程开发：
- ms-vscode-remote.remote-ssh、ms-vscode-remote.remote-containers、ms-vscode.remote-explorer

其他值得注意的扩展：
- github.vscode-github-actions — GitHub Actions 支持
- editorconfig.editorconfig — EditorConfig 合规
- akamud.vscode-theme-onedark、azemoh.one-monokai — 主题
- ms-vscode.css、octref.vetur — Web/样式相关

ww 包 — 已全局安装
与 VS Code 一同，ww 已作为可编辑的全局包（~/.local/bin/ww）基于系统 Python 3.12 提前安装，可在任意终端中直接使用。
