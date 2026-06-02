---
audio: false
generated: true
lang: zh
layout: post
title: 通过UF2刷写Pico固件
translated: true
type: note
---

要通过将 `.uf2` 文件复制到 `RPI-RP2` 驱动器来将固件刷入 Raspberry Pi Pico（或基于 RP2040 的开发板）的 BOOTSEL 模式，请按照以下步骤操作：

### 逐步指南

1. **确认设备处于 BOOTSEL 模式**：
   - 当设备连接到计算机时，应显示为一个名为 `RPI-RP2` 的 USB 驱动器。这确认其处于 BOOTSEL 模式（如 `Bus 001 Device 009: ID 2e8a:0003 Raspberry Pi RP2 Boot` 所示）。
   - 如果未处于 BOOTSEL 模式，请拔下设备，按住 Pico 上的 BOOTSEL 按钮，然后在按住按钮的同时将其插入计算机的 USB 端口。几秒钟后释放按钮。

2. **获取有效的 `.uf2` 文件**：
   - **MicroPython**：从 [MicroPython 官网](https://micropython.org/download/rp2-pico/) 下载适用于 Raspberry Pi Pico 的最新 MicroPython 固件。选择 Pico 或 Pico W 的 `.uf2` 文件（例如 `rp2-pico-latest.uf2`）。
   - **CircuitPython**：从 [CircuitPython 官网](https://circuitpython.org/board/raspberry_pi_pico/) 下载适用于 Pico 或 Pico W 的 CircuitPython 固件。
   - **自定义程序**：如果您编写了程序（例如使用 Pico SDK 的 C/C++ 程序），请编译生成 `.uf2` 文件。例如，使用 Pico SDK 或 Arduino IDE 构建项目。
   - 将 `.uf2` 文件保存到计算机上易于访问的位置（例如桌面或下载文件夹）。

3. **定位 RPI-RP2 驱动器**：
   - 在计算机上打开文件资源管理器：
     - **Windows**：在“此电脑”下查找名为 `RPI-RP2` 的可移动驱动器。
     - **macOS**：驱动器应显示在桌面或 Finder 的“设备”下。
     - **Linux**：在 `/media` 或 `/mnt` 下检查，或使用 `lsblk` 列出连接的驱动器。
   - 如果驱动器未出现，请确保 USB 电缆支持数据传输（而非仅供电），并尝试不同的 USB 端口或电缆。

4. **将 `.uf2` 文件复制到 RPI-RP2 驱动器**：
   - 将 `.uf2` 文件拖放到 `RPI-RP2` 驱动器上，或使用文件资源管理器复制并粘贴。
   - 或者，使用终端命令（在 Linux/macOS 上）：

     ```bash
     cp /path/to/your/file.uf2 /media/your_username/RPI-RP2/
     ```

     将 `/path/to/your/file.uf2` 替换为您的 `.uf2` 文件路径，并根据需要调整挂载点。

5. **等待刷写过程完成**：
   - 复制 `.uf2` 文件后，Raspberry Pi Pico 会自动刷写固件。设备重启时，`RPI-RP2` 驱动器会消失（卸载），表示过程已完成。
   - 这通常需要几秒钟。在此期间请勿拔下设备。

6. **验证设备**：
   - 刷写后，Pico 应退出 BOOTSEL 模式并运行新固件。
   - 对于 MicroPython 或 CircuitPython，使用终端（例如 PuTTY、screen 或 Thonny IDE）通过 USB 串行端口（例如 Windows 上的 `COM3` 或 Linux/macOS 上的 `/dev/ttyACM0`）连接到设备。您应看到 Python REPL 提示符。
   - 对于自定义程序，检查预期行为（例如 LED 闪烁、串行输出等）。
   - 如果 `RPI-RP2` 驱动器重新出现，则刷写可能失败。请尝试使用不同的 `.uf2` 文件或检查硬件问题（例如 USB 电缆、闪存芯片）。

### 故障排除

- **驱动器未显示**：确保 Pico 处于 BOOTSEL 模式且 USB 电缆支持数据传输。尝试按住 BOOTSEL 按钮，然后在连接时短暂按下 RESET 按钮（如果可用）。
- **复制失败或驱动器重新出现**：`.uf2` 文件可能已损坏，或闪存可能存在故障。下载新的 `.uf2` 文件或使用最小化文件（如 MicroPython）进行测试。如果问题持续，使用 `picotool` 进行诊断：

  ```bash
  picotool info
  ```

  从 [Raspberry Pi Pico SDK](https://github.com/raspberrypi/picotool) 安装 `picotool`。
- **刷写后无响应**：如果使用 MicroPython/CircuitPython，请确保您的 IDE（例如 Thonny）设置为正确的串行端口。对于自定义程序，请验证代码是否正确编译。

### 示例：刷写 MicroPython

1. 从 [micropython.org](https://micropython.org/download/rp2-pico/) 下载 MicroPython 的 `.uf2` 文件。
2. 按住 BOOTSEL 按钮，插入 Pico，然后释放 BOOTSEL 按钮。
3. 打开文件资源管理器，找到 `RPI-RP2` 驱动器，并将 `.uf2` 文件复制到其中。
4. 等待驱动器消失。
5. 打开 Thonny IDE，选择 Pico 的串行端口，然后开始使用 MicroPython 编程。

如果您需要有关特定 `.uf2` 文件、工具或设置（例如安装 `picotool` 或使用 Thonny）的帮助，请告诉我！
