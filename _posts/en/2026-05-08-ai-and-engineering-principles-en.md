---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI Doesn't Replace Engineering Principles
translated: false
type: note
---

Question: Is it okay to just follow a “as long as it runs, it’s fine” coding approach because AI can fix things later, as long as it doesn’t harm others and follows a general “do no harm” principle?

Answer:

What you’re describing is a real spectrum in how people approach engineering, and yes—there is diversity in practice. But it’s important to separate *short-term convenience* from *sustainable engineering quality*.

A “it runs, so it’s fine” mindset can work in very narrow contexts:

* prototypes
* throwaway scripts
* personal experiments
* rapid validation of ideas

In those cases, AI tools absolutely lower the cost of sloppiness, because you can regenerate or fix code quickly.

However, the moment code becomes:

* part of a shared codebase
* something you depend on long-term
* something other people will debug or extend
* something that handles data, money, or users

then “just run it” becomes a technical debt generator. The cost doesn’t disappear—it just gets delayed and amplified.

The key misconception is this: AI doesn’t remove the need for principles; it shifts *where* discipline matters. If anything, it increases the value of fundamentals because:

* AI-generated code often “looks correct” but hides edge cases
* architectural mistakes scale faster when code is produced faster
* debugging becomes harder when you didn’t understand what was generated

About the “do no harm, everything is fine” idea:
That’s a good ethical baseline, but engineering has a stricter version of it:

> Not harming users is not enough—you also want not to burden future maintainers (including yourself).

So a more robust mental model is:

* You can be flexible in experimentation
* You should be strict in anything that persists
* AI is a tool, not a substitute for understanding

A practical middle ground many strong engineers adopt is:

* Let AI generate freely first
* Then *you* enforce structure, readability, and correctness
* Treat AI like a fast junior developer, not an authority

So yes, there is world diversity in how people code—but in serious systems, “principles + AI” beats “AI replaces principles” by a large margin.