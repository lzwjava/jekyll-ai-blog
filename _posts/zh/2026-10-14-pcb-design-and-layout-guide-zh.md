---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PCB设计与布局指南
translated: true
type: note
---

**问题：** 如何设计和绘制 PCB（主板）电路？

**回答：**

设计 PCB 涉及从概念到可制造电路板的多阶段工作流程。以下是完整流程：

---

### 阶段 1 — 选择你的 EDA（电子设计自动化）软件

EDA（Electronic Design Automation）软件是工程师用来设计、仿真、验证并准备电路制造的工具。2026 年的主流工具：

| 工具 | 最适合 | 费用 |
|---|---|---|
| **KiCad** | 初学者与专业人士 | 免费 / 开源 |
| **EasyEDA** | 基于网页，快速原型 | 提供免费版本 |
| **Altium Designer** | 专业 / 企业团队 | 付费 |
| **Autodesk Fusion 360** | 机械 + PCB 集成设计 | 个人使用免费 |
| **Flux.ai** | 云端团队协作 | 免费增值模式 |

KiCad 已成为领先的开源 EDA 解决方案，无需授权费用即可提供专业级 PCB 设计能力。对大多数人来说，它是最佳起点。

---

### 阶段 2 — 绘制原理图

从一个清晰的目标开始：在打开软件之前，先明确电路的功能。将电路分成几个部分 —— 电源、输入处理、核心逻辑和输出驱动。这个视觉化指南可以防止设计过程陷入混乱。

关键步骤：
- 放置元件符号（IC、电阻、电容、连接器）
- 用导线/网络连接元件
- 标注网络（VCC、GND、信号）
- 指定元件值和封装

---

### 阶段 3 — 将原理图转换为 PCB 布局

设计过程包含两个主要阶段：创建原理图（电路的蓝图）和布局物理电路板。

在这个阶段你需要：
1. **设置板框尺寸** —— 定义物理大小和形状
2. **放置元件** —— 在电路板上合理排列元件（电源靠近电源，信号路径短）
3. **布线** —— 根据原理图网络表绘制铜线连接元件
4. **添加地平面** —— 连接到 GND 的实心铜填充；可提高信号完整性并降低噪声
5. **添加丝印标注** —— 元件编号、Logo、引脚标记

---

### 阶段 4 — 设计规则检查（DRC）

大多数 PCB 设计软件都包含 DRC 工具，用于确保设计符合制造商规格要求且无错误。

DRC 检查项包括：走线宽度违规、间距错误、未连接网络、短路。

---

### 阶段 5 — 生成 Gerber 文件并制造

将电路板设计发送给制造商的经典方法是从设计中生成 Gerber 文件。这些文件描述电路板的每一层（铜层、丝印层、阻焊层、钻孔）。

常见且价格实惠的 PCB 制造商：**JLCPCB**、**PCBWay**、**NEXTPCB** —— 花不到 5 美元就能拿到 5 块样板，这并不罕见。

---

### 阶段 6 — 组装与焊接

收到裸 PCB 后，将元件（SMD 或通孔）焊接到板上，然后进行测试。

---

### 给初学者的关键 PCB 设计技巧

- 让高频信号保持短距离并远离电源走线
- 至少使用 2 层（顶层 + 底层铜）
- 始终在某一层铺地平面
- 查阅元件数据手册，确认推荐封装
- 先打样，再批量订购

---

**参考资料：**
- [PCB Board Design: A Step-by-Step Guide for Beginners – JLCPCB](https://api.jlcpcb.com/blog/pcb-board-design-beginners-guide)
- [Beginner's Guide to PCB Design: From Schematic to Gerbers – AllPCB](https://www.allpcb.com/allelectrohub/beginners-guide-to-pcb-design-from-schematic-to-gerbers)
- [PCB Designing Tutorial for Beginners – BestPCBs](https://www.bestpcbs.com/blog/2025/06/pcb-designing-tutorial-for-beginners/)
- [Best EDA Tools for PCB Design 2026 – EMA](https://www.ema-eda.com/ema-resources/blog/best-eda-tools-for-pcb-design-2025-emd/)
- [Top 10 Free PCB Design Software (2026) – NextPCB](https://www.nextpcb.com/blog/top-10-free-pcb-design-software-2026)