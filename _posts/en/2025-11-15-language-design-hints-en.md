---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Hints on Programming Language Design
translated: false
type: note
---

### Overview

"Hints on Programming Language Design" is a classic, highly influential paper by Sir Tony Hoare (C. A. R. Hoare), originally presented as the keynote address at the **SIGACT/SIGPLAN Symposium on Principles of Programming Languages** in October 1973, and later published in 1974.

It’s not a formal academic paper with theorems — it’s a personal, opinionated, and remarkably prescient set of “hints” (advice) from one of the greatest minds in computing on how programming languages should (and should not) be designed.

### Core Message

Hoare’s central thesis is that **programming language design has been dominated too much by hasty implementation and not enough by careful, long-term intellectual discipline**. He believes most languages of the early 1970s (PL/I, ALGOL 68, Pascal, etc.) suffered from over-complexity, arbitrary choices, and poor abstraction — and that future languages must be radically simpler and more principled.

### Key Hints / Ideas in the Paper

1. **Premature optimization is the root of all evil** (in language design)
   Don’t add features just because they give 10–20 % performance gains if they complicate the language forever.

2. **Simplicity over power**
   “The price of reliability is the pursuit of the utmost simplicity.”
   A language should have as few concepts as possible. Complexity should be pushed into libraries, not the core language.

3. **Avoid “one language to rule them all”**
   He criticizes huge general-purpose languages (especially PL/I and ALGOL 68). Better to have small, clean languages tailored to specific domains.

4. **Orthogonality and regularity**
   Language features should combine in predictable, non-surprising ways (a principle later made famous by Perl’s “there’s more than one way to do it” — which Hoare would hate).

5. **Abstraction and information hiding**
   Strong support for modules, abstract data types, and encapsulation — ideas that directly influenced CLU, Modula-2, and later Ada and object-oriented languages.

6. **Security and reliability first**
   Languages should make it easy to write correct, provable programs. He was already pushing for strong typing, proofs of correctness, and avoiding features that make verification hard.

7. **Concrete syntax matters, but not as much as people think**
   Curly braces vs BEGIN/END is relatively unimportant compared to semantic clarity.

8. **Historical regrets**
   He reflects on ALGOL 60 (which he loved for its elegance) vs ALGOL 68 (which he thought was a disaster of over-engineering).

9. **Ideal language vision (1973!)**
   - Very small core
   - Powerful module/abstraction system
   - Strong static typing
   - Separate compilation
   - Facilities for concurrent programming (Communicating Sequential Processes — CSP — is already hinted at here; he published CSP five years later in 1978)

### Famous Quotes from the Paper

- “There are two ways of constructing a software design: One way is to make it so simple that there are obviously no deficiencies and the other way is to make it so complicated that there are no obvious deficiencies. The first method is far more difficult.”
- “I conclude that there are two ways of designing programming languages: make them so complicated that there are no obvious deficiencies, or make them so simple that there are obviously no deficiencies.”

### Impact & Legacy

This 1973 talk basically predicted the next 30–40 years of language design philosophy:

- Influenced Simula → Smalltalk → modern OO
- Directly inspired Modula, Ada, ML, Haskell’s module system
- The entire “simplicity first” movement (Go, Rust’s original philosophy, etc.) owes him a huge debt
- His criticism of ALGOL 68 and PL/I is still quoted when people complain about C++, Java, or Scala bloat

### Where to read it

The original 1973 Stanford technical report version (most commonly cited):
[Hints on Programming Language Design – C. A. R. Hoare (1973)](http://i.stanford.edu/pub/cstr/reports/cs/tr/73/403/CS-TR-73-403.pdf)

A slightly cleaned-up version appears in the book *Programming Language Design and Implementation* and in Hoare’s collected works.

It’s only about 25 pages and is remarkably readable even 50+ years later — highly recommended if you care about language design.
