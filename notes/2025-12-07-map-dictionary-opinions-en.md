---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Controversial Map and Dictionary Opinions
translated: false
type: note
---

Question: What are some unpopular opinions about maps/dictionaries in programming?

Answer:

Here are some genuinely unpopular or controversial opinions about maps/dictionaries that you’ll often see veteran programmers defend (and most people disagree with or find extreme):

- **Maps should never be the default collection**
  Many experienced developers argue that reaching for a hash map first is a code smell. Arrays/vectors with integer indices or sorted structures are often faster, use less memory, and have better cache locality. Maps encourage “stringly-typed” or sloppy data modeling (e.g., using arbitrary keys instead of proper structs/classes).

- **Ordered dictionaries (e.g., LinkedHashMap, Rust’s IndexMap, Go maps since 1.9) are almost always a mistake**
  Preserving insertion order looks convenient, but it hides nondeterminism in APIs and encourages relying on accidental ordering. Real ordered data should be in a vector/array + explicit sort, not a side effect of a hash table.

- **JSON objects { } should not have been ordered either**
  A huge source of bugs and interop problems comes from people assuming JSON object key order matters. The fact that most implementations now preserve order (since ES2015, JSON spec change) is regretted by some low-level devs.

- **Null/non-existent keys should throw, not return null/nil/None**
  Languages like Python (`dict.get`) or JavaScript that silently return `undefined`/`None` when a key is missing encourage defensive code full of `if x is not None`. Go’s `value, ok := map[key]` comma-idiom or Rust’s `.get()` returning `Option` is strictly better; silently failing teaches bad habits.

- **Hash tables are overrated for small N (< ~20 elements)**
  Linear search in an array of pairs or a switch/if-else ladder is often faster in practice for tiny datasets because of branch prediction and no hashing overhead. Some C++ folks will literally write a 15-case `switch` instead of using `std::unordered_map`.

- **Language-provided dict literals are harmful**
  They make it too easy to create ad-hoc anonymous structs. You end up with codebases full of `{ "foo": 1, "bar": "x" }` instead of proper types. Languages like Go (no map literals with type inference in some contexts) or Rust (requiring you to build a HashMap explicitly) force you to be deliberate.

- **Iteration order should be explicitly nondeterministic**
  Python randomizing dict order in 3.6+ was a good thing. Languages that still guarantee insertion order (PHP, Ruby, modern JS) make it too easy to write accidentally order-dependent code that only fails under load when the hash function is reseeded.

- **Maps with non-hashable keys (e.g., lists or other maps as keys in Python) are pure evil**
  They exist, people use them, and then wonder why serialization, equality, or debugging becomes impossible.

These opinions tend to come from systems programmers, compiler writers, or people who have maintained huge codebases where “just use a dict” turned into technical debt nightmares.

References:

- [The “Stringly Typed” Problem](https://blog.codinghorror.com/new-programming-jargon/#stringly-typed)
- [Python 3.6+ dict order randomization rationale](https://mail.python.org/pipermail/python-dev/2017-December/151283.html)
- [Go maps are intentionally unordered](https://go.dev/blog/maps)
