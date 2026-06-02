---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: A Skeptical History of Rust
translated: false
type: note
---

### English Translation & Explanation of the Post
Title: “The History of Rust as I’ve Seen It”

This is a long, personal, and quite critical reflection written by a experienced programmer (likely Taiwanese, posting in Chinese) about their early encounter with Rust and why, despite its current popularity, they remain deeply skeptical of it—both technically and culturally.

#### Early Encounter (2009, Indiana University)
- While studying at Indiana University (IU), the author had two classmates (non-CS undergrad majors) who struggled badly in Dan Friedman’s advanced programming-languages course.
- These classmates were the kind who “talked a big game” but didn’t really understand the deep concepts. Yet they were good at networking and self-promotion.
- In summer 2009, these two classmates interned at Mozilla Research and worked on an early version of the Rust language (this would have been Graydon Hoare’s personal project that Mozilla later adopted; the classmates were probably very early contributors or summer interns on the project).
- At the end of the summer, they gave a university talk introducing Rust to everyone. This was the author’s very first exposure to the language.

#### The 2009 Talk (the author’s first impression)
- The talk was pure marketing: big slogans, almost no technical substance.
- They showed a triangle slide with “Rust’s three big features” — one was “safety,” the other two the author forgets.
- The killer claim: Rust would achieve completely safe memory management through static analysis alone with zero garbage collection (no GC at all).
- The author walked out thinking: “This is just Mozilla hype. They’ll never ship a browser in it. It’ll die like all their other research projects.” (He specifically mentions DrServ/DrJS as another Mozilla research project that went nowhere.)

#### Doubts About the Designer & Bootstrap Choice
- The author questions Graydon Hoare’s (the original creator’s) depth in programming-language theory.
- In particular, he thinks choosing OCaml as the first implementation language showed lack of taste or deep understanding (a controversial but not uncommon opinion among some PL old-timers who dislike OCaml’s quirks).

#### Later Developments
- One of those classmates later started a PhD project on a “general-purpose” GPU language that claimed you could build trees, graphs, etc. on GPUs. The author thought it was doomed because GPUs are designed for data-parallel workloads, not arbitrary pointer-heavy structures. The project indeed never became practical, but the classmate still got a PhD and now works on the Rust compiler at a big tech company.

#### The Author’s Own Journey with Memory Management
- The author was personally fascinated by the idea of 100% static memory safety without GC (exactly Rust’s original pitch).
- He spent a lot of time designing memory models and static analyses trying to achieve that dream.
- One day he told his advisor Kent Dybvig (the legendary author of Chez Scheme) about the idea. Kent calmly replied:
  “Completely static memory management — is that even possible? Memory management is inherently a dynamic process.”
- This single sentence shattered the author’s illusions. He realized that precise garbage collection is undecidable in the general case (related to the halting problem).
- When he suggested reference counting instead, Kent pointed out that ref-counting has high overhead and often performs worse than a good generational GC. Good GC pauses are not a real problem if the collector is well engineered (Chez Scheme proves it).

#### Chez Scheme as Counter-Example
- The author deeply respects Kent Dybvig and Chez Scheme:
  - Lightning-fast compilation
  - Highly tunable, low-pause GC
  - Philosophy: don’t waste time optimizing stupid code; assume the programmer is competent; choose the right simple abstractions.
- In other words, wisdom > brute-force sophistication.

#### How Rust Actually Turned Out
- The original dream of “purely static memory management, no GC ever” is dead.
- Modern Rust has:
  - `Rc<T>` / `Arc<T>` (reference counting with cycle collection via `Weak`)
  - `unsafe` code (mandatory for many real-world libraries: network stacks, browsers, OS kernels, etc.)
  - Ongoing research trying to make parts of `unsafe` safer (Stacked Borrows, Tree Borrows, etc.), but each new model adds restrictions again.
- Yet the marketing and community still repeat the mantra of “strong static guarantees” and “fearless concurrency.”
- When you point out the gaps, the official answer becomes “that’s just Rust’s philosophy” or “you don’t understand the borrow checker.”

#### The Author’s Current Stance
- He fully understands lifetimes, borrowing, etc., and has even taught advanced Rust courses where students implemented functional-language interpreters in Rust.
- But the more he teaches Rust, the more he appreciates C++:
  - C++ smart pointers + RAII are simpler and more expressive for many tasks.
  - When you really need maximum performance, he’ll still pick C/C++ over Rust.
- He finds Rust’s error messages notoriously hard to decipher, and the constant need to fight the borrow checker annoying.
- The “philosophy” defense feels like a religious excuse for design compromises.

#### Bottom Line
The author sees modern Rust’s success as largely marketing triumph + ecosystem momentum, not as proof that its core ideas were fundamentally sounder than decades of prior art (Region systems, Cyclone, linear types, high-performance GCs, etc.). He believes the original grandiose claims were naive, the compromises were inevitable, and the community now hides behind “philosophy” when confronted with the gaps.

It’s a rare insider-style critique from someone who:
1. saw Rust literally at its birth,
2. deeply studied memory safety himself,
3. had Kent Dybvig as mentor,
4. still chooses C/C++ in 2025 despite the hype.

Whether you agree or not, it’s a thoughtful counter-narrative to the dominant “Rust is the future that has already arrived” story.
