---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Quick Sort Versus Merge Sort
translated: false
type: note
---

### Why Quick Sort Feels Tricky (and Merge Sort Doesn't)

You're spot on—implementing Quick Sort from scratch without references can feel like wrestling a greased pig, while Merge Sort is more like folding laundry: methodical and predictable. Merge Sort's "divide, conquer, combine" flow is linear and recursive in a clean way, with no surprises in the merging step. Quick Sort, on the other hand, is *in-place* and relies on a clever partitioning trick that involves swapping elements around a "pivot" (a chosen dividing point). It feels chaotic at first because the pivot isn't fixed—it's more like a referee who gets shuffled around during the game. But once you grok the intuition, it's elegantly efficient (average O(n log n) time, worst-case O(n²) if pivots are bad).

Let me introduce Quick Sort with a natural, story-like lens: imagine sorting a messy pile of books on a shelf by height. Instead of splitting the pile in half, measuring everything, and merging (that's Merge Sort), you pick one book as a "benchmark" (the pivot), then rearrange the others so all shorter books are to its left and all taller ones to its right. The pivot ends up in its *final* spot, and you recurse only on the left and right sub-piles. No extra space needed—just swaps on the shelf. It's like the Dutch "quicksort" flag-raising ceremony (hence the name), where you partition into three groups: shorter, benchmark, taller.

### Why It Works: The Magic of Partitioning

Quick Sort works because of **divide-and-conquer with a guarantee**: every partition step places *at least one element* (the pivot) in its correct final position, shrinking the problem by at least that much each time. In the best case, the pivot splits the array evenly (like halving in Merge Sort), leading to balanced recursion. In the worst case (e.g., already-sorted array with bad pivot choice), it degenerates to O(n²) like bubble sort—but good pivot choices make it blazing fast in practice.

The key insight: **partitioning enforces invariants**. After one partition:
- Everything left of pivot ≤ pivot.
- Everything right of pivot ≥ pivot.
- Pivot is now sorted forever—no need to touch it again.

This guarantees progress: the recursion tree's depth is at most log n on average, and each level does O(n) work total (scanning and swapping).

### How to Choose the Pivot (and Why It "Moves" During Comparisons)

The pivot isn't sacred—it's just any element you pick to benchmark against. Bad choices (like always the first element) can unbalance things, so here's a natural progression of strategies, from simple to robust:

1. **Naive: Pick the first (or last) element.**
   - Easy to code, but risky. On a sorted array `[1,2,3,4,5]`, pivot=1 means left is empty, right is 4 elements—recursion skews deep.
   - The "moving": During partition, you compare everything else to this pivot value, but you swap elements *around* its position. The pivot itself gets swapped into place as boundaries cross it.

2. **Better: Pick the middle element.**
   - Swaps it to the end temporarily, uses it as pivot. More balanced intuitively (closer to median), but still vulnerable to sorted/reverse-sorted inputs.

3. **Best for practice: Pick a random element.**
   - Swap it to the end, partition. Randomness averages out bad cases, making worst-case unlikely (with high probability, still O(n log n)). This is what most libs use.

4. **Fancy (for interviews): Median-of-three.**
   - Pick the median of first/middle/last as pivot. Quick to compute, dodges common pitfalls.

In code, you often "fix" the pivot by swapping it to the end first, partition around its *value* (not position), then swap it back to where it belongs. That's why it feels like the pivot "moves"—it's not static; the partition process dynamically finds its spot via two pointers (left and right) that leapfrog toward each other, swapping violators.

### A Hands-On Example: Sorting [3, 7, 1, 9, 4] with Last Element as Pivot

Let's walk through one partition step. Array: `[3, 7, 1, 9, 4]`. Pivot = last = 4. (We'll swap it around as needed.)

- Start with left pointer at index 0 (value 3), right at index 3 (value 9, since pivot is at 4).
- Scan from left: 3 < 4? Yes, leave it. Next, 7 > 4? Yes, but wait—we swap with the first >4 from right.
- Actually, standard Lomuto partition (simple one-pointer style):
  1. i = -1 (boundary for < pivot).
  2. For j from 0 to n-2 (skip pivot):
     - If arr[j] ≤ pivot (4), swap arr[++i] with arr[j]. (Grow the left side.)
  3. Finally, swap pivot with arr[++i] to place it.

Step-by-step:
- j=0: 3 ≤4? Yes. i=0, swap arr[0] with arr[0] (noop). Array: [3,7,1,9,4]
- j=1: 7 ≤4? No. Skip.
- j=2: 1 ≤4? Yes. i=1, swap arr[1] (7) with arr[2] (1). Array: [3,1,7,9,4]
- j=3: 9 ≤4? No. Skip.
- End: Swap pivot (4 at index 4) with arr[++i=2] (7). Array: [3,1,4,9,7]

Now: Left of 4 (index 2) is [3,1] (both ≤4, unsorted), right [9,7] (both ≥4, unsorted). Pivot=4 is *done*. Recurse on left [3,1] and right [9,7].

- Left: Pivot=1, partitions to [1,3].
- Right: Pivot=7, partitions to [7,9].

Full sort: [1,3,4,7,9]. See? Each step locks in progress, and swaps "move" the pivot home.

### Pseudocode Sketch (To Ease Implementation)

```
quicksort(arr, low, high):
    if low < high:
        pivot_idx = partition(arr, low, high)
        quicksort(arr, low, pivot_idx-1)
        quicksort(arr, pivot_idx+1, high)

partition(arr, low, high):  # Lomuto style, pivot at high
    pivot = arr[high]
    i = low - 1
    for j in low to high-1:
        if arr[j] <= pivot:
            i += 1
            swap arr[i], arr[j]
    swap arr[i+1], arr[high]
    return i+1
```

The "moving" happens in those swaps: elements dance past each other until the pivot settles. Practice on paper with 5-6 elements—once the partition clicks, the recursion feels natural. If you hit snags, try animating it mentally as that book-sorting shelf.

For deeper dives:
[Quick Sort Visualization](https://visualgo.net/en/sorting?slide=9)
[CLRS Chapter on Quicksort](https://mitpress.mit.edu/sites/default/files/sicp/full-text/book/book-Z-H-20.html#%_sec_3.3)
