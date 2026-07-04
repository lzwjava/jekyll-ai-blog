---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Linux Mint上的Arduino Uno
translated: true
type: note
---

**问题：** 我能否在 Linux Mint 上为 Arduino Uno 进行开发？

**答案：**

可以，完全支持。Linux Mint（基于 Ubuntu）可以直接与 Uno 配合使用——该板本身在 ATmega328P 上运行自己的固件；你的 Mint 机器只是作为编译和通过 USB 烧录的主机。

有两种设置方式：

**选项 1 — Arduino IDE 2.x（最快捷）：**

```bash
# 从 arduino.cc 下载 AppImage，然后：
chmod +x arduino-ide_*.AppImage
./arduino-ide_*.AppImage

# 关键：将自己添加到 dialout 组以获取串口访问权限
sudo usermod -aG dialout $USER
# 注销并重新登录使其生效
```

**选项 2 — arduino-cli（终端优先，更适合你的工作流程）：**

```bash
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
export PATH=$PATH:~/bin

arduino-cli core update-index
arduino-cli core install arduino:avr

# 编译并烧录一个 sketch
arduino-cli compile --fqbn arduino:avr:uno blink/
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:uno blink/

# 串口监视器
arduino-cli monitor -p /dev/ttyACM0 -c baudrate=9600
```

Uno 会识别为 `/dev/ttyACM0`（正品板，ATmega16U2 USB 芯片）或 `/dev/ttyUSB0`（CH340 克隆板——驱动已包含在主内核中，无需安装）。插入后可用 `ls /dev/tty{ACM,USB}*` 检查。

在 Mint 上唯一常见的陷阱：`brltty`（盲文显示器守护进程）有时会占用 CH340 克隆板。如果端口在插入后立即消失：

```bash
sudo apt remove brltty
```

由于你偏向终端操作，`arduino-cli` + Makefile（或仅使用 shell 别名）是简洁的路径——完全不需要 GUI，并且可以轻松集成到代理工作流中。
