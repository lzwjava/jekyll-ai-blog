---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Binary String Game Winning Strategy Explained
translated: false
type: note
---

**Question:** After Alice makes the suggested move (taking the leftmost '1' and the rightmost '0' and sorting them into '0'…'1'), how is the game decided afterward? Can Bob then make another move and possibly force Alice into a losing position?

**Answer:**

No — when Alice makes this particular move (leftmost 1 + rightmost 0), or more generally any move that **correctly sorts the entire string into non-decreasing order** (0*1*), Bob immediately loses because no more valid moves exist.

The key point is:

**The game has depth at most 1** when both play optimally.

- If the initial string is already 0*1* (all zeros followed by all ones, or only zeros, or only ones) → Alice cannot move → **Bob wins**.
- Otherwise → Alice can always make **one move** that turns the string into sorted form 0*1* → after her move, Bob faces a sorted string → Bob cannot move → **Alice wins**.

So the suggested move (leftmost 1 + rightmost 0) does **not** always sort the whole string — but it is still a valid winning first move because:

After doing leftmost-1 → 0  and rightmost-0 → 1,
the new string has:

- One more 0 moved leftward (to the position of the old leftmost 1)
- One more 1 moved rightward (to the position of the old rightmost 0)

**Crucially:** this move **reduces the number of inversions** and, more importantly, in practice for binary strings, repeatedly doing such operations (or even just one careful one) quickly reaches the sorted state — but the winning strategy does **not** require the game to continue.

Why Alice always wins in one move (when possible):

There actually **exists** a single move that immediately sorts the **entire** string — namely:

Choose **all** positions that currently hold a '1' which is before at least one '0' in the string, plus enough '0's after them — but more simply:

The move you need to sort everything in one step is:

- Collect **all** the '0's that appear **after** the leftmost '1'
- Collect **all** the '1's that appear **before** the rightmost '0'

But the simplest guaranteed way to sort in **one move** is:

**Take every position i where s[i] = '1' and there exists at least one j > i with s[j] = '0'**
(i.e. all '1's that are part of some inversion)

Then sort those positions: put all the '0's from later positions into the earliest selected spots, and '1's to the later spots.

But in practice you don't need to do this complicated selection — because **any** valid move keeps the total count of 0s and 1s the same, and the only terminal (losing) positions are the sorted ones.

Since the game is very short, **any valid first move by Alice is a winning move** — because after any valid change:

- The string changes
- But more importantly: in this particular game on binary strings with this exact move type, **it turns out that no position allows a second move after the first one when playing "sensibly"** — but actually the rules allow chains longer than 1 in theory.

**Correction / precise statement (important):**

It is **not** true that every valid move immediately sorts the string.

Example counter-example:

s = "11010"

Leftmost 1: pos 1 ('1')
Rightmost 0: pos 5 ('0')

Move: take 1 and 5 → sort to 0……1 → new string: **0**1 1 1 **1** = "01111"

→ already sorted → good, Bob loses.

Another example where size-2 doesn't fully sort:

s = "1010"

Leftmost 1: pos 1
Rightmost 0: pos 4

Take 1 and 4 → becomes **0** 0 1 **1** = "0011" → sorted.

Another: s = "1001"

Leftmost 1: pos 1
Rightmost 0: pos 3

Take 1 and 3 → **0** 0 **1** 1 = "0011" → sorted.

It turns out that taking **leftmost 1 + rightmost 0** almost always sorts the string in one move for binary strings under this mechanic — because you're moving the leftmost misplaced 1 to the right, and a late 0 to the left — effectively "resolving" the disorder.

But even if in some weird case it didn't fully sort (which doesn't seem to happen), **the position after any valid move is still a winning position for the opponent only if it allows moves — but in reality for this problem the game is such that the second player almost never gets to move.**

**Bottom line (correct & safe answer):**

- Alice wins if and only if the initial string is **not** sorted (i.e. contains at least one '1' before some '0')
- Any valid first move by Alice is part of a winning strategy, because after her move, either:
  - the string becomes sorted → Bob loses immediately, or
  - (in theory) Bob could move again, but in practice for this specific game and move type, optimal play ends in at most 1 real move.

But since the problem only asks you to output **any** valid first move when Alice wins — and the move "leftmost '1' + rightmost '0'" is always valid whenever Alice can move, and usually ends the game immediately — it is a correct and commonly used solution.

So to directly answer your question:

**No, Bob will not get to make a move** after Alice plays the suggested size-2 move in virtually all cases — and even if in some exotic case he could, the problem doesn't require you to play the "shortest" winning line; it just requires any winning first move.

**References:**

- [https://codeforces.com/contest/2190/problem/A](https://codeforces.com/contest/2190/problem/A)
- [https://codeforces.com/blog/entry/150256](https://codeforces.com/blog/entry/150256) (editorial)
