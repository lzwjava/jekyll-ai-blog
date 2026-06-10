---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 从Mac控制iPhone
translated: true
type: note
---

**问题：** Mac 能否通过蓝牙等方式连接 iPhone 并远程控制它——发送向上/向下滑动手势来滚动 TikTok 视频？

**答案：**

可以——有三种可行方案，从零代码到完全可编程。注意有一件事**行不通**：macOS 无法原生作为**蓝牙 HID 外设**（键盘/鼠标服务器），因此“Mac 伪装成 iPhone 的蓝牙鼠标”这条路径在没有额外硬件的情况下被封锁。

## 方案 1 — iPhone 镜像（零代码，macOS 15+ / iOS 18+）

苹果官方解决方案。Mac 和 iPhone 通过蓝牙/Wi-Fi 配对；iPhone 屏幕串流到 Mac 窗口，你的触控板手势（双指滑动 = 屏幕滑动）会透传过去。在镜像窗口中打开 TikTok，双指向上滑动 → 下一个视频。支持锁屏状态，无需线缆。

设置：同一 Apple ID，蓝牙 + Wi-Fi 开启，然后在 Mac 上执行：`open -a "iPhone Mirroring"`。

限制：仅限交互式操作——无法干净地进行脚本化控制（该窗口对合成滚动事件的支持不一致，且苹果主动对其进行了沙盒隔离）。

## 方案 2 — 通过 WebDriverAgent 实现可编程滑动（构建者路线）

如果你的目标是**自动化**轮播（例如“每 N 秒滑动一次”，或由智能体决定何时滑动），这就是你需要的方案。WDA 在 iPhone 上运行 XCUITest 服务器；你通过 USB 或 Wi-Fi 用 Python 驱动它。

一次性设置：

```bash
# 1. 克隆 WDA 并在 Xcode 中用免费 Apple ID 签名（设置你自己的团队）
git clone https://github.com/appium/WebDriverAgent
open WebDriverAgent/WebDriverAgent.xcodeproj
# Product > Test 在 iPhone 上运行一次，在设备上信任开发者证书

# 2. Python 客户端
pip install facebook-wda tidevice
tidevice wdaproxy -B com.<yourname>.WebDriverAgentRunner.xctrunner --port 8100
```

然后滑动循环只需约 10 行代码：

```python
import wda, time, random

c = wda.Client("http://localhost:8100")
c.app_launch("com.zhiliaoapp.musically")  # TikTok 的 Bundle ID

while True:
    c.swipe(0.5, 0.8, 0.5, 0.2, duration=0.2)   # 向上滑动 = 下一个视频
    time.sleep(random.uniform(5, 12))            # 类人停留时间
```

`c.swipe(0.5, 0.2, 0.5, 0.8)` 返回（向下滑动）。坐标是相对于屏幕的浮点数，因此与分辨率无关。你可以轻松地在上面叠加 LLM——通过 `c.screenshot()` 截图，喂给视觉模型，决定滑动/点赞/跳过。这就成了一个不到 100 行的 TikTok 智能体。

注意事项：用免费 Apple ID 签名的 WDA 每 7 天过期；付费开发者账户（$99/年）可延长至一年。Appium 本质相同但仪式感更强——直接使用 `facebook-wda` 更精简。

## 方案 3 — 通过 ESP32 实现真正的蓝牙 HID（约 $5 硬件）

如果你特别想要蓝牙鼠标模型：将 ESP32 刷入 [ESP32-BLE-Mouse](https://github.com/T-vK/ESP32-BLE-Mouse)，与 iPhone 配对（iOS 13+ 通过 AssistiveTouch 支持 BLE 鼠标），然后让 Mac 通过 USB 串口向 ESP32 发送命令：

```cpp
// ESP32 草图：串口字节 'u' → 拖动向上手势
#include <BleMouse.h>
BleMouse mouse;
void setup() { Serial.begin(115200); mouse.begin(); }
void loop() {
  if (Serial.read() == 'u') {
    mouse.press();
    for (int i=0; i<30; i++) { mouse.move(0,-10); delay(8); }
    mouse.release();
  }
}
```

```python
# Mac 端
import serial, time
s = serial.Serial('/dev/tty.usbserial-XXXX', 115200)
while True:
    s.write(b'u'); time.sleep(8)
```

此方案无需越狱，与具体应用无关，且能经受 iOS 更新——iPhone 只会认为有一个鼠标在拖动。缺点：必须启用 AssistiveTouch 指针，且拖动模拟不如手指滑动那样精准干脆。

**推荐建议：** 如果你只想悠闲地从你的 Air 上滚动，选方案 1；如果你在构建自动化（它能自然地与你的智能体工具组合——`wda` + 视觉模型就是一个真正的“AI 看 TikTok”项目），选方案 2；如果你想要硬件级别的鲁棒性，选方案 3。

**参考资料：**

- [facebook-wda (Python WDA 客户端)](https://github.com/openatx/facebook-wda)
- [WebDriverAgent](https://github.com/appium/WebDriverAgent)
- [ESP32-BLE-Mouse](https://github.com/T-vK/ESP32-BLE-Mouse)
- [Apple — iPhone 镜像](https://support.apple.com/en-us/120421)