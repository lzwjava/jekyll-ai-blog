---
audio: false
generated: true
lang: zh
layout: post
title: 基于声音的美泰克洗衣机检测
translated: true
type: note
---

使用声音检测您的Maytag MHW8630HW洗衣机何时停止工作，是基于摄像头方案的可行替代方案。通过将声音传感器靠近洗衣机放置，您可以监测运行期间产生的噪音（例如电机嗡鸣、水流或滚筒转动），并在声音停止时检测到洗涤周期结束。下面我将说明如何调整之前的项目，改用声音传感器而非摄像头，重点关注硬件、算法和代码变更，同时保留Telegram通知系统。

---

### 技术栈

#### 硬件

1. **Arduino开发板**：
   - **ESP32-CAM**（仍可使用）– 保留Wi-Fi功能用于Telegram集成，尽管不需要摄像头。
   - 替代方案：**ESP8266 NodeMCU** 或带ESP8266模块的 **Arduino Uno**（如果不需要摄像头，更简单）。
2. **声音传感器**：
   - **KY-038麦克风声音传感器** 或类似产品 – 价格实惠，通过模拟输出检测声音级别。
   - 替代方案：**MAX9814驻极体麦克风放大器** – 更灵敏，带可调增益，检测效果更好。
3. **电源**：
   - 用于ESP32或其他开发板的5V USB电源适配器或电池组。
4. **安装**：
   - 将声音传感器靠近洗衣机放置（例如粘贴在侧面或顶部），使其能够检测运行声音，但避免直接接触水。
   - 使用小型外壳保护传感器和开发板。
5. **Wi-Fi路由器**：
   - 用于互联网连接以发送Telegram通知。

#### 软件

- **Arduino IDE**：用于编程ESP32或其他开发板。
- **库**：
  - **Universal Arduino Telegram Bot Library** by Brian Lough – 用于Telegram集成。
  - **ArduinoJson** – 用于处理Telegram API通信中的JSON数据。
- **Telegram Bot**：与之前相同，使用BotFather获取机器人令牌和聊天ID。
- **编程语言**：C++（Arduino草图）。

---

### 使用声音检测洗衣机状态的算法

声音传感器将检测洗衣机产生的噪音级别。当洗衣机运行时，它会产生持续的声音（例如电机、水流或滚筒声）。当它停止时，声音级别显著下降。该算法处理这些声音级别以确定机器的状态。

#### 检测算法

1. **声音采样**：
   - 持续读取声音传感器的模拟输出以测量噪音级别。
2. **信号处理**：
   - **平均化**：在短时间窗口（例如1-2秒）内计算平均声音级别，以平滑瞬态噪音（例如门砰击声）。
   - **阈值化**：将平均声音级别与预定义阈值进行比较。高级别表示机器正在运行，而低级别表示已停止。
3. **状态机**：
   - 根据声音级别跟踪机器的状态（开启或关闭）。
   - 如果声音级别在多个周期内超过阈值，则假定机器正在运行。
   - 如果声音级别降至阈值以下并保持低位一段时间（例如5分钟），则假定洗涤周期完成。
4. **去抖动**：
   - 实施延迟（例如5分钟）以确认机器已停止，避免在静默阶段（例如浸泡或周期暂停）产生误通知。
5. **通知**：
   - 当确认机器停止时，发送Telegram消息（例如“洗衣机已停止！该晾衣服了。”）。

#### 为什么使用声音检测？

- 声音检测比图像处理更简单，因为它不需要复杂的算法或高计算资源。
- 与基于摄像头的检测相比，它对环境光线变化不太敏感。
- 然而，它可能受到背景噪音（例如大声的电视）的影响，因此放置和阈值调校至关重要。

---

### 实施指南

#### 步骤1：设置Telegram机器人

- 按照原始指南中的相同步骤操作：
  - 使用 **@BotFather** 创建一个机器人以获取 **机器人令牌**。
  - 使用 **@GetIDsBot** 或检查传入消息获取您的 **聊天ID**。
  - 确保在手机上设置Telegram以接收通知。

