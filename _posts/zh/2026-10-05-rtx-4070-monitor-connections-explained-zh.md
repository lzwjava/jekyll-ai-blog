---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RTX 4070显示器连接详解
translated: true
type: note
---

Question: 如果我用RTX 4070通过HDMI连接，单个或多个显示器需要什么接口？

Answer: RTX 4070在这方面的表现很好。大多数RTX 4070显卡配备**3个DisplayPort 1.4a和1个HDMI 2.1**，并且可以同时驱动最多4台显示器。

**此设置中的HDMI**
- HDMI端口是HDMI 2.1，因此一根好的HDMI线缆可以支持4K 120Hz（使用压缩技术可支持更高规格）。
- 请使用一根**“超高速”HDMI 2.1线缆**（48 Gbps认证）。旧线缆可能会将你限制在4K 60Hz或导致画面闪烁。
- 你的显示器也必须具备HDMI 2.1端口才能获得全速。如果显示器只有HDMI 2.0，最高只能达到4K 60Hz或1440p 144Hz。

**多显示器配置**
- 显卡只有**一个HDMI端口**，因此连接2台或3台显示器时，其他显示器需要使用DisplayPort。
- 典型设置：显示器1接DisplayPort，显示器2接DisplayPort，显示器3接HDMI。
- 如果显示器没有DisplayPort输入，请使用**DisplayPort转HDMI转接头或转换线**（主动式转接头在高刷新率或4K下效果最佳）。

**DisplayPort vs HDMI**
- **DisplayPort 1.4a**通常是PC显示器的最佳选择，尤其对于高刷新率（144Hz及以上）和G-Sync。
- **HDMI 2.1**更适合电视或只有HDMI接口的显示器。

**快速提示**
- 将每台显示器直接插入显卡，而非主板的视频接口（主板接口使用集成显卡，而非4070）。
- 检查你具体显卡型号的端口布局，因为少数定制设计有所不同。
- 连接后，在Windows中手动设置刷新率（设置 > 显示 > 高级显示），因为系统可能默认设置为60Hz。

如果你告诉我你的显示器型号或分辨率和刷新率，我可以确切告诉你该买哪种线缆。

参考资料：
- 此回答未使用外部来源。