---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 英文维基百科下载指南
translated: true
type: note
---

这是来自官方维基媒体下载镜像之一的目录列表（通常是 https://dumps.wikimedia.org/enwiki/latest/）。
其中包含了截至2025年11月初的当前英文维基百科文章的所有下载方式。

### 主要格式及其实际内容

| 文件名模式 | 说明 | 近似大小（未压缩） | 是否最适合训练LLM？ | 备注 |
| --- | --- | --- | --- | --- |
| `enwiki-latest-pages-articles.xml.bz2` | 单个巨型文件，包含**所有**文章+讨论页、模板、重定向页等 | ~85–90 GB 未压缩 | 是，非常常用 | 如果您有足够的空间和带宽，这是最简单的选择 |
| `enwiki-latest-pages-articles1.xml-p1p41242.bz2`  … 直到 … `enwiki-latest-pages-articles27.xml-…` | 相同的数据，但分割成27个较小的块（多流格式） | 每个压缩后约200–600 MB → 总计未压缩仍为~85–90 GB | 是，最受欢迎的选择 | 支持并行下载和轻松断点续传 |
| `enwiki-latest-pages-articles-multistreamX.xml.bz2` (例如 multistream27) | 属于上述分割版本的实际大型压缩数据文件 | 每个压缩后300–600 MB | 这些是您真正需要的数据文件 | 您需要这些文件 + 索引文件 |
| `enwiki-latest-pages-articles-multistreamX.xml.bz2.md5` / `.meta` | 校验和及小型元数据文件 | < 1 KB | 不用于文本处理 | 仅用于验证下载完整性 |
| `enwiki-latest-pages-articles-multistream-indexX.xml.bz2` | 索引文件，指示各文章在大型多流文件中的字节偏移量 | 每个压缩后约30–60 MB | 如果使用多流格式则必需 | 用于快速随机访问；大多数处理脚本都需要它们 |

### 推荐：2025年训练模型时几乎所有人使用的方式

事实上的标准方法（被LLaMA、Mistral、Qwen、DeepSeek、Gemma、Phi等使用）是：

下载 **27个多流文件 + 对应的27个索引文件**
（即所有以 `enwiki-latest-pages-articlesXX.xml-p…p….bz2` 开头以及匹配的 `…-indexXX…bz2` 文件）

或者更简单：如果您的网络连接和磁盘能够处理，直接下载**单个巨型文件**：

```
enwiki-latest-pages-articles.xml.bz2    ← 压缩后24.6 GB，未压缩约85–90 GB
```

两者包含完全相同的原始XML数据（所有主命名空间文章 + 大量额外页面）。

### 为什么不使用小文件（multistream3.xml-p…, multistream4.xml-p… 等）？
这些是2010–2015年间非常旧的分割文件，仅包含维基百科的一小部分（当时恰好落入该页面ID范围内的文章）。它们仅为历史原因保留，现在基本上已无用。

### 快速开始命令（2025年转储）

并行下载推荐的27+27个文件（最快）：

```bash
# 获取文件列表
wget -q https://dumps.wikimedia.org/enwiki/latest/ -O - | \
  grep -E 'enwiki-latest-pages-articles[0-9]+[02468]\.xml-p[0-9]+p[0-9]+\.bz2"' | \
  sed -e 's/.*href="//' -e 's/".*//' | \
  xargs -n1 -P10 wget https://dumps.wikimedia.org/enwiki/latest/

# 同时下载匹配的索引文件
wget -q https://dumps.wikimedia.org/enwiki/latest/ -O - | \
  grep -E 'enwiki-latest-pages-articles-multistream-index' | \
  sed -e 's/.*href="//' -e 's/".*//' | \
  xargs -n1 -P10 wget https://dumps.wikimedia.org/enwiki/latest/
```

或者仅下载单个文件（最简单）：

```bash
wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2
```

之后您通常使用以下工具进行处理：
- wikiextractor (Python) → 清理文本
- Hugging Face `datasets` 的维基百科加载器（已为您完成所有处理）
- DeepSeek 或 EleutherAI 的处理脚本等

简而言之：
下载单个24 GB的 `enwiki-latest-pages-articles.xml.bz2` 文件，或者27个分割文件 + 索引文件。列表中的其他所有内容要么是校验和、旧垃圾数据，要么是训练不需要的元数据。
