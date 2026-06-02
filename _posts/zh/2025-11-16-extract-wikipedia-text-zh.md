---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 从维基百科转储文件中提取文本
translated: true
type: note
---

以下是针对您提供的维基百科`.bz2`转储文件（`enwiki-latest-pages-articles1.xml-p1p41242.bz2`）提取纯文本最常用且有效的方法。

### 推荐工具与方法（按从易到难排序）

#### 1. 使用wikiextractor（适合多数用户——快速且干净）

这是自然语言处理/机器学习领域处理维基百科转储的标准工具。

```bash
# 安装（仅需一次）
pip install wikiextractor

# 提取文本（移除模板、表格等，提供每篇文章的干净文本）
wikiextractor enwiki-latest-pages-articles1.xml-p1p41242.bz2 --output wiki_text
```

- 输出：创建`wiki_text/`文件夹，内含AA、AB等子文件夹，包含干净的JSON/文本文件。
- 获取纯文本（每篇文章一行）：

```bash
wikiextractor enwiki-latest-pages-articles1.xml-p1p41242.bz2 --processes 8 -o wiki_text --json
# 如需将JSON转为纯文本
find wiki_text -name '*' -exec cat {} \; | grep '"text":' | sed 's/.*"text": "//;s/"$//' > all_text.txt
```

#### 2. 使用gensim的WikiCorpus（适合在Python中进行自然语言处理）

```python
from gensim.corpora import WikiCorpus

# 自动处理.bz2文件并提取文本+分词
wiki = WikiCorpus("enwiki-latest-pages-articles1.xml-p1p41242.bz2", dictionary=False)

# 遍历文章
with open("output.txt", "w", encoding="utf-8") as f:
    for i, text in enumerate(wiki.get_texts()):
        f.write(" ".join(text) + "\n")
        if i % 10000 == 0:
            print(f"已处理 {i} 篇文章")
```

#### 3. 简单bzip2 + grep/awk（快速但粗糙，无清理）

```bash
# 仅解压查看原始XML
bzip2 -dc enwiki-latest-pages-articles1.xml-p1p41242.bz2 | less

# 仅提取<text>内容（非常粗略，保留维基标记）
bzip2 -dc enwiki-latest-pages-articles1.xml-p1p41242.bz2 | \
  sed -n '/<text /,/<\/text>/p' | \
  sed 's/<text[^>]*>//g;s/<\/text>//g' > raw_text_with_markup.txt
```

#### 4. 处理完整转储且需要高速并行（适用于后续所有分块）

您的文件仅是第一个分块（p1p41242），但如果后续需要处理全部约30+个分块：

```bash
# 并行提取所有分块
ls *.bz2 | xargs -P 8 -I {} wikiextractor {} --output wiki_extracted
```

### 当前推荐方案总结

```bash
pip install wikiextractor
wikiextractor enwiki-latest-pages-articles1.xml-p1p41242.bz2 -o extracted_wiki --bytes 1M --json
```

几分钟内即可获得清晰可读的文章（您的压缩文件仅约2-3GB，非常易于处理）。

如需以下定制处理请告知：

- 仅需主名字空间（真实文章，非讨论页）
- 纯文本而非JSON格式
- 分词后输出
- 需处理中文维基百科（zhwiki）——流程完全一致

祝提取顺利！🚀
