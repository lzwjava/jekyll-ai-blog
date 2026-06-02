---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: FineWeb 2013数据集概要
translated: true
type: note
---

**CC-MAIN-2013-20**（2013年夏季数据转储）在FineWeb数据集中：

- **.parquet文件数量**：约**460–500个**
  （文件分片大小不一：多数约1 GB，部分较大可达2 GB。目录总容量为**422 GB**，按平均0.9 GB计算约含460–480个分片。文件命名按序从`000_00000.parquet`至约`000_004xx.parquet`）

- **所有parquet文件总大小**：**422 GB**

- **使用GPT风格分词器编码后的词元数量**（GPT-4采用的cl100k_base或FineWeb报告使用的旧版GPT-2分词器）：
  **1445亿词元**（经过FineWeb的数据清洗、过滤与去重流程后）

注：原始Common Crawl转储数据规模更大（过滤前约3930亿词元），但FineWeb仅保留高质量英文文本，因此这个2013年的旧转储数据经处理后大幅缩减。

若下载整个目录（例如通过`huggingface-cli download`或遍历所有分片的脚本），最终将获得约422 GB的parquet文件，内含1445亿个可直接用于训练的词元。

[FineWeb数据集卡片（含各转储词元统计表）](https://huggingface.co/datasets/HuggingFaceFW/fineweb)
[HF上的CC-MAIN-2013-20目录（显示总容量）](https://huggingface.co/datasets/HuggingFaceFW/fineweb/tree/main/data/CC-MAIN-2013-20)
