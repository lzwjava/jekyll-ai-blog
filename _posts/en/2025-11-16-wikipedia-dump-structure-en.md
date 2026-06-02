---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Wikipedia Dump File Structure Differences
translated: false
type: note
---

The key difference is how the full Wikipedia article text is split across multiple files — specifically whether one `.xml.bz2` file contains only one stream of revisions (non-multistream) or many compressed streams bundled together (multistream).

### 1. Non-multistream dumps (older style, or the default “pages-articles” files)
Example filename:
`enwiki-20251101-pages-articles1.xml-p1p41242.bz2`

- Each `.xml.bz2` file contains a portion of the pages (e.g., pages 1–41242) in page-ID order.
- Inside the file there is exactly one continuous `<page>` … `<page>` … sequence.
- All revisions of a single page are together inside that one page tag (the latest revision + older ones if you asked for “current + history”).
- To extract a single article, you just decompress and parse the big XML normally with any XML/BZ2 tool.
- `wget -c` works perfectly in the simple way: it resumes exactly where it stopped because the file is one single bzip2 stream.

### 2. Multistream dumps (the files that contain “multistream” in the name)
Example filename (the one you linked):
`enwiki-20251101-pages-articles-multistream1.xml-p1p41242.bz2`

- The same page range (p1p41242) is still covered, but the full text of every revision is no longer stored inside the main XML file.
- Instead:
  - The main XML file only contains metadata (title, id, restrictions, latest revision timestamp, etc.) and a pointer (byte offset + length) to where the actual revision text lives.
  - The actual revision texts are stored separately in many small compressed streams inside the same `.bz2` file (hence “multistream”).
- There is usually a companion `...-multistream-index1.txt.bz2` file that contains the exact byte offsets for each page/revision so tools can jump directly to the right compressed stream and extract only that text without decompressing the whole 10–30 GB file.

### Why does this matter for `wget -c`?

In practice, both commands:

```bash
wget -c https://.../enwiki-20251101-pages-articles1.xml-p1p41242.bz2
wget -c https://.../enwiki-20251101-pages-articles-multistream1.xml-p1p41242.bz2
```

behave exactly the same from wget’s point of view: both are normal single bzip2 files, so resumable download with `-c` works perfectly in both cases.

The difference only appears when you start processing the downloaded file.

### Summary Table

| Feature                              | Non-multistream (regular)                      | Multistream                                      |
|--------------------------------------|-------------------------------------------------|--------------------------------------------------|
| Filename contains                    | `-pages-articlesN.xml-...bz2`                  | `-pages-articles-multistreamN.xml-...bz2`        |
| Article text location                | Inside the XML `<page><revision><text>...</text></revision></page>` | Outside the XML, in separate compressed streams |
| File size (for the same page range)  | Much larger (often 2–3×)                        | Much smaller                                    |
| Random access / single-page extract  | Very slow (must decompress whole file)          | Very fast (with the index file)                  |
| Tools that understand it directly    | Any XML parser (SAX, xmltodict, etc.)           | wikimedia’s dump-generator tools, pywiki, mwxml, etc. |
| Needs companion index file?          | No                                              | Yes (`-multistream-index....txt.bz2`)            |
| `wget -c` resumability               | Perfect                                         | Perfect (still one bzip2 file)                   |

### So which one should you download?

- If you just want to do a full sequential pass once (e.g. train a language model), the non-multistream files are simpler.
- If you ever want to look up individual pages quickly, or you care about disk space and extraction speed, always prefer the multistream + index pair. Almost all serious Wikimedia processing tools (WikiExtractor, gensim’s WikiCorpus, jawiki scripts, etc.) expect or strongly recommend the multistream version nowadays.

Both files you can resume with `wget -c` without any problem; the “multistream” part only changes what is inside the file, not how HTTP/wget sees it.
