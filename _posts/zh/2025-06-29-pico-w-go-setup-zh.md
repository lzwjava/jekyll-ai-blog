---
audio: false
generated: true
lang: zh
layout: post
title: VSCode Pico-W-Go MicroPython开发环境
translated: true
type: note
---

在 Visual Studio Code (VSCode) 中使用 **Raspberry Pi Pico** 扩展是在树莓派 Pico 上进行 MicroPython 开发的绝佳选择，它提供了类似 Thonny 的简化工作流程，同时兼具 VSCode 强大的编辑环境。您可能指的是 **Pico-W-Go**（或类似的 **Pico-Go** 扩展），这是专为树莓派 Pico 和 Pico W 的 MicroPython 开发而设计的扩展。以下将指导您设置和使用 **Pico-W-Go** 扩展（最流行且持续维护的选项），将简单的 MicroPython 程序上传到 Pico，假设 MicroPython 已刷入（使用您已刷入的 `RPI_PICO-20250415-v1.25.0.uf2` 文件）。

---

### 前提条件
1. **已刷入 MicroPython**：您的 Pico 已安装 MicroPython，如您已刷入。
2. **已安装 VSCode**：确保已安装 VSCode（[code.visualstudio.com](https://code.visualstudio.com)）。
3. **已安装 Python**：Pico-W-Go 依赖项需要：
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```
4. **USB 连接**：Pico 通过支持数据传输的 USB 线缆连接。

---

### 在 VSCode 中使用树莓派 Pico (Pico-W-Go) 扩展的分步指南

1. **安装 Pico-W-Go 扩展**：
   - 打开 VSCode。
   - 进入扩展视图（`Ctrl+Shift+X` 或 macOS 上 `Cmd+Shift+X`）。
   - 搜索 **Pico-W-Go** 并安装（由 Paul Obermeier 等人开发）。
   - 注意：如果您指的是其他扩展（如 Pico-Go），请告知，但 Pico-W-Go 是 Pico MicroPython 开发最常用的扩展。

2. **安装 Pico-W-Go 依赖项**：
   - Pico-W-Go 需要 `pyserial` 和 `esptool` 用于串口通信和刷写：
     ```bash
     pip3 install pyserial esptool
     ```
   - 确保这些库安装在您的 Python 环境中（使用 `pip3 list` 验证）。

3. **配置 Pico-W-Go**：
   - 在 VSCode 中打开命令面板（`Ctrl+Shift+P` 或 `Cmd+Shift+P`）。
   - 输入并选择 **Pico-W-Go > Configure Project**。
   - 按照提示操作：
     - **串口**：选择 Pico 的串口（如 `/dev/ttyACM0`）。通过以下命令查找：
       ```bash
       ls /dev/tty*
       ```
       查找 `/dev/ttyACM0` 或类似名称，Pico 连接时会显示。
     - **解释器**：选择 MicroPython (Raspberry Pi Pico)。
     - **项目文件夹**：选择或创建项目文件夹（如 `~/PicoProjects/MyProject`）。
   - Pico-W-Go 会在项目文件夹中创建 `.picowgo` 配置文件以存储设置。

4. **编写简单的 MicroPython 程序**：
   - 在 VSCode 中打开项目文件夹（文件 > 打开文件夹）。
   - 创建名为 `main.py` 的新文件（MicroPython 启动时自动运行 `main.py`）。
   - 添加简单程序，例如闪烁板载 LED：
     ```python
     from machine import Pin
     import time

     led = Pin(25, Pin.OUT)  # Pico W 使用 "LED"
     while True:
         led.on()
         time.sleep(0.5)
         led.off()
         time.sleep(0.5)
     ```
   - 保存文件（`Ctrl+S`）。

5. **将程序上传到 Pico**：
   - 确保 Pico 已连接且选择了正确的串口（如有需要，重新运行 **Pico-W-Go > Configure Project**）。
   - 打开命令面板（`Ctrl+Shift+P`）。
   - 选择 **Pico-W-Go > Upload Project to Pico**。
     - 这将上传项目文件夹中的所有文件（如 `main.py`）到 Pico 的文件系统。
   - 或者，上传单个文件：
     - 在 VSCode 文件资源管理器中右键单击 `main.py`。
     - 选择 **Pico-W-Go > Upload File to Pico**。
   - 文件传输到 Pico 后，如果是 `main.py`，将在启动时自动运行。

6. **运行和测试程序**：
   - **自动执行**：如果上传了 `main.py`，重置 Pico（拔插 USB 线或按 RESET 按钮）。LED 应开始闪烁。
   - **手动执行**：
     - 打开命令面板并选择 **Pico-W-Go > Run**。
     - 这将在 Pico 上执行当前文件。
   - **使用 REPL**：
     - 打开命令面板并选择 **Pico-W-Go > Open REPL**。
     - REPL 将出现在 VSCode 的终端中，您可以在其中测试命令：
       ```python
       from machine import Pin
       led = Pin(25, Pin.OUT)
       led.on()
       ```
     - 按 `Ctrl+C` 停止 REPL 中运行的程序。

7. **管理 Pico 上的文件**：
   - **列出文件**：使用 **Pico-W-Go > Download Project from Pico** 查看或从 Pico 文件系统检索文件。
   - **删除文件**：打开命令面板并选择 **Pico-W-Go > Delete All Files** 清除 Pico 文件系统，或在 REPL 中使用：
     ```python
     import os
     os.remove('main.py')
     ```
   - **检查输出**：程序输出（如 `print` 语句）将显示在 REPL 或配置的 VSCode 终端中。

---

### 故障排除
- **未检测到串口**：
  - 运行 `ls /dev/tty*` 确认 Pico 的串口（如 `/dev/ttyACM0`）。
  - 确保 USB 线支持数据传输，并尝试其他端口。
  - 在 **Pico-W-Go > Configure Project** 中重新配置串口。
- **上传失败**：
  - 验证 `pyserial` 和 `esptool` 是否安装（`pip3 list`）。
  - 检查 MicroPython 是否运行（应可访问 REPL）。
  - 如有需要，重新进入 BOOTSEL 模式并复制 `.uf2` 文件以重新刷写 MicroPython。
- **LED 不闪烁**：
  - 确认正确的 GPIO 引脚（Pico 为 `25`，Pico W 为 `"LED"`）。
  - 在 REPL 中测试：
    ```python
    from machine import Pin
    led = Pin(25, Pin.OUT)
    led.on()
    ```
- **缺少 Pico-W-Go 命令**：确保扩展已安装并激活。如有需要，重启 VSCode。

---

### Pico-W-Go 在 VSCode 中的优势
- **集成工作流程**：在 VSCode 中结合代码编辑、文件管理和 REPL 访问。
- **高级功能**：利用 VSCode 的 Git 集成、扩展和自定义功能。
- **跨平台**：支持 Linux、Windows 和 macOS。

### 与 Thonny 相比的局限性
- 设置稍复杂（如安装 `pyserial`、配置串口）。
- REPL 集成可能不如 Thonny 的一体化界面流畅。
- 对首次使用 MicroPython 的用户不太友好。

---

### 替代扩展
如果您指的是其他扩展（如 **Pico-Go**），请注意 Pico-Go 是 Pico-W-Go 的旧版替代方案，功能或更新可能较少。设置类似，但推荐使用 Pico-W-Go，因为它积极开发且支持 Pico 和 Pico W。如果您使用其他特定扩展，请说明，我可以调整说明。

---

### 示例工作流程
1. 安装 Pico-W-Go 和依赖项。
2. 使用正确的串口（`/dev/ttyACM0`）配置项目。
3. 编写并保存带 LED 闪烁代码的 `main.py`。
4. 使用 **Pico-W-Go > Upload Project to Pico** 上传。
5. 重置 Pico 或使用 **Pico-W-Go > Run** 查看 LED 闪烁。
6. 使用 REPL 进行交互式测试或调试。

如果您需要有关特定 Pico-W-Go 命令、其他程序示例或故障排除（如串口问题、扩展错误）的帮助，请告知！
