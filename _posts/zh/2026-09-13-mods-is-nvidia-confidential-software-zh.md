---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MODS是NVIDIA的机密软件
translated: true
type: note
---

MODS **不公开提供下载**。它属于 **NVIDIA 机密**软件，文档中已明确说明：

> *"本文档中的信息属于保密信息，归 NVIDIA 公司所有。未经 NVIDIA 事先授权，不得分发本文档。"*

> *"NVIDIA 机密 | 根据 NDA 准备并提供"*

## 如何获取 MODS

**1. 对于 NVIDIA 合作伙伴/客户** — 请联系您的 **NVIDIA 代表**：
> *"请联系您的 NVIDIA 代表，了解迁移至 Linux MODS 的事宜。"*

文档提到 MODS 以软件包形式分发，部件号如 **"618-60506-3501-CX0"**，这些版本已针对特定产品完成认证。

**2. 对于 NVIDIA 员工** — 可通过 **NVIDIA 内部网络**获取：
> *"NVIDIA 提供可即用的 Linux 软件包，可通过 NVIDIA 内部网络获取。"*

**3. 对于其他人员** — 您**无法**直接下载 MODS。该软件未出现在 NVIDIA 官方网站、GitHub 或任何公共仓库中，仅提供给以下对象：
- NVIDIA 板卡合作伙伴（OEM/ODM）
- NVIDIA 内部工程团队
- 已签署 NDA（保密协议）的客户

## 如需 GPU 诊断工具

如果您并非 NVIDIA 合作伙伴，并希望测试消费级 GPU：

- **NVIDIA 公共工具**：当前没有面向最终用户的 MODS 等效公开工具
- **标准 NVIDIA 驱动**：通过 `nvidia-smi` 和 `nvidia-settings` 提供有限的诊断功能
- **第三方 GPU 工具**：GPU-Z、FurMark、OCCT 或 3DMark 等工具可进行基础压力测试，但无法提供 MODS 所具备的低层级寄存器/硬件访问能力
- **制造缺陷处理**：请使用 GPU 厂商的 RMA/保修流程

**核心要点**：MODS 是 NVIDIA 内部制造诊断工具。除非您与 NVIDIA 签署了 NDA/合作协议，否则无法获取该软件。