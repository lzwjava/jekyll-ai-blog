---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 华南B75进入BIOS
translated: true
type: note
---

问题：如何在华南B75主板上进入BIOS？

回答：

对于大多数**华南B75**主板：

1. 开机或重启电脑。
2. 立即**反复按下`Delete`（`Del`）键**。
3. 您应能进入BIOS/UEFI设置界面。

如果`Del`键无效，可尝试：

```text
Del   ← 首选
F2
F12
Esc
```

### 如果您正在排查显卡或整机问题

对于B75 + 至强/酷睿i5配置，我建议：

```text
关机
↓
将键盘直接连接至背部USB 2.0接口
↓
开机
↓
立即连续敲击Del键
↓
进入BIOS
```

**重要提示：** 不要长按按键，应从按下电源键起快速连续敲击。

如果**完全无显示**，此时进入BIOS并非首要问题——您需要判断自检是否完成。提供您这块华南B75主板的清晰照片，我就能准确识别BIOS按键及相关的跳线/接口位置。

我还可以针对**显卡测试/维修场景**，详细指导您配置B75的BIOS设置，包括PCIe主显示、CSM兼容性支持模块、安全启动和启动顺序等。