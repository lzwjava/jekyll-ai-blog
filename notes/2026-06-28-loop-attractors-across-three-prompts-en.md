---
audio: false
generated: true
image: false
lang: en
layout: post
title: Loop Attractors Across Three Prompts
translated: false
type: note
---

Here's the analysis of all 3 new prompts:

---

PROMPT 8: DIGITAL BANKING PLATFORM
===================================
Input: 70 words. Digital banking in SE Asia, 12M customers, $14.6B payment volume, NIM 3.2%.

Generated output (first ~400 tokens):
- Input echoed perfectly: correct figures ($287M NII, 34% growth, 3.2% NIM)
- After 1 continuation paragraph, enters a "Net interest income" bullet-point loop
- Every bullet starts with "Net interest income increased/decreased $X.X million, or N%"
- All comparisons are "fiscal year 2023 vs fiscal year 2023" (same year both sides)
- Scale collapse: input says $287M NII, generated bullets are $1-31M range
- Phrase "partially offset by the change in the average balance of interest-earning assets and liabilities" repeated 6+ times
- Generated a "Liquidity and Capital Resources" section header (learned template)

Key failure: Loop attractor on "Net interest income [direction] $X million, or N%"

---

PROMPT 9: MUTUAL FUND OPERATIONS
=================================
Input: 75 words. Asset mgmt division, 147 strategies, $89.4B AUM, $6.2B inflows, 18.4% return.

Generated output (first ~500 tokens):
- Input echoed well: correct AUM ($89.4B), fee rates (62bps), distribution costs ($340M)
- First continuation: "Operating expenses were lower at $1.9 billion" (contradicts "flat at $420M" in input)
- Drifts into full balance sheet generation with table formatting
- Generates a complete balance sheet: accounts receivable, prepaid expenses, property, intangibles, goodwill
- Table numbers are plausible ($8M-$3.8B range) but internally inconsistent
- Generates stockholders' equity section with par values, authorized shares
- Collapses into "Cash and Cash" repetition loop at the end
- Domain drift: from mutual fund ops to corporate financial statements

Key failure: Mode collapse into table generation + "Cash and" repetition sink

---

PROMPT 10: FINANCE LEDGER ADJUSTMENTS
======================================
Input: 73 words. General ledger platform, 45K journal entries/month, 340 entities, maker-checker controls.

Generated output (first ~500 tokens):
- Input echoed perfectly: 45,000 entries, 340 entities, 18% manual, $2.4M avg, $500K threshold
- First continuation references intercompany eliminations, FX revaluations (from input)
- After 2 paragraphs, enters a "$0.X million in sales" loop
- Loop pattern: "During the year ended December 31, 2023, we generated significant sales and $0.5 million in sales and $0.3 million in sales..."
- Repeats "in sales and" 80+ times in the generated text
- Occasionally breaks pattern with "in marketing" or "in development" then returns to "in sales"
- Numbers are all small ($0.1M-$0.7M) regardless of the $2.4M input context
- Total output is ~90% repetitive "sales and $0.X million" phrases

Key failure: Strongest loop attractor of all 3 — "$0.X million in sales and" dominates entire output

---

SUMMARY ACROSS ALL 3
=====================
Pattern                  | Prompt 8 (Banking) | Prompt 9 (Mutual Fund) | Prompt 10 (Ledger)
-------------------------|--------------------|-----------------------|-------------------
Input echo quality       | Excellent          | Excellent             | Excellent
First continuation       | Good               | Contradicts input     | Good
Loop phrase              | "Net interest income" | "Cash and"         | "$0.X million in sales"
Domain drift             | Banking stays      | Drifts to balance sheet | Sales/rev stays
Table generation         | No                 | Yes (full balance sheet)| No
Scale consistency        | Collapses to $1-31M| Plausible but wrong   | Collapses to $0.1-0.7M
Numerical logic          | Same year vs same year| Internally inconsistent| No logic, just repetition

All 3 follow the same pattern as the original 5 prompts: strong echo, rapid loop attractor, scale collapse. The finance ledger prompt (10) has the most extreme repetition — the model found "sales and $0.X million" as an even stronger attractor than the bank-related prompts.
