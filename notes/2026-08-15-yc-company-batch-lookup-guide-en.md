---
audio: false
generated: true
image: false
lang: en
layout: post
title: YC Company Batch Lookup Guide
translated: false
type: note
---

## Question: How to know a YC company, which batch it is from, and what companies are in each batch?

## Answer:

The easiest way is to use the **official YC company directory**:

[Y Combinator Company Directory](https://www.ycombinator.com/companies?utm_source=chatgpt.com)

It contains YC-funded companies with:

* Company name
* YC batch
* Founder names
* Industry
* Location
* Website
* Status (active/acquired/public)
  ([YC Founder List][1])

---

### 1. Understand YC batch naming

YC batches use:

```
<W/S/F/P><year>
```

Examples:

| Batch | Meaning     |
| ----- | ----------- |
| W24   | Winter 2024 |
| S24   | Summer 2024 |
| W25   | Winter 2025 |
| S25   | Summer 2025 |
| F25   | Fall 2025   |

Historically YC had mainly:

```
Winter (W)
Summer (S)
```

Later they added more seasons. ([Extruct AI][2])

---

### 2. Search a company

Example:

Search:

```
Cursor YC
```

You find:

```
Cursor
Batch: W24
Industry: Artificial Intelligence
```

or:

```
Perplexity
Batch: W19
```

---

### 3. Browse all companies in one batch

Example:

"Show me all AI startups in YC S25"

Go to:

```
YC directory
↓
Filter
↓
Batch = S25
↓
Industry = Artificial Intelligence
```

You can see the whole cohort.

Recent examples:

* W24 had around 248 companies. ([Seedtable][3])
* S25 had around 160+ companies. ([Seedtable][4])

---

### 4. Programmatically access YC data

If you want to analyze YC like a dataset:

```bash
git clone https://github.com/yc-oss/api
```

Then:

```python
import requests

companies = requests.get(
    "https://yc-oss.github.io/api/companies/all.json"
).json()

for c in companies:
    if c["batch"] == "W24":
        print(c["name"], c["one_liner"])
```

The YC community API dataset contains thousands of companies and batch metadata. ([GitHub][5])

---

### 5. For AI startup research, filter like this

A useful workflow:

```
YC directory
    |
    +-- Batch: W24/S24/W25/S25
    |
    +-- Industry:
          - Artificial Intelligence
          - Developer Tools
          - B2B SaaS
          - Robotics
    |
    +-- Status:
          Active
          Hiring
```

This gives you the "current YC frontier".

---

### 6. Famous YC companies by batch

| Company  | Batch |
| -------- | ----- |
| Airbnb   | W09   |
| Dropbox  | S07   |
| Stripe   | S09   |
| OpenAI   | S12   |
| Coinbase | S12   |
| Scale AI | W16   |

---

For studying AI startups, I would mainly watch:

```
W23
S23
W24
S24
W25
S25
W26
```

because these batches contain the current wave of:

* AI agents
* coding agents
* AI infrastructure
* model tooling
* robotics
* vertical AI companies

References:

* [Y Combinator Company Directory](https://www.ycombinator.com/companies?utm_source=chatgpt.com)
* [YC Open Source API](https://github.com/yc-oss/api?utm_source=chatgpt.com)
* ([YC Founder List][1])

[1]: https://ycfounderlist.com/blog/how-to-find-yc-companies?utm_source=chatgpt.com "How to find YC companies & founders — the complete directory guide"
[2]: https://www.extruct.ai/data-room/ycombinator-companies/?utm_source=chatgpt.com "Y Combinator Companies - Complete Intelligence Database | Extruct AI"
[3]: https://seedtable.com/investors/y-combinator/batch/w24?utm_source=chatgpt.com "Y Combinator W24 Batch — Companies | Seedtable"
[4]: https://seedtable.com/investors/y-combinator/batch/s25?utm_source=chatgpt.com "Y Combinator S25 Batch — Companies | Seedtable"
[5]: https://github.com/yc-oss/api?utm_source=chatgpt.com "GitHub - yc-oss/api: 📎 Public API for companies funded by Y Combinator · GitHub"