#### 步骤2：硬件设置

1. **选择声音传感器**：
   - **KY-038**：提供与声音强度成比例的模拟输出（对于ESP32的10位ADC为0-1023）。它还有一个数字输出，但模拟输出更适合细微检测。
   - **MAX9814**：更灵敏，带可通过电位器调节的增益。连接到模拟引脚。
2. **连接声音传感器**：
   - 对于KY-038：
     - **VCC** 连接到5V（或3.3V，取决于开发板）。
     - **GND** 连接到GND。
     - **模拟输出（A0）** 连接到ESP32的模拟引脚（例如GPIO 4）。
   - 对于MAX9814：
     - 类似连接，但使用板载电位器调整增益以获得最佳灵敏度。
3. **放置传感器**：
   - 将传感器靠近洗衣机放置（例如在侧面或顶部），使其能够检测电机或滚筒噪音。避免有水暴露的区域。
   - 在洗涤周期期间通过监测声音级别测试放置位置（使用串行监视器记录值）。
4. **为开发板供电**：
   - 将5V USB电源适配器或电池组连接到ESP32或其他开发板。
   - 确保电源稳定，因为Wi-Fi通信需要一致的电压。
5. **安装**：
   - 使用小型外壳或胶带固定传感器和开发板，确保麦克风暴露以捕捉声音。

#### 步骤3：软件设置

- **Arduino IDE**：按照原始指南中的说明安装。
- **ESP32开发板支持**：通过开发板管理器添加ESP32开发板包（与之前相同的URL）。
- **库**：
  - 按照说明安装 **Universal Arduino Telegram Bot Library** 和 **ArduinoJson**。
- **Wi-Fi**：确保开发板可以连接到您的2.4GHz Wi-Fi网络。

#### 步骤4：编写Arduino代码

以下是用于ESP32（或ESP8266）的示例Arduino草图，用于检测声音级别并发送Telegram通知。假设KY-038声音传感器连接到GPIO 4。

```cpp
#include <WiFi.h>
#include <UniversalTelegramBot.h>
#include <ArduinoJson.h>

// Wi-Fi凭据
#define WIFI_SSID "您的Wi-Fi名称"
#define WIFI_PASSWORD "您的Wi-Fi密码"

// Telegram机器人凭据
#define BOT_TOKEN "您的机器人令牌"
#define CHAT_ID "您的聊天ID"

// 声音传感器引脚
#define SOUND_PIN 4 // 用于模拟输入的GPIO 4

// 声音检测参数
#define SOUND_THRESHOLD 300 // 根据测试调整（0-1023）
#define SAMPLE_WINDOW 2000 // 2秒用于平均
#define STOP_DELAY 300000 // 5分钟，以毫秒为单位

WiFiClientSecure client;
UniversalTelegramBot bot(BOT_TOKEN, client);

bool machineRunning = false;
unsigned long lastOnTime = 0;

void setup() {
  Serial.begin(115200);

  // 连接到Wi-Fi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi已连接");

  // 配置Telegram客户端
  client.setInsecure(); // 为简化起见；在生产环境中考虑使用适当的SSL

  // 设置声音传感器引脚
  pinMode(SOUND_PIN, INPUT);
}

void loop() {
  // 在窗口内采样声音级别
  unsigned long startMillis = millis();
  uint32_t totalSound = 0;
  uint16_t sampleCount = 0;

  while (millis() - startMillis < SAMPLE_WINDOW) {
    totalSound += analogRead(SOUND_PIN);
    sampleCount++;
    delay(10); // 采样间的小延迟
  }

  float avgSound = sampleCount > 0 ? (float)totalSound / sampleCount : 0;
  Serial.print("平均声音级别: ");
  Serial.println(avgSound);

  // 状态机
  if (avgSound > SOUND_THRESHOLD) {
    if (!machineRunning) {
      machineRunning = true;
      Serial.println("机器正在运行");
    }
    lastOnTime = millis();
  } else {
    if (machineRunning && (millis() - lastOnTime > STOP_DELAY)) {
      machineRunning = false;
      Serial.println("机器已停止");
      bot.sendMessage(CHAT_ID, "洗衣机已停止！该晾衣服了。", "");
    }
  }

  delay(10000); // 每10秒检查一次
}
```

