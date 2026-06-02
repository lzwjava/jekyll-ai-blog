---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: OpenWebText与维基百科数据集种子
translated: true
type: note
---

### OpenWebText 数据集种子文件

OpenWebText 是 OpenAI WebText 数据集的开源复现版本，包含从高评分 Reddit 链接中提取的约 38GB 清洁文本（主要经过质量筛选的网页内容）。这是训练语言模型常用的超大规模文本语料库。虽然完整抓取文本并不总是以单一种子形式提供，以下是可靠获取方式：

- **URL 列表（过滤版，约 480MB）**：经过预过滤的约 2600 万条 URL 列表，用于抓取 OpenWebText。您可用此列表自行下载和处理文本。
  - 种子文件：[OpenWebText-urls-26M-filtered.xz](https://academictorrents.com/details/f5161721b322bca66ed74da32b963c1066e64312)
  - 来源：Academic Torrents（社区做种）

- **URL 列表（完整版，约 1.75GB）**：来自 Reddit 提交内容的完整去重 URL 集合。
  - 种子文件：[WebText dataset urls.txt.tar.gz](https://academictorrents.com/details/15f3494b2991e75194d3af72bf7afa5025a7abc3)
  - 来源：Academic Torrents（社区做种）

- **分词处理版（约 16GB）**：基于抓取语料库的 GPT-2 分词文本文件（395 个文件，可直接用于模型训练）。
  - 种子文件：[OpenWebText (Gokaslan's distribution, 2019), GPT-2 Tokenized](https://academictorrents.com/details/36c39b25657ce1639ccec0a91cf242b42e1f01db)
  - 来源：Academic Torrents（由 OSUOSL 和社区做种）

如需获取完整原始文本语料库，请查阅[OpenWebText GitHub 仓库](https://github.com/eukaryote31/openwebtext)的直接下载链接（非种子方式）或使用上述 URL 配合抓取脚本。增强版本 OpenWebText2（约数 TB 规模）可通过 [EleutherAI 仓库](https://github.com/EleutherAI/openwebtext2)获取，但采用流式传输而非种子方式。

### 维基百科数据转储种子文件

维基百科数据转储是每月发布的完整数据库 XML 导出文件（包含文章、修订记录、元数据）。英文版数据规模庞大（摘要版压缩后约 20-25GB，完整历史版超过 100GB）。种子文件由社区维护（非官方但经过官方校验和验证）并通过维基媒体服务器进行网络做种以确保可靠性。请务必通过 [dumps.wikimedia.org](https://dumps.wikimedia.org/enwiki/latest/) 的哈希值验证下载文件。

种子文件主要集散地为 [Meta-Wiki 数据转储种子页面](https://meta.wikimedia.org/wiki/Data_dump_torrents#enwiki)，其中列出了最新的英文维基百科转储（例如 enwiki-20251101）。以下是近期转储概览：

| 转储日期 | 文件类型 | 压缩后大小 | 种子链接 | 备注 |
|-----------|-----------|-----------------|--------------|-------|
| 2025-11-01 | 页面-文章（XML，仅摘要） | ~22GB | [enwiki-20251101-pages-articles-multistream.xml.bz2](https://meta.wikimedia.org/wiki/Data_dump_torrents#enwiki) | 多流格式，最便于文本提取 |
| 2025-11-01 | 页面-文章-历史（XML，完整修订版） | ~120GB | [enwiki-20251101-pages-meta-history*.xml.bz2](https://meta.wikimedia.org/wiki/Data_dump_torrents#enwiki) | 包含所有编辑记录，分数据流存储便于处理 |
| 2025-10-01 | 页面-文章（XML，仅摘要） | ~21GB | [enwiki-20251001-pages-articles-multistream.xml.bz2](https://meta.wikimedia.org/wiki/Data_dump_torrents#enwiki) | 上月转储，适用于历史对比 |

- **完整合集**：可在 [Academic Torrents 维基百科合集](https://academictorrents.com/collection/wikipedia) 浏览所有历史英文维基百科种子文件（包含最早至 2010 年的旧版转储）
- **Kiwix ZIM 格式**：如需可浏览的离线维基百科（HTML 格式，约 100GB），可尝试 [wikipedia_en_all_maxi_2024-01.zim.torrent](https://download.kiwix.org/zim/wikipedia/wikipedia_en_all_maxi_2024-01.zim.torrent) – 社区做种版本，但请访问 [Kiwix 下载页面](https://download.kiwix.org/zim/wikipedia/) 查看 2025 年更新

如需将这些数据转换为纯文本格式，建议使用 Python 的 `wikiextractor` 等工具。种子下载方式可降低服务器负载并支持断点续传 – 推荐使用 qBittorrent 等客户端。如需其他语言或子集的数据转储，可通过 Meta-Wiki 页面的筛选功能查找。
