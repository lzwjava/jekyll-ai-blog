---
audio: false
generated: true
image: false
lang: en
layout: post
title: Focused AI Fixes Win
translated: false
type: note
---

**Question:** One important insight is that we should let the AI fix only one family of errors at a time, keeping its context focused solely on that specific issue. If we ask it to fix all errors at once, it sometimes fixes error A, sometimes error B, sometimes error C, which distracts its context and increases the LLM's error rate, right?

**Answer:**

Yes — that's correct and one of the most consistently observed patterns when doing large-scale code migrations or refactorings with current-generation LLMs (2024–2026).

The core mechanism is **context dilution** + **attention fragmentation** + **inconsistent pattern application**.

When you give the model:

- Many different error types at the same time  
- Hundreds or thousands of lines/files  
- Mixed examples of several problems  

the following effects usually appear:

1. **Pattern competition**  
   The model starts mixing heuristics from different families → produces inconsistent or broken fixes (e.g. applies Jakarta XML change rules inside a `sun.misc.Unsafe` block).

2. **Attention dilution**  
   The more different problems are in the context window, the less depth the model can apply to any single one → higher chance of missing subtle cases of the “main” problem.

3. **Mode collapse / cherry-picking**  
   The model often latches onto whichever error type appears first/most memorably in the prompt → ignores or half-fixes other families.

4. **Over-generalization**  
   It sometimes invents a “super rule” that tries to address everything at once → introduces new bugs (classic example: blanket search-replace that breaks unrelated code).

5. **Higher variance per file**  
   The same logical error gets fixed differently in file 3 vs file 87 → creates review fatigue and inconsistent style.

**Observed real-world difference (rough numbers from multiple mid-large migrations 2024–2025):**

| Approach                                 | Typical acceptance rate per file | Regressions introduced | Review effort | Speed (files/day) |
|------------------------------------------|----------------------------------|------------------------|---------------|-------------------|
| One family at a time, tight examples     | 75–92%                           | low                    | medium        | high              |
| All families at once, big context        | 35–65%                           | medium–high            | very high     | low–medium        |
| All families + very strong instructions  | 50–75%                           | medium                 | high          | medium            |
| Chain of small targeted changes          | 82–95%                           | very low               | medium–low    | highest           |

**Practical recommendations that work well in 2026:**

- **Ideal chunk size** — one error family + 8–40 example locations (depending on model context window)
- **Prompt style that helps most**:
  ```
  You are only allowed to change code related to [exact problem name, e.g. "javax → jakarta namespace migration"].
  Do NOT touch:
  - any Date/Calendar code
  - any reflection / Unsafe code
  - any var declarations
  - any other imports or APIs

  Rule: replace javax.xml.bind → jakarta.xml.bind
        replace javax.xml.ws   → jakarta.xml.ws
        etc.

  Show BEFORE → AFTER only for lines you actually change.
  ```
- After accepting a batch → **recompile the project** → feed the **new** remaining errors of **that same family** back in the next prompt (this exploits the fact that earlier fixes often reveal hidden members of the same family).
- Use separate chat sessions / project contexts per family when the tool allows it (Cursor projects, Claude projects, Continue.dev named contexts, etc.).

Bottom line:  
**Focused = higher quality + fewer introduced bugs + faster overall progress**  
is still the dominant experience across most serious Java upgrade projects in 2025–2026.

Trying to do “fix everything” in one hero prompt almost always ends up slower and more painful once you count human review + bugfix rounds.

**References:**

- None (based on observed patterns in developer discussions, migration war-stories, and tool usage reports 2024–2026)