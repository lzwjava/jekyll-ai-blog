---
audio: false
generated: true
image: false
lang: zh
layout: post
title: X99M-D D3 ReBAR：需要修改BIOS
translated: true
type: note
---

**问题：** 精粤 X99M-D D3 V1.2 主板是否支持 Resizable BAR 和 Above 4G Decoding？

**回答：**

该具体型号没有可用的官方文档，但根据此类主板的已知信息，以下为完整情况。

---

**简短回答：原生不支持，但可通过 BIOS 修改部分实现。**

---

**这款主板是什么**

精粤 X99M-D D3 V1.2 是一款基于 Intel X99/C612 芯片组（LGA2011-3）的廉价国产 micro-ATX 主板，面向 Xeon E5 v3/v4 使用。名称中的“D3”表示支持 DDR3 内存。此类主板与其他国产 X99 主板（如劲鲸、华南、摩奇）共享相同的 BIOS 基础（AMI Aptio 架构）。它们的原始 BIOS 菜单中均未包含原生的 ReBAR 或 Above 4G Decoding 选项。

---

**可实现的情况：**

| 特性 | 原生支持 | 是否存在变通方案？ |
| --- | --- | --- |
| Above 4G Decoding | ❌ 无可见选项 | ⚠️ 可能 —— 隐藏的 BIOS 变量 |
| Resizable BAR | ❌ 不支持 | ⚠️ 可通过 BIOS 修改部分实现 |

**路径 1  —  Above 4G Decoding（隐藏变量法）**

许多国产 X99 主板的 BIOS 固件中存在 Above 4G Decoding 选项，但被隐藏于 UI 之外。你可以在 GRUB EFI shell 中使用 `setup_var` 直接写入 BIOS 变量偏移量，例如 `setup_var 0x93 0x1`，但需要先通过提取主板的 IFR（内部表单表示）来识别正确的偏移量。不同主板版本的偏移量不同，因此你需要导出自己的 BIOS，并用 AMIBCP 或 UEFITool 检查以找到正确的偏移量。

**路径 2  —  通过 ReBarDxe 注入实现 Resizable BAR**

ReBarUEFI 项目提供了一个 DXE 驱动，可使用 UEFITool 将其注入 BIOS，从而在支持的系统上启用 Resizable BAR，前提是需要先启用 4G Decoding。

如果你的主板未启用 Above 4G Decoding，可设置的 ReBAR 最大容量为 1 GB  —  设置更高将导致系统无法启动。即便如此，1 GB 的 ReBAR 相比默认的 256 MB 窗口仍能带来一定的 GPU 性能提升。

**路径 3  —  CSM 冲突风险**

在类似的国产 X99-M D4/D3 主板上，一个已知问题是仅 CSM/Legacy 模式能正常显示输出，而纯 UEFI 模式无显示  —  这意味着无法禁用 CSM，而禁用 CSM 是启用 ReBAR 的前提条件。你的 V1.2 主板是否也存在此问题，取决于你使用的 GPU 是否支持 UEFI GOP。

---

**实用建议**

在尝试任何 BIOS 修改之前：

1. 检查你的显卡是否具备 UEFI GOP ROM（禁用 CSM 所需）
2. 准备一个 **CH341A 编程器** 作为恢复备份，以防刷写失败
3. 导出当前 BIOS，用 **AMIBCP** 打开，检查是否存在 Above 4G Decoding 字符串
4. 如果存在，使用隐藏变量法；如果不存在，则只能使用 ≤1 GB 的 ReBAR

---

**参考资料：**

- [榨干矿卡：老主板修改BIOS开启ReBAR – Bilibili](https://www.bilibili.com/opus/743982326937026580)
- [JGINYUE X99-M D4 BIOS & ReBAR discussion – WinRaid](https://winraid.level1techs.com/t/guide-overclock-bios-mods-for-chinese-x99-mbs/104683/68)
- [xCuri0/ReBarUEFI – GitHub](https://github.com/xCuri0/ReBarUEFI)
- [ReBarUEFI Release Thread – WinRaid Level1Techs](https://winraid.level1techs.com/t/release-resizable-bar-bios-efi-module/100235)
