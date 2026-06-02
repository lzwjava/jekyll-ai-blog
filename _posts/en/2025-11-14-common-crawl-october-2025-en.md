---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Common Crawl October 2025 Dataset Summary
translated: false
type: note
---

This table is the official summary of the **Common Crawl October 2025 crawl**, specifically the dataset labeled **CC-MAIN-2025-43**. Common Crawl is a non-profit project that crawls the entire public web every month or two and releases the raw data for free so researchers, companies, and anyone else can use it (e.g., for training large language models like GPT, LLaMA, Grok, etc.).

Here’s what each part of the table means:

### Basic facts
- **Name**: CC-MAIN-2025-43 → the 43rd weekly crawl released in 2025, done roughly in October 2025.
- **Size**: 2.61 billion individual web pages were captured.

### The different data types and what they contain

| Data Type              | What it is                                                                                  | Total uncompressed size | # of files | Compressed size |
|------------------------|---------------------------------------------------------------------------------------------|-------------------------|------------|-----------------|
| **WARC**               | The raw, full crawl data (complete HTTP responses: headers + HTML + embedded resources)    | ~ hundreds of TiB       | 100,000    | 97.73 TiB       |
| **WAT**                | Metadata extracted from the WARC files (e.g., outgoing links, language, content-length, etc.) in JSON format |                         | 100,000    | 18.39 TiB       |
| **WET**                | Only the extracted plain text (no HTML tags, no boilerplate, just cleaned text)             |                         | 100,000    | 7.38 TiB        |
| **Robots.txt files**   | All robots.txt files that were fetched during the crawl                                     |                         | 100,000    | 0.15 TiB        |
| **Non-200 responses**  | Responses that were not successful (404s, 500s, redirects, etc.)                            |                         | 100,000    | 3.07 TiB        |
| **URL index files**    | Index that lets you look up which WARC file contains a specific URL (old format)            |                         | 302        | 0.20 TiB        |
| **Columnar URL index** | Newer, faster columnar index (Parquet format) for big-data tools like Spark, DuckDB, etc.   |                         | 900        | 0.23 TiB        |

### Why the different formats exist
- If you just want to train a language model → you usually download the **WET** files (already cleaned text, smallest size).
- If you need full HTML, images, CSS, etc. → you download the **WARC** files (biggest).
- If you need metadata (links, detected language, etc.) without the full HTML → **WAT**.
- The indexes let you find pages without scanning all 100,000 files.

### How the files are organized
Everything is split into 100, followed by **segments** (roughly 1 TiB compressed each for WARC). Each segment contains many smaller .warc.gz (or .wat.gz, .wet.gz) files. The *.paths.gz files you see listed are just text files that contain the full list of S3 URLs for each type.

You can access everything for free on AWS S3 at:
`s3://commoncrawl/crawl-data/CC-MAIN-2025-43/`
(or via HTTPS: https://data.commoncrawl.org/)

In short: This is one of the largest open web datasets in the world (2.61 billion pages from October 2025), freely available in different processed forms, and the table is just telling you how big each processed version is and where to find the file lists.
