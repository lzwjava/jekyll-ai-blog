---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: AVL Tree Overview
translated: false
type: note
---

### What is an AVL Tree?

An AVL tree is a type of **self-balancing binary search tree (BST)**, invented in 1962 by Georgy Adelson-Velsky and Evgenii Landis (hence the name). Like any BST, it stores data in a sorted manner: all nodes in the left subtree are smaller than the parent, and all in the right are larger. The key feature is that it automatically adjusts its structure after insertions or deletions to stay balanced.

### How Does It Work?

- **Balance Factor**: For every node, the tree calculates a "balance factor" as the height of the left subtree minus the height of the right subtree. This must always be -1, 0, or +1 (i.e., subtrees differ by at most one level).
- **Rotations for Balancing**: If an insertion or deletion violates the balance factor:
  - **Single rotations** (left or right) fix imbalances where the violation is in the nearer child.
  - **Double rotations** (left-right or right-left) handle cases where it's in the farther child.
- These rotations preserve the BST property while restoring balance, and they run in O(1) time per operation.

Example: Inserting nodes in sorted order into a plain BST would make it a linked list (unbalanced). In an AVL tree, rotations keep it roughly height-balanced, like this simplified before/after:

```
Unbalanced (after inserts: 1,2,3):
    2
   /
  1
 /
3  (wait, actually skewed right: 1->2->3)

After rotation:
  2
 / \
1   3
```

### Why Is It Special?

- **Guaranteed Efficiency**: Unlike regular BSTs, which can become O(n) in the worst case (e.g., skewed like a list), AVL trees ensure **O(log n)** average and worst-case time for search, insert, and delete. This makes them ideal for applications needing consistent performance, like databases or symbol tables.
- **Trade-off**: They're stricter than other balanced trees (e.g., red-black trees, which allow slightly more imbalance for faster inserts/deletes). AVL prioritizes search speed over modification speed.
- **Space**: Uses an extra field per node for height/balance tracking, but that's minor.

In short, AVL trees are "special" for their rigorous self-balancing, turning potentially chaotic BSTs into reliable, logarithmic performers.

For more details: [AVL Tree on Wikipedia](https://en.wikipedia.org/wiki/AVL_tree)
