---
audio: false
generated: true
image: false
lang: en
layout: post
title: FineWeb Dataset Size Details
translated: false
type: note
---

Question: Is FineWeb 44TB? Is that its maximum data size?

Answer:

**Yes, 44TB is correct — but it refers to the disk space of the original FineWeb v1.0 release, not an absolute maximum.**

Here's a comprehensive breakdown:

---

## 🍷 FineWeb — Original Release (v1.0)

Hugging Face released FineWeb on May 31, 2024, as a large-scale dataset drawing from **96 CommonCrawl snapshots**, encompassing **15 trillion tokens** and occupying **44TB of disk space**.

So yes — **44TB** is the correct disk size figure for the original FineWeb dataset.

---

## Has the Dataset Grown Since Then?

The dataset has been updated and expanded. The current FineWeb dataset (as of the Hugging Face page) now consists of **more than 18.5 trillion tokens** (originally 15 trillion tokens) of cleaned and deduplicated English web data from CommonCrawl.

This means the 44TB figure corresponds to the **initial 15T token release**, and the actual size has grown with subsequent updates.

---

## FineWeb-Edu Subset

Alongside the main dataset, Hugging Face introduced **FineWeb-Edu**, a subset of **1.3 trillion tokens** from FineWeb that was rated as highly educational by a custom classifier. This subset is much smaller than the full dataset.

---

## Key Facts Summary

| Property | Value |
| --- | --- |
| Source | 96 CommonCrawl snapshots |
| Original token count | 15 trillion tokens |
| Updated token count | 18.5+ trillion tokens |
| Disk space (original) | **44TB** |
| FineWeb-Edu subset | 1.3 trillion tokens |
| Language | English only |
| License | ODC-By 1.0 |

---

**Conclusion:** 44TB is the disk footprint of the **original FineWeb v1.0**, not a hard cap. The dataset has since grown beyond 18.5 trillion tokens, so the actual storage footprint is now larger than 44TB.

References:

- [HuggingFace FineWeb Dataset Page](https://huggingface.co/datasets/HuggingFaceFW/fineweb)
- [FineWeb Paper (arXiv)](https://arxiv.org/html/2406.17557v1)
- [MarkTechPost Article](https://www.marktechpost.com/2024/06/03/huggingface-releases-%F0%9F%8D%B7-fineweb-a-new-large-scale-15-trillion-tokens-44tb-disk-space-dataset-for-llm-pretraining/)
