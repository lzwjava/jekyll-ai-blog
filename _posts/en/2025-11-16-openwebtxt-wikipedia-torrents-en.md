---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: OpenWebText and Wikipedia Dataset Torrents
translated: false
type: note
---

### OpenWebText Dataset Torrents

OpenWebText is an open-source replication of OpenAI's WebText dataset, consisting of ~38GB of cleaned text extracted from high-karma Reddit links (primarily web pages scraped and filtered for quality). It's a popular large-scale text corpus for training language models. While the full scraped text isn't always directly available as a single torrent, here are reliable options:

- **URLs List (Filtered, ~480MB)**: A pre-filtered list of ~26 million URLs used for scraping OpenWebText. You can use this to download and process the text yourself.
  - Torrent: [OpenWebText-urls-26M-filtered.xz](https://academictorrents.com/details/f5161721b322bca66ed74da32b963c1066e64312)
  - Source: Academic Torrents (seeded by community).

- **URLs List (Full, ~1.75GB)**: The complete deduplicated URLs from Reddit submissions.
  - Torrent: [WebText dataset urls.txt.tar.gz](https://academictorrents.com/details/15f3494b2991e75194d3af72bf7afa5025a7abc3)
  - Source: Academic Torrents (seeded by community).

- **Tokenized Version (~16GB)**: GPT-2 tokenized text files from the scraped corpus (395 files, ready for model training).
  - Torrent: [OpenWebText (Gokaslan's distribution, 2019), GPT-2 Tokenized](https://academictorrents.com/details/36c39b25657ce1639ccec0a91cf242b42e1f01db)
  - Source: Academic Torrents (seeded by OSUOSL and community).

For the full raw text corpus, check the official site for direct downloads (not torrent-based) or use the URLs above with scraping scripts from the [OpenWebText GitHub repo](https://github.com/eukaryote31/openwebtext). An enhanced version, OpenWebText2 (~multi-TB scale), is available via [EleutherAI's repo](https://github.com/EleutherAI/openwebtext2) but uses streaming rather than torrents.

### Wikipedia Dump Torrents

Wikipedia dumps are monthly XML exports of the entire database (articles, revisions, metadata). The English version is massive (~20-25GB compressed for abstracts, up to 100+GB for full history). Torrents are community-maintained (unofficial but verified against official checksums) and web-seeded from Wikimedia servers for reliability. Always verify downloads against [dumps.wikimedia.org](https://dumps.wikimedia.org/enwiki/latest/) hashes.

The main hub for torrents is the [Meta-Wiki Data Dump Torrents page](https://meta.wikimedia.org/wiki/Data_dump_torrents#enwiki), which lists the latest English Wikipedia dumps (e.g., enwiki-20251101). Here's a summary of recent ones:

| Dump Date | File Type | Compressed Size | Torrent Link | Notes |
| ----------- | ----------- | ----------------- | -------------- | ------- |
| 2025-11-01 | Pages-Articles (XML, abstracts only) | ~22GB | [enwiki-20251101-pages-articles-multistream.xml.bz2](https://meta.wikimedia.org/wiki/Data_dump_torrents#enwiki) | Multistream format; easiest for text extraction. |
| 2025-11-01 | Pages-Articles-History (XML, full revisions) | ~120GB | [enwiki-20251101-pages-meta-history*.xml.bz2](https://meta.wikimedia.org/wiki/Data_dump_torrents#enwiki) | Includes all edits; split into streams for easier handling. |
| 2025-10-01 | Pages-Articles (XML, abstracts only) | ~21GB | [enwiki-20251001-pages-articles-multistream.xml.bz2](https://meta.wikimedia.org/wiki/Data_dump_torrents#enwiki) | Previous monthly; good for historical comparison. |

- **Full Collection**: Browse all historical English Wikipedia torrents on [Academic Torrents Wikipedia Collection](https://academictorrents.com/collection/wikipedia) (includes older dumps back to ~2010).
- **Kiwix ZIM Format**: If you want a browsable offline Wikipedia (HTML, ~100GB), try [wikipedia_en_all_maxi_2024-01.zim.torrent](https://download.kiwix.org/zim/wikipedia/wikipedia_en_all_maxi_2024-01.zim.torrent) – community-seeded, but check for 2025 updates on [Kiwix downloads](https://download.kiwix.org/zim/wikipedia/).

For processing these into plain text, use tools like `wikiextractor` from Python. Torrents reduce server load and resume interrupted downloads – use a client like qBittorrent. If you need dumps for other languages or subsets, the Meta-Wiki page has filters.
