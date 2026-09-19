---
audio: false
generated: true
image: false
lang: zh
layout: post
title: X99 ReBAR 支持查询
translated: true
type: note
---

**问题：** 精粤 X99M GD4 ARGB 主板是否原生支持 Resizable BAR 和 Above 4G Decoding？

**回答：**

目前没有官方文档或具体用户报告能确认**精粤 X99M GD4 ARGB** 主板是否原生支持这些功能。不过，基于 X99 平台的整体情况，以下内容适用于您的板子：

---

**简短回答：几乎肯定不支持原生支持——但存在部分变通方案。**

---

**为什么不原生支持：**

X99 芯片组发布于 2014 年。Resizable BAR 作为原生 BIOS 功能，仅在 Intel 400 系列（Comet Lake）及更新的平台以及 AMD 400 系列及更新的平台上才被引入。像您这样的廉价国产 X99 主板在设计时并未考虑 ReBAR 或 Above 4G Decoding，其 BIOS 供应商（通常是基于 AMI Aptio 的）也未包含这些选项。

---

**您可以尝试的方法：**

对于 X99 主板，社区中有三种途径，但都需要谨慎操作：

1. **通过隐藏 BIOS 变量开启 Above 4G Decoding** — 在许多 X99 主板上，该选项存在但被隐藏。您可以通过 GRUB EFI shell 使用 `setup_var` 方法来解锁它。偏移量因主板而异；您需要提取并读取 BIOS 的 IFR（内部表单表示）来找到正确的偏移量。对于某些 X99 主板，Above 4G Decoding 的偏移量位于 `0x16D`，操作步骤是先将其设为 `0x0`，重启，再设为 `0x1` 并再次重启。

2. **ReBarDxe BIOS 修改** — `ReBarUEFI` 项目提供了一个 DXE 驱动，可以使用 UEFITool 将其注入到 BIOS 中，从而在任何支持的系统上启用 Resizable BAR，唯一硬性要求是必须先启用 4G Decoding。没有 Above 4G Decoding，您只能使用低于 4 GB 的 BAR 大小——通常**最大 1 GB**。

3. **不使用 Above 4G Decoding** — 即使不启用 4G Decoding，您仍然可以尝试将 ReBAR 设置为 256 MB、512 MB 或 1 GB，并可能看到一些性能提升，尽管无法达到完整的显存大小。

---

**针对您这块主板的特别注意事项：**

- 精粤 X99M GD4 ARGB 是一款廉价国产主板，社区文档有限。修改其 BIOS 存在变砖风险，且目前没有已知的现成修改版 BIOS 适用于该特定型号。
- 类似的主板如 JGINYUE X99-M D4 曾报告过 UEFI/CSM 冲突——部分用户发现只能使用 CSM/Legacy 模式，这意味着他们无法禁用 CSM，而禁用 CSM 是启用 ReBAR 的前提条件。您的主板可能也存在同样问题。
- 在尝试任何 BIOS 刷写之前，您需要准备一个硬件编程器（如 CH341A）作为安全备份。

---

**参考链接：**
- [ReBarUEFI 发布帖 – WinRaid Level1Techs](https://winraid.level1techs.com/t/release-resizable-bar-bios-efi-module/100235)
- [xCuri0/ReBarUEFI GitHub](https://github.com/xCuri0/ReBarUEFI)
- [指南：国产 X99 主板超频 BIOS 修改 – WinRaid](https://winraid.level1techs.com/t/guide-overclock-bios-mods-for-chinese-x99-mbs/104683)
- [启用隐藏的 4G Decoding – ReBarUEFI Wiki](https://github.com/xCuri0/ReBarUEFI/wiki/Enabling-hidden-4G-decoding)