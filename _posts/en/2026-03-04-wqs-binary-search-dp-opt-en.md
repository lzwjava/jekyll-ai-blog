---
audio: false
generated: true
image: false
lang: en
layout: post
title: WQS Binary Search for DP Optimization
translated: false
type: note
---

**WQS binary search** (also known as **Aliens trick**, **alien optimization**, **WQS optimization**, or **Lagrange optimization / convex hull trick variant**) is a very powerful technique in competitive programming for optimizing certain **dynamic programming** problems that have an extra dimension (usually a count / number of groups / number of segments / number of operations ≤ K).

It was popularized by the legendary **IOI 2016 "Aliens"** problem (hence the name "Aliens trick"), but the core idea was invented / described earlier by **Wang QinShi (王钦石, WQS)** in Chinese training materials around 2012–2013.

### Core Idea in One Sentence

When you have a DP where you minimize **cost** while using **exactly/at most K** something (groups, merges, operations), and the optimal cost as function of K is **convex**, you can binary search on a **penalty λ** (a real number / slope) and compute the **unconstrained** optimum of **(true cost − λ × number_of_items_used)** instead — this removes the K dimension from the DP.

### Typical Problem Shape That It Applies To

You want to solve one of these (very common patterns):

- Divide N elements into **at most K groups** → minimize sum of **cost(group)** over groups  
  → cost(group) is often convex, e.g. (size)², (max−min)², diameter², etc.

- Select / merge with **at most K operations** → minimize penalty

- Cover N points with **≤ K** structures → minimize total size / cost

Examples:

- IOI 2016 Aliens (cover points with ≤ K special squares, minimize covered cells)
- Many segment DP problems: divide array into ≤ K segments, cost per segment = (something convex like variance / diameter / (max-min)²)
- Task grouping: assign N tasks to ≤ K machines, cost = (number of tasks on machine)²
- CF problems like "New Year and Handle Change", "divide into K increasing subsequences", etc.

### Why Convexity Matters

Let f(k) = minimum cost using **exactly k** groups/operations/segments.

In many natural problems f(k) satisfies:

- f(k) is **decreasing** (more groups → never worse cost)
- f(k) − f(k+1) is **non-increasing** (the marginal gain of adding one more group gets smaller or equal)

→ This makes f(k) **convex** (second differences ≥ 0, or discrete convex)

When f is convex, the function g(λ) = min over k of [f(k) + λ · k]  is achieved at different k depending on λ, and as λ increases, the optimal k **decreases** (monotonic!).

### How the Trick Works (Step by Step)

1. **Rewrite the objective**  
   Instead of min cost with ≤ K groups, we consider for a fixed **penalty λ** (a real number we will binary search):  
   min over all possible number of groups m:  
   **real_cost(m) + λ × m**  
   (or sometimes real_cost(m) − λ × m — sign depends on whether we minimize cost or maximize score)

2. **Compute the DP without the K constraint**  
   Now do DP where each time you "start a new group / pay for an extra item", you **add λ to the cost**.  
   → The DP state usually becomes **O(N)** or **O(N log N)** instead of **O(N·K)** !

   Very often this modified DP can use **convex hull trick / Li Chao tree / divide & conquer optimization** because the transitions become linear/slope-based.

3. **Count how many groups m(λ) were used** in the optimal solution for this λ.

4. **Binary search on λ**  
   - If m(λ) > K → we used too many groups → increase λ (make starting new groups more expensive)  
   - If m(λ) < K → we used too few → decrease λ  
   - The crossing point where m(λ) jumps around K is what we want.

5. **Recover the true answer**  
   After binary search finds a good λ where optimal m is around K:  
   **true minimum cost ≈ DP_value(λ) − λ × K**  
   (or + λ×K depending on sign convention)

   Because:  
   DP_value(λ) ≈ real_cost(K) + λ × K  
   → real_cost(K) ≈ DP_value(λ) − λ × K

   Important: because of convexity, there often exists a range of λ where the optimal m is exactly the same, and the formula gives the correct min cost even if we fix m = K in the recovery.

### Important Details / Gotchas

- Binary search is usually done on **real numbers** → set lo = -1e9..1e12, hi = 1e9..1e12, run ~80–100 iterations for precision.
- Sometimes you need slightly different recovery: DP[λ] − λ × actual_m_used, or force exactly K, etc. — depends if ≤K or exactly K, and whether more groups are always better.
- The DP must allow computing both **the min modified cost** and **the number of groups used** in that optimum.
- If the function is not strictly convex or has flat parts → binary search might land in a flat region → but the recovery formula usually still works.

### Summary Table: When to Suspect Aliens / WQS

| Property                          | Good candidate for WQS? |
|-----------------------------------|--------------------------|
| DP has extra dimension ≤ K        | Yes                      |
| Cost per group/segment is convex  | Yes (crucial)            |
| O(N·K) DP is too slow             | Yes                      |
| Marginal benefit of +1 group decreases | Yes                      |
| You see (size)², (max-min)², etc. | Strong hint              |

It's one of the most beautiful and mind-bending optimizations in modern CP — once you internalize the "pay λ for each extra group" intuition, many hard-looking DP problems suddenly become solvable in O(N log N) or O(N log² N).

If you want, I can walk through a concrete small example (e.g. divide array into ≤ K segments minimizing sum of (max-min)² per segment) to show the numbers.