---
audio: false
generated: true
image: false
lang: zh
layout: post
title: BGA在GPU维修中的工作原理
translated: true
type: note
---

问题：BGA（Ball Grid Array）在 GPU 维修中如何工作？

答案：

BGA 是一种封装技术，用于将 GPU（以及许多其他芯片）安装到电路板上。它的工作原理及维修涉及的内容如下：

**什么是 BGA**

BGA 封装在芯片底部有数百或数千个微小的焊球，按网格排列。这些焊球在组装过程中熔化，形成芯片与 PCB（印刷电路板）之间的电气连接。GPU 使用 BGA，是因为它们需要在紧凑区域内拥有大量连接。

**与 BGA 相关的常见 GPU 故障**

- **Cold solder joints** — 由于热循环（加热/冷却），连接会随时间变脆并开裂
- **Delamination** — 芯片部分从电路板上翘起
- **Bridging** — 相邻焊球短路在一起
- **Pad damage** — 芯片被不当移除时，PCB 上的铜焊盘被撕掉

**BGA 维修流程**

1. **Diagnosis** — X 射线检查是金标准，无需移除芯片即可查看开裂或桥接的焊球
2. **Reballing** — 移除旧焊球，清洁芯片，然后使用模板和焊膏涂布新焊球
3. **Reflow** — BGA 返修工作站（热风 + 红外线）小心加热电路板，熔化并重新就位焊点；温度曲线必须精确以避免翘曲
4. **Re-inspection** — X 射线或功能测试确认修复效果

**关键设备**

| 工具 | 用途 |
|---|---|
| BGA 返修工作站 | 受控加热，用于移除/回流焊 |
| X 射线机 | 无需拆卸即可进行内部检查 |
| 模板 | 精确放置新焊球 |
| 助焊剂 | 帮助焊料流畅流动 |
| 显微镜 | 目视检查焊盘和焊球 |

**为什么维修困难**

GPU 是大型 BGA 芯片，这使得均匀加热非常困难。PCB 或芯片翘曲是真实风险。许多“GPU 回流焊”技巧（如烤箱烘烤）最多只是暂时的——正确的维修需要专业的返修设备。

参考链接：
- [Ball Grid Array (BGA) Overview – IPC](https://www.ipc.org)
- [BGA Rework Process Guide – Pace World](https://www.paceworldwide.com)
- [GPU Reballing Explained – Louis Rossmann (YouTube)](https://www.youtube.com/@rossmanngroup)