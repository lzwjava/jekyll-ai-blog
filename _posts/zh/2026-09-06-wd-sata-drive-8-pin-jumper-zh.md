---
audio: false
generated: true
image: false
lang: zh
layout: post
title: WD SATA硬盘8针跳线
translated: true
type: note
---

**问题：** 在 WD SATA 硬盘上，有三个连接器——一个连接 PSU（电源），一个是 SATA 数据线。第三个 8 针连接器是什么？

**回答：**

那是一个**跳线针脚座（jumper pin block）**——在正常使用中不需要插入任何东西。

它们是跳线针脚。你可以通过在特定针脚对上放置一个跳线帽（jumper shunt），在它们之间形成电气回路，从而启用特定设置。这些跳线启用的设置由硬盘印刷电路板（PCB）硬编码决定。

具体到 Western Digital SATA 硬盘，各针脚对的功能如下：

- **针脚 1 和 2** — 禁用硬盘的扩频时钟（SSC）功能，该功能有助于抑制电磁干扰。
- **针脚 5 和 6** — 将数据传输速率限制为 150 MB/s（SATA I 速率），适用于较旧的控制器。
- **针脚 3 和 4** — 在支持的硬盘上启用 PM2 模式。

在台式机硬盘上，这 8 个针脚用于工厂固件或跳线启用设置（例如「加电待机」（Power-Up In Standby，PUIS）），而不是用于传输用户数据。

**简而言之：你不需要向它连接任何东西。** 不需要向这个 8 针接口连接任何东西——保持无跳线状态即为默认行为。这是从 IDE 时代遗留下来的传统功能，主要在某些企业级或兼容性场景中有用。

---

**参考资料：**
- [我硬盘上的这个 8 针连接器是什么？ – PCPartPicker](https://pcpartpicker.com/forums/topic/359090-what-is-this-8-pin-connector-on-my-hard-drive)
- [如何在 SATA 硬盘上使用跳线 – Chron](https://smallbusiness.chron.com/use-jumpers-sata-hard-drive-69047.html)
- [这个 SATA 硬盘上的 8 个针脚是做什么用的？ – Tom's Hardware](https://forums.tomshardware.com/threads/what-are-the-8-pins-for-on-this-1tb-sata-hard-drive.2094318/)