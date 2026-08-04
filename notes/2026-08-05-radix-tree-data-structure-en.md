---
audio: false
generated: true
image: false
lang: en
layout: post
title: Radix Tree Data Structure
translated: false
type: note
---

A **radix tree** (also called a **compressed trie**, **compact prefix tree**, or **Patricia trie** in a common variant) is a tree data structure for storing strings or other sequences where **common prefixes are shared**, and chains of single-child nodes are compressed into a single edge.

### Start with a regular trie

Suppose you store these words:

```
cat
car
cart
dog
```

A regular trie looks like this:

```
(root)
 ├── c
 │    └── a
 │         ├── t
 │         └── r
 │              └── t
 └── d
      └── o
           └── g
```

Each edge represents one character.

---

### A radix tree compresses paths

Notice that some paths have no branching:

* `c → a`
* `d → o → g`

These can be compressed into longer edge labels:

```
(root)
 ├── "ca"
 │      ├── "t"
 │      └── "r"
 │            └── "t"
 └── "dog"
```

Instead of one character per edge, each edge stores a **string**.

This reduces the number of nodes significantly.

---

## How lookup works

Suppose you search for `"cart"`.

1. Start at the root.
2. Match `"ca"`.
3. Remaining string is `"rt"`.
4. Follow edge `"r"`.
5. Remaining string is `"t"`.
6. Follow edge `"t"`.
7. Word found.

Unlike a trie, you compare **multiple characters at once** on each edge.

---

## Insertion example

Imagine the tree contains only:

```
"dog"
```

```
(root)
 └── "dog"
```

Now insert:

```
dot
```

The longest common prefix is `"do"`.

Split the edge:

```
(root)
 └── "do"
      ├── "g"
      └── "t"
```

Edge splitting is the key operation in radix trees.

---

## Why use a radix tree?

### Saves memory

A normal trie has many nodes with only one child.

For example:

```
international
```

A trie would create one node per character.

A radix tree stores:

```
"international"
```

as a single edge if there are no branches.

---

### Fast prefix searches

Finding all words beginning with:

```
inter
```

is efficient because shared prefixes are stored only once.

Applications include:

* autocomplete
* spell checking
* routing tables
* IP prefix matching
* dictionaries
* search engines

---

## Time complexity

Let:

* **n** = length of the search string

| Operation     | Complexity                 |
| ------------- | -------------------------- |
| Search        | O(n)                       |
| Insert        | O(n)                       |
| Delete        | O(n)                       |
| Prefix search | O(prefix length + results) |

Although edge labels may contain multiple characters, the total number of characters examined is proportional to the key length.

---

## Comparison with a trie

| Trie                   | Radix Tree                         |
| ---------------------- | ---------------------------------- |
| One character per edge | Multiple characters per edge       |
| Many nodes             | Fewer nodes                        |
| More memory            | Less memory                        |
| Simpler implementation | More complex due to edge splitting |
| O(n) lookup            | O(n) lookup                        |

---

## Small example

Store:

```
bear
bell
bid
bull
buy
sell
stock
stop
```

A trie would have one node per character.

A radix tree might look like:

```
(root)
├── "b"
│    ├── "e"
│    │    ├── "ar"
│    │    └── "ll"
│    ├── "id"
│    └── "u"
│         ├── "ll"
│         └── "y"
└── "s"
     ├── "ell"
     └── "to"
          ├── "ck"
          └── "p"
```

Common prefixes are shared, while long unbranched paths are compressed.

---

## Intuition

You can think of the progression like this:

* **Binary Search Tree:** organizes data by ordering.
* **Trie:** organizes data by **one character at a time**.
* **Radix Tree:** organizes data by **shared prefixes**, but compresses long, unbranched paths into single edges to save space.

The main advantage of a radix tree is that it preserves the fast prefix-search capabilities of a trie while using much less memory for datasets where many keys share long prefixes.
