---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 华硕Z170-A主板上的红色BOOT LED指示灯
translated: true
type: note
---

**问题：** 为什么我的 ASUS Z170-A 主板上的红色“BOOT DEVICE LED”灯亮起？

**答案：**

ASUS Z170-A 上“BOOT DEVICE LED”标签旁边的红色 LED 表示系统**无法检测到可启动设备**。这是 POST（Power-On Self-Test）调试 LED 之一。

常见原因：

1. **未连接存储设备** — 没有 SSD/HDD 插入 SATA 或 M.2 端口。
2. **未检测到启动驱动器** — 驱动器已连接但未被识别（线缆松动、驱动器损坏或 SATA 端口错误）。
3. **未安装操作系统** — 驱动器为空白，没有可启动的操作系统。
4. **BIOS 中的启动顺序错误** — BIOS 正在尝试从错误的设备启动。
5. **M.2 插槽冲突** — 在 Z170-A 上，使用某些 M.2 模式可能会禁用特定的 SATA 端口，导致已连接的驱动器消失。
6. **SATA 模式不匹配** — 驱动器为 AHCI 格式，但 BIOS 设置为 IDE（或反之）。

**可尝试的步骤：**
- 进入 BIOS（启动时按 **Del** 键），检查启动驱动器是否出现在 Storage/Boot 下。
- 重新插拔 SATA 线缆，并确保它们插入正确的端口。
- 检查 BIOS 中的 Boot Priority 顺序。
- 如果使用 M.2，请确认它没有禁用 SATA 端口。

---

**参考资料：**
- [ASUS Z170-A 手册与 POST LED 指南](https://www.asus.com/motherboards-components/motherboards/all-series/z170-a/)
- [ASUS POST LED 故障排除](https://www.asus.com/support/FAQ/1045839/)