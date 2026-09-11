---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 最便宜的人工智能BIOS控制器原型
translated: true
type: note
---

问题：构建一个最便宜的原型，用于一个**能从BIOS开始看到PC并通过键盘控制它的AI代理**，特别是用于你的GPU维修/测试台。

答案：我会构建**不带Raspberry Pi的v1版本**。你现有的4070机器可以作为AI/控制器计算机。

```text
                    你的4070 / AI PC
              ┌──────────────────────────┐
              │                          │
 HDMI 采集    │   Python 代理            │
 ────────────►│   ┌──────────────────┐   │
              │   │ 屏幕截图         │   │
              │   │ 视觉 / OCR       │   │
              │   │ LLM 推理         │   │
              │   │ 动作选择         │   │
              │   └────────┬─────────┘   │
              │            │             │
              │       USB HID            │
              └────────────┼─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ HID 设备    │
                    │ RP2040      │
                    └──────┬──────┘
                           │ USB
                           ▼
                 ┌───────────────────┐
                 │  目标 PC          │
                 │                   │
 HDMI 输出 ─────►│ BIOS → GRUB → OS  │
                 │       │           │
                 │       ▼           │
                 │     GPU           │
                 └───────────────────┘
```

### 1. 硬件

最低物料清单大致如下：

| 组件                          | 用途                            |
| ----------------------------- | ------------------------------- |
| USB HDMI 采集棒               | 目标 PC → AI PC                 |
| RP2040 / Raspberry Pi Pico    | AI PC → 模拟 USB 键盘           |
| HDMI 线                       | 目标 GPU/iGPU → 采集设备        |
| USB 线                        | RP2040 → 目标 PC                |
| 你现有的 4070 PC              | 视觉 + LLM + 编排               |

**RP2040 很重要**，因为你希望目标主板看到：

```text
USB 设备描述符
    ↓
HID 键盘
    ↓
BIOS 说："哦，是个键盘。"
```

不需要在目标端安装任何软件。

### 2. 先从确定性控制开始

不要立即让 LLM 介入。

首先验证：

```text
HDMI → 屏幕截图 → Python
USB HID → 按键 → BIOS
```

例如：

```python
# controller.py

import time
import cv2

cap = cv2.VideoCapture(0)

while True:
    ok, frame = cap.read()
    if not ok:
        raise RuntimeError("capture failed")

    cv2.imshow("target PC", frame)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
```

然后让 RP2040 模拟键盘。

概念上：

```python
keyboard.press("f2")
time.sleep(0.1)
keyboard.release("f2")
```

此时你应该能够亲眼观察到：

```text
AI PC 屏幕
      │
      └── 目标 BIOS
             │
             └── AI PC 发送 F2
                       │
                       ▼
                   目标 BIOS
```

### 3. 再加入计算机视觉

不要每 100 毫秒就把整个 1920×1080 的屏幕截图发送给 LLM。

使用较慢的代理循环：

```text
采集
   ↓
裁剪 / 缩放
   ↓
OCR + 视觉
   ↓
代理
   ↓
动作
   ↓
HID
```

类似这样：

```python
while True:
    frame = capture()

    observation = vision(frame)

    action = agent(
        observation,
        goal="将集成显卡设为主显示设备"
    )

    execute_hid(action)

    time.sleep(0.5)
```

动作空间一开始应该很小：

```python
ACTIONS = {
    "UP",
    "DOWN",
    "LEFT",
    "RIGHT",
    "ENTER",
    "ESC",
    "F1",
    "F2",
    "F10",
    "F12",
    "SPACE",
}
```

一开始不要让模型生成任意的键盘扫描码。

### 4. 给代理一个状态机

这会让它变得可靠得多。

例如：

```text
开机
   │
   ▼
等待 POST
   │
   ├── "按 DEL 进入设置"
   │
   ▼
BIOS
   │
   ├── 找到 "高级"
   ├── 找到 "图形"
   ├── 找到 "主显示设备"
   └── 选择 "IGD"
   │
   ▼
保存并退出
   │
   ▼
启动
   │
   ▼
LINUX
   │
   ▼
运行 MATS
```

此时 LLM 成为**规划者**，而不是盲目控制每一次按键。

### 5. 对于你的 GPU 维修台来说，这会变得非常有趣

你最终可以拥有：

```text
                 ┌─────────────────┐
                 │    AI 代理      │
                 └────────┬────────┘
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
         HDMI 视觉                USB HID
              │                       │
              ▼                       ▼
       目标主板                  BIOS 键盘
              │
       ┌──────┴──────┐
       ▼             ▼
     iGPU           NVIDIA GPU
       │             │
       │          MATS/MODS
       │             │
       └──────┬──────┘
              ▼
         测试结果
              │
              ▼
       AI 诊断
```

然后你的代理可以执行诸如：

```text
"启动机器。"

"进入 BIOS。"

"启用 iGPU。"

"启动 Debian。"

"对 GPU #1 运行 MATS。"

"MATS 在通道 X 上报告错误。"

"关机。"

"请技术人员检查 VRAM M5。"
```

这比通用的 GUI 代理实用得多，因为**AI 甚至在操作系统存在之前就能访问物理机器**。

### 6. 一个重要升级：ATX 电源控制

最终我会添加一个小型微控制器控制的继电器/ATX 接口：

```text
AI
 │
 ├── HDMI 采集
 ├── USB HID
 └── 电源控制
          │
          ▼
       ATX 电源
          │
          ▼
       主板
```

这样代理就可以控制完整的生命周期：

```text
关机
   ↓
开机
   ↓
观察 POST
   ↓
BIOS 交互
   ↓
启动 OS
   ↓
MATS
   ↓
关机
```

这将从**AI 计算机使用**转变为更接近**AI 控制的硬件测试夹具**。

对于你目前的 GPU 维修设置，我会构建**v1 版本，只需要三样东西：HDMI 采集 + RP2040 HID + Python**，首先验证 BIOS 控制，然后再连接视觉/LLM 层。