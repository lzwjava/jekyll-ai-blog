---
audio: false
generated: true
lang: zh
layout: post
title: 将MicroPython上传至Pico
translated: true
type: note
---

将 MicroPython 刷入 Raspberry Pi Pico（使用前文所述的 `.uf2` 文件）后，您可以使用 Thonny IDE 等工具上传并运行简单的 MicroPython 程序。该工具对初学者友好，被广泛用于 MicroPython 开发。以下是设置 MicroPython 并向 Pico 上传简单程序的步骤。

---

### 准备工作

1. **已刷入 MicroPython**：您已将 `RPI_PICO-20250415-v1.25.0.uf2` 复制到 `RPI-RP2` 驱动器，且 Pico 已重启（`RPI-RP2` 驱动器应不再显示）。
2. **USB 连接**：Pico 通过支持数据传输的 USB 线连接到计算机。
3. **Thonny IDE**：如未安装请先安装：
   - **Linux**：通过包管理器安装或从 [thonny.org](https://thonny.org) 下载：

     ```bash
     sudo apt update
     sudo apt install thonny
     ```

   - 或使用 `pip` 安装：

     ```bash
     pip install thonny
     ```

   - Windows/macOS 用户请从 [thonny.org](https://thonny.org) 下载安装。

---

### 上传简单 MicroPython 程序的步骤详解

1. **连接 Pico 并打开 Thonny**：
   - 将 Pico 插入计算机的 USB 端口。
   - 打开 Thonny IDE。

2. **配置 Thonny 以使用 MicroPython**：
   - 在 Thonny 中进入 **工具 > 选项 > 解释器**（或 **运行 > 选择解释器**）。
   - 从解释器下拉菜单中选择 **MicroPython (Raspberry Pi Pico)**。
   - 如果未自动识别 Pico 的串行端口（例如 Linux 系统中的 `/dev/ttyACM0`）：
     - 在下拉菜单中检查可用端口，或在终端中运行 `ls /dev/tty*` 识别 Pico 端口（通常为 `/dev/ttyACM0` 或类似名称）。
     - 手动选择正确端口。
   - 点击 **确定** 保存。

3. **验证 MicroPython 运行状态**：
   - 在 Thonny 的 **Shell** 面板中应看到 MicroPython REPL 提示符：

     ```
     >>>
     ```

   - 输入简单命令进行测试，例如：

     ```python
     print("Hello, Pico!")
     ```

     按回车键后，将在 Shell 中看到输出内容。

4. **编写简单 MicroPython 程序**：
   - 在 Thonny 主编辑器中创建新文件并编写程序。例如控制 Pico 板载 LED 闪烁的程序（Pico 使用 GPIO 25，Pico W 使用 "LED"）：

     ```python
     from machine import Pin
     import time

     # 初始化板载 LED
     led = Pin(25, Pin.OUT)  # Pico W 请使用 Pin("LED", Pin.OUT)

     # LED 闪烁逻辑
     while True:
         led.on()           # 开启 LED
         time.sleep(0.5)    # 等待 0.5 秒
         led.off()          # 关闭 LED
         time.sleep(0.5)    # 等待 0.5 秒
     ```

   - 注意：若使用 Pico W，请将 `Pin(25, Pin.OUT)` 替换为 `Pin("LED", Pin.OUT)`。

5. **将程序保存至 Pico**：
   - 点击 **文件 > 另存为**。
   - 在对话框中选择 **Raspberry Pi Pico** 作为保存目标（非计算机本地）。
   - 将文件命名为 `main.py`（MicroPython 启动时会自动运行该文件）或其他名称如 `blink.py`。
   - 点击 **确定** 将文件保存至 Pico 文件系统。

6. **运行程序**：
   - 点击 Thonny 中的绿色 **运行** 按钮（或按 **F5**）执行程序。
   - 若保存为 `main.py`，重置 Pico（拔插 USB 或按 RESET 按钮）后程序将自动运行。
   - 此时应观察到板载 LED 以 0.5 秒间隔闪烁。

7. **停止程序**（如需要）：
   - 在 Thonny 的 Shell 中按 **Ctrl+C** 可中断运行中的脚本。
   - 如需取消 `main.py` 的自动运行，请从 Pico 中删除该文件：
     - 在 Thonny 中进入 **视图 > 文件**，选择 Pico 文件系统，右键点击 `main.py` 后选择 **删除**。

---

### 测试与故障排除

- **无 REPL 提示符**：若 Thonny 未显示 MicroPython REPL：
  - 检查解释器设置中是否选对端口。
  - 确认 MicroPython 刷入成功。若失败请重新刷入 `.uf2` 文件。
  - 检查 USB 线（需支持数据传输）并尝试更换端口。
- **LED 未闪烁**：确认使用正确的 GPIO 引脚（Pico 为 `25`，Pico W 为 `"LED"`）。如仍无效，可通过 REPL 命令测试 LED：

  ```python
  from machine import Pin
  led = Pin(25, Pin.OUT)
  led.on()
  ```

- **文件保存失败**：确认 Thonny 已连接 Pico 且解释器设置为 MicroPython (Raspberry Pi Pico)。

---

### 补充提示

- **使用其他工具**：除 Thonny 外，还可使用 `rshell` 或 `ampy` 管理 Pico 文件：

  ```bash
  pip install rshell
  rshell --port /dev/ttyACM0
  cp blink.py /pyboard/main.py
  ```

- **更多示例程序**：
  - 读取按钮状态（例如 GPIO 14）：

    ```python
    from machine import Pin
    button = Pin(14, Pin.IN, Pin.PULL_UP)
    while True:
        print(button.value())
    ```

  - 通过调整 GPIO 引脚编号控制外部 LED 或其他外设。
- **自动运行**：将文件保存为 `main.py` 可使其在启动时自动运行。使用 `boot.py` 存放先于 `main.py` 执行的初始化代码。

如果您遇到具体问题（如端口识别异常、Thonny 报错或硬件问题），或想尝试其他程序，请随时告知，我将进一步指导！
