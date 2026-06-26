---
audio: false
generated: true
image: false
lang: en
layout: post
title: SEC-EDGAR 124M Generation Review
translated: false
type: note
---

Here's the detailed quality analysis across all 5 generations:

================================================================
SEC-EDGAR 124M GENERATION QUALITY REVIEW (Step 37k, val_loss 2.45)
================================================================

PROMPT 1 — Business Overview (Healthcare SaaS)
----------------------------------------------

INPUT:  ~3 paragraphs, $487.2M revenue, 8200 employees, EHR platform
OUTPUT: 4 coherent paragraphs, then total collapse

WHAT WORKED (lines 17-20):

- "Our business is heavily dependent on the resources of our clinical
  trials" — plausible SEC language, pivots from SaaS to biotech framing
- "technology costs are based on materials, manufacturing, test, and
  customer support costs" — generic but grammatically correct
- Bullet list structure with ● formatting maintained

WHAT FAILED (lines 22-112):

- After ~200 generated tokens, enters a "commercialization of new
  product candidates" loop that runs for 90+ lines
- Hallucinated drug names: X-Avent, X-Zentib, S-Zentib, Q-partnerib,
  X-Zitib — none exist, all follow pharma naming patterns
- Self-contradictory: starts as healthcare SaaS, becomes biotech
- Grammatical collapse: "commercializing our product candidates" used
  as noun, verb, adjective interchangeably

LONG-RANGE COHERENCE: ★★☆☆☆ — Maintains topic (healthcare) but
switches sub-domain (SaaS -> biotech) within 3 paragraphs. No
memory of the original company description (EHR, hospitals, etc.)

PROMPT 2 — MD&A (Revenue/Cost Analysis)
----------------------------------------

INPUT:  Revenue +28%, cost of revenue +22%, gross margin 64.4%
OUTPUT: First continuation paragraph perfect, then 10 paragraphs
        of "Cost of revenue increased/decreased by $X" loops

WHAT WORKED (line 19, first continuation):

- "Cost of revenue increased by $32.1 million, or 26%... primarily
  attributable to decreased depreciation and amortization expense
  in the period of the acquisition of DMR"
- Proper SEC formula: dollar amount + percentage + explanation
- References a specific acquisition (DMR) — hallucinated but plausible

WHAT FAILED (lines 20-27):

- 10 consecutive paragraphs all starting with "Cost of revenue
  increased/decreased by $X.X million, or X%"
- Numbers become nonsensical: "$40.0 million, or 2%, to $107.1
  million... from $162.8 million" (2% of $162.8M is not $40M)
- Internal contradictions: "decreased by $61.2 million, or 13%,
  to $1.9 million from $2.7 million" ($61.2M decrease from $2.7M?)
- Same sentence structures repeated verbatim with number swaps

LONG-RANGE COHERENCE: ★☆☆☆☆ — After the first continuation
paragraph, loses all numerical consistency. The model learned the
TEMPLATE of MD&A paragraphs but can't maintain arithmetic logic.

PROMPT 3 — Risk Factors
------------------------

INPUT:  Net losses $42.3M/$67.8M/$89.1M, accumulated deficit $523.4M
OUTPUT: 2 coherent risk factor paragraphs, then "product candidates"
        loop for 30+ lines

WHAT WORKED (lines 18-24):

- "Our quarterly revenue and operating results have varied in the
  past and may continue to vary significantly from quarter to
  quarter" — textbook SEC risk factor language
- "Factors that may cause our quarterly results to fluctuate include
  the timing of large enterprise contracts, seasonal purchasing
  patterns in the healthcare industry" — specific, plausible
- Maintains bullet point format with proper transitions

WHAT FAILED (lines 25-49):

- "product candidates" appears 47 times in 25 lines
- Recursive self-reference: "Our product candidates may fail to
  develop, develop and commercialize our product candidates may fail"
- Grammatical breakdown: "We have suffered a number of risks involved
  in our research and development programs"
- Loses thread of healthcare SaaS, becomes generic biotech risk factors

LONG-RANGE COHERENCE: ★★★☆☆ — Better than others. Maintains risk
factor STRUCTURE (heading + explanation) for longer. But content
degenerates into repetitive "product candidates" loop. The model
clearly over-indexed on biotech risk factors in training data.

PROMPT 4 — Revenue Recognition Notes (with table)
--------------------------------------------------

INPUT:  Revenue table ($380M subscription, $89M services, $18M HW)
        + remaining performance obligations ($892.3M)
