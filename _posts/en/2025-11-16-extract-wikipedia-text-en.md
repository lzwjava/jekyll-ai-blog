---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Extracting Text from Wikipedia Dumps
translated: false
type: note
---

Here are the most common and effective ways to extract plain text from Wikipedia `.bz2` dump files like yours (`enwiki-latest-pages-articles1.xml-p1p41242.bz2`).

### Recommended Tools & Methods (from easiest to most efficient)

#### 1. Use wikiextractor (best for most people – fast and clean)

This is the standard tool used by almost everyone in NLP/ML for Wikipedia dumps.

```bash
# Install (once)
pip install wikiextractor

# Extract text (removes templates, tables, etc., gives clean text per article)
wikiextractor enwiki-latest-pages-articles1.xml-p1p41242.bz2 --output wiki_text
```

- Output: creates a folder `wiki_text/` with subfolders AA, AB, … containing `.bz2` files of clean JSON/text.
- To get plain text (one article per line):

```bash
wikiextractor enwiki-latest-pages-articles1.xml-p1p41242.bz2 --processes 8 -o wiki_text --json
# Then convert JSON to plain text if needed
find wiki_text -name '*' -exec cat {} \; | grep '"text":' | sed 's/.*"text": "//;s/"$//' > all_text.txt
```

#### 2. Use gensim’s WikiCorpus (great if you’re doing NLP in Python)

```python
from gensim.corpora import WikiCorpus

# This automatically handles .bz2 and extracts text + tokenizes
wiki = WikiCorpus("enwiki-latest-pages-articles1.xml-p1p41242.bz2", dictionary=False)

# Iterate over articles
with open("output.txt", "w", encoding="utf-8") as f:
    for i, text in enumerate(wiki.get_texts()):
        f.write(" ".join(text) + "\n")
        if i % 10000 == 0:
            print(f"Processed {i} articles")
```

#### 3. Simple bzip2 + grep/awk (quick & dirty, no cleaning)

```bash
# Just decompress and see raw XML
bzip2 -dc enwiki-latest-pages-articles1.xml-p1p41242.bz2 | less

# Extract only <text> content (very rough, keeps wiki markup)
bzip2 -dc enwiki-latest-pages-articles1.xml-p1p41242.bz2 | \
  sed -n '/<text /,/<\/text>/p' | \
  sed 's/<text[^>]*>//g;s/<\/text>//g' > raw_text_with_markup.txt
```

#### 4. If you have the full dump and want everything fast (parallel)

Your file is only the first chunk (p1p41242), but if you have all ~30+ chunks later:

```bash
# Extract all in parallel
ls *.bz2 | xargs -P 8 -I {} wikiextractor {} --output wiki_extracted
```

### Summary – What I recommend for you right now

```bash
pip install wikiextractor
wikiextractor enwiki-latest-pages-articles1.xml-p1p41242.bz2 -o extracted_wiki --bytes 1M --json
```

This will give you clean, readable articles in a few minutes (your file is only ~2-3 GB compressed, so very manageable).

Let me know if you want:

- Only main namespace (real articles, not talk pages)
- Plain text instead of JSON
- Tokenized output
- Chinese Wikipedia instead (zhwiki) – the process is identical

Happy extracting! 🚀
