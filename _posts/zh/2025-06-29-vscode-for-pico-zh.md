---
audio: false
generated: true
lang: zh
layout: post
title: 树莓派Pico的VSCode MicroPython开发环境
translated: true
type: note
---

是的，你可以使用 Visual Studio Code（VSCode）来编写、上传和运行 Raspberry Pi Pico 上的 MicroPython 程序，类似于使用 Thonny 的方式。VSCode 是一款功能强大的编辑器，通过安装合适的扩展和工具，它可以高效地处理 MicroPython 开发。以下是一步一步的指南，帮助你在 VSCode 中设置环境，用于上传一个简单的 MicroPython 程序到 Pico，假设 MicroPython 已经刷入（正如你使用 `.uf2` 文件所做的那样）。

---

### 前提条件

1. **已刷入 MicroPython**：你的 Pico 已安装 MicroPython（例如，从 `RPI_PICO-20250415-v1.25.0.uf2` 文件刷入）。
2. **已安装 VSCode**：如果尚未安装，请从 [code.visualstudio.com](https://code.visualstudio.com) 下载并安装 VSCode。
3. **已安装 Python**：通过以下命令安装 Python（MicroPython 工具需要）：

   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```

4. **USB 连接**：Pico 通过支持数据传输的 USB 线缆连接到你的计算机。

---

### 使用 VSCode 进行 Raspberry Pi Pico MicroPython 开发的步骤指南

1. **安装必需的 VSCode 扩展**：
   - 打开 VSCode。
   - 进入扩展视图（`Ctrl+Shift+X` 或 macOS 上 `Cmd+Shift+X`）。
   - 安装以下扩展：
     - **Python**（由 Microsoft 提供）：用于 Python 和 MicroPython 的语法高亮和 IntelliSense。
     - **Pico-W-Go**（可选但推荐）：一个专为 Raspberry Pi Pico 的 MicroPython 开发设计的扩展。搜索 “Pico-W-Go” 并安装。
       - 注意：Pico-W-Go 简化了文件传输和 REPL 访问，但需要额外的设置（如下所述）。
     - 或者，如果你更喜欢手动控制，可以使用通用扩展如 **Remote-SSH** 或 **Serial Monitor**。

2. **设置 Pico-W-Go（推荐）**：
   - **安装依赖项**：Pico-W-Go 需要 `pyserial` 和 `esptool`。通过 pip 安装它们：

     ```bash
     pip3 install pyserial esptool
     ```

   - **配置 Pico-W-Go**：
     - 打开 VSCode 的命令面板（`Ctrl+Shift+P` 或 `Cmd+Shift+P`）。
     - 输入并选择 **Pico-W-Go > Configure Project**。
     - 按照提示设置你的项目：
       - 选择 Pico 的串行端口（例如 `/dev/ttyACM0`）。在终端中运行 `ls /dev/tty*` 来查找它。
       - 选择 MicroPython
