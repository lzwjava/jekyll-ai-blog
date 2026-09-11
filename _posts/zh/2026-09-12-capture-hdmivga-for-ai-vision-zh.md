---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 捕获HDMI/VGA用于AI视觉
translated: true
type: note
---

问题：如何从另一台电脑物理捕获 **HDMI 或 VGA 输出**，以便你的 AI 机器能够读取 BIOS/UEFI 屏幕？

答案：关键在于 **HDMI/VGA 是输出接口**，因此你需要一个**捕获设备**，将电信号视频转换为 USB 帧，供你的电脑读取。

### HDMI — 最简单的方式

使用一个廉价的 **USB HDMI 采集棒**：

```text
目标 PC
GPU / iGPU HDMI 输出
        │
        │ HDMI
        ▼
┌──────────────────┐
│ HDMI USB 采集卡  │
│                  │
│ HDMI 输入 → USB  │
└────────┬─────────┘
         │ USB
         ▼
     AI 电脑
         │
         ▼
 /dev/video0
```

在 Linux 上：

```bash
v4l2-ctl --list-devices
```

你通常会看到类似这样的信息：

```text
USB Video:
    /dev/video0
```

然后：

```bash
ffplay /dev/video0
```

或者用 Python / OpenCV：

```python
import cv2

cap = cv2.VideoCapture("/dev/video0")

while True:
    ok, frame = cap.read()
    if not ok:
        break

    cv2.imshow("target", frame)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
```

现在你的 AI 电脑实际上正在接收 **BIOS 像素作为图像**。

### VGA 稍有不同

VGA 是模拟 RGB 信号：

```text
VGA
 ├── 红
 ├── 绿
 ├── 蓝
 ├── 行同步
 └── 场同步
```

通常你不希望将 VGA 直接连接到普通的 USB 端口。

请使用：

```text
目标 PC VGA 输出
       │
       ▼
VGA → HDMI 转换器
       │
       ▼
HDMI 采集卡
       │
       ▼
USB
       │
       ▼
AI PC
```

或者专用的：

```text
VGA → USB 采集卡
```

设备。

VGA→HDMI 转换器执行重要的**模拟 → 数字转换**。

### 针对你的 GPU 维修工作台

实际上我建议尽可能**统一使用 HDMI**：

```text
                    ┌─────────────────────┐
                    │ AI / 控制电脑       │
                    │                     │
                    │ OpenCV              │
                    │ OCR                 │
                    │ VLM                 │
                    │ Agent               │
                    └──────────┬──────────┘
                               │ USB
                         ┌─────▼─────┐
                         │ HDMI      │
                         │ 采集卡    │
                         └─────▲─────┘
                               │ HDMI
                               │
                    ┌──────────┴──────────┐
                    │ 目标主板            │
                    │                     │
                    │ iGPU / GPU          │
                    └─────────────────────┘
```

你甚至可以拥有**两个目标输出**：

```text
iGPU HDMI ─────┐
               ├── HDMI 切换器 ── 采集卡 ── AI
GPU HDMI ──────┘
```

这样 AI 就可以检查主板的 iGPU 输出或独立 GPU 的输出。

### 一个重要的 BIOS 细节

廉价的采集卡不一定能捕获**所有 BIOS 信号**。

某些 BIOS 系统会输出不常见的分辨率 / 刷新率，而廉价的 HDMI 采集设备可能无法锁定这些信号。

例如：

```text
BIOS:
640×480 @ 60
800×600 @ 60
1024×768 @ 60
        ↓
采集设备
        ↓
USB UVC 720p/1080p
```

现代 UEFI 的 1080p 信号则更容易处理。

对于你的 **B75/B150 GPU 诊断机器**，我建议先用一个廉价的 UVC HDMI 采集棒进行测试：

```bash
v4l2-ctl --list-formats-ext -d /dev/video0
```

然后：

```bash
ffplay -f v4l2 /dev/video0
```

一旦这一步成功，下一层就很简单了：

```python
frame = capture.read()
```

这个 `frame` 就成了**提供给 agent 的视觉观察输入**。
