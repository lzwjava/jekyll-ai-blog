---
audio: false
generated: true
image: false
lang: en
layout: post
title: Whisper Refine Prompt Expansion
translated: false
type: note
---

File parses cleanly. Here's a summary of what changed:

**File:** `/Users/lzwjava/projects/ww/ww/audio/whisper_refine.py`

**What changed:** The `REFINE_RULE` prompt string expanded from ~1,200 words to ~3,900 words — roughly 3x more comprehensive.

**What was added (10 numbered sections, each expanded):**

1. **Anti-summarization preface** — Strong upfront warning that LLMs naturally condense, with explicit "stop and write out details" directive and a "200 paragraphs in, 200 paragraphs out" rule.

2. **Content & Structure** — Title: specific-not-generic rule with examples. Summary: must touch every H2 section. H2/H3 guidance: don't force H3 when a single topic. Sequence preservation: don't regroup chronological walkthroughs. Topic grouping across time: merge scattered discussion with "circled back" markers.

3. **Detail Preservation** (the biggest expansion):
   - Anti-summarization rules with a CRITICAL TEST (scan input vs output for omissions)
   - Collapse-only-same-speaker-redundancy exception
   - Expanded "NOT to do" examples (5 concrete before/after pairs)
   - Numbers/dates: 10+ conversion examples (percentages, milliseconds, quarters, GB, currency)
   - Approximation markers: "roughly 100" vs guessing
   - Ambiguous numbers: "(15 or 50?)" not guessing
   - Anti-pattern list: 13 phrases to never write ("etc.", "among other things", "several approaches", etc.)
   - Code formatting: inline code and fenced code blocks with language specifiers
   - Architecture: descriptive prose, no ASCII art

4. **Action Items, Decisions, Commitments** (entirely new section):
   - **Decision:** format, conditional decisions, explicit "not to" decisions, rationale required
   - **Action item:** owner + task + deadline format, unassigned items, concrete-verifiable rule
   - Action items grouped per-section under H3, not in a global appendix
   - Open questions, deferred topics, no-consensus markers

5. **Tone & Fidelity** — Expanded with: concrete before/after examples showing scrubbed vs preserved tone. Metaphor preservation. Emphasis handling (bold/italics). Intensity gradient (strong agreement → leaning). Disagreement and contradiction rules — present both sides fairly, note walk-backs, don't synthesize false consensus.

6. **Speaker Handling** — Added: do NOT infer roles from content. Do NOT consistently associate positions with voices. Expanded third-person phrase bank (15 patterns). Direct quotation rules (2-3 per article max, no quotes for paraphrasing). Back-and-forth grouping pattern.

7. **Noise Removal** — Expanded filler list ("er", "ah", "mm", "so", "well", "I think" as hedge). Added "keep" section with examples of substantive "yeah"/"exactly". Added test: if removal changes meaning, keep it.

8. **Reorganization** — Added: tangent handling (off-topic cat → omit; related technical tangent → its own section). Transitional phrase guidance (one per major shift, not between sub-topics).

9. **Language** — Added: code-switching section with Chinese-English mixed examples. Pinyin + parenthetical for untranslatable concepts. Company name canonization table (ByteDance, Tencent, Alibaba). Terminology consistency rule.

10. **Output Format** — Added: strict first-character rule. No trailing whitespace/separators. Markdown conventions (ATX headings, `-` lists, bold/italic/blockquote/table rules). **Final quality check** — 8-item mental checklist before finalizing.

11. **Technical Formatting** (entirely new section): Inline code rules for 13 categories (function names, files, commands, env vars, ports, etc.). Fenced code block rules with language specifiers. Architecture description rules.
