---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 同步时分复用
translated: true
type: note
---

问题：当每个信号源被分配一个固定的、不能在源之间转移的时间片时，这种多路复用方法叫什么？

答案：这种多路复用方法称为**同步时分多路复用（Synchronous Time Division Multiplexing，STDM）**。

在同步TDM中，总传输时间被划分为固定长度的**帧**，每个帧又被细分为固定数量的**时隙**。每个信号源（信道）永久地分配在每个帧中一个特定的时隙——无论该源是否有数据要发送。时隙分配是固定的，不可转让。

关键特性：

- **固定时隙分配**——每个源始终拥有每个帧中相同的时隙位置
- **可能浪费**——如果某个源没有数据，其时隙将为空（浪费带宽）
- **同步简单**——无需寻址开销；仅凭位置即可识别源
- **与统计时分多路复用（Statistical TDM）对比**——统计TDM中时隙仅动态分配给有数据的源，消除了浪费，但需要地址头

一个经典的现实世界例子是**T1/E1电话线路**，其中每个语音信道在每个125微秒的帧中获得一个固定的8位时隙。

参考文献：
- [时分多路复用 – Wikipedia](https://en.wikipedia.org/wiki/Time-division_multiplexing)
- [同步TDM与异步TDM的区别 – GeeksforGeeks](https://www.geeksforgeeks.org/difference-between-synchronous-tdm-and-asynchronous-tdm/)