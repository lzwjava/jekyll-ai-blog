---
audio: false
generated: true
image: false
lang: en
layout: post
title: Rust Hype Versus Reality Debunked
translated: false
type: note
---

Question: What is the main argument of this article about "so-called memory-safe languages," and how should we understand it critically?

Answer:

## Overview

This article is written by **Wang Yin (王垠)**, a well-known and controversial Chinese programmer/blogger, expressing a critical — and at times dismissive — view of Rust and the hype around "memory-safe languages." The Weibo link requires login, but the full article text is provided in your document. Here is a comprehensive breakdown of his arguments and how to evaluate them.

---

## His Core Claims

### 1. "Memory-safe language" is not unique to Rust

Wang Yin argues that most people misread the White House/NSA report as endorsing Rust specifically, when in fact **almost every language with automatic memory management (GC or RC) is already memory-safe** — including Java, Python, JavaScript, Ruby, C#, Swift, Lisp, and even Fortran. Rust is just the newest entry on that list, and was placed first alphabetically or for attention.

**Is this correct?** — **Yes, largely.** The NSA's "memory-safe languages" category does include Java, C#, Go, Python, etc. Rust is not singled out as the only safe option. However, the key distinction is that Rust achieves memory safety *without* a garbage collector, making it uniquely suited for systems-level programming where GC-based languages are impractical.

---

### 2. Rust's innovations are just C++ smart pointers with static checks

He claims Rust's ownership/borrow model is essentially `unique_ptr` and `shared_ptr` from C++, with added compile-time enforcement.

**Is this correct?** — **Partially.** The conceptual overlap is real — both are inspired by RAII and linear/affine type theory. However, Rust's **borrow checker is enforced at the language level**, not as an opt-in library feature. In C++, programmers can still mix raw pointers freely; in Rust, they cannot (in safe code). The enforcement being built into the compiler is the critical difference, not just the concept itself.

---

### 3. Rust's memory safety doesn't solve all security problems

Wang Yin correctly points out that **memory safety is only a small subset of software security**. Logic bugs, race conditions (at a higher level), injection attacks, authentication flaws — none of these are prevented by memory safety.

**Is this correct?** — **Absolutely correct, and this is widely acknowledged.** Even Rust's own community and the NSA report acknowledge this. Memory safety eliminates a *specific, very common* class of vulnerabilities (buffer overflows, use-after-free, etc.), which account for roughly 60–70% of critical CVEs in C/C++ codebases — but it is not a silver bullet.

---

### 4. Rust's cognitive overhead is too high

He argues that Rust imposes a massive mental burden through its ownership rules, comparable to (or worse than) C++ smart pointers, and that this cognitive load distracts from solving real problems.

**Is this a fair point?** — **This is debatable and context-dependent.** It is true that Rust has a steep learning curve — especially the borrow checker. However, many engineers report that once the mental model is internalized, Rust actually *reduces* debugging time by catching errors at compile time rather than runtime. The tradeoff depends on the project type and team experience. For application-level software, GC languages are almost always more productive. For systems software, Rust's overhead is often considered worthwhile.

---

### 5. Legacy code cannot and should not be rewritten in Rust

He makes a pragmatic point: billions of lines of C/C++ (and even COBOL) code embody decades of hard-won domain knowledge and bug fixes. Rewriting them introduces new risks.

**Is this correct?** — **Yes, this is a sound and widely-accepted software engineering principle.** "Rewrites are risky" is well-understood. The realistic path is incremental adoption of Rust in new components, not full rewrites.

---

### 6. The White House report's timing is suspicious

He questions why the report appeared after Rust's rise in popularity rather than decades ago when C/C++ memory issues were already well-known.

**Analysis:** This is speculative and somewhat conspiratorial. The more mundane explanation is that the report was motivated by modern, high-profile vulnerabilities (exploits in government-critical software), growing industry momentum around Rust, and the increasing cost of memory-related CVEs. It's not unusual for policy documents to lag behind technical realities.

---

## How to Understand This Article Overall

Wang Yin makes several **legitimate and important points** that are worth internalizing:

- Rust is not the only memory-safe language, and GC-based languages deserve equal recognition.
- Memory safety is not the same as software security.
- Rust's cognitive overhead is real and non-trivial.
- Blind rewrites of legacy codebases are dangerous and wasteful.

However, the article also has notable **weaknesses**:

- It downplays the unique value of Rust in the *systems programming* niche, where GC is not feasible (OS kernels, embedded firmware, game engines, databases).
- It overstates the equivalence of C++ smart pointers and Rust's borrow checker — the enforcement model is meaningfully different.
- The conspiratorial tone toward the White House report weakens the otherwise reasonable technical arguments.
- The dismissal is somewhat ideological and colored by his preference for GC-based languages (he is a known advocate of functional/Lisp-style languages).

---

## Bottom Line

This article is best read as a **corrective to Rust hype** rather than a balanced technical assessment. Its strongest points are the reminders that (1) memory safety is not unique to Rust, (2) it doesn't solve all security problems, and (3) cognitive overhead matters. Its weakest points are the dismissal of Rust's unique niche value and the speculative political commentary.

References:

- [NSA Memory Safety Guidance (related)](https://www.nsa.gov/Press-Room/News-Highlights/Article/Article/3215760/nsa-releases-guidance-on-how-to-protect-against-software-memory-safety-issues/)
- [Rust memory safety study - Huawei Cloud](https://bbs.huaweicloud.com/blogs/193974)
- [Blue team perspective: What is memory safety really?](https://deathking.github.io/2020/08/03/blue-team-rust-what-is-memory-safety-really/)