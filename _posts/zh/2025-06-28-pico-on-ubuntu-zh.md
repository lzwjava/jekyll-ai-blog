---
audio: false
generated: true
lang: zh
layout: post
title: 在Ubuntu上配置树莓派Pico
translated: true
type: note
---

在 **Ubuntu** 系统上使用 **Raspberry Pi Pico**，需要搭建开发环境、安装必要软件并配置工具来对 Pico 进行编程。Pico 支持使用 **MicroPython**、**C/C++** 或 **CircuitPython** 进行编程。下文将针对最常用的配置方案，分别说明具体步骤和所需软件。

### 通用前提条件
- **Raspberry Pi Pico**（或 Pico W）及 USB 数据线（Pico 使用 Micro-USB 接口，Pico 2 使用 USB-C 接口）。
- **Ubuntu** 系统（例如 Ubuntu 20.04、22.04 或更新版本；本文说明以较新版本如 24.04 为准）。
- 熟悉终端基本操作。

### 方案一：使用 MicroPython 编程
MicroPython 是 Pico 最易上手的编程方式。这是一个为微控制器设计的轻量级 Python 实现。

#### 需安装的软件
1. **MicroPython 固件**
   - 从 [MicroPython 官网](https://micropython.org/download/rp2-pico/) 或 [Raspberry Pi Pico 页面](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html) 下载适用于 Raspberry Pi Pico 的最新 MicroPython UF2 固件文件。
   - 若使用 Pico W 或 Pico 2，请确保选择对应的固件（例如 Pico W 应选择 `rp2-pico-w`）。

2. **Python 3**
   - Ubuntu 通常预装 Python 3。可通过以下命令验证：
     ```bash
     python3 --version
     ```
   - 若未安装，请执行：
     ```bash
     sudo apt update
     sudo apt install python3 python3-pip
     ```

3. **Thonny IDE**（推荐初学者使用）
   - Thonny 是一款用于通过 MicroPython 对 Pico 编程的简易 IDE。
   - 安装 Thonny：
     ```bash
     sudo apt install thonny
     ```
   - 或使用 `pip` 安装最新版：
     ```bash
     pip3 install thonny
     ```

4. **可选：`picotool`（用于高级管理）**
   - 可用于管理 MicroPython 固件或检查 Pico 状态。
   - 安装 `picotool`：
     ```bash
     sudo apt install picotool
     ```

#### 设置步骤
1. **安装 MicroPython 固件**
   - 按住 Pico 上的 **BOOTSEL** 按钮，同时通过 USB 连接到 Ubuntu 电脑（此时 Pico 进入 bootloader 模式）。
   - Pico 将显示为一个 USB 存储设备（例如 `RPI-RP2`）。
   - 将下载的 MicroPython `.uf2` 文件拖放至 Pico 的存储设备中。Pico 将自动重启并完成 MicroPython 安装。

2. **配置 Thonny**
   - 打开 Thonny：在终端输入 `thonny` 或通过应用程序菜单启动。
   - 进入 **工具 > 选项 > 解释器**。
   - 选择 **MicroPython (Raspberry Pi Pico)** 作为解释器。
   - 选择正确的端口（例如 `/dev/ttyACM0`）。如需确认端口，可在终端运行 `ls /dev/tty*`。
   - 此时 Thonny 应已连接至 Pico，可开始编写并运行 Python 脚本。

3. **测试程序**
   - 在 Thonny 中编写简单脚本，例如：
     ```python
     from machine import Pin
     led = Pin(25, Pin.OUT)  # 板载 LED（Pico 对应 GP25）
     led.toggle()  # 切换 LED 亮/灭
     ```
   - 点击 **运行** 按钮，在 Pico 上执行代码。

4. **可选：使用 `picotool`**
   - 验证 Pico 状态：
     ```bash
     picotool info
     ```
   - 如需进入 bootloader 模式，请确保按住 BOOTSEL 按钮连接。

### 方案二：使用 C/C++ 编程
针对进阶用户，可使用官方 **Pico SDK** 通过 C/C++ 对 Pico 进行编程。

#### 需安装的软件
1. **Pico SDK 与工具链**
   - 安装构建 C/C++ 程序所需的工具：
     ```bash
     sudo apt update
     sudo apt install cmake gcc-arm-none-eabi libnewlib-arm-none-eabi build-essential git
     ```

2. **Pico SDK**
   - 克隆 Pico SDK 代码库：
     ```bash
     git clone -b master https://github.com/raspberrypi/pico-sdk.git
     cd pico-sdk
     git submodule update --init
     ```
   - 设置 `PICO_SDK_PATH` 环境变量：
     ```bash
     export PICO_SDK_PATH=~/pico-sdk
     echo 'export PICO_SDK_PATH=~/pico-sdk' >> ~/.bashrc
     ```

3. **可选：Pico 示例代码**
   - 克隆 Pico 示例代码库供参考：
     ```bash
     git clone -b master https://github.com/raspberrypi/pico-examples.git
     ```

4. **Visual Studio Code（可选）**
   - 为提升开发体验，可安装 VS Code：
     ```bash
     sudo snap install code --classic
     ```
   - 在 VS Code 中安装 **CMake Tools** 和 **C/C++** 扩展插件。

#### 设置步骤
1. **创建项目**
   - 为项目新建目录，例如 `my-pico-project`。
   - 从 `pico-examples` 复制示例 `CMakeLists.txt` 或自行创建：
     ```cmake
     cmake_minimum_required(VERSION 3.13)
     include($ENV{PICO_SDK_PATH}/pico_sdk_init.cmake)
     project(my_project C CXX ASM)
     pico_sdk_init()
     add_executable(my_project main.c)
     pico_add_extra_outputs(my_project)
     target_link_libraries(my_project pico_stdlib)
     ```
   - 编写简单的 C 程序（例如 `main.c`）：
     ```c
     #include "pico/stdlib.h"
     int main() {
         const uint LED_PIN = 25;
         gpio_init(LED_PIN);
         gpio_set_dir(LED_PIN, GPIO_OUT);
         while (true) {
             gpio_put(LED_PIN, 1);
             sleep_ms(500);
             gpio_put(LED_PIN, 0);
             sleep_ms(500);
         }
     }
     ```

2. **构建与烧录**
   - 进入项目目录：
     ```bash
     cd my-pico-project
     mkdir build && cd build
     cmake ..
     make
     ```
   - 此操作将生成 `.uf2` 文件（例如 `my_project.uf2`）。
   - 按住 Pico 的 **BOOTSEL** 按钮，通过 USB 连接电脑，然后将 `.uf2` 文件复制到 Pico 的存储设备：
     ```bash
     cp my_project.uf2 /media/$USER/RPI-RP2/
     ```

3. **调试（可选）**
   - 安装 `openocd` 用于调试：
     ```bash
     sudo apt install openocd
     ```
   - 使用调试器（例如将另一块 Pico 作为调试探针）并运行：
     ```bash
     openocd -f interface/raspberrypi-swd.cfg -f target/rp2040.cfg
     ```

### 方案三：使用 CircuitPython 编程
CircuitPython 是另一种基于 Python 的方案，与 MicroPython 类似但更侧重于 Adafruit 生态系统。

#### 需安装的软件
1. **CircuitPython 固件**
   - 从 [Adafruit CircuitPython 官网](https://circuitpython.org/board/raspberry_pi_pico/) 下载适用于 Pico 的 CircuitPython UF2 文件。
   - 若使用 Pico W 或 Pico 2，请选择对应固件。

2. **Python 3 及工具**
   - 与 MicroPython 要求相同（Python 3、Thonny 等）。

#### 设置步骤
1. **安装 CircuitPython 固件**
   - 与 MicroPython 类似：按住 **BOOTSEL** 按钮连接 Pico，然后将 CircuitPython `.uf2` 文件复制到 Pico 的存储设备。
   - Pico 将重启为一个名为 `CIRCUITPY` 的 USB 驱动器。

2. **使用 Thonny 或文本编辑器编程**
   - 参照 MicroPython 章节的方法使用 Thonny，选择 **CircuitPython** 作为解释器。
   - 或直接使用任意文本编辑器编辑 `CIRCUITPY` 驱动器中的 `code.py` 文件。
   - 示例 `code.py`：
     ```python
     import board
     import digitalio
     import time
     led = digitalio.DigitalInOut(board.LED)
     led.direction = digitalio.Direction.OUTPUT
     while True:
         led.value = True
         time.sleep(0.5)
         led.value = False
         time.sleep(0.5)
     ```

### 补充说明
- **权限设置**：如果无法访问 Pico 的端口（例如 `/dev/ttyACM0`），请将用户加入 `dialout` 组：
  ```bash
  sudo usermod -a -G dialout $USER
  ```
  需重新登录以生效。

- **Pico W 注意事项**：使用 Pico W 时请确保使用其专用固件（例如支持 Wi-Fi 的 MicroPython）。Wi-Fi 编程需要额外库，如 MicroPython 的 `network` 库。

- **Pico 2**：新版 Raspberry Pi Pico 2（搭载 RP2350）可能需要更新的固件或 SDK 版本。请查阅官方 Raspberry Pi 文档确认兼容性。

- **故障排除**：
  - 如果 Pico 未进入 bootloader 模式，请检查 USB 数据线（必须支持数据传输而非仅供电）。
  - 运行 `lsusb` 或 `dmesg` 确认 Ubuntu 是否识别 Pico。
  - 对于 C/C++ 构建，请确保正确设置 Pico SDK 路径。

### 推荐方案
- **初学者**：使用 **MicroPython 配合 Thonny**，简单快捷。
- **进阶用户**：使用 **C/C++ 配合 Pico SDK**，可获得更高性能及底层控制能力。
- **Adafruit 生态用户**：若计划使用 Adafruit 库或硬件，建议使用 **CircuitPython**。

如果您有特定项目或编程偏好需求，我可以进一步提供针对性指导！
