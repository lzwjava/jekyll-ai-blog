---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MODS下载未公开提供
translated: true
type: note
---

问题：**实际上在哪里可以下载 NVIDIA MODS？**

回答：我查阅了当前的 NVIDIA 文档和旧的 MODS 文档。你粘贴的摘要**基本正确**：我找不到 MODS 制造测试包的合法公开下载地址。

关键区别在于：

* **MODS 本身**（制造诊断/测试套件）是通过 NVIDIA 的合作伙伴/客户渠道分发的。旧的 NVIDIA 文档明确说明这些包带有 NVIDIA 部件号，例如 `618-60506-3501-CX0`，而不是提供公开下载链接。（[pdfcoffee.com][1]）
* NVIDIA 仍然发布相关诊断系统的文档，但**不提供 MODS 二进制文件的公开下载**。
* 对于受支持的数据中心 GPU，确实存在一个公开记录的替代方案：**NVIDIA DCGM Diagnostics / EUD**。NVIDIA 为 Linux 提供了可安装的诊断包。（[NVIDIA Docs][2]）

### 如果你实际需要的是 GPU 硬件诊断

首先尝试 DCGM：

```bash
# 安装相应的 NVIDIA/DCGM 包后
dcgmi diag -r 1
dcgmi diag -r 3
```

当前的 NVIDIA 诊断插件会执行持续的计算/内存测试，并检查以下项目：错误结果、帧缓冲/数据路径故障、XID、不可纠正的内存错误、时钟和功耗。（[NVIDIA Docs][3]）

对于受支持的系统，NVIDIA 还记录了**最终用户诊断（EUD）**，其 Linux 包安装路径为：

```text
/usr/share/nvidia/diagnostic/
```

（[NVIDIA Docs][2]）

[NVIDIA DCGM Diagnostics 文档](https://docs.nvidia.com/datacenter/dcgm/3.1/user-guide/dcgm-diagnostics.html?utm_source=chatgpt.com)

[NVIDIA EUD 文档](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-eud.html?utm_source=chatgpt.com)

### 如果你特别需要 **MODS**

我无法提供任何公开的 NVIDIA 下载链接。合法的途径是：

```text
NVIDIA 代表
        ↓
请求 Linux MODS / 现场诊断
        ↓
NVIDIA 确定产品/客户权限
        ↓
NVIDIA 提供的包
```

**不要相信随机出现的“MODS 下载”网站**。特别是，在网上找到旧的 MODS 手册并不意味着对应的二进制包可以合法下载。旧的文档证实 MODS 是一个制造测试套件，并以经认证的 NVIDIA 包形式分发。（[pdfcoffee.com][1]）

一个有趣的细节：NVIDIA 公开的 **HW Field Diag** 文档说明 Field Diag 本身使用了 `mods` 内核模块（`/dev/mods`），并明确讨论了 Field Diag 与 MODS 之间的交互。（[NVIDIA Docs][4]）

因此，如果你正在尝试**诊断特定的 NVIDIA GPU/板卡**，请告诉我具体的 GPU 型号（例如 RTX 4090、H100 SXM、A100 PCIe 等），以及你正在测试的项目是**VRAM、SM、PCIe、NVLink、板卡制造缺陷还是一般稳定性**。我可以为你提供最接近的公开诊断堆栈及具体命令。

[1]: https://pdfcoffee.com/mods-2-pdf-free.html?utm_source=chatgpt.com "mods - PDFCOFFEE.COM"
[2]: https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-eud.html?utm_source=chatgpt.com "扩展实用诊断 (EUD) — NVIDIA DCGM 文档 最新版"
[3]: https://docs.nvidia.com/datacenter/dcgm/latest/reference/diagnostics/plugins/diagnostic.html?utm_source=chatgpt.com "诊断插件 — NVIDIA DCGM 文档"
[4]: https://docs.nvidia.com/deploy/hw-field-diag/index.html?utm_source=chatgpt.com "HW Field Diag :: GPU 部署与管理文档"