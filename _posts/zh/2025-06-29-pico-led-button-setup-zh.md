---
audio: false
generated: true
lang: zh
layout: post
title: 树莓派Pico LED按钮配置
translated: true
type: note
---

要设置 Raspberry Pi Pico 运行提供的 MicroPython 代码（通过按钮控制 LED），请按照以下步骤操作：

### 硬件需求

- **Raspberry Pi Pico**（或 Pico W）
- **LED**（需搭配合适限流电阻，如 220–330 欧姆）
- **按压式开关**
- **跳线**
- **面包板**（可选，便于连接）
- **USB 数据线**（用于连接 Pico 与电脑）

### 硬件设置

1. **连接 LED**：
   - 将 LED 阳极（较长引脚）连接至 Pico 的 **GPIO 25**（物理引脚 30）
   - 将 LED 阴极（较短引脚）通过 220–330 欧姆限流电阻连接至 **接地（GND）** 引脚（如物理引脚 3）

2. **连接按钮**：
   - 将按压开关一端连接至 **GPIO 14**（物理引脚 19）
   - 将开关另一端连接至 **3.3V** 引脚（如物理引脚 36，3V3(OUT)）
   - 代码使用内部下拉电阻（`Pin.PULL_DOWN`），因此无需外接下拉电阻。当按钮按下时，GPIO 14 将读取高电平（1）；未按下时读取低电平（0）

3. **检查连接**：
   - 确保所有连接牢固。使用面包板或直接接线时，请仔细检查 LED 极性是否正确，电阻是否安装到位
   - 参考 Pico 引脚分布图（可在线获取或查阅 Pico 数据手册）确认引脚分配

### 软件设置

1. **在 Pico 上安装 MicroPython**：
   - 从 [MicroPython 官网](https://micropython.org/download/rp2-pico/) 下载最新版 Raspberry Pi Pico 的 MicroPython UF2 固件
   - 按住 **BOOTSEL** 键的同时通过 USB 数据线将 Pico 连接至电脑
   - Pico 将显示为 USB 驱动器（RPI-RP2）。将下载的 `.uf2` 文件拖入该驱动器
   - Pico 将自动重启并完成 MicroPython 安装

2. **配置开发环境**：
   - 安装兼容 MicroPython 的 IDE，推荐初学者使用 **Thonny**：
     - 从 [thonny.org](https://thonny.org) 下载并安装 Thonny
     - 在 Thonny 中进入 **工具 > 选项 > 解释器**，选择 **MicroPython (Raspberry Pi Pico)** 并选择对应端口（如 Windows 的 `COMx` 或 Linux/macOS 的 `/dev/ttyACM0`）
   - 也可使用 `rshell`、`ampy` 或搭载 MicroPython 扩展的 Visual Studio Code

3. **上传并运行代码**：
   - 将以下代码复制到名为 `main.py` 的文件中：

     ```python
     from machine import Pin
     import time

     led = Pin(25, Pin.OUT)
     button = Pin(14, Pin.IN, Pin.PULL_DOWN)

     while True:
         if button.value():
             led.on()
         else:
             led.off()
         time.sleep(0.05)
     ```

   - 在 Thonny 中：
     - 新建文件并粘贴代码，将其保存至 Pico 并命名为 `main.py`（MicroPython 启动时会自动运行 `main.py`）
     - 点击 **运行** 按钮或按 **F5** 上传并执行代码
   - 或使用 `ampy` 上传文件：

     ```bash
     ampy --port /dev/ttyACM0 put main.py
     ```

     请将 `/dev/ttyACM0` 替换为您的 Pico 端口号

4. **测试程序**：
   - 代码上传后，按下按钮时 LED 应点亮，松开时熄灭。`time.sleep(0.05)` 设置的 50ms 延迟可消除按键抖动并降低 CPU 负载

### 故障排除

- **LED 不亮**：
  - 检查 LED 极性（阳极接 GPIO 25，阴极经电阻接 GND）
  - 确认 GPIO 引脚（25）与代码和物理连接一致
  - 验证 LED 和电阻是否完好（可用万用表或其他电路测试）
- **按钮无响应**：
  - 确认 GPIO 14 连接正确，且按钮按下时与 3.3V 导通
  - 检查 `Pin.PULL_DOWN` 配置是否合适；若按钮采用其他接线方式（如连接 GND），需改用 `Pin.PULL_UP` 并反转逻辑（`if not button.value()`）
- **代码无法运行**：
  - 确保 MicroPython 安装正确
  - 确认文件以 `main.py` 命名保存在 Pico 中
  - 检查 USB 连接及 IDE 中的端口设置

### 注意事项

- 本代码假设按钮按下时 GPIO 14 与 3.3V 连接。若按钮连接至 GND，需修改代码使用 `Pin.PULL_UP` 并反转逻辑：

  ```python
  button = Pin(14, Pin.IN, Pin.PULL_UP)
  while True:
      if not button.value():  # 按钮按下 = 低电平
          led.on()
      else:
          led.off()
      time.sleep(0.05)
  ```

- 若出现按键抖动（LED 闪烁），可增加 `time.sleep` 数值或实施软件消抖
- Pico W 的设置完全相同，但需确保使用正确的 GPIO 引脚（引脚分布与 Pico 一致）

如需进一步说明或解决具体问题，请随时告知！
