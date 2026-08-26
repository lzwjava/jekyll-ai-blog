---
audio: false
generated: true
image: false
lang: zh
layout: post
title: KiCad开源EDA套件
translated: true
type: note
---

**问题：** 托管在 GitLab 仓库 `gitlab.com/kicad/code/kicad` 的 KiCad 项目是什么？

**答案：**

**KiCad** 是一款免费、开源的电子设计自动化（EDA）套件，主要用于设计电子原理图和印刷电路板（PCB）。

**起源与许可证**

KiCad 由 Jean-Pierre Charras 于 1992 年最初开发，如今已发展成为目前最强大的开源 EDA 工具之一。它采用 GNU GPL v3 许可证，可在 Windows、Linux 和 macOS 上运行。

**功能概述**

KiCad 提供用于原理图捕获、PCB 布局、封装和符号库管理、3D 可视化、电气规则检查和设计规则检查，以及生成制造输出（如 Gerber 文件、钻孔文件、BOM 清单和贴片数据）的集成工具。与需要在不同程序之间导出网表的分散工具链不同，KiCad 在单个项目内保持原理图和电路板数据的同步。

**主要特性**

- 支持多达 32 个铜层的 PCB，并能够创建各种复杂度的设计，包括原理图捕获、PCB 布局、SPICE 仿真、物料清单生成和 3D PCB 模型。
- 导出标准制造格式，包括 Gerber (RS-274X)、Excellon 钻孔文件、IPC-2581、ODB++、STEP 和 VRML 3D 模型，并包含拥有数千个符号、封装和 3D 模型的广泛官方库。

**适用对象**

KiCad 项目的目标是为专业电子设计师提供尽可能最好的跨平台电子设计应用程序，同时让新用户和经验不足的用户也能轻松上手。

**GitLab 仓库**

该仓库主要使用 C++ 编写，拥有超过 57,000 次提交、11 个分支和 159 个标签——反映了数十年的积极开发。

---

**参考文献：**
- [KiCad GitLab Repository](https://gitlab.com/kicad/code/kicad)
- [About KiCad | KiCad Official](https://www.kicad.org/about/kicad/)
- [What Is KiCad? — aivon.com](https://www.aivon.com/blog/kicad-hub/what-is-kicad-a-complete-introduction-to-open-source-pcb-design-software/)
- [KiCad EDA Guide 2026 — PCBSync](https://pcbsync.com/kicad-eda/)