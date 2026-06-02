---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Unpopular Opinions About Programming Sets
translated: false
type: note
---

Question: What are some unpopular opinions about `set` (the set data structure) in programming?

Answer:

Here are some genuinely unpopular (or at least contrarian) opinions about sets that you’ll rarely see praised in tutorials or Reddit threads:

- **Sets are overrated for most real-world code**
  People reach for `set` the moment they need “unique items” or “fast membership testing,” but in practice a plain list or array is often faster and uses less memory when the data is small-to-medium sized (< ~100k elements) or when you only do a handful of lookups. Hash tables have high constant factors.

- **Ordered sets (like Java’s `LinkedHashSet` or C++’s `std::unordered_set` + manual ordering) are almost always a code smell**
  If you care about insertion order or sorted order, you probably actually want a list/dict or a proper sorted structure (tree map, B-tree, skip list). Hybrid “ordered set” types encourage people to couple unrelated concerns (uniqueness + order) into one leaky abstraction.

- **Python’s `set` being unhashable and unpickleable by default is a terrible design**
  You can’t put a set in another set or reliably serialize it without jumping through hoops. This makes nested sets basically impossible without converting to frozenset everywhere, which is clunky. Most languages (Java HashSet, JS Set, etc.) let you nest sets just fine.

- **Sets make code harder to reason about in many cases**
  Because order is undefined and iteration order can change between runs (CPython 3.6+ stabilizes it, but it’s still nondeterministic across implementations), using sets for anything where humans will read the output (logging, debugging, config) creates nondeterministic output that drives people insane.

- **Membership testing with sets is often premature optimization**
  `x in my_list` (O(n)) is perfectly fine when n is small and the code is clearer. Micro-benchmarks show that lists beat sets for membership testing up to thousands of elements once you account for hash computation and cache misses.

- **Immutable sets (frozenset, ImmutableSet in Guava, etc.) are underused and should be the default**
  Most of the time you don’t need to mutate a set after creation (lookup tables, configuration, graph nodes, etc.). Making the mutable version the default encourages unnecessary mutation and side effects.

- **Sets are a terrible choice for “small fixed collections of flags/options”**
  People do `{"fast", "verbose", "dry-run"}` when a bitfield/enum flags integer would be faster, smaller, and give O(1) union/intersection with bitwise ops.

- **Language-provided set literals are a trap**
  Python `{1, 2, 3}` and JavaScript `new Set([1, 2, 3])` look convenient, but they hide the fact that you’re paying for a full hash table allocation even when you have 2–3 constant elements. A lot of production code is littered with tiny throwaway sets that murder start-up time and memory.

These opinions tend to trigger strong reactions from people who love sets, but they come from years of profiling and cleaning up real codebases. Sets are great when you genuinely need O(1) average-case membership on large, dynamic collections of hashable items—otherwise they’re often just fashionable overhead.
