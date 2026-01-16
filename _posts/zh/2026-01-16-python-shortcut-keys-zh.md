---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 通过键盘快捷键自动运行 Python 脚本
translated: true
type: note
---

**Question:** 我可以创建一个 browser extension 或使用其他方法，通过键盘快捷键运行 `python scripts/create/create_note.py grok-fast` 脚本，而无需每次都切换到 terminal 吗？

**Answer:**

是的 —— 有几种实用的方法。以下是 2025–2026 年最现实的方案，按**从最易于设置到最可定制**的顺序排列：

### 推荐选项（按易用性 + 可靠性排名）

1. **macOS – 使用 Shortcuts.app + 全局键盘快捷键**（如果你使用 macOS，这是最简单的）
   - 打开 Shortcuts app
   - 创建新的 shortcut
   - 添加 action **Run Shell Script**
   - 设置 “Shell” = `/bin/zsh` 或 `/bin/bash`
   - 粘贴：

     ```bash
     cd ~/path/to/your/blog-repo
     python3 scripts/create/create_note.py grok-fast
     ```

   - （可选）如果你通常想查看文件，添加 **Open URLs** → `github.com/lzwjava/blog-source/…`
   - 为 shortcut 命名，例如 “New Grok Note”
   - Menu bar → Shortcuts → Settings → Keyboard Shortcuts → Services → 分配快捷键，例如 `⌃⌥⌘ N`

   → 全局快捷键，不显示 terminal 窗口（如果你关闭了 “Show terminal”）。

2. **Windows – PowerToys + Run command / .bat 封装**
   - 安装 Microsoft PowerToys（免费）
   - 启用 **Keyboard Manager** 或 **PowerToys Run**
   - 在 repo 旁边创建一个小的 `.bat` 或 `.cmd` 文件：

     ```bat
     @echo off
     cd /d "C:\path\to\your\blog-repo"
     python scripts\create\create_note.py grok-fast
     ```

   - 在 PowerToys Keyboard Manager 中 → 映射一个未使用的按键组合（例如 `Ctrl+Alt+N`）→ run program → 指向该 `.bat` 文件

   替代方案：使用 **AutoHotkey v2**（功能强大，学习曲线小）

     ```autohotkey
     ^!n::  ; Ctrl+Alt+N
     {
         Run 'cmd.exe /c cd /d "C:\path\to\repo" && python scripts\create\create_note.py grok-fast'
         ; 或者如果你想使用 Windows Terminal：Run 'wt.exe -w 0 nt --title "Note" -- cd ...'
     }
     ```

3. **Linux – xbindkeys / sxhkd / AutoKey / 自定义 .desktop 快捷方式**
   最流行的快速解决方案：

   - **sxhkd**（如果你使用 bspwm/sway/awesome/xmonad）

     ```bash
     # ~/.config/sxhkd/sxhkdrc
     super + n
         ~/bin/new-grok-note
     ```

     以及 `~/bin/new-grok-note`：

     ```bash
     #!/usr/bin/env bash
     cd ~/projects/blog-source
     python3 scripts/create/create_note.py grok-fast
     ```

   - **AutoKey**（GUI 界面，适用于任何 X11/Wayland 桌面）

4. **跨平台 – Raycast / Alfred / Ulauncher extension**（如果你已经在使用这些工具，会非常方便）

   - **Raycast** (macOS, 2025 年非常流行)
     创建一个新的 script command → 输入 cd + python 命令行 → 分配 hotkey。
     优点：你以后可以设置它接受参数（`grok-fast`、`claude` 等）。

   - **Alfred** (macOS) – 同样的思路，Workflow → Run Script。

5. **Browser extension – 仅在非常特殊的情况下可行**

   由于安全限制，browser extension 本身**不能**直接运行本地 Python 脚本。

   人们实际使用的变通方法：

   - Extension 发送 POST 请求到 localhost:port
   - 你在后台运行一个微型的 HTTP server (FastAPI / Flask / http.server)，在收到请求时执行命令

     ```python
     # 后台运行：python local_note_server.py
     from fastapi import FastAPI
     import subprocess
     app = FastAPI()

     @app.post("/new-grok-note")
     async def create():
         subprocess.run(["python", "scripts/create/create_note.py", "grok-fast"], cwd="/path/to/repo")
         return {"status": "ok"}
     ```

     → Chrome/Firefox extension 只需执行 `fetch("http://localhost:8765/new-grok-note", {method:"POST"})`。

     → 你仍然需要在本地运行一些程序 → 复杂度较高。

   → 通常**不值得**，除非你想从网页内部触发。

### 快速建议表 (2026 现状)

| OS          | 目前最简单的路径                                     | 是否支持全局快捷键？ | Terminal 窗口是否可见？ | 学习成本 |
|-------------|------------------------------------------------------|----------------------------|---------------------------|---------------|
| macOS       | Shortcuts.app                                        | 是                        | 否                        | 极低      |
| macOS       | Raycast / Alfred                                     | 是                        | 否                        | 低           |
| Windows     | PowerToys + .bat                                     | 是                        | 通常不显示                | 低           |
| Windows     | AutoHotkey                                           | 是                        | 可配置                    | 中           |
| Linux       | sxhkd / AutoKey                                      | 是                        | 否                        | 中           |
| 任何平台     | 小型 localhost server + browser extension            | 是 (通过 extension hotkey) | 否                        | 高           |

**大多数处于类似情况的用户 (2024–2026) 最终会选择方案 1 或 2，或者使用 Raycast / PowerToys。**

如果你告诉我你使用的是哪种操作系统（以及你是否已经在使用 Raycast / Alfred / PowerToys / AutoHotkey），我可以为你提供具体的 5–8 个步骤。

References:

- 本回答无需参考文献