#### 步骤5：自定义代码

1. **更新凭据**：
   - 将 `您的Wi-Fi名称`、`您的Wi-Fi密码`、`您的机器人令牌` 和 `您的聊天ID` 替换为实际值。
2. **调校 `SOUND_THRESHOLD`**：
   - 运行洗衣机并通过串行监视器（`Serial.println(analogRead(SOUND_PIN));`）监测声音级别。
   - 将 `SOUND_THRESHOLD` 设置为高于环境噪音但低于机器运行噪音的值（例如200-500，取决于您的设置）。
3. **调整 `SAMPLE_WINDOW`**：
   - 2秒窗口（`2000` 毫秒）可平滑瞬态噪音。如果背景噪音导致误读，请增加此值。
4. **调整 `STOP_DELAY`**：
   - 设置为 `300000`（5分钟）以避免在静默阶段（如浸泡）产生误通知。

#### 步骤6：测试和部署

1. **上传代码**：
   - 通过USB转串口适配器将ESP32连接到计算机。
   - 在Arduino IDE中选择 **ESP32 Wrover Module**（对于ESP8266选择 **NodeMCU**）并上传草图。
2. **测试系统**：
   - 启动洗衣机并监测串行监视器以查看声音级别和状态变化。
   - 验证机器停止时的Telegram通知。
3. **微调**：
   - 如果出现误报/漏报，调整 `SOUND_THRESHOLD` 或 `STOP_DELAY`。
   - 在不同条件下（例如有背景噪音时）测试以确保可靠性。
4. **永久安装**：
   - 将传感器和开发板固定在外壳中，靠近机器，确保麦克风暴露但受防水保护。

---

### 声音检测的优势

- **处理更简单**：无需图像处理，减少ESP32上的计算负载。
- **成本效益高**：像KY-038这样的声音传感器价格低廉（通常低于5美元）。
- **非侵入性**：无需直接连接到机器的面板灯。

### 挑战与缓解措施

- **背景噪音**：家庭噪音（例如电视、谈话）可能会干扰。缓解措施包括：
  - 将传感器靠近机器的电机或滚筒放置。
  - 调校 `SOUND_THRESHOLD` 以忽略环境噪音。
  - 使用定向麦克风或调整MAX9814的增益。
- **静默阶段**：某些洗涤周期有暂停（例如浸泡）。`STOP_DELAY` 确保仅在长时间静默后发送通知。
- **水暴露**：确保传感器置于防水外壳中，因为洗衣机可能有溅水或湿度。

### 可选增强功能

- **频率分析**：如果背景噪音持续存在问题，使用快速傅里叶变换（FFT）库（如 `arduinoFFT`）分析声音频率（例如50-200 Hz的电机嗡鸣）。这需要更多处理能力，并且在没有优化的情况下在基本ESP32上可能不可行。
- **双传感器**：结合声音和振动传感器（例如SW-420）以实现冗余。如果两者都指示机器关闭，则检测置信度增加。
- **电池供电**：为便于携带，使用可充电LiPo电池和充电模块（例如TP4056）代替USB适配器。

---

### 故障排除

- **无声音检测**：检查传感器接线，使用串行监视器测试，并确保传感器靠近机器的噪音源。
- **误通知**：增加 `STOP_DELAY` 或调整 `SOUND_THRESHOLD` 以过滤背景噪音或周期暂停。
- **Wi-Fi问题**：验证2.4GHz Wi-Fi凭据和机器附近的信号强度。
- **无Telegram消息**：确认机器人令牌和聊天ID，检查串行监视器中的错误。

这种基于声音的方法比基于摄像头的方法更简单，且在变化的光照条件下更稳健，使其成为洗衣机监测器的理想选择。如果您在具体步骤、传感器校准或集成附加功能方面需要帮助，请告诉我！
