---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: English Wikipedia Download Guide
translated: false
type: note
---

This is a directory listing from one of the official Wikimedia download mirrors (usually <https://dumps.wikimedia.org/enwiki/latest/>).
It contains all the different ways you can download the current English Wikipedia articles (as of early November 2025).

### Main formats and what they actually contain

| File name pattern | What it is | Approx. size (uncompressed) | Best for training LLMs? | Notes |
| --- | --- | --- | --- | --- |
| `enwiki-latest-pages-articles.xml.bz2` | One single giant file with **all** articles + talk pages, templates, redirects, etc. | ~85–90 GB uncompressed | Yes, very commonly used | Easiest if you have space and bandwidth |
| `enwiki-latest-pages-articles1.xml-p1p41242.bz2`  … up to … `enwiki-latest-pages-articles27.xml-…` | The same data, but split into 27 smaller chunks (multistream) | Each ~200–600 MB compressed → total still ~85–90 GB uncompressed | Yes, most popular choice | Lets you download in parallel and resume easily |
| `enwiki-latest-pages-articles-multistreamX.xml.bz2` (e.g. multistream27) | The actual huge compressed data files that belong to the split version above | 300–600 MB each compressed | These are the real data files you want | You need these + the index files |
| `enwiki-latest-pages-articles-multistreamX.xml.bz2.md5` / `.meta` | Checksum and tiny metadata files | < 1 KB | Not needed for text | Only for verifying downloads |
| `enwiki-latest-pages-articles-multistream-indexX.xml.bz2` | Index files that tell you which article is at which byte offset in the big multistream files | ~30–60 MB each compressed | Required if you use multistream | Needed for fast random access; most processing scripts expect them |

### Recommendation: What almost everyone uses to train models in 2025

The de-facto standard way (used by LLaMA, Mistral, Qwen, DeepSeek, Gemma, Phi, etc.) is:

Download the **27 multistream files + their 27 index files**
(that is everything that starts with `enwiki-latest-pages-articlesXX.xml-p…p….bz2` and the matching `…-indexXX…bz2`)

Or even simpler: just download the **single giant file** if your connection and disk can handle it:

```
enwiki-latest-pages-articles.xml.bz2    ← 24.6 GB compressed, ~85–90 GB uncompressed
```

Both contain exactly the same raw XML data (all main-namespace articles + a lot of extra pages).

### Why not the tiny files (multistream3.xml-p…, multistream4.xml-p… etc.)?

Those are very old splits from 2010–2015 that only contain a tiny fraction of Wikipedia (articles that happened to fall into that page-ID range back then). They are kept only for historical reasons and are basically useless today.

### Quick start commands (2025 dump)

Parallel download of the recommended 27+27 files (fastest):

```bash
# Get the list of files
wget -q https://dumps.wikimedia.org/enwiki/latest/ -O - | \
  grep -E 'enwiki-latest-pages-articles[0-9]+[02468]\.xml-p[0-9]+p[0-9]+\.bz2"' | \
  sed -e 's/.*href="//' -e 's/".*//' | \
  xargs -n1 -P10 wget https://dumps.wikimedia.org/enwiki/latest/

# Also download the matching index files
wget -q https://dumps.wikimedia.org/enwiki/latest/ -O - | \
  grep -E 'enwiki-latest-pages-articles-multistream-index' | \
  sed -e 's/.*href="//' -e 's/".*//' | \
  xargs -n1 -P10 wget https://dumps.wikimedia.org/enwiki/latest/
```

Or just the single file (simplest):

```bash
wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2
```

After that you normally process it with tools like:

- wikiextractor (Python) → clean text
- the Hugging Face `datasets` Wikipedia loader (already does everything for you)
- DeepSeek’s or EleutherAI’s processing scripts, etc.

So in short:
Download either the single 24 GB `enwiki-latest-pages-articles.xml.bz2` or the 27 split files + indexes. Everything else in that list is either checksums, old garbage, or metadata you don’t need for training.
