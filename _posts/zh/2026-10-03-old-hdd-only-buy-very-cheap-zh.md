---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 旧硬盘，只买非常便宜的
translated: true
type: note
---

问题：这款500GB HGST Z5K500 2.5英寸5400转SATA机械硬盘怎么样？

答案：**这是一款可用的老旧笔记本电脑硬盘，但只值得非常便宜地购买。**

* **型号：** HGST Z5K500，500GB，2.5英寸，SATA，5400转，16MB缓存
* **接口：** SATA，因此应该兼容普通的SATA笔记本/台式机适配器。
* **性能：** 健康状态下连续读写速度大约**80–120 MB/s**；随机I/O相比任何SSD都会非常慢。
* **容量：** 500GB适合用于大容量存储、Linux测试、ISO/模型数据集、日志等。
* **功耗：** 低功耗2.5英寸机械盘，适合笔记本电脑和小型测试机。
* **年代：** 这是一款**老一代的HGST/日立硬盘**。“几乎全新外观”并不代表磁介质或轴承的使用时间少。

### 重要部分：检查SMART

不要仅因为卖家说“功能正常”就购买。索要以下命令的截图/输出：

```bash
smartctl -a /dev/sdX
```

我特别要检查：

```text
SMART overall-health
Reallocated_Sector_Ct
Current_Pending_Sector
Offline_Uncorrectable
Power_On_Hours
UDMA_CRC_Error_Count
```

对于二手硬盘，理想状态是：

```text
Reallocated_Sector_Ct = 0
Current_Pending_Sector = 0
Offline_Uncorrectable = 0
```

如果你确实在意数据，那么运行一次长测试：

```bash
sudo smartctl -t long /dev/sdX
# 等待完成
sudo smartctl -a /dev/sdX
```

### 价格

针对你的使用场景，我的大致估价如下：

| 价格 | 我的看法 |
| --------: | ------------------------------------------------------ |
| **¥20–30** | 非常便宜，值得拿来做测试/存储盘 |
| **¥30–50** | 如果SMART数据优秀，还算合理 |
| **¥50–70** | 仅在真正低使用时长/SMART极佳的情况下才考虑 |
| **¥80+** | 我不会买 |
| **¥100+** | 不如买个二手SATA SSD |

对于**GPU/LLM实验室机器**，我不会用它做系统盘。一块便宜的240/480GB SATA SSD会让体验快得多。这块硬盘更适合作为**辅助大容量/测试盘**。

如果你告诉我**闲鱼上的要价**，我可以判断这个具体链接是否值得购买。
