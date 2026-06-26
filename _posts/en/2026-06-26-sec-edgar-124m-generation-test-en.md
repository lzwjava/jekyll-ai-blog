---
audio: false
generated: true
image: false
lang: en
layout: post
title: SEC-EDGAR 124M Generation Test
translated: false
type: note
---

Here's the full summary of long-prompt generation quality:

    ================================================================
    SEC-EDGAR 124M — LONG PROMPT GENERATION TEST RESULTS
    (Step 37k/47.4k, val_loss 2.45, 78% trained)
    ================================================================

    PROMPT 1: Notes to Financial Statements (ASC 606 revenue recognition)
    - Input: 966 chars of proper accounting policy text
    - Output: ~2000 chars of good continuation, then degenerates into
      repeating "The Company recognizes revenue when..." with slight
      variations, eventually hitting gibberish chars (vvvvvvvvv)
    - Verdict: First 3-4 paragraphs are coherent and accurate SEC language

    PROMPT 2: MD&A (biopharma company overview)
    - Input: 1388 chars with clinical-stage company description
    - Output: Continued the pharma narrative well — mentions ABC-123,
      lysosomal storage disorders, accumulated deficit $245.3M.
      Then loops hard on "raise additional capital" / "incur significant
      losses" for the remaining ~800 tokens
    - Verdict: Good 2-3 paragraph continuation, then repetitive loop

    PROMPT 3: Risk Factors (biopharma)
    - Input: 1726 chars of risk factor boilerplate
    - Output: Continues with COVID-19 pandemic risks, regulatory risks,
      financing risks. Mentions "CARVID-19" (hallucinated name). Loops
      on "raise additional financing" theme
    - Verdict: Realistic risk factor language, some hallucination

    PROMPT 4: Financial table with numbers
    - Input: 2002 chars with a full P&L table + narrative explanation
    - Output: Echoed the table correctly, continued with "increase in
      revenue was primarily driven by subscription platform grew 42%"
      (coherent!), then jumped to fiscal 2005/2004 dated content and
      loops on marketing/advertising expenses
    - Verdict: Best continuation — first paragraph post-table is good

    ================================================================
    PATTERN SUMMARY:
    - Model handles NARRATIVE prompts (500+ chars) well for 2-4 paragraphs
    - Falls into repetitive loops after ~300-500 generated tokens
    - Tables/balance sheets loop faster (~200 tokens)
    - "Revenue recognition" and "raise additional capital" are the
      biggest loop attractors — very common in training data
    - Temperature 0.7 vs 0.8: less variation but same loop behavior
    - Hallucinated facts (CARVID-19, fiscal 2005) show it's pattern
      matching, not factual recall
    ================================================================

    This is typical for a 124M model at 78% training. The language quality
    is solid — proper SEC jargon, realistic numbers, correct formatting.
    The main weakness is degeneration into loops on longer generations,
    which should improve slightly when training completes.

    Tmux session sec-sample still active — you can run more prompts with:
      tmux attach -t sec-sample
