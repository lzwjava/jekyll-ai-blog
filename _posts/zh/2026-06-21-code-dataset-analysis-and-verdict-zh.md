---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 代码数据集分析与裁决
translated: true
type: note
---

现在我已经有了完整的图景。以下分析：

================================================================
代码数据集探索 — 分析
================================================================

## 1. The Stack v2 (bigcode/the-stack-v2-dedup)

| 项目 | 详情 |
| ------ | ------ |
| 大小 | 67.5TB 完整 / 32.1TB 去重后 |
| 令牌数 | ~900B |
| 语言 | 658种 |
| 格式 | 仅SWHID（文件ID，非实际代码） |

结论：**不实用。** HF数据集只存储Software Heritage ID，不包含代码内容。要获取实际文件，你需要：

- AWS S3凭证（softwareheritage存储桶）
- 与Software Heritage + INRIA达成协议
- 通过S3 API逐文件下载

这专为BigCode的内部流水线设计，不适合个人下载。

## 2. The Stack v1 (bigcode/the-stack)

| 项目 | 详情 |
| ------ | ------ |
| 大小 | 6.4TB 完整 / 2.9TB 去重后 |
| 令牌数 | ~200B |
| 语言 | 358种 |
| 格式 | 直接代码内容 |

结论：**可能可行但需协议。** 你必须在HF上接受条款并提供联系方式。2.9TB去重后勉强能塞进这块1.8TB硬盘，需要选择性语言下载。

## 3. codeparrot/github-code

| 项目 | 详情 |
|------|------|
| 大小 | ~1TB 未压缩 / ~300GB 压缩 |
| 令牌数 | 1.15亿文件 |
| 语言 | 32种 |
| 格式 | 直接代码，可从HF流式读取 |

结论：**此机器的最佳选择。** 可直接下载，无需特殊协议。1TB可放入（972GB空闲）。包含Python、JS、TS、C++、Rust、Go、Java等。可通过`datasets`库流式读取。

## 4. bigcode/the-stack-smol

| 项目 | 详情 |
|------|------|
| 大小 | 2.6GB |
| 样本 | 30万文件 |
| 语言 | 30种 |
| 格式 | 直接代码内容 |

结论：**仅适合测试。** 对真实预训练来说太小（约1亿令牌）。但在投入大下载前可用于验证你的流水线。

## 5. nampdn-ai/tiny-codes

| 项目 | 详情 |
|------|------|
| 大小 | ~2GB |
| 样本 | 160万代码片段 |
| 语言 | 11种 |
| 重点 | 通过代码进行推理（if/else，逻辑） |

结论：**微调数据，非预训练。** 受"Textbooks Are All You Need"启发。适合以较小比例混入以提升推理能力，但太小且为合成数据，不适合预训练。

## 6. FineWeb / FineWeb-Edu（已在磁盘上）

| 项目 | 详情 |
| ------ | ------ |
| 磁盘上 | 285GB（nanoGPT分片）+ 374GB（zz-backup parquet） |
| 内容 | 英文网页文本（文章、博客、论坛） |
| 代码内容 | 极少——这不是代码数据集 |

结论：**已处理，但数据类型错误。** FineWeb是一般网页文本。它含有少量偶然出现的代码（StackOverflow回答、教程），但不是代码语料库。你现有的760M配置将其用于通用语言模型训练。

## 7. StarCoder 训练仓库

| 仓库 | 用途 |
|------|------|
| bigcode-project/starcoder | 仅含微调 + 推理脚本 |
| bigcode-project/starcoder2 | 使用LoRA/PEFT微调 |

结论：**对预训练无用。** 这些仓库包含微调代码，而非预训练流水线。StarCoder2使用Megatron-LM的分支进行预训练（未以干净仓库形式公开发布）。

================================================================
针对你当前设置的推荐
================================================================

你的机器：RTX 4070（12GB），64GB RAM，972GB空闲磁盘。

**步骤1：用the-stack-smol（2.6GB）进行测试**

```bash
pip install datasets
python3 -c "
from datasets import load_dataset
ds = load_dataset('bigcode/the-stack-smol', split='train')
print(ds)
print(ds[0])
"
```

**步骤2：下载codeparrot/github-code（压缩后约300GB）**
这是可直接下载的最佳真实代码数据集。若磁盘紧张可按语言过滤：

```bash
python3 -c "
from datasets import load_dataset
# 先只下载Python子集
ds = load_dataset('codeparrot/github-code', streaming=True, split='train',
                  languages=['Python'])
# 处理为nanoGPT格式...
"
```

**步骤3：与FineWeb-Edu混合**
对于代码+通用语言模型，按70%代码 + 30% FineWeb-Edu混合。你现有的nanoGPT数据流水线可处理此操作。

================================================================

需要我下载the-stack-smol做快速测试，还是开始拉取codeparrot/github-code（先下载Python子集）？
