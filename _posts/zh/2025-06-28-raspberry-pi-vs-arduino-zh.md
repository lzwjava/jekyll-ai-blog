---
audio: false
generated: true
lang: zh
layout: post
title: 树莓派与Arduino在洗衣机监测及Telegram告警中的应用对比
translated: true
type: note
---

使用树莓派替代 Arduino（如 ESP32-CAM）来检测您的 Maytag MHW8630HW 洗衣机何时停止并发送 Telegram 通知是一个可行的替代方案，它以更高的复杂性和功耗为代价，提供了更强的处理能力和灵活性。下面，我将比较树莓派方案与 Arduino 方案，概述其他微控制器选项，并提供使用树莓派实现该系统的详细指南。我还将讨论替代方法（例如，其他硬件或传感器），以确保回答全面。

---

### 对比：树莓派 vs. Arduino vs. 其他选项

| **特性**                 | **树莓派**                                                                         | **Arduino (ESP32-CAM)**                                                  | **其他选项（例如，NodeMCU, ESP8266）**                           |
|--------------------------|------------------------------------------------------------------------------------|--------------------------------------------------------------------------|-----------------------------------------------------------------|
| **处理能力**             | 高（四核 CPU，1-8GB RAM）– 支持高级图像处理，OpenCV。                                | 有限（双核，520KB SRAM）– 仅支持基本图像处理。                             | 非常有限 – 不适合基于摄像头的处理。                               |
| **摄像头支持**           | 易于使用 USB 网络摄像头或 Pi Camera 模块（例如，8MP Pi Camera v2）。                | 内置 OV2640（2MP）摄像头，但分辨率和质量较低。                             | 需要外部摄像头模块，集成复杂。                                    |
| **Wi-Fi**                | 内置（大多数型号，例如 Pi 4, Zero 2 W）。                                           | 内置（ESP32-CAM）。                                                       | 内置（例如 ESP8266），但无原生摄像头支持。                         |
| **编程**                 | Python, OpenCV，灵活但需要操作系统设置（Raspberry Pi OS）。                         | Arduino IDE 中的 C++，对初学者更简单。                                    | C++ 或 Lua（例如 NodeMCU），图像处理库有限。                       |
| **功耗**                 | 较高（Pi Zero 约 2.5W，Pi 4 约 5-10W）。                                            | 较低（ESP32-CAM 约 1-2W）。                                               | 最低（ESP8266 约 0.5-1W）。                                       |
| **成本**                 | $10（Pi Zero W）到 $35+（Pi 4）+ $15（Pi Camera）。                               | ~$10（带摄像头的 ESP32-CAM）。                                            | ~$5-10（ESP8266/NodeMCU）+ 传感器成本。                           |
| **设置难度**             | 中等（操作系统设置，Python 编码）。                                                 | 简单（Arduino IDE，单个程序）。                                           | 简单传感器方案简单，摄像头方案复杂。                              |
| **最佳使用场景**         | 高级图像处理，未来扩展灵活（例如，ML 模型）。                                        | 简单的低成本光检测与 Telegram 集成。                                      | 非摄像头解决方案（例如，振动或电流传感器）。                       |

**树莓派优势**：
- 使用 OpenCV 进行卓越的图像处理，实现鲁棒的光检测。
- 更易于调试和扩展（例如，添加 Web 界面或多个传感器）。
- 支持更高质量的摄像头，在不同光照条件下提供更好的准确性。

**树莓派劣势**：
- 需要更多设置（操作系统安装，Python 环境）。
- 功耗较高，不太适合电池供电的设置。
- 比 ESP32-CAM 更昂贵。

**其他选项**：
- **NodeMCU/ESP8266**：适合非摄像头解决方案（例如，使用振动传感器或电流传感器）。有限的处理能力使得摄像头集成不切实际。
- **振动传感器**：检测机器振动而非面板灯。简单但可能错过细微的周期变化。
- **电流传感器**：测量功耗（例如，ACS712 模块）以检测机器何时停止。非侵入式但需要电气设置。

---

### 树莓派实现指南

#### 技术栈
**硬件**：
1. **树莓派**：
   - **Raspberry Pi Zero 2 W**（$15，紧凑，支持 Wi-Fi）或 **Raspberry Pi 4**（$35+，更强大）。
2. **摄像头**：
   - **Raspberry Pi Camera Module v2**（$15，8MP）或 USB 网络摄像头。
