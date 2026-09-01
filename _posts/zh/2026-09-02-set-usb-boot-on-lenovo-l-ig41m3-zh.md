---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 设置联想L-IG41M3的USB启动
translated: true
type: note
---

问题：如何在联想 L-IG41M3 主板上确认 BIOS 访问并从 USB 驱动器启动？

答案：
很高兴听到按 **F1** 成功打开了 BIOS 设置实用程序！现在您已进入 BIOS，请按照以下确切步骤将 USB 驱动器设置为第一启动设备：

1. **插入 USB：** 确保在开机或重启前连接好可启动的 USB 闪存盘，以便 BIOS 正确检测到它。
2. **导航到启动菜单：** 使用方向键选择顶部的 **Startup** 或 **Boot** 标签。
3. **选择主启动顺序：** 高亮 **Primary Boot Sequence**（或 **Boot Device Priority**）并按 **Enter**。
4. **将 USB 移到顶部：** 找到您的 USB 驱动器（它可能被命名为 **USB-HDD**、**USB Storage** 或驱动器的品牌名称）。使用 **+** 和 **-** 键（或 **Page Up / Page Down**）将 USB 选项移动到位置 **1**。
5. **保存并退出：** 按 **F10**，选择 **Yes** 保存更改，然后按 **Enter**。

您的系统将重新启动并直接从 USB 驱动器启动。
