---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 区分GPU核心与VRM故障
translated: true
type: note
---

**问题：** 如何区分 GPU 故障是发生在核心（die）还是 MOSFET/VRM 问题——以及 Nvidia GPU 常见的故障类型和症状有哪些？

---

**回答：**

## 🔬 如何区分 GPU 核心故障与 MOSFET/VRM 故障

### 第一步 — 先进行目视检查

VRM 相关故障通常通过物理损坏即可直接发现——烧毁的 MOSFET、过热的 PCB 区域、灼烧痕迹——提前发现这些有助于确定电气测试的优先级。检查以下内容：
- 供电电路周围出现烧焦/变黑的区域
- 鼓包或开裂的 MOSFET
- 烧毁的电感或电容

---

### 第二步 — 测量供电轨电阻与电压

测量 GPU 供电轨的电阻和电压可以快速判断是否存在短路、断路或供电缺失情况。核心或显存轨对地短路通常表明 MOSFET 损坏或 GPU 内部损坏，而电压缺失则可能指向控制器或使能信号问题。

使用万用表：
- **核心供电轨对地短路** → MOSFET 短路或 GPU 核心损坏
- **供电轨存在但无输出** → PWM 控制器/驱动 IC 问题

---

### 第三步 — MOSFET 测试（建议离线进行）

测试 N 沟道 MOSFET 时，将模拟万用表置于 ×10K 欧姆档：黑色表笔接漏极。红色表笔触碰栅极以预充栅极电容。然后将红色表笔移至源极——表针应摆动至中段刻度。放电 FET 时，触碰一次栅极引脚。此时再次触碰源极应无偏转。以上为良好 FET 的特征。

> ⚠️ 注意：在线测试不可靠，因为所有 MOSFET 在漏极和源极之间都存在寄生二极管，不控制栅极电压的情况下，简单的通断测试毫无意义。

---

### 第四步 — 关键性的"注入电流"测试（进阶操作）

仅靠电阻测试只能发现明显的短路。只有当实际注入电流时，受损的 GPU 核心才会暴露出来——核心在注入电流下发热，从而确认核心已损坏。这是电子维修中的常规操作：你可能需要先更换 MOSFET 以消除 12V 供电轨短路，然后单独重新测试 GPU 核心，判断其是否还有修复价值。

以下是关键的诊断区分表格：
| 测试结果 | 判读结论 |
|---|---|
| 更换 MOSFET 后短路消除 | **MOSFET 损坏**，GPU 核心可能正常 |
| 更换 MOSFET 后核心仍然发热 | **GPU 核心也已损坏** |
| 供电轨电压缺失，无物理损坏 | PWM/驱动 IC 问题 |

---

## 💥 常见 Nvidia GPU 故障模式与症状

### 1. MOSFET / VRM 故障
- VRM 相关故障是较容易修复的 GPU 故障之一，通常由 MOSFET 短路、电容干涸/失效或电感损坏引起——通常表现为无供电输出（完全无法开机）。
- **症状：** 风扇转动，完全无显示信号，有时伴有烧焦味

### 2. 显存故障
- 显存芯片（GDDR6/GDDR6X）故障是导致画面花屏、纹理错乱和应用崩溃的常见原因。有缺陷的显存会呈现可重复的视觉图案、色块或驱动层面的显存访问错误，尤其是在负载下。
- **症状：** 棋盘格图案、纹理损坏、带有内存错误代码的蓝屏

### 3. GPU 核心故障
- 在负载下出现并逐渐在启动过程中提前发生的视觉异常、像素拖尾、闪烁颜色或棋盘格图案，表明显存故障或 GPU 核心退化。
- **症状：** 逐渐恶化的花屏 → 最终黑屏

### 4. 过热 / VRM 过载（负载下黑屏）
- 某些 GPU 在桌面环境下正常运行，但一旦负载增大即丢失显示输出。这通常发生在显卡过热或功耗尖峰超过电源或 VRM 承受能力时——强烈表明是散热或供电问题，而非软件故障。
- **测试：** 运行 FurMark 15–30 分钟。如果 PC 在 FurMark 运行期间黑屏或重启，则说明显卡的供电相位或内部 VRM 在负载下失效。

---

## 📊 故障类型速查表

| 症状 | 最可能的原因 |
|---|---|
| 无法开机自检，无显示，风扇 100% 转速 | MOSFET 损坏 / VRM 短路 |
| 负载下出现花屏后崩溃 | 显存或 GPU 核心退化 |
| 仅在高负载下黑屏 | VRM 过热/电流过载 |
| 桌面正常，游戏中崩溃 | VRM 老化或核心早期故障 |
| PCB 上有物理烧灼/气味 | MOSFET 烧毁（通常伴随核心损坏） |
| 设备管理器中显示错误代码 43 | BIOS 损坏或核心故障 |

---

**参考文献：**
- [GPU 维修与故障诊断指南 – Blikai](https://www.blikai.com/blog/components-parts/graphics-card-repair-gpu-components-fault-diagnosis-guide)
- [MOSFET 测试方法 – DigiKey 论坛](https://forum.digikey.com/t/how-to-test-a-mosfet/1985)
- [RTX 4090 MOSFET + 核心损坏案例研究 – Yahoo/Tom's Hardware](https://tech.yahoo.com/computing/articles/gpu-surgeon-attempts-rescue-fatally-153540641.html)
- [GPU 故障症状 – ITU Online](https://www.ituonline.com/blogs/graphics-card-failures/)
- [FurMark VRM 压力测试指南 – PC Power Up](https://pcpowerup.co.uk/blogs/news/how-to-tell-if-your-graphics-card-is-failing-gpu-artifacts-stress-test-guide)