3. **电源**：
   - 5V USB-C（Pi 4）或 micro-USB（Pi Zero），输出 2-3A。
4. **安装**：
   - 外壳或粘性支架，用于将摄像头对准洗衣机的面板灯。

**软件**：
1. **操作系统**：Raspberry Pi OS（Lite 版更高效，Full 版设置更简单）。
2. **编程语言**：Python。
3. **库**：
   - **OpenCV**：用于图像处理以检测面板灯。
   - **python-telegram-bot**：用于 Telegram 通知。
   - **picamera2**（用于 Pi Camera）或 **fswebcam**（用于 USB 网络摄像头）。
4. **Telegram 机器人**：与 Arduino 设置相同（使用 BotFather 获取机器人令牌和聊天 ID）。

#### 算法
该算法与 Arduino 方法类似，但利用 OpenCV 进行更鲁棒的图像处理：
1. **图像捕获**：使用 Pi Camera 或网络摄像头定期捕获图像（例如，每 10 秒）。
2. **感兴趣区域（ROI）**：在图像中定义面板灯周围的矩形区域。
3. **图像处理**：
   - 转换为灰度图。
   - 应用高斯模糊以减少噪声。
   - 使用自适应阈值处理来检测背景中的明亮面板灯。
   - 计算 ROI 中的平均像素强度或计算明亮像素的数量。
4. **状态机**：
   - 如果 ROI 明亮（灯亮），标记机器为运行中。
   - 如果 ROI 变暗（灯灭）持续 5 分钟，标记机器为停止并发送 Telegram 通知。
5. **去抖动**：实现 5 分钟延迟以确认机器已停止。

#### 实现步骤
1. **设置树莓派**：
   - 使用 Raspberry Pi Imager 下载并将 **Raspberry Pi OS**（Lite 或 Full）刷入 SD 卡。
   - 通过编辑 `/etc/wpa_supplicant/wpa_supplicant.conf` 或使用 GUI 将 Pi 连接到 Wi-Fi。
   - 通过 `raspi-config` 启用摄像头接口（Interfacing Options > Camera）。

2. **安装依赖**：
   ```bash
   sudo apt update
   sudo apt install python3-opencv python3-picamera2 python3-pip
   pip3 install python-telegram-bot
   ```

3. **定位摄像头**：
   - 安装 Pi Camera 或 USB 网络摄像头，使其对准洗衣机的面板灯。
   - 使用以下命令测试摄像头：
     ```bash
     libcamera-still -o test.jpg
     ```
     或对于 USB 网络摄像头：
     ```bash
     fswebcam test.jpg
     ```

4. **Python 脚本**：
   以下是一个示例 Python 脚本，用于树莓派检测面板灯并发送 Telegram 通知。

```python
import cv2
import numpy as np
from picamera2 import Picamera2
import telegram
import asyncio
import time

# Telegram 机器人配置
BOT_TOKEN = "your_bot_token"
CHAT_ID = "your_chat_id"
bot = telegram.Bot(token=BOT_TOKEN)

# 摄像头配置
picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration(main={"size": (640, 480)}))
picam2.start()

# ROI 配置（根据摄像头视图调整）
ROI_X, ROI_Y, ROI_WIDTH, ROI_HEIGHT = 200, 150, 50, 50
THRESHOLD = 150  # 亮度阈值 (0-255)
STOP_DELAY = 300  # 5 分钟，以秒为单位

machine_running = False
last_on_time = 0

async def send_telegram_message(message):
    await bot.send_message(chat_id=CHAT_ID, text=message)

def is_light_on(frame):
    # 转换为灰度图
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 应用高斯模糊
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    # 提取 ROI
    roi = gray[ROI_Y:ROI_Y+ROI_HEIGHT, ROI_X:ROI_X+ROI_WIDTH]
    # 计算平均亮度
    avg_brightness = np.mean(roi)
    return avg_brightness > THRESHOLD

async def main():
    global machine_running, last_on_time
    while True:
        # 捕获图像
        frame = picam2.capture_array()
        # 检查灯是否亮
        if is_light_on(frame):
            if not machine_running:
                machine_running = True
                print("Machine is ON")
            last_on_time = time.time()
        else:
            if machine_running and (time.time() - last_on_time > STOP_DELAY):
                machine_running = False
                print("Machine stopped")
                await send_telegram_message("Washing machine stopped! Time to hang up clothes.")
        time.sleep(10)  # 每 10 秒检查一次

if __name__ == "__main__":
    asyncio.run(main())
```

