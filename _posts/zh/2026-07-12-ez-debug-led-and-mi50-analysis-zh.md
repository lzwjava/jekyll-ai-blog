---
audio: false
generated: true
image: false
lang: zh
layout: post
title: EZ Debug LED 与 MI50 分析
translated: true
type: note
---

## 事实核查表

| 断言 | 判定 | 依据 |
|---|---|---|
| 主板有4个EZ Debug LED（CPU/DRAM/VGA/BOOT） | **确认** | MSI官方手册将4个EZ Debug LED列为MAG B760M MORTAR WIFI II的标准功能 |
| 每个LED的功能含义 | **确认，逐字准确** | 手册说明LED指示主板调试状态：CPU表示CPU未检测到/故障，DRAM表示内存未检测到/故障，VGA表示GPU未检测到/故障，BOOT表示未找到可启动设备——粘贴回答中的表格与此完全一致 |
| 物理位置：“右上边缘，靠近24针ATX” | **合理但未经独立确认** | 我无法从检索到的手册文本中提取出明确的LED簇与ATX_PWR1位置关联的表述——图表无法很好地提取为文字。这是MSI在其主板上的常见惯例，因此是一个合理的推断，但按照你自身的证据标准，我想指出这是推断而非确认事实 |
| 13900KF没有核显 | **确认**（常识，无需搜索） | 所有Intel“F”后缀SKU均缺乏集成显卡——粘贴回答的这一部分正确，无需保留余地 |
| MI50“有时存在PCIe/BIOS兼容性问题” | **表述不足** | 见下文——这并非边缘情况，几乎可以说是默认体验 |

## MI50是粘贴回答中最薄弱的部分

这是我要最强烈反驳的部分。MI50并非有点古怪的GPU——它是一个数据中心计算加速器（Vega 20，HBM2），本来就不是为引导消费级桌面而设计的：

- **默认无显示输出。** 物理迷你DisplayPort接口存在于PCB上，但出厂时已禁用——一份Vega20 MI50的硬件清单明确显示DisplayPort处于“关闭”状态，与那些只是未物理实现的端口不同；另外单独的第一手测试确认，在将Radeon Pro VII VBIOS刷入该卡之前，DisplayPort不会输出任何图像。同代的Vega20 Instinct卡也有相同的限制——默认没有视频输出，需要刷写WX9100 BIOS才能解锁隐藏的迷你DisplayPort并改善消费级硬件兼容性。
- **供电不可忽视。** 该卡需要两个8针电源连接器，功耗高达300瓦——如果你的机器只接了一个8针，或者使用了molex/6转8针适配器链，仅此一项就可能产生与粘贴回答所诊断的完全相同的“风扇转，无显示”症状，甚至在你触及BIOS/VGA-LED问题之前就已如此。
- **启动失败通常依赖于插槽顺序和BIOS设置，而非偶然。** Dells工作站上的一个真实故障排查帖子显示，MI50在某些PCIe插槽位置完全无法进入POST，需要将加速器移至显示GPU之前的PCIe枚举顺序插槽，系统才能启动。

所以，“有时存在兼容性问题”的说法虽然正确，但轻描淡写了——在消费级B760M主板上使用MI50，我会将无启动/无视频视为预期的首次结果，而非例外情况；真正的修复路径通常是：(1) 确认两个8针电源线都连接在独立的PSU线缆上，而非分接器；(2) 单独使用MI50，不安装其他GPU；(3) 检查BIOS中的Above 4G Decoding / Resizable BAR设置（这些对于大BAR计算卡很重要）；(4) 如果仍然无效，预期你可能需要刷写VBIOS才能从该卡获得任何视频信号——这是一个非平凡的、中等风险的操作，而非一个勾选框设置。

## 在采取行动前值得注意的一点

MI50并未出现在我们之前的讨论中——你最初的零件清单和线圈啸叫诊断基于RTX 4070加上你为测试而换入的第二张AMD卡（型号未指定，消费级，因为它执行正常显示任务）。如果这个粘贴的问答涉及的是同一台物理机器，那么这与我们之前调试噪音的GPU完全不同——值得确认这是否是另一台机器（可能如此，因为MI50 32GB卡是本地LLM社区中众所周知的高性价比显存选择，也适合你的训练工作负载用例），还是同一台机器增加了该卡，因为根据具体情况，EZ Debug LED故障排除步骤会有很大变化。

## 总结

粘贴的回答在直接来自MSI官方文档的部分（LED功能含义、KF芯片无核显）是准确的，在物理LED位置方面合理但未经验证。其薄弱之处在于将MI50启动失败视为偶发的兼容性脚注，而该卡的主要文献将“无显示、无法启动，直到你解决供电/BIOS/VBIOS问题”视为任何人将该卡放入非服务器硬件时的默认首次启动体验。

参考资料：

- [MSI MAG B760M MORTAR II / WIFI II — 官方用户指南（PDF）](https://download-2.msi.com/archive/mnu_exe/mb/MAGB760MMORTARII_MAGB760MMORTARWIFIII_EN.pdf)
- [MSI MAG B760M MORTAR MAX WIFI 手册 — EZ Debug LED 部分](https://www.manualslib.com/manual/3270648/Msi-Mag-B760m-Mortar-Max-Wifi.html)
- [AMD Radeon Instinct MI50 32GB VBIOS 参考 — GitHub Gist](https://gist.github.com/evilJazz/14a4c82a67f2c52a6bb5f9cea02f5e13)
- [AMD Radeon Instinct MI25 — ArchWiki](https://wiki.archlinux.org/title/AMD_Radeon_Instinct_MI25)
- [ThinkPad P50 + MI50 跨刷以输出显示 — eGPU.io 论坛](https://egpu.io/forums/pc-setup/thinkpad-p50-radeon-instict-mi50-with-radeon-pro-vii-vbios/)
- [Dell Precision 7820 中添加 AMD Instinct MI50 后无法启动/无视频 — Dell 社区](https://www.dell.com/community/en/conversations/precision-fixed-workstations/no-boot-no-video-when-adding-an-amd-instinct-mi50-in-my-7820/6858a82c03f07b7681d3fb2f)
- [AMD Radeon Instinct MI50 规格 — technical.city](https://technical.city/en/video/Radeon-Instinct-MI50)