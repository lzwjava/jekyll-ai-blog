---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 小规模高质量数据集的替代方案
translated: true
type: note
---

是的，OpenWebText 数据集非常庞大（约 90 亿词元，17GB 的 uint16 文件），预处理耗时且占用大量磁盘空间。以下是更小规模的高质量替代方案，常用于快速测试、调试或训练小型模型：

| 数据集                   | 约计词元量     | 最终 .bin 文件大小 (uint16) | 优势特点                                                                 | 快速获取方式                                              |
|--------------------------|----------------|--------------------------|--------------------------------------------------------------------------|-----------------------------------------------------------|
| **OpenWebText-10k**      | ~4000 万       | ~80MB                    | 与完整版数据分布完全一致，仅取前 1 万篇文档                             | `load_dataset("openwebtext", split="train[:10k]")`        |
| **OpenWebText-100k**     | ~4 亿          | ~800MB                   | 仍具代表性，数分钟即可完成词元化处理                                    | `split="train[:100k]"`                                    |
| **FineWeb-Edu 样本**     | 5000 万–10 亿  | 100MB–2GB                | 质量优于 OWT（采用 LLaMA 式过滤），近期备受推崇                         | `load_dataset("HuggingFaceFW/fineweb-edu", name="sample-10BQ", split="train")` → 约 5000 万词元 |
| **Shakespeare**          | ~100 万        | ~2MB                     | 经典微型数据集，适合快速验证模型基础能力                                | `load_dataset("tiny_shakespeare")` 或直接下载单文本文件    |
| **PG-19（图书）**        | 完整版 28 亿   | ~5.5GB                   | 来源为公版图书，文本纯净，可按需截取部分数据                            | `load_dataset("pg19", split="train[:5%]")` → 约 1.4 亿词元 |
| **C4（子集）**           | 可调节         | 可调节                   | 经 T5 团队清洗的 Common Crawl 数据，纯英文内容                           | `load_dataset("allenai/c4", "en", split="train[:1%]")` streaming=True |
| **RedPajama 样本**       | 500 万–2 亿    | 10MB–400MB               | 多源混合数据（CommonCrawl、维基百科、图书等），复现 LLaMA 数据配方       | `load_dataset("togethercomputer/RedPajama-Data-1T", name="sample", split="train")` |

### 根据需求推荐的方案

1. 需要 5 分钟内跑完且体积最小 → **tiny_shakespeare**
   （nanoGPT 用户首选）

2. 需要真实网络文本但体积小巧 → OpenWebText 前 1 万篇文档
   ```python
   dataset = load_dataset("openwebtext", split="train[:10000]")
   ```

3. 需要当前（2025年）最高质量的小型数据集 → FineWeb-Edu 100 亿词元样本
   （约 5000 万词元，比 OWT 更纯净，质量接近顶尖实验室标准）

   ```python
   dataset = load_dataset(
       "HuggingFaceFW/fineweb-edu",
       name="sample-10BQ",  # 从 100 亿词元中采样，分片后每片约 5000 万词元
       split="train"
   )
   ```

4. 需要小于 500MB 且内容多样 → RedPajama 2 亿词元版本样本
   ```python
   dataset = load_dataset("togethercomputer/RedPajama-Data-1T", name="sample-200M", split="train")
   ```

所有这些数据集都可直接代入现有预处理脚本（仅需替换 load_dataset 语句）。

为提升迭代效率，我通常保留三个二进制文件：
- `shakespeare.bin`   (~2MB)   → 过拟合测试
- `owt_10k.bin`       (~80MB)  → 代码调试
- `fineweb_edu_1B.bin` (~2GB) → 真实小模型训练

如需特定规模的数据集，我可以提供对应的单行加载代码！
