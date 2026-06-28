---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DIY CAN总线赛车仪表盘
translated: true
type: note
---

现在图片清晰多了——这是一个**基于 CAN 总线的数字仪表盘/赛车显示屏**，几乎可以确定是为**模拟赛车**或真实车辆的 OBD/CAN 遥测数据打造的。

解读电路板：

**显示屏（顶部）：**

- **`3`**（橙色大数字）——当前 **gear**
- **`70` CLUTCH**——clutch 位置/压力百分比
- **`102` OIL**——oil 温度或压力
- 蓝色竖条——很可能是 **RPM/换挡指示器**

**计算模块：**

- 那块灰色电路板，标有 **"...TICK S3"**，是 **LilyGO T-Display-S3**（或类似型号）——一块 **ESP32-S3** 开发板，带有内置彩色 IPS LCD 和 USB-C 接口。上面的 "S3" 标识和外形很容易辨认。

**下方的扩展板：**

- 绿色 PCB 上印有 **"CAN"** 字样，并有一颗点亮的绿色 LED，这是一个 **CAN 收发器模块**——通常是 **SN65HVD230** 或 **MCP2515 + TCAN/MCP2562** 收发器。标记 **`CTX/CRX`**（CAN TX/RX）和 **`3V3 / GND`** 证实了这一点。
- 左侧带有箭头的 **"+IN / OUT+ / OUT-"** 模块是一个小型 **升降压转换器或信号隔离器**（用于将 12V 汽车电源稳压到 5V/3.3V）。
- 黄色线 = **CAN-H / CAN-L** 双绞线。

**实际功能：**

ESP32-S3 读取 CAN 帧（可以来自真实车辆的 OBD-II/CAN 总线，也可以来自模拟赛车遥测数据，如 iRacing/Assetto Corsa 通过 CAN 网关输出），解码 gear/clutch/oil/RPM 信号，并在 LCD 上渲染为赛车仪表盘。

这与第一张图片中的 G 力计出自**同一位制作者**——相同的原型风格（洞洞板、ESP32-S3、USB-C、黑底橙色 UI 主题）。这是一个典型的 **DIY 汽车/模拟赛车仪表盘**项目。

典型架构：

```
ESP32-S3 (T-Display-S3)
   │  SPI → 内置 ST7789 LCD
   │  GPIO → SN65HVD230 CAN 收发器
   ▼
CAN 总线 (CAN-H / CAN-L, 汽车通常使用 500 kbps)
   ▼
车辆 ECU  /  模拟赛车 CAN 网关
```

最小固件结构（Arduino-ESP32，使用内置 TWAI/CAN 外设）：

```cpp
#include "driver/twai.h"

void setup() {
  twai_general_config_t g = TWAI_GENERAL_CONFIG_DEFAULT(GPIO_NUM_43, GPIO_NUM_44, TWAI_MODE_NORMAL);
  twai_timing_config_t  t = TWAI_TIMING_CONFIG_500KBITS();
  twai_filter_config_t  f = TWAI_FILTER_CONFIG_ACCEPT_ALL();
  twai_driver_install(&g, &t, &f);
  twai_start();
  // 初始化 ST7789 显示屏...
}

void loop() {
  twai_message_t msg;
  if (twai_receive(&msg, pdMS_TO_TICKS(10)) == ESP_OK) {
    switch (msg.identifier) {
      case 0x1F0: gear   = msg.data[0]; break;   // 示例 ID —
      case 0x1F1: clutch = msg.data[1]; break;   // 取决于你的 DBC 文件
      case 0x1F2: oil    = msg.data[2]; break;
    }
    drawDash(gear, clutch, oil);
  }
}
```

真正的工作在于 **DBC 文件**——将 CAN 仲裁 ID + 字节偏移 + 缩放因子映射到物理信号（gear, RPM, oil 温度）的对应关系。对于模拟赛车，人们通常使用一个 PC 插件（SimHub），通过串口/CAN 推送遥测数据；对于真实车辆，则需要逆向分析 OEM 的 CAN ID。

需要我编写完整的 T-Display-S3 仪表盘固件吗？包括 TWAI 接收循环和一个干净的 ST7789 gear/clutch/oil 布局，匹配那种黑底橙色的美学风格。大约 150 行代码。