5. **自定义脚本**：
   - 将 `BOT_TOKEN` 和 `CHAT_ID` 替换为您的 Telegram 凭据。
   - 通过捕获测试图像并使用 GIMP 或 Python 等工具分析来调整 `ROI_X`, `ROI_Y`, `ROI_WIDTH`, `ROI_HEIGHT`，以定位面板灯。
   - 根据测试图像调整 `THRESHOLD`（亮度越高，值越大）。
   - 如果需要，修改 `STOP_DELAY`。

6. **运行脚本**：
   ```bash
   python3 washer_monitor.py
   ```
   - 使用 `nohup python3 washer_monitor.py &` 在后台运行，或使用 systemd 服务以提高可靠性。

7. **测试和部署**：
   - 启动洗衣机并监控脚本输出。
   - 验证 Telegram 通知。
   - 将 Pi 和摄像头固定在永久设置中。

---

### 其他替代方案
1. **振动传感器**：
   - **硬件**：使用振动传感器（例如，SW-420）与 ESP8266 或树莓派。
   - **设置**：将传感器连接到洗衣机以检测振动。
   - **算法**：监控持续无振动（例如，5 分钟）以检测机器何时停止。
   - **优点**：简单，低成本，不受环境光影响。
   - **缺点**：可能错过有长暂停的周期（例如，浸泡）。
   - **代码示例（ESP8266）**：
     ```cpp
     #include <ESP8266WiFi.h>
     #include <UniversalTelegramBot.h>
     #define VIBRATION_PIN D5
     #define BOT_TOKEN "your_bot_token"
     #define CHAT_ID "your_chat_id"
     WiFiClientSecure client;
     UniversalTelegramBot bot(BOT_TOKEN, client);
     bool machineRunning = false;
     unsigned long lastVibrationTime = 0;
     void setup() {
       pinMode(VIBRATION_PIN, INPUT);
       WiFi.begin("ssid", "password");
       while (WiFi.status() != WL_CONNECTED) delay(500);
       client.setInsecure();
     }
     void loop() {
       if (digitalRead(VIBRATION_PIN)) {
         machineRunning = true;
         lastVibrationTime = millis();
       } else if (machineRunning && (millis() - lastVibrationTime > 300000)) {
         machineRunning = false;
         bot.sendMessage(CHAT_ID, "Washing machine stopped!", "");
       }
       delay(1000);
     }
     ```

2. **电流传感器**：
   - **硬件**：使用 ACS712 电流传感器与 ESP8266 或树莓派。
   - **设置**：非侵入式地将传感器夹在洗衣机的电源线上。
   - **算法**：检测电流降至阈值以下（例如，<0.5A）持续 5 分钟。
   - **优点**：准确，非侵入式。
   - **缺点**：需要电气知识，需校准机器的功耗。

3. **麦克风**：
   - **硬件**：使用麦克风模块（例如，KY-038）与树莓派。
   - **算法**：分析声音水平以检测机器噪音何时停止。
   - **优点**：非视觉，在低光条件下工作。
   - **缺点**：对环境噪声敏感，需要信号处理。

---

### 推荐
- **树莓派**：最适合鲁棒的图像处理和未来可扩展性。如果您熟悉 Python 并希望在不同光照条件下具有高可靠性，请使用此方案。
- **Arduino (ESP32-CAM)**：最适合低成本、简单的设置。如果您希望配置最少且满足于基本图像处理，这是理想选择。
- **振动或电流传感器**：最适合非摄像头解决方案，特别是当面板灯不可靠时（例如，昏暗或被遮挡）。与 ESP8266 一起使用以简化操作。
- **麦克风**：由于环境噪声，可靠性较低，但可作为辅助传感器。

对于您的两层住宅，由于您在二楼且需要通过 Telegram 进行可靠的远程通知，带有摄像头的树莓派或 ESP32-CAM 是理想选择。树莓派在光检测方面提供更好的准确性，而 ESP32-CAM 更便宜且部署更简单。如果您偏好非摄像头方案，带有 ESP8266 的振动传感器是最简单的替代方案。

如果您想深入了解任何特定方案、需要设置帮助或需要替代传感器的代码，请告诉我！