OUTPUT: Perfect table echo, one sentence continuation, then blank

WHAT WORKED (lines 12-25):

- Table echoed EXACTLY — all numbers, alignment, formatting preserved
- "The aggregate amount of the transaction price allocated to remaining
  performance obligations was $892.3 million" — exact copy of input
- Proper ASC 606 language maintained

WHAT FAILED (lines 26-29):

- "The table below presents our revenues in the periods indicated"
  — tries to start another table, then outputs blank spaces
- Only generated ~50 actual tokens of continuation before collapse
- Model can't generate new table rows — only echo existing ones

LONG-RANGE COHERENCE: ★★☆☆☆ — Perfect at echoing input, zero
ability to extend. This is the fundamental limitation: the model
memorized table FORMATS but can't generate new coherent numbers.

PROMPT 5 — Proxy Statement (Executive Comp Table)
--------------------------------------------------

INPUT:  3 executives with full comp breakdown ($5.5M, $3.6M, $3.0M)
OUTPUT: Perfect table echo, adds one broken row, then blank

WHAT WORKED (lines 14-24):

- Table structure perfectly preserved — column alignment, dollar signs
- All 3 executive rows echoed exactly with correct numbers
- "Our executive compensation program is designed to attract, retain,
  and motivate" — proper proxy boilerplate

WHAT FAILED (line 25):

- Attempts to add "William R. Gras" as 4th executive
- Only gets: "William R. Gras    100,000  $" — missing most columns
- Then blank spaces — model can't continue the table pattern
- "Gras" is likely a hallucinated name fragment

LONG-RANGE COHERENCE: ★★☆☆☆ — Same as Prompt 4. Perfect echo,
broken extension. The model treats tables as fixed patterns to
reproduce, not as structured data to extend.

================================================================
CROSS-PROMPT PATTERNS
================================================================

1. ECHO vs GENERATE DISTINCTION:
   - Model is excellent at ECHOING input (tables, numbers, formatting)
   - Model is poor at GENERATING new content that maintains consistency
   - This suggests the model learned surface patterns, not underlying
     data relationships

2. LOOP ATTRACTORS:
   - "commercialization of product candidates" (Prompt 1, 3)
   - "Cost of revenue increased by $X million" (Prompt 2)
   - "raise additional capital" (earlier tests)
   - These are the most common SEC phrases in training data — the
     model falls into them as probability sinks

3. NUMERICAL COHERENCE:
   - Dollar amounts: plausible scale ($1M-$500M range) but internally
     inconsistent (can't do arithmetic)
   - Percentages: often don't match the dollar changes cited
   - Dates: consistent (always "December 31, 2023/2022")
   - The model learned the FORMAT of numbers, not their MEANING

4. DOMAIN DRIFT:
   - Healthcare SaaS prompt → biotech/pharma within 200 tokens
   - This suggests training data is dominated by biotech 10-Ks
   - Or: biotech risk factors are the "default" SEC content the
     model generates when uncertain

5. GRAMMAR vs LOGIC:
   - Grammatical structure remains correct even when content is
     nonsensical ("We have suffered a number of risks involved
     in our research and development programs")
   - Subject-verb agreement maintained even in loops
   - This is typical for n-gram-level learning without reasoning

6. TABLE HANDLING:
   - Can reproduce tables with perfect alignment
   - Cannot extend tables with new rows
   - Cannot maintain numerical consistency across rows
   - Suggests table formatting is learned as character patterns,
     not as structured data

================================================================
OVERALL ASSESSMENT
================================================================

The 124M model at 78% training has learned:
  ✓ SEC document structure (headings, bullets, tables)
  ✓ Financial vocabulary and boilerplate language
  ✓ Proper formatting (dollar signs, percentages, alignment)
  ✓ Grammatical sentence construction

The model has NOT learned:
  ✗ Numerical consistency (can't do arithmetic)
  ✗ Long-range topic coherence (drifts to dominant training patterns)
  ✗ Table extension (can echo, can't continue)
  ✗ Factual grounding (hallucinates drug names, acquisitions)

This is expected for a 124M parameter model. GPT-2 1.5B (12x larger)
shows similar but less severe patterns. The model is useful for:

- Generating SEC boilerplate language
- Suggesting section structures
- Drafting placeholder text that LOOKS like real SEC filings

It is NOT useful for:

- Generating accurate financial data
- Maintaining consistency across long documents
- Producing factually grounded content
