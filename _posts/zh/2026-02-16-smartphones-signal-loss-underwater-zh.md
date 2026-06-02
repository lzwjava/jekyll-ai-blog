---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 智能手机水下快速失去信号
translated: true
type: note
---

问题：电磁波在水中的表现如何？将手机装在袋子里扔进水中后，信号会发生什么变化？

答案：

电磁波（EM波），包括智能手机使用的无线电波（如蜂窝信号、Wi-Fi、蓝牙），在水中的行为与空气中截然不同，主要是由于水的电学特性导致的**吸收**和**衰减**。

### 电磁波在水中的行为

- 水（特别是含盐的海水）是一种**导电介质**，会导致电磁波能量快速损失。
- 高频波（如现代手机使用的频率）比低频波遭受**更强的衰减**。
- 关键影响因素：
  - **海水**（高电导率约 4 S/m）：极高的衰减。
  - **淡水**（低电导率约 0.01 S/m）：衰减较低，但对手机频率仍然显著。
- 衰减随频率急剧增加：
  - 在手机频率范围（4G/5G 通常为 700 MHz – 2.6 GHz）和 Wi-Fi/蓝牙（2.4 GHz 或 5 GHz）下，衰减非常严重。
  - 在海水中，2.4 GHz 频率的衰减可超过**每米 700 分贝**——意味着信号在几厘米内几乎消失。
  - 在淡水中，衰减较低（约 1–数分贝/米），但仍足以迅速阻断信号。

低频信号（如潜艇使用的 ELF/VLF）能传播更远，但消费类设备（如智能手机）无法使用这些频率。

### 手机被扔进水中（如装在袋子里）时的信号表现

现代智能手机使用高频无线电波进行蜂窝通信、Wi-Fi 和蓝牙——这些信号在水中都会遭受严重衰减。

- **实际结果** —— 水下几乎无可用信号：
  - 在**海水**（海洋、海水）中：信号在**几厘米**内（通常 <10–20 cm）即消失。即使刚没入水面，连接也会中断。
  - 在**淡水**（泳池、湖泊、河流）中：穿透能力稍好，但通常在**10–50 cm**深度内信号仍会丧失（有时在极浅水域或接近水面且对准良好时可稍微延长）。
  - 实验和报告显示，手机完全浸没后，蜂窝信号、Wi-Fi 和蓝牙几乎立即中断——即使是防水手机，在未采用特殊技术的情况下也无法在水下保持连接。
- 防护袋（如防水袋）无法改善信号传播——它可能保持手机内部干燥且功能正常，但电磁波仍无法有效穿透周围水体到达基站或 Wi-Fi 路由器。
- 极浅浸没（仅几厘米，天线接近水面）在淡水中可能允许弱/间歇信号传输，但这种情况不可靠且不实用。

总结：将智能手机（即使装在防水袋中）扔进水中，会导致其**迅速丧失所有无线信号**（蜂窝、Wi-Fi、数据）在淡水和海水中均如此。手机内部（屏幕、应用等）可能仍能正常工作（如果防水），但需回到水面附近或上方才能恢复联网。

参考资料：

- [https://en.wikipedia.org/wiki/Electromagnetic_absorption_by_water](https://en.wikipedia.org/wiki/Electromagnetic_absorption_by_water)
- [https://www.researchgate.net/figure/Attenuation-experienced-by-EM-signals-in-fresh-and-seawater-for-different-frequencies_fig1_302259776](https://www.researchgate.net/figure/Attenuation-experienced-by-EM-signals-in-fresh-and-seawater-for-different-frequencies_fig1_302259776)
- [https://www.scirp.org/journal/paperinformation?paperid=5906](https://www.scirp.org/journal/paperinformation?paperid=5906)
- [https://electronics.howstuffworks.com/would-a-cell-phone-work-on-a-submerged-submarine.htm](https://electronics.howstuffworks.com/would-a-cell-phone-work-on-a-submerged-submarine.htm)
- [https://underwatermessaging.cs.washington.edu/underwater_comms.pdf](https://underwatermessaging.cs.washington.edu/underwater_comms.pdf)
