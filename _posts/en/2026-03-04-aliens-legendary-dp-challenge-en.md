---
audio: false
generated: true
image: false
lang: en
layout: post
title: Aliens Legendary DP Challenge
translated: false
type: note
---

**IOI 2016 "Aliens"** is one of the most legendary and talked-about problems in competitive programming history. It was **Day 2 Problem 3** at the **International Olympiad in Informatics 2016** (held in Kazan, Russia).

### Problem Summary (very simplified)

You are given **N points of interest** (up to 2000) on a **grid** (coordinates up to ~10^9, but N is small).  
You need to cover all these points using **at most K axis-aligned squares** (K up to 2000 in hardest subtasks).  
Each square can be of **any size** and positioned anywhere (but with a special property: two opposite corners lie on the same diagonal — actually 45° rotated squares in taxicab/Chebyshev distance terms).  

The cost of a square is **(side length)²** — basically the **number of unit cells** it covers.  
Goal: **minimize the total number of cells covered** (union of all squares), while covering every point at least once, using ≤ K squares.

It's essentially a **minimum cost set cover**-like problem but geometric, turned into a very clever DP.

### Difficulty — Is it hard?

**Yes — extremely hard**, especially for full points.

- Subtasks gave partial points (e.g. small K, or loose constraints) → many people got 30–60 points
- Full 100 points solution required a combination of very advanced techniques:
  - DP on sorted points (after coordinate compression / sorting by x+y or similar)
  - **Convex Hull Trick** (CHT / Li Chao tree style) for optimizing the DP transitions
  - The famous **"Aliens trick"** (also called **WQS binary search**, or **alien optimization**, or **convex hull optimization + binary search on slope**)

This "Aliens trick" became **so famous** that the optimization technique itself is now universally called **"Aliens trick"** or **"WQS binary search"** in CP communities — even when the problem has nothing to do with aliens.

Many top contestants consider it one of the hardest / most innovative problems ever set at IOI.

### Who solved it (full points)?

At IOI 2016, **only one contestant** achieved **full 100 points** on Aliens.

That person was **Qinshi Wang** (王钦石) from China.

He's often called a "legend you've never heard of" because he didn't become as publicly famous as some repeat medalists, but solving Aliens completely alone in-contest is considered an extraordinary achievement.

Very few people (even among gold medalists) solved it fully during the contest. Most top solutions came months/years later when people studied the official analysis.

Today the problem (and especially the "Aliens trick") is studied a lot — it's a classic example of advanced DP optimization + binary search on the dual / Lagrangian relaxation idea.

If you're interested in the technique, many blogs explain it using this problem (or simpler variants like grouping tasks with cost = (group size)^2).