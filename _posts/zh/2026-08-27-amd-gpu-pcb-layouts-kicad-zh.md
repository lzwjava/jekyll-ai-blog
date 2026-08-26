---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD GPU PCB布局 KiCad
translated: true
type: note
---

问题：如何为KiCad找到AMD GPU PCB布局/原理图？

答案：

AMD GPU相较于NVIDIA的**更容易获取**，这得益于其开源GPU驱动方面的努力，但完整的PCB布局仍然很大程度上是专有的。以下是可用的资源：

**1. AMD的开源资源**

- AMD开源了其**GPU驱动和固件**，但并未开源板级PCB设计
- 不过，AMD生态系统的开放性意味着社区文档资料更加丰富
- 查看 [AMD的GitHub](https://github.com/RadeonOpenCompute) 以获取任何硬件参考材料

**2. 参考板设计（最佳途径）**

- AMD向AIB合作伙伴（华硕、微星、蓝宝石等）发布**参考卡设计**
- 在GitHub上搜索：
  - `RX 6900 XT PCB`
  - `Navi 21 schematic`
  - `AMD reference card boardview`

**3. AMD GPU的板视图文件**

- AMD显卡在维修数据库中更为常见
- 搜索以下关键词：
  - `RX 6800 XT boardview .brd`
  - `Navi 21 .bdv`
  - `AMD GPU boardview`
- 打开这些文件的工具：

| 工具 | 支持的格式 |
| --- | --- |
| OpenBoardView | `.brd`, `.bdv`, `.obv` |
| FlexBV | `.brd`, `.bv2`, `.fbv` |

**4. 社区追踪的原理图**

- **Louis Rossmann的社区**以及GPU维修论坛经常分享AMD板级走线
- [Badcaps论坛](https://www.badcaps.net/forum/) — GPU维修板块有AMD相关专题
- 搜索：`AMD RX 6000 schematic repair PDF`

**5. 蓝宝石 / 憾讯等AIB厂商原理图**

- 部分AIB合作伙伴的维修站偶尔会泄露或分享部分原理图
- 蓝宝石（AMD最紧密的AIB合作伙伴）的显卡文档最为常见
- 搜索：`Sapphire RX 6900 XT schematic`

**6. 转换为KiCad的工作流程**

```
板视图 (.brd/.bdv)  →  OpenBoardView  →  在KiCad中参考走线
PDF原理图          →  KiCad原理图编辑器  →  手动录入
Altium文件          →  KiCad内置Altium导入器  →  KiCad原生格式
```

> ⚠️ AMD实际的PCB光绘文件/KiCad文件并未公开发布。现有资料大多由维修技术人员反向工程得出。在用于任何设计前务必验证其准确性。

---

参考资料：

- [OpenBoardView GitHub](https://github.com/OpenBoardView/OpenBoardView)
- [FlexBV Boardview Tool](https://www.fluxeng.com/flexbv/)
- [Badcaps GPU维修论坛](https://www.badcaps.net/forum/)
- [AMD开源GPU GitHub](https://github.com/RadeonOpenCompute)
- [KiCad Altium导入器文档](https://docs.kicad.org/7.0/en/eeschema/eeschema.html#importing-schematics)
