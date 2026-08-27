---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 从KiCad到物理PCB
translated: true
type: note
---

**问题：** 如何从 KiCad 设计中制造 PCB？

**答案：**

以下是 KiCad 设计到物理 PCB 的完整工作流程：

---

### 第一步 — 生成 Gerber 文件（标准制造格式）

在 KiCad 的 **PCB 编辑器 (Pcbnew)** 中：
1. 转到 **文件 → 制造输出 → Gerber 文件 (.gbr)**
2. 选择您需要的层：
   - `F.Cu` / `B.Cu` — 正面/背面铜层
   - `F.SilkS` / `B.SilkS` — 丝印层
   - `F.Mask` / `B.Mask` — 阻焊层
   - `Edge.Cuts` — 板框
3. 同时生成 **钻孔文件**：**文件 → 制造输出 → 钻孔文件 (.drl)**

---

### 第二步 — 生成 BOM 和贴片文件（如需组装）

- **BOM：** 文件 → 制造输出 → BOM
- **元件贴装 (CPL/PnP)：** 文件 → 制造输出 → 元件贴装

如果您希望制造商同时焊接元件，则需要这些文件。

---

### 第三步 — 使用 Gerber 查看器验证

在发送文件之前，请通过视觉验证：
- KiCad 内置的 **GerbView**
- 在线工具：[gerber.ucamco.com](https://gerber.ucamco.com) 或 **JLCPCB 的 Gerber 查看器**

---

### 第四步 — 选择 PCB 制造商

| 制造商 | 备注 |
|---|---|
| **JLCPCB** | 原型最便宜；同时提供 SMT 组装服务 |
| **PCBWay** | 质量好 + 组装服务 |
| **OSH Park** | 美国公司；紫色电路板；非常适合爱好者 |
| **Eurocircuits** | 欧洲公司；高质量 |
| **Seeed Fusion** | 适合小批量生产 |

---

### 第五步 — 上传并下单

1. 将所有 Gerber 文件和钻孔文件打包成一个 `.zip` 文件
2. 上传到制造商的网站
3. 配置选项：层数、板厚（通常为 1.6mm）、铜厚（1oz）、表面处理（HASL 或 ENIG）
4. 如果使用组装服务：上传 BOM 和 CPL 文件，选择元件
5. 检查预览，然后下单

---

### 第六步 — 焊接元件（如果不使用组装服务）

当裸板到达后：
- **手工焊接**用于直插和简单的 SMD 元件
- **回流焊炉 / 热板**用于 SMD 焊膏 + 回流焊
- **钢网**（可与电路板一起订购）用于均匀涂抹焊膏

---

**参考资源：**
- [KiCad 官方文档 — 生成 Gerber 文件](https://docs.kicad.org/8.0/en/pcbnew/pcbnew.html#fabrication-outputs)
- [JLCPCB — 如何从 KiCad 生成 Gerber 文件](https://jlcpcb.com/help/article/how-to-generate-gerber-and-drill-files-in-kicad-7)
- [PCBWay KiCad 指南](https://www.pcbway.com/blog/PCB_Design_Tutorial/Generate_Gerber_file_from_Kicad.html)
- [KiCad 社区论坛](https://forum.kicad.info)