---
audio: false
generated: true
lang: zh
layout: post
title: 基于Arduino与Telegram提醒的智能洗衣机监控器
translated: true
type: note
---

要创建一个系统来检测您的 Maytag MHW8630HW 洗衣机何时停止（使用其面板灯作为指示器），并通过 Telegram 机器人通知您挂起衣物，您可以使用带有摄像头模块的 Arduino 来监控洗衣机的状态。以下是关于技术栈、硬件设置、算法和实现步骤的详细指南。

---

### 技术栈

#### 硬件

1. **Arduino 板**：
   - **ESP32-CAM**（推荐）– 结合了微控制器与内置的 OV2640 摄像头和 Wi-Fi 功能，非常适合图像处理和 Telegram 集成。
   - 替代方案：Arduino Uno + 独立的摄像头模块（例如 OV7670）和用于 Wi-Fi 的 ESP8266，但设置更复杂。
2. **摄像头模块**：
   - OV2640（随 ESP32-CAM 附带）– 2MP 摄像头，足以检测面板灯。
3. **光线传感器（可选）**：
   - 光敏电阻（LDR）或 TSL2561 – 用于补充基于摄像头的灯光检测，以实现冗余或更简单的设置。
4. **电源供应**：
   - 5V USB 电源适配器或电池组，用于 ESP32-CAM。
5. **安装**：
   - 小型外壳或 3D 打印盒，用于固定 ESP32-CAM，并确保其清晰视野对准洗衣机的控制面板。
6. **Wi-Fi 路由器**：
   - 用于 ESP32-CAM 连接到互联网并与 Telegram 机器人通信。

#### 软件

1. **Arduino IDE**：
   - 用于编程 ESP32-CAM。
2. **库**：
   - **Universal Arduino Telegram Bot Library** by Brian Lough – 用于 Telegram 机器人集成。
   - **ArduinoJson** – 用于处理 Telegram API 通信的 JSON 数据。
   - **ESP32-CAM Camera Libraries** – 用于捕获和处理图像的内置库。
3. **Telegram 机器人**：
   - 在 Telegram 上使用 BotFather 创建机器人，并获取机器人令牌和聊天 ID。
4. **编程语言**：
   - C++（Arduino 草图）。
5. **可选工具**：
   - OpenCV（Python）用于在将图像处理算法移植到 Arduino 之前在计算机上进行原型设计（针对 ESP32-CAM 进行了简化）。

---

### 检测洗衣机状态的算法

由于 Maytag MHW8630HW 有一个面板灯指示机器是否开启，您可以使用摄像头来检测此灯光。该算法将处理图像以确定灯光是开启还是关闭，从而指示机器的状态。

#### 检测算法

1. **图像捕获**：
   - 使用 ESP32-CAM 定期捕获洗衣机控制面板的图像。
2. **感兴趣区域（ROI）选择**：
   - 在图像中定义面板灯所在的特定区域（例如，围绕电源指示灯的矩形区域）。
3. **图像处理**：
   - **灰度转换**：将捕获的图像转换为灰度以简化处理。
   - **阈值处理**：应用亮度阈值来检测灯光的存在。面板灯在开启时会产生一个亮斑，而在关闭时则是一个较暗的区域。
   - **像素强度分析**：计算 ROI 中的平均像素强度。高强度表示灯光开启，低强度表示关闭。
4. **状态机**：
   - 基于连续读数跟踪机器的状态（开启或关闭）。
   - 如果灯光在多个周期内被检测为开启，则假定机器正在运行。
   - 如果灯光转换为关闭并保持关闭状态一段时间（例如 5 分钟），则假定洗涤周期已完成。
5. **去抖动**：
   - 实施延迟（例如 5 分钟）以确认机器已停止，避免在洗涤周期暂停期间（例如浸泡或注水）产生误通知。
6. **通知**：
   - 当确认机器停止时，发送 Telegram 消息（例如，“洗衣机已停止！该挂起衣物了。”）。

#### 为什么不使用更复杂的算法？

- 高级算法如机器学习（例如用于对象检测的 CNN）对于此任务来说过于复杂，并且对于 ESP32-CAM 有限的处理能力来说资源密集。
- 简单的阈值处理就足够了，因为面板灯是一个清晰的二进制指示器（开启/关闭）。

---

### 实现指南

#### 步骤 1：设置 Telegram 机器人

1. **创建 Telegram 机器人**：
   - 打开 Telegram，搜索 **@BotFather**，并开始聊天。
   - 发送 `/newbot`，为您的机器人命名（例如 “WasherBot”），并获取 **机器人令牌**。
   - 向您的机器人发送 `/start`，并使用像 `@GetIDsBot` 这样的服务或通过检查代码中的传入消息来获取您的 **聊天 ID**。
2. **在手机上安装 Telegram**：
   - 确保您可以接收来自机器人的消息。

#### 步骤 2：硬件设置

1. **定位 ESP32-CAM**：
   - 将 ESP32-CAM 安装在一个小型外壳中或用胶带固定，使其面向洗衣机的控制面板。
   - 确保摄像头对面板灯有清晰的视野（用样张照片测试）。
   - 固定设置以避免移动，因为这可能会影响 ROI 的一致性。
2. **为 ESP32-CAM 供电**：
   - 将 5V USB 电源适配器或电池组连接到 ESP32-CAM 的 5V 引脚。
   - 确保电源稳定，因为摄像头和 Wi-Fi 会消耗大量电力。
3. **可选的光线传感器**：
   - 如果使用光敏电阻，请将其连接到 ESP32-CAM 的模拟引脚（例如 GPIO 4），并配备分压电路（例如 10kΩ 电阻接地）。

#### 步骤 3：软件设置

1. **安装 Arduino IDE**：
   - 从 [arduino.cc](https://www.arduino.cc/en/software) 下载并安装 Arduino IDE。
2. **添加 ESP32 板支持**：
   - 在 Arduino IDE 中，转到 **文件 > 首选项**，将以下 URL 添加到附加开发板管理器网址：

     ```
     https://raw.githubusercontent.com/espressif/arduino-esp32/master/package_esp32_index.json
     ```

   - 转到 **工具 > 开发板 > 开发板管理器**，搜索 “ESP32”，并安装 ESP32 包。
3. **安装库**：
   - 安装 **Universal Arduino Telegram Bot Library**：
     - 从 [GitHub](https://github.com/witnessmenow/Universal-Arduino-Telegram-Bot) 下载，并通过 **草图 > 包含库 > 添加 .ZIP 库** 添加。
   - 安装 **ArduinoJson**：
     - 转到 **草图 > 包含库 > 管理库**，搜索 “ArduinoJson”，并安装 6.x.x 版本。
4. **配置 Wi-Fi**：
   - 确保您的 ESP32-CAM 可以连接到您的家庭 Wi-Fi 网络（2.4GHz，因为不支持 5GHz）。

#### 步骤 4：编写 Arduino 代码

以下是一个示例 Arduino 草图，用于 ESP32-CAM 检测面板灯并发送 Telegram 通知。此代码假定您已确定面板灯的 ROI 坐标。

```cpp
#include <WiFi.h>
#include <UniversalTelegramBot.h>
#include <ArduinoJson.h>
#include "esp_camera.h"

// Wi-Fi 凭据
#define WIFI_SSID "您的_wifi_ssid"
#define WIFI_PASSWORD "您的_wifi_密码"

// Telegram 机器人凭据
#define BOT_TOKEN "您的_bot_token"
#define CHAT_ID "您的_chat_id"

// 摄像头配置（用于 ESP32-CAM）
#define PWDN_GPIO_NUM 32
#define RESET_GPIO_NUM -1
#define XCLK_GPIO_NUM 0
#define SIOD_GPIO_NUM 26
#define SIOC_GPIO_NUM 27
#define Y9_GPIO_NUM 35
#define Y8_GPIO_NUM 34
#define Y7_GPIO_NUM 39
#define Y6_GPIO_NUM 36
#define Y5_GPIO_NUM 21
#define Y4_GPIO_NUM 19
#define Y3_GPIO_NUM 18
#define Y2_GPIO_NUM 5
#define VSYNC_GPIO_NUM 25
#define HREF_GPIO_NUM 23
#define PCLK_GPIO_NUM 22

WiFiClientSecure client;
UniversalTelegramBot bot(BOT_TOKEN, client);

#define ROI_X 100 // 根据摄像头视野调整（ROI 的 x 坐标）
#define ROI_Y 100 // ROI 的 y 坐标
#define ROI_WIDTH 50 // ROI 的宽度
#define ROI_HEIGHT 50 // ROI 的高度
#define THRESHOLD 150 // 亮度阈值（0-255）
#define STOP_DELAY 300000 // 5 分钟，以毫秒为单位

bool machineRunning = false;
unsigned long lastOnTime = 0;

void setup() {
  Serial.begin(115200);

  // 初始化摄像头
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_GRAYSCALE; // 灰度以简化处理
  config.frame_size = FRAMESIZE_QVGA; // 320x240
  config.jpeg_quality = 12;
  config.fb_count = 1;

  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("摄像头初始化失败，错误代码 0x%x", err);
    return;
  }

  // 连接到 Wi-Fi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi 已连接");

  // 配置 Telegram 客户端
  client.setInsecure(); // 为简化起见；在生产环境中考虑使用适当的 SSL
}

void loop() {
  // 捕获图像
  camera_fb_t *fb = esp_camera_framebuffer_get();
  if (!fb) {
    Serial.println("摄像头捕获失败");
    return;
  }

  // 计算 ROI 中的平均亮度
  uint32_t totalBrightness = 0;
  uint16_t pixelCount = 0;
  for (int y = ROI_Y; y < ROI_Y + ROI_HEIGHT; y++) {
    for (int x = ROI_X; x < ROI_X + ROI_WIDTH; x++) {
      if (x < fb->width && y < fb->height) {
        totalBrightness += fb->buf[y * fb->width + x];
        pixelCount++;
      }
    }
  }
  esp_camera_framebuffer_return(fb);

  float avgBrightness = pixelCount > 0 ? (float)totalBrightness / pixelCount : 0;

  // 状态机
  if (avgBrightness > THRESHOLD) {
    if (!machineRunning) {
      machineRunning = true;
      Serial.println("机器已开启");
    }
    lastOnTime = millis();
  } else {
    if (machineRunning && (millis() - lastOnTime > STOP_DELAY)) {
      machineRunning = false;
      Serial.println("机器已停止");
      bot.sendMessage(CHAT_ID, "洗衣机已停止！该挂起衣物了。", "");
    }
  }

  delay(10000); // 每 10 秒检查一次
}
```

#### 步骤 5：自定义代码

1. **更新凭据**：
   - 将 `您的_wifi_ssid`、`您的_wifi_密码`、`您的_bot_token` 和 `您的_chat_id` 替换为实际值。
2. **调整 ROI 和阈值**：
   - 使用 ESP32-CAM 捕获测试图像（修改代码以将图像保存到 SD 卡或流式传输）。
   - 通过分析图像确定 ROI 坐标（`ROI_X`、`ROI_Y`、`ROI_WIDTH`、`ROI_HEIGHT`），以聚焦于面板灯。
   - 根据测试图像调整 `THRESHOLD`（例如，开启时更亮，关闭时更暗）。
3. **调整 `STOP_DELAY`**：
   - 设置为 300000（5 分钟）以避免在周期暂停期间产生误通知。

#### 步骤 6：测试和部署

1. **上传代码**：
   - 通过 USB 转串口适配器（例如 FTDI 模块）将 ESP32-CAM 连接到计算机。
   - 在 Arduino IDE 中选择 **ESP32 Wrover Module** 并上传草图。
2. **测试系统**：
   - 启动洗衣机并监控串行监视器以获取状态变化。
   - 验证机器停止时的 Telegram 通知。
3. **微调**：
   - 如果出现误报/漏报，调整 ROI、阈值或延迟。
4. **永久安装**：
   - 将 ESP32-CAM 固定在其外壳中，并确保电源供应稳定。

---

### 替代方法：光线传感器

如果基于摄像头的检测过于复杂或不可靠（例如由于环境光线），请使用光敏电阻：

- **设置**：将光敏电阻连接到面板灯（例如用胶带），并将其连接到模拟引脚。
- **代码修改**：用模拟读数替换图像处理：

  ```cpp
  int lightValue = analogRead(A0); // 光敏电阻连接至 GPIO 4
  if (lightValue > 500) { // 调整阈值
    machineRunning = true;
    lastOnTime = millis();
  } else if (machineRunning && (millis() - lastOnTime > STOP_DELAY)) {
    machineRunning = false;
    bot.sendMessage(CHAT_ID, "洗衣机已停止！该挂起衣物了。", "");
  }
  ```

- **优点**：更简单，资源消耗更少。
- **缺点**：需要物理连接到灯光，灵活性较差。

---

### 注意事项

- **功耗**：ESP32-CAM 在使用摄像头和 Wi-Fi 时会消耗大量电力。请确保使用可靠的电源。
- **环境光线**：基于摄像头的检测可能会受到室内光线的影响。在各种条件下测试或使用光线传感器以提高鲁棒性。
- **安全性**：示例代码为简化起见使用了 `setInsecure()`。对于生产环境，请为 Telegram 通信配置适当的 SSL 证书。
- **参考资料**：此方法受到诸如使用振动传感器的 ESP32-CAM Telegram 安全系统和洗衣监控器等项目的启发，并针对基于灯光的检测进行了调整。[](https://www.instructables.com/Home-Security-System-Using-ESP32-CAM-and-Telegram-/)[](https://www.instructables.com/Arduino-Washer-Dryer-Alert-Push-Notification-to-Ph/)

---

### 故障排除

- **摄像头初始化失败**：检查接线，确保电源充足，并验证摄像头配置。
- **Wi-Fi 连接问题**：确认 2.4GHz Wi-Fi 和正确的凭据。
- **没有 Telegram 消息**：验证机器人令牌和聊天 ID，检查串行监视器以获取错误信息。
- **误通知**：调整 `THRESHOLD` 或 `STOP_DELAY` 以考虑周期暂停。

此解决方案利用 ESP32-CAM 的功能，提供了一种经济高效、非侵入性的方式来监控您的洗衣机并通过 Telegram 通知您。如果您在具体步骤或调试方面需要帮助，请告诉我！
