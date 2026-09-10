---
audio: false
generated: true
image: false
lang: zh
layout: post
title: JUSB3内部USB 2.0接口
translated: true
type: note
---

问题：**MSI B150M PRO 上的 JUSB3 是什么？**

答案：**JUSB3 是主板上的一个内部 USB 2.0 插针**。

通常它是一个 **9 针（2×5，缺一根针）** 连接器，用于前置面板的 USB 2.0 端口：

```text
JUSB3
┌─────────┐
│ • • • • •│
│ • • • •  │
└─────────┘
     ↑
   USB 2.0
```

你可以连接以下设备：

* 机箱前置 USB 2.0 端口
* 部分内部 USB 2.0 设备
* 某些一体式水冷/控制器设备

它与 **CPU/内存自检（POST）无关**。对于你当前的无显示排查问题，可以 **完全不连接 JUSB3**。

如果你上传一张主板的照片，我可以帮你识别你这块 B150M PRO 上 **JUSB3 及其周围的插针**。