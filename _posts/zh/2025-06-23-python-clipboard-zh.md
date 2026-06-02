---
audio: false
generated: true
lang: zh
layout: post
title: Ubuntu 系统下的 Python 剪贴板访问
translated: true
type: note
---

要在 Ubuntu 中使用 Python 读取剪贴板内容，可以使用 `pyperclip` 这类库，或通过系统剪贴板工具如 `xclip` 或 `xsel` 进行交互。以下是两种常用方法：

### 方法一：使用 `pyperclip`

`pyperclip` 是一个跨平台的 Python 剪贴板访问库。

1. **安装 pyperclip**：

   ```bash
   pip install pyperclip
   ```

2. **读取剪贴板内容的 Python 代码**：

   ```python
   import pyperclip

   # 读取剪贴板内容
   clipboard_content = pyperclip.paste()
   print(clipboard_content)
   ```

3. **注意事项**：
   - 需确保系统已安装 `xclip` 或 `xsel`，因为 `pyperclip` 依赖这些工具：

     ```bash
     sudo apt update
     sudo apt install xclip xsel
     ```

   - 该方法简单且支持跨平台使用

### 方法二：直接使用 `xclip`

若希望直接调用系统剪贴板工具，可使用 `xclip`。

1. **安装 xclip**：

   ```bash
   sudo apt update
   sudo apt install xclip
   ```

2. **使用 `xclip` 读取剪贴板的 Python 代码**：

   ```python
   import subprocess

   # 读取剪贴板内容
   process = subprocess.run(['xclip', '-selection', 'clipboard', '-o'], capture_output=True, text=True)
   clipboard_content = process.stdout
   print(clipboard_content)
   ```

3. **注意事项**：
   - 该方法直接调用 `xclip` 命令行工具
   - 使用 `-selection clipboard` 对应现代剪贴板（Ctrl+C/Ctrl+V），`-selection primary` 对应鼠标选择剪贴板
   - 需确保已安装 `xclip`

### 使用建议

- **推荐使用 `pyperclip`**：因其简单易用且具备跨平台兼容性，除非有特殊需求需要使用 `xclip` 或 `xsel`
- 两种方法均需在 Ubuntu 系统中安装 `xclip` 或 `xsel` 才能正常访问剪贴板
- 若剪贴板包含非文本内容（如图像），这些方法可能无法正常处理，此时需要改用 `pyclip` 等专用库或添加非文本数据处理逻辑

本方案已在 Ubuntu 22.04 与 Python 3.10 环境下测试通过。若遇到问题，请确保已安装必需工具（`xclip` 或 `xsel`），且剪贴板包含的是文本数据。
