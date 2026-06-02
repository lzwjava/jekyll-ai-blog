---
audio: false
generated: true
lang: zh
layout: post
title: 检查Ubuntu系统对树莓派Pico的识别
translated: true
type: note
---

要检查 Raspberry Pi Pico 插入 Ubuntu 后是否被识别，请按以下步骤操作：

1. **检查 USB 设备**：
   - 打开终端并执行：

     ```bash
     lsusb
     ```

   - 查找包含 `Raspberry Pi Pico` 或供应商 ID 为 `2E8A`（树莓派供应商 ID）的设备条目。例如：

     ```
     Bus XXX Device XXX: ID 2e8a:0003 Raspberry Pi Pico
     ```

2. **检查串行端口**：
   - 若 Pico 处于 BOOTSEL 模式（用于固件烧录）或运行带串行输出的 MicroPython/Arduino 程序，请检查串行端口：

     ```bash
     ls /dev/tty*
     ```

   - 查找类似 `/dev/ttyACM0` 或 `/dev/ttyUSB0` 的设备。运行 MicroPython 时 Pico 通常显示为 `/dev/ttyACM0`

3. **检查磁盘设备（BOOTSEL 模式）**：
   - 若 Pico 处于 BOOTSEL 模式（插入时按住 BOOTSEL 按钮），它会显示为大容量存储设备。执行：

     ```bash
     lsblk
     ```

   - 查找带有挂载点且通常标记为 `RPI-RP2` 的设备，如 `/dev/sdb`（或类似名称）

4. **使用 `dmesg` 查看内核日志**：
   - 执行：

     ```bash
     dmesg | tail -n 20
     ```

   - 检查是否出现 Pico 被识别的信息，例如：

     ```
     [1234.567890] usb 1-1: New USB device found, idVendor=2e8a, idProduct=0003
     [1234.567891] usb 1-1: Product: Pico
     [1234.567892] cdc_acm 1-1:1.0: ttyACM0: USB ACM device
     ```

   - 这能确认 Pico 已被识别并分配端口（如 `ttyACM0`）

5. **MicroPython 测试（如已安装）**：
   - 若使用 MicroPython，请安装 `picocom` 或 `minicom` 工具：

     ```bash
     sudo apt install picocom
     ```

   - 连接 Pico 串行端口：

     ```bash
     picocom /dev/ttyACM0
     ```

   - 若识别成功，会看到 MicroPython 的 REPL 提示符 (>>>)。按 `Ctrl+C` 退出

**注意事项**：

- 请确保使用支持数据传输的优质 USB 线缆（而非仅供电线缆）
- BOOTSEL 模式下 Pico 显示为存储设备，而非串行设备
- 若未识别，请尝试更换 USB 端口、线缆，或检查驱动（如串行通信的 `cdc_acm`）是否加载：

  ```bash
  lsmod | grep cdc_acm
  ```

如果通过以上检查仍未发现 Pico，请提供更多详细信息（例如 Pico 的工作模式、当前操作目标），我将协助进一步排查问题！
