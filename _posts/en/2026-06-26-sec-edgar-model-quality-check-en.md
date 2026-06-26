---
audio: false
generated: true
image: false
lang: en
layout: post
title: SEC-EDGAR Model Quality Check
translated: false
type: note
---

Here's the summary of the SEC-EDGAR 124M generation quality (checkpoint at step ~37k / 47.4k = 78% done, val_loss 2.45):

QUALITY ASSESSMENT:

1. NARRATIVE SECTIONS (good):
   - "The company reported revenue of..." → proper SEC language, accounting terms (goodwill impairment, SFAS, deferred tax, FIFO), realistic financial figures, table-of-contents formatting
   - "ITEM 1A. RISK FACTORS" → proper regulatory language, Securities Act references, bullet-point risk disclosures, forward-looking statement boilerplate
   - "MANAGEMENT'S DISCUSSION AND ANALYSIS..." → coherent business description, marketing/sales org structure, bullet-point development plans, financing risk factors

2. STRUCTURED/TABULAR (loop issues):
   - "CONSOLIDATED BALANCE SHEETS" → starts well (realistic line items with two-column comparative figures: Cash $2,826/$1,741, A/R $9,924/$5,853) but loops on "Common stock, $0.01 par value" entries after ~200 tokens
   - "$" prompt → loops on "$X.X million, or Y%" financial ratio patterns

3. KEY OBSERVATIONS:
   - Narrative text quality is strong — proper SEC jargon, realistic corporate structure, coherent paragraphs
   - Tables/balance sheets work for the initial rows then degenerate into loops (expected for 124M)
   - At temp=0.8, output is fluent but occasionally redundant ("marketing" repeated many times)
   - The model hasn't finished training yet (78%) — final ~2.2-2.3 val_loss should improve coherence further

The model is in tmux session `sec-sample` if you want to try more prompts interactively. Run:
  tmux attach -t sec-sample
