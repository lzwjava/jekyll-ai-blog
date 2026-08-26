---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 开放GPU PCB选项
translated: true
type: note
---

问题：有没有适用于 KiCad 的开源 GPU PCB 布局？

答案：

完全开源的 GPU 设计**极为罕见**，因为 GPU 芯片本身是专有的。不过，以下是一些实际存在的近似方案：

---

**1. 基于 RISC-V 的开源 GPU（最接近真正的开源方案）**

| 项目 | 描述 | 链接 |
|---|---|---|
| **Nyuzi** | 基于 Verilog 的开源 GPGPU 处理器 | [GitHub](https://github.com/jbush001/NyuziProcessor) |
| **MIAOW** | 兼容 AMD Southern Islands 指令集的开源 GPU | [GitHub](https://github.com/VerticalResearchGroup/miaow) |
| **VeriGPU** | 基于 Verilog 的简单开源 GPU | [GitHub](https://github.com/hughperkins/VeriGPU) |

> 这些是 **RTL/HDL 设计**，而非 KiCad PCB 布局——但它们是现有最开放的开源 GPU 工作。

---

**2. 开源 PCIe 卡 PCB 设计（已适配 KiCad）**

这些并非 GPU，但你可以学习或借鉴这些开源的 PCIe 板卡设计：

- **[开源 PCIe 载板](https://github.com/enjoy-digital/litepcie)** — Enjoy-Digital 的 LitePCIe
- **[Glasgow 接口探索器](https://github.com/GlasgowEmbedded/glasgow)** — 开源硬件，包含 KiCad 源文件
- **[LUNA USB 硬件](https://github.com/greatscottgadgets/luna)** — 基于 KiCad 的开源 PCB 示例

---

**3. 基于 FPGA 的 GPU 替代方案（最接近 KiCad 中的真实 GPU PCB）**

FPGA 可以模拟 GPU 功能，并且许多 FPGA 板卡拥有开源的 KiCad 设计：

- **ULX3S** — 开源 FPGA 板卡，包含 KiCad 文件
  - [GitHub](https://github.com/emard/ulx3s)
- **OrangeCrab** — 基于 KiCad 的开源 FPGA 板卡
  - [GitHub](https://github.com/orangecrab-fpga/orangecrab-hardware)
- **Colorlight 5A-75B** — 用于 DIY GPU 类渲染项目
  - 社区中有基于 KiCad 的复刻版本（GitHub 可查）

---

**4. 最接近开源 GPU PCB 的项目**

- **[TinyGPU](https://github.com/adam-maj/tiny-gpu)** — 最小化 GPU 架构，适合学习
- **[Tiny Tapeout GPU 提交](https://tinytapeout.com)** — 提交用于实际芯片制造的小型 GPU 核心

---

**坦诚总结**

```
你想要的是：          KiCad 中开源的 RTX/RX 级别 GPU PCB
实际存在的：          开源 FPGA 板卡 + 开源 GPU RTL 逻辑
差距：                目前没有人公开流片并发布过
                      KiCad 格式的独立 GPU PCB
```

如果你的目标是**学习 GPU PCB 设计**，最佳路径是：
1. 学习开源 FPGA 板卡的 KiCad 文件（ULX3S 非常优秀）
2. 参考真实 AMD/NVIDIA 显卡的 boardview 文件
3. 结合 PCIe 电气规范（来自 PCIe 标准）

---

参考文献：
- [Nyuzi 开源 GPGPU](https://github.com/jbush001/NyuziProcessor)
- [ULX3S 开源 FPGA 板卡（KiCad）](https://github.com/emard/ulx3s)
- [LitePCIe 开源 PCIe 框架](https://github.com/enjoy-digital/litepcie)
- [Tiny Tapeout 开源芯片](https://tinytapeout.com)
- [OrangeCrab FPGA 硬件](https://github.com/orangecrab-fpga/orangecrab-hardware)