---
audio: false
generated: true
image: false
lang: en
layout: post
title: arXiv HTML Better Than PDF
translated: false
type: note
---

**Question: Is arXiv HTML better than PDF for reading papers, especially with dark mode?**

**Answer: Yes, for daily reading, arXiv HTML is often much better than PDF.** The link you gave:

[https://arxiv.org/html/1706.03762v7](https://arxiv.org/html/1706.03762v7)

is the HTML version of **"Attention Is All You Need"** (Transformer paper), and it demonstrates why papers are moving toward web-native formats. arXiv officially introduced HTML papers as an additional format alongside PDF to improve accessibility and reading experience. ([arXiv][1])

Advantages:

### 1. Dark mode

Yes. HTML follows browser settings, so if your OS/browser uses dark mode, the paper can render in dark mode automatically. arXiv's HTML design specifically supports appearance changes such as dark mode and font adjustments. ([Scribd][2])

Example:

```
Light:
white background + black text

Dark:
dark background + light text
```

Much easier on eyes for long reading sessions.

---

### 2. Better on laptop / phone

PDF is a fixed page:

```
PDF:
+----------------+
| paper page     |
|                |
| tiny text      |
|                |
+----------------+
```

HTML is responsive:

```
Browser width
      |
      v

+----------------+
| Attention Is   |
| All You Need   |
|                |
| text flows     |
| naturally      |
+----------------+
```

You can:

* resize fonts
* use browser zoom
* read on phone
* copy equations/text easier
* search within the document

This was one of the main motivations for arXiv HTML. ([Alexander Van Werde][3])

---

### 3. Better for AI workflows

For someone working with LLMs, HTML is much better.

PDF:

```
paper.pdf
   |
   v
OCR / parser
   |
   v
sometimes broken equations
```

HTML:

```
paper.html
   |
   v
structured DOM
   |
   +-- headings
   +-- equations
   +-- references
   +-- figures
```

You can directly:

* copy sections into ChatGPT
* scrape papers
* build RAG datasets
* convert to Markdown

Many AI paper tools now rely on arXiv HTML when available. ([GitHub][4])

---

### 4. Equations are nicer

For example:

PDF:

```
Attention(Q,K,V)=softmax(QKᵀ/√dk)V
```

You may need zoom.

HTML:

* equation is rendered separately
* can scale with browser
* sometimes has MathML accessibility

---

### 5. PDF still has advantages

PDF remains better for:

* printing
* exact page references
* conference submission format
* annotations on iPad
* archiving

Researchers still use PDF because it is the canonical "camera-ready" format.

---

My workflow for ML papers:

```
First reading:
arxiv.org/html/xxxxx
        |
        |
        v
understand ideas
take notes

Deep dive:
download PDF
        |
        |
        v
check exact equations
figures
appendix
```

For papers like:

* Attention Is All You Need
* FlashAttention
* GPT-3
* DeepSeek papers
* LLaMA papers

I would start with HTML now.

References:

* arXiv HTML papers announcement ([arXiv][1])
* HTML format benefits and dark mode discussion ([Scribd][2])
* arXiv accessibility update ([Vuink.com][5])

[1]: https://arxiv.org/abs/2402.08954?utm_source=chatgpt.com "HTML papers on arXiv -- why it is important, and how we made it happen"
[2]: https://www.scribd.com/document/882301275/2402-08954v1?utm_source=chatgpt.com "HTML Format for Accessible arXiv Papers | PDF | Te X | Html"
[3]: https://alexandervanwerde.be/applications-of-html-support-on-arxiv/?utm_source=chatgpt.com "HTML support on arXiv could be great! – Alexander Van Werde"
[4]: https://github.com/huggingface/skills/blob/main/skills/huggingface-papers/SKILL.md?utm_source=chatgpt.com "skills/skills/huggingface-papers/SKILL.md at main · huggingface/skills · GitHub"
[5]: https://vuink.com/post/oybt-d-dnekvi-d-dbet/2023/12/21/accessibility-update-arxiv-now-offers-papers-in-html-format?utm_source=chatgpt.com "Accessibility update: arXiv now offers papers in HTML format"
