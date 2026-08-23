---
audio: false
generated: true
image: false
lang: en
layout: post
title: ICML's Double-Blind Peer Review
translated: false
type: note
---

**Question:** What is ICML, and how does its peer review process work — including double-blind reviewing?

---

**Answer:**

## What is ICML?

The International Conference on Machine Learning (ICML) is the premier gathering of professionals dedicated to the advancement of machine learning, globally renowned for presenting and publishing cutting-edge research across machine learning and closely related areas such as artificial intelligence, statistics, data science, computer vision, computational biology, speech recognition, and robotics.

ICML consistently ranks among the top three ML conferences worldwide alongside NeurIPS and ICLR, based on metrics such as Google Scholar's h5-index. It has been held annually since 1980, with proceedings openly accessible on OpenReview.net.

---

## Scale & Acceptance Rate

ICML is highly selective, with acceptance rates hovering around 25–27%, e.g., 26.9% for ICML 2025 (3,260 accepted out of 12,107 submissions). ICML 2026 accepted 6,352 papers out of 23,918 submissions — an acceptance rate of 26.6% — marking a record year in submission volume.

---

## Peer Review Structure

### 1. Double-Blind Review

ICML uses a double-blind peer review process: the identities of all authors are removed from submitted papers, so neither names, affiliations, nor seniority are visible to reviewers. Equally, no part of the reviewers' identities is disclosed to authors.

Authors are expected to refer to their own prior work in the third person, and must refrain from including acknowledgements, grant numbers, or links to public code repositories that could reveal their identity.

Reviewers should not search the internet for papers they are assigned to review, as this could violate the double-blind policy. The goal is to reduce biases that might arise from knowing a submission's authors.

### 2. Reciprocal Reviewing

Each submitted paper must nominate a qualified "reciprocal reviewer" — an author who in turn reviews other papers. Authors submitting four or more papers must themselves be involved as a reviewer, area chair, or senior area chair.

ICML has also introduced a cap on the number of papers that can designate the same person as a reciprocal reviewer, to combat "thinly sliced contributions" — large batches of papers with small variations on a theme.

### 3. Author Rebuttal & Discussion

There are three rounds of author-reviewer discussion (rebuttal, reviewer follow-up, and author follow-up), each limited to 5,000 characters. Reviewers are expected to read the authors' responses and actively participate in discussions.

### 4. Public Reviews (New)

For accepted papers (and rejected papers that opt in), reviews and author responses are made public at the end of the review process.

---

## LLM Use in Reviewing (Recent Policy)

ICML 2026 introduced a novel **two-policy framework** for LLM use in reviewing:

**Policy A (Conservative):** LLM use for reviewing is strictly prohibited. **Policy B (Permissive):** Reviewers may use LLMs to help understand the paper and related works, and to polish reviews — but submissions can only be fed to privacy-compliant LLMs. Under both policies, reviewers must read the entire paper themselves and are fully responsible for their review content, including any hallucinated content, which is subject to disciplinary action.

In 2026, ICML desk-rejected 497 papers (~2% of all submissions) corresponding to reciprocal reviewers who violated their agreed LLM policies.

---

## Ethical Rules

Plagiarism in any form is forbidden. Advertising a submission as being under review at ICML during the review period is forbidden. Any form of collusion — whether explicit or tacit — between authors and reviewers to obtain favorable reviews is also strictly forbidden.

---

**References:**
- [ICML 2026 Call for Papers](https://icml.cc/Conferences/2026/CallForPapers)
- [ICML 2026 Peer Review FAQ](https://icml.cc/Conferences/2026/PeerReviewFAQ)
- [ICML 2026 LLM Policy](https://icml.cc/Conferences/2026/LLM-Policy)
- [ICML Blog – What's New in ICML 2026 Peer Review](https://blog.icml.cc/2026/01/08/whats-new-in-icml-2026-peer-review/)
- [Wikipedia – International Conference on Machine Learning](https://en.wikipedia.org/wiki/International_Conference_on_Machine_Learning)
- [CS Conf Stats – ICML Acceptance Rates](https://csconfstats.xoveexu.com/conferences/icml/)
