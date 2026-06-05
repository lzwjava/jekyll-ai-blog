---
audio: false
generated: false
image: true
lang: zh
layout: post
title: LLM粥 — 简单粥看世界
translated: true
---

白粥简单，快速吃完。这出人意料地接近FlashAttention的LLM训练与推理。你可以说，两者在某个关键方面完全一致。

要想吃得快，就得用平铺开的浅盘子。当浅盘子装不下时，就需要多个浅盘子。这与GPU的计算块（tile）——计算砖块——是同一逻辑。

![电饭煲里煮着的粥](/assets/images/porridge/p1.jpg)

简单白粥看世界。简单白粥看大语言模型。大道至简。

![桌上三碗粥](/assets/images/porridge/p2.jpg)

## 类比

FlashAttention的工作原理是将注意力矩阵分块为能放入GPU SRAM的小块——即平铺开的浅盘子。每个计算块（一块GPU砖块）处理矩阵的一部分，无需在HBM中实例化完整的O(n²)注意力矩阵。当一块不够用时，就依次使用多块计算块。与白粥同理：一个浅盘子盛不下一碗粥，那就分到几个盘子里。

<div style="text-align: center; margin: 1.5em 0;">
  <img src="/assets/images/porridge/p3.jpg" alt="FlashAttention信息图——分块演进" style="max-width: 100%; border-radius: 6px;" />
  <p style="font-size: 0.85em; color: #888; margin-top: 0.5em;">图片来源：网络</p>
</div>

## 光盘——推理成功

光盘。Token米粒顺利通过浅盘子（GPU砖块）进入我的胃里。推理成功。

唯一美中不足：我用了三个盘子而不是四个。无法进行并行计算。

![光盘——Token已消耗](/assets/images/porridge/p4.jpg)

四个盘子意味着四个GPU计算块并行运行——充分利用。三个盘子则有一个计算块闲置。这就是硬件利用率75%与100%的差别。粥反正都能吃完，但吞吐量的故事就不同了。

大道至简：摊平工作，多用计算块，全部消耗。白粥与Transformer共享同一智慧。
