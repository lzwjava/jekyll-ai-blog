---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Karnaugh Map Minimization Example
translated: false
type: note
---

### Example of Karnaugh Map Usage: Minimizing a 3-Variable Boolean Function

Let's walk through a practical example of using a K-map to simplify a Boolean expression. We'll use a 3-variable function (A, B, C) where the output is 1 for minterms m(1, 2, 4, 7). This means:

- f(A, B, C) = A'B'C + A'BC' + AB'C' + ABC

The goal is to minimize this into the fewest terms (and literals) possible, which reduces the number of logic gates in a circuit.

#### Step 1: Construct the K-Map

A 3-variable K-map is a 2x4 grid (or 4x2, but we'll use rows for AB and columns for C). The rows are labeled in Gray code order (00, 01, 11, 10) to ensure adjacent cells differ by only one bit. Place 1s in the cells corresponding to the minterms:

| AB \ C | 0     | 1     |
|--------|-------|-------|
| **00** | 0     | 1 (m1) |
| **01** | 1 (m2) | 0     |
| **11** | 0     | 1 (m7) |
| **10** | 1 (m4) | 0     |

(Here, m1 = A'B'C, m2 = A'BC', m4 = AB'C', m7 = ABC.)

#### Step 2: Group Adjacent 1s

The key to minimization is finding the largest possible groups (rectangles or squares) of 1s that are adjacent (including wrap-around edges, like a torus). Each group must be a power of 2 (1, 2, 4, 8, etc.) in size. Groups can overlap.

- **Group 1**: The two 1s in the left column (m2 and m4) form a vertical pair. They share A'B'C' wait no—analyzing bits: m2 (010) and m4 (100) differ only in A and B, but in Gray code, row 01 and 10 are adjacent. This group covers A changing, so it's B'C' (A is don't care).
- **Group 2**: The two 1s in the right column (m1 and m7) form a vertical pair that wraps around (rows 00 and 11 are not directly adjacent, wait—actually for this map, better grouping: notice m1 (001) and m2 (010) are horizontal adjacent in row 00-01? Wait, let's correct.

Wait, re-plot for clarity—actually, optimal groups for this function:

- Horizontal pair: m1 (row00 col1) and m2 (row01 col0)? No, not adjacent.
Standard grouping for these minterms:
- Quad? No. Pairs:
  - m1 and m2? m1=001, m2=010—differ in two bits, not adjacent.
  Better: m2 (010) and m4 (100)—differ in A and B? 010 and 100 differ in A (0 to 1) and B (1 to 0), two bits—not adjacent.

I picked a bad example—let me choose a better one with clear groups to illustrate.

**Revised Example for Clarity**: Let's use f(A, B, C) = Σ m(0, 1, 2, 4, 5, 6) = A'B'C' + A'B'C + A'BC' + AB'C' + AB'C + ABC'

K-map:

| AB \ C | 0     | 1     |
|--------|-------|-------|
| **00** | 1 (m0) | 1 (m1) |
| **01** | 1 (m2) | 0 (m3) |
| **11** | 0 (m6? m6=110 col0=1 wait) |
Wait, m6=ABC' =110 col0 yes.

Correct table:

| AB \ C | 0 (C') | 1 (C) |
|--------|--------|-------|
| 00 (A'B') | 1 (000) | 1 (001) |
| 01 (A' B) | 1 (010) | 0 (011) |
| 11 (A B ) | 1 (110) | 0 (111) |
| 10 (A B') | 1 (100) | 1 (101) Wait, m5=101=1, but I said m5 yes.

Minterms: 0(000),1(001),2(010),4(100),5(101),6(110)—yes m3(011)=0, m7(111)=0.

So table:

| AB \ C | 0     | 1     |
|--------|-------|-------|
| **00** | 1     | 1     |
| **01** | 1     | 0     |
| **11** | 1     | 0     |
| **10** | 1     | 1     |

#### Step 3: Identify Groups

Now, group the 1s:

- **Large group (4 1s)**: The entire left column (C=0): m0, m2, m6, m4. These are all cells where C=0, and AB varies—all adjacent in a column (wraps for rows). This covers **C'** (since C is 0, A and B don't care).
- **Pair group (2 1s)**: Top row right (m0 and m1? m0 col0, m1 col1—horizontal pair in row 00: A'B' (C don't care).
- But m1 (001) is not covered yet? Wait, top row: m0 and m1 are adjacent horizontally, covering A'B' (C varies).
- Also, bottom row right m5 (101 col1 row10)—but to cover m1 and m5? They are in col1, rows 00 and 10, which are adjacent (wrap around), so vertical pair in col1: m1 and m5, covering AC (wait, bits: 001 and 101 = A don't care, B=0, C=1? 001 B=0 C=1, 101 A=1 B=0 C=1—yes B'C.

To minimize, we choose non-overlapping or minimal covering groups that cover all 1s with largest sizes.

Optimal:

- Group 1: 4-cell vertical in col0: covers C' (all 1s there: m0,m2,m4,m6 → term: C')
- Group 2: 2-cell horizontal in row00: m0 and m1 → A'B'
- Group 3: 2-cell vertical wrap in col1 rows10 and 00? Wait, rows 00 and 10 are adjacent for col1: m1(001) and m5(101) → differ only in A, so B'C (A don't care).

m5 is covered, m1 covered.

Note: m0 is in both group1 and group2, but that's OK—overlaps allowed.

#### Step 4: Derive the Minimized Expression

Each group becomes a product term (AND of the common literals):

- Group 1 (C'): **C'**
- Group 2 (A'B'): **A' B'**
- Group 3 (B' C): **B' C**

So, minimized SOP (Sum of Products): f = C' + A'B' + B'C

Verify: This has 3 terms (vs original 6), fewer literals (4 vs 12), simpler circuit (3 AND/OR gates basically).

You can plot this on a truth table to confirm it matches the original 1s.

#### Why This Minimizes?

- **Adjacency rule**: Groups only where variables change by one bit, ensuring the term ignores that variable (don't care = - in map).
- **Largest first**: Bigger groups = fewer variables in term = simpler.
- **Cover all 1s**: No 1 left out; 0s must stay 0 (don't group them).
- For more variables (4-var K-map is 4x4), same process, but harder visually.

This example shows how K-maps turn a sum-of-minterms into a compact form quickly without algebraic manipulation. For 4+ vars, use software, but practice with 2-3 var examples builds intuition.

[Digital Logic Design Basics](https://www.allaboutcircuits.com/textbook/digital/chpt-7/karnaugh-mapping/)
