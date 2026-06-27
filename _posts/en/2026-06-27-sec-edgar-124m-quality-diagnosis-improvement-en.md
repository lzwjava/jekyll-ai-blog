---
audio: false
generated: true
image: false
lang: en
layout: post
title: SEC-EDGAR 124M Quality Diagnosis & Improvement
translated: false
type: note
---

OK, I've reviewed everything. Here's my analysis and improvement suggestions.

================================================================
SEC-EDGAR 124M — Quality Diagnosis & Improvement Plan
================================================================

CURRENT STATE:
  Model:     GPT-2 124M (12 layers, 768 dim)
  Data:      1.66B tokens, 1 epoch on RTX 4070
  Val loss:  ~2.28 (final)
  Quality:   Good SEC language/structure, but loops, drifts to biotech

================================================================
ROOT CAUSE #1: DATA IS 100% 10-K FILINGS ONLY
================================================================

This is the biggest problem. You downloaded ALL 10 filing types
(10-K, 10-Q, 8-K, S-1, S-8, 144, 20-F, 3, 4, 5) but only 10-K
actually has data (10GB, 17 parquet files). The rest are empty
directories (4KB each).

10-K annual reports are dominated by biotech/pharma companies
(thousands of small-cap biotechs file 10-Ks with nearly identical
risk factors about "product candidates"). This explains:

- Model always drifts to biotech ("product candidates" loop)
- "commercialization" is the #1 loop attractor
- Domain drift from SaaS → biotech within 200 tokens

FIX: Download the other filing types. They add diversity:

- 10-Q: quarterly updates, more varied industries
- 8-K: material events, M&A, executive changes
- S-1/S-8: IPO filings, different structure
- 20-F: foreign company filings (different accounting)
- 144: insider trading filings (short, structured)

================================================================
ROOT CAUSE #2: NO DATA CLEANING
================================================================

The raw SEC filings contain:

- XBRL inline tags (<ix:nonFraction>, etc.)
- HTML artifacts (tables with raw HTML)
- Boilerplate repeated verbatim across filings
- Repetitive legal disclaimers (same text in thousands of filings)

The model memorized these surface patterns. That's why it can
ECHO tables perfectly but can't GENERATE new content.

FIX: Clean the data before tokenization:

  1. Strip XBRL/HTML tags (keep plain text)
  2. Deduplicate near-identical paragraphs (SimHash or exact match)
  3. Normalize whitespace/formatting
  4. Optionally: separate sections (risk factors, MD&A, financials)
     and train with section markers

================================================================
ROOT CAUSE #3: MODEL CAPACITY (124M)
================================================================

124M parameters is GPT-2 small. It can learn:
  ✓ Document structure and vocabulary
  ✓ Grammatical sentence construction
  ✓ Template patterns (headings, bullets)

It fundamentally cannot learn:
  ✗ Numerical reasoning (arithmetic consistency)
  ✗ Long-range coherence (>500 tokens)
  ✗ Table extension (needs structured understanding)

FIX OPTIONS (in order of effort):

A. REPEAT DATA (easiest, free):
   Train for 2-3 epochs instead of 1. The val_loss was still
   declining at step 47k — more passes could help. Set
   max_iters = 142200 (3x) and lr_decay_iters to match.
   Risk: overfitting on repeated data. Monitor val_loss closely.

B. BETTER DECODING (immediate, no retraining):

- Use repetition penalty (1.1-1.3) to kill loops
- Lower temperature (0.5-0.6) for more focused output
- Use top-k=50 or top-p=0.9 instead of pure sampling
- Add a frequency penalty to reduce "product candidates" spam

C. DATA CLEANING + REDO (medium effort):
   Clean the 10-K data + download other filing types.
   Retrain for 2 epochs on the improved corpus.
   This is the highest-impact change.

D. SCALE UP (if you have more VRAM):
   GPT-2 355M (24 layers, 1024 dim) would fit on 12GB VRAM
   with batch_size=2, grad_accum=16. Significantly better
   at long-range coherence.

E. USE A BETTER BASE MODEL:
   Instead of training from scratch, fine-tune an existing
   GPT-2 or a small LLaMA on SEC data. You get all the
   general language ability for free, then add domain knowledge.
   This is the modern approach — nobody trains from scratch anymore.

================================================================
RECOMMENDED PRIORITY ORDER
================================================================

1. IMMEDIATE (no retraining):
   - Add repetition_penalty to generation code
   - Lower temperature to 0.5
   - Test with top-p=0.9

2. SHORT TERM (1-2 days):
   - Download 10-Q + 8-K + S-1 filings (add diversity)
   - Clean XBRL/HTML from existing data
   - Retrain for 2 epochs on cleaned+diversified data

3. MEDIUM TERM:
   - Fine-tune a pre-trained model instead of from-scratch
   - Try GPT-2 355M if VRAM allows

Want me to start on any of these? I can:
  a) Fix the generation code to add repetition penalty
  b) Download the missing filing types (10-Q, 8-K, S-1, etc.)
  c) Write a data cleaning script (strip XBRL/HTML, dedup)
  d) Set up a fine-tuning pipeline on a pre-trained GPT-2
