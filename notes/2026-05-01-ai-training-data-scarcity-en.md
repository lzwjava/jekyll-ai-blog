---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI Training Data Value and Scarcity
translated: false
type: note
---

Question: Is the analysis in this conversation about personal data collections and their value for AI training correct?

Answer:

The conversation touches on several interesting and largely **accurate** points about AI training data. Here's a breakdown:

---

## 1. Proprietary / Rare Data Will Be Increasingly Valuable — ✅ Correct

As publicly available internet data gets exhausted, AI labs are actively seeking:

- **Rare books** not digitized online
- **Domain-specific expert knowledge** (e.g., nonwoven fabric engineering books)
- **Private datasets** with unique information

This is well-documented. The "data wall" problem is a real concern in the AI industry right now.

---

## 2. FineWeb is a Real Dataset — ✅ Correct

FineWeb is a large-scale web crawl dataset released by Hugging Face, commonly used for LLM pretraining. 44TB is a realistic scale for such datasets.

---

## 3. Dario Amodei / Book Scanning Leak — ⚠️ Partially True

There have been reports and internal discussions at major AI companies (including Anthropic) about using **book scanning / OCR** to expand training corpora. However, specific details of leaked emails should be treated carefully — not all reported leaks are fully verified.

---

## 4. DeepSeek Using OCR to Extract Text from Images — ✅ Plausible

Many modern AI labs use OCR pipelines to extract text from scanned documents and images. DeepSeek has strong document understanding capabilities, consistent with this approach.

---

## 5. E-books Are the Most Valuable by Content Density — ✅ Correct

Per GB of storage:

| Data Type | Information Density | AI Training Value |
| ----------- | ------------------- | ------------------- |
| Video | Low (mostly visual) | Lower |
| Audio | Medium | Medium |
| E-books / Text | Very High | **Highest** |

Text is the most efficient format for training language models — this is well established.

---

## 6. "Digital Archaeology" Analogy — ✅ Good Analogy

Obscure, out-of-print, or niche books that current LLMs **cannot access** represent genuine value, similar to archaeological discoveries. If the data isn't in the training set, the model simply doesn't know it.

---

## Summary

Your friend's intuition is largely correct: **rare, text-dense, hard-to-find data collections will become increasingly strategic assets** as AI companies push beyond publicly crawled web data.
