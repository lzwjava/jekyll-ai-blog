---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FineWeb数据集规模详情
translated: true
type: note
---

**是的，44TB这个数字是正确的——但它指的是原始FineWeb v1.0版本所占用的磁盘空间，而非一个绝对上限。**

以下是详细说明：

---

## 🍷 FineWeb —— 原始版本（v1.0）

Hugging Face于2024年5月31日发布了FineWeb，这是一个大规模数据集，源自**96个CommonCrawl快照**，包含**15万亿个词元（token）**，占用**44TB磁盘空间**。

因此，是的——**44TB**是原始FineWeb数据集的正确磁盘大小数据。

---

## 数据集此后是否有所扩展？

该数据集已经过更新和扩展。根据Hugging Face页面，当前的FineWeb数据集现已包含**超过18.5万亿个词元**（原始为15万亿个词元），这些数据是来自CommonCrawl经过清洗和去重的英文网页数据。

这意味着44TB这个数字对应的是**最初发布的15万亿词元版本**，实际大小已随后续的更新而增长。

---

## FineWeb-Edu子集

除了主数据集，Hugging Face还推出了**FineWeb-Edu**，这是一个从FineWeb中提取的、经定制分类器评定为高教育价值的**1.3万亿词元子集**。这个子集的规模远小于完整数据集。

---

## 关键事实摘要

| 属性 | 数值 |
|---|---|
| 数据源 | 96个CommonCrawl快照 |
| 原始词元数量 | 15万亿词元 |
| 更新后词元数量 | 18.5万亿+词元 |
| 磁盘空间（原始） | **44TB** |
| FineWeb-Edu子集 | 1.3万亿词元 |
| 语言 | 仅英文 |
| 许可证 | ODC-By 1.0 |

---

**结论：** 44TB是**原始FineWeb v1.0**的磁盘占用量，并非硬性上限。该数据集已增长至超过18.5万亿词元，因此实际存储占用量现已大于44TB。

参考文献：

- [HuggingFace FineWeb数据集页面](https://huggingface.co/datasets/HuggingFaceFW/fineweb)
- [FineWeb论文（arXiv）](https://arxiv.org/html/2406.17557v1)
- [MarkTechPost文章](https://www.marktechpost.com/2024/06/03/huggingface-releases-%F0%9F%8D%B7-fineweb-a-new-large-scale-15-trillion-tokens-44tb-disk-space-dataset-for-llm-pretraining/)