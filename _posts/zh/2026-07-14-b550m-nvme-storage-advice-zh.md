---
audio: false
generated: true
image: false
lang: zh
layout: post
title: B550M NVMe存储建议
translated: true
type: note
---

问题：这个配置（R5 5600 + B550M-GAMING WIFI6E V14 + MI50 16GB + 32GB DDR4-3200）应该添加什么存储？

回答：

像这款预算型B550M主板通常提供 **2个M.2插槽**：一个直连CPU的PCIe 4.0 x4，另一个通过B550芯片组连接的PCIe 3.0 x4。购买两块Gen4硬盘前请务必查阅手册确认——将Gen4硬盘放在芯片组侧插槽纯属浪费，因为那里只能以Gen3速度运行。

**主盘：1TB–2TB NVMe Gen4，安装在CPU直连M.2插槽。**

这是你的操作系统+活跃模型存储。本地推理工作的容量选择逻辑：
- 量化后的7B模型（Q4_K_M GGUF）：每个约4-5GB
- 量化后的13B：约8GB
- 量化后的70B：约40GB
- 如果你保留原始fp16/bf16用于重新量化，体积为上述的2倍

如果你只运行适合MI50 16GB显存的模型（实际为7B-13B级别，或高度量化的30B），**1TB足够**装下操作系统+15-20个模型+数据集。如果你还进行本地微调实验，检查点会快速消耗空间——上2TB。

**不要在这块硬盘上贪便宜**——加载模型分片和mmap'd GGUF文件时，随机4K读取性能比顺序读写更重要。坚持使用知名主控（Samsung、WD Black、Crucial P系列、Kingston KC/Fury），避免杂牌QLC硬盘，因为缺乏足够SLC缓存的QLC硬盘在大规模顺序写入（下载/量化模型）时会出现严重卡顿。

**副盘（可选）：便宜的2TB+ SATA SSD或HDD，用于芯片组M.2/SATA接口**，如果你囤积原始数据集、safetensors原文件或不需要NVMe速度的训练数据。

**具体推荐：** 在CPU直连插槽安装2TB Gen4 NVMe（例如Crucial P3 Plus、WD Black SN770/SN850X级别）。除非你确定要囤积原始数据集，否则先跳过第二块硬盘——后续随时可加装，这块主板升级只需5分钟。

参考：
- [B550芯片组M.2插槽布线（CPU直连 vs 芯片组）](https://www.amd.com/en/products/chipsets/b550)
- [NVMe QLC vs TLC持续写入行为](https://www.tomshardware.com/reviews/best-ssds,5518.html)