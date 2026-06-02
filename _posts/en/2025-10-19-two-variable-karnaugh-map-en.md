---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Two-Variable Karnaugh Map Example
translated: false
type: note
---

### Simple Karnaugh Map Example: 2-Variable Function

Let's use a very basic 2-variable Boolean function: f(A, B) = A'B + AB' + AB (sum of minterms m(1, 2, 3)). This is the OR gate: f = A + B, but we'll "discover" that using a K-map.

#### Step 1: Construct the K-Map

A 2-variable K-map is a 2x2 grid. Rows for A (0, 1), columns for B (0, 1) in Gray code (already simple). Place 1s for the minterms:

| A \ B | 0 (B') | 1 (B) |
|-------|--------|-------|
| **0 (A')** | 0 (m0) | 1 (m1) |
| **1 (A)**  | 1 (m2) | 1 (m3) |

#### Step 2: Group Adjacent 1s

Look for largest groups of 1s (powers of 2: 1, 2, 4...). Adjacent means sharing a side (no diagonals).

- **Group 1**: Right column (m1 and m3)—vertical pair. Common: B (A varies, so don't care).
- **Group 2**: Bottom row (m2 and m3)—horizontal pair. Common: A (B varies).

(Overlap on m3 is fine.)

#### Step 3: Derive the Minimized Expression

Each group gives a term:

- Group 1: **B**
- Group 2: **A**

Minimized: f = A + B

This simplifies from 3 terms (9 literals originally, wait no: 3 terms with 2 literals each) to 2 terms with 1 literal each—fewer gates!

It matches the OR function. For even simpler practice, try all 1s: groups to just 1 (true).

[All About Circuits: Karnaugh Maps](https://www.allaboutcircuits.com/textbook/digital/chpt-7/karnaugh-mapping/)
