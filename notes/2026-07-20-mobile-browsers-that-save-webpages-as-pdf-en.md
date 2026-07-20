---
audio: false
generated: true
image: false
lang: en
layout: post
title: Mobile Browsers That Save Webpages as PDF
translated: false
type: note
---

**Question: Which mobile browsers can convert a web page into PDF?**

Several mobile browsers support **"Save webpage as PDF"** either directly or through the system print function:

| Browser          | Platform      | Web → PDF support | How                                   |
| ---------------- | ------------- | ----------------- | ------------------------------------- |
| Google Chrome    | Android / iOS | ✅ Yes             | Share / Menu → Print → Save as PDF    |
| Microsoft Edge   | Android / iOS | ✅ Yes             | Share → Print → Save as PDF           |
| Safari           | iPhone/iPad   | ✅ Excellent       | Share → Options → PDF → Save to Files |
| Firefox          | Android / iOS | ⚠️ Limited        | Usually via Print/share system        |
| Brave            | Android / iOS | ✅ Yes             | Share → Print → Save PDF              |
| Samsung Internet | Android       | ✅ Yes             | Menu → Print → Save PDF               |

My preference:

1. **iPhone/iPad → Safari**

   * Best integration.
   * Native PDF generation.
   * Keeps reader mode formatting.

2. **Android → Chrome or Edge**

   * Uses Android's system print pipeline.
   * Produces clean PDFs.

3. **For technical articles/docs → Edge**

   * Edge often handles long pages better because of Chromium + PDF integration.

For developers, another powerful option is:

```bash
# Desktop/headless Chrome
chrome --headless \
  --print-to-pdf=page.pdf \
  https://example.com
```

or:

```bash
npx playwright pdf https://example.com output.pdf
```

This gives much higher quality for archiving docs, blog posts, research papers, etc.
