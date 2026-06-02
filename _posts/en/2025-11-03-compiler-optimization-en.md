---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Compiler Optimization for Skilled Programmers
translated: false
type: note
---

### Compiler Optimization

In Kent Dybvig's compiler course, he once told us that many compiler courses heavily emphasize "optimization," but most of these optimizations are really geared toward sloppy programmers. For example, common subexpression elimination (CSE)—pulling out repeated, expensive expressions. A well-trained programmer should avoid writing redundant computations in the first place by defining variables to reuse results. Yet compilers take this on themselves, as if it's a big deal. It's not.

What *is* important is the speed of the compiler itself. Many compilers pile on these kinds of pointless "optimizations" in an attempt to turn bad code into good code, which ends up slowing down the compiler. Building a project takes forever, stretching out the cycle from code changes to seeing results, and tanking developer productivity.

That's why Chez Scheme skips most of these basic optimizations—it assumes programmers have the basic skills to avoid redundant, costly expressions on their own. Chez's optimizations focus mainly on code that the compiler itself generates, like closure optimization to shrink the memory footprint of closures as much as possible. These are areas programmers can't directly control, so the compiler should aim for the best possible outcome there. But even these have limits: if chasing optimization makes the compiler painfully slow while barely speeding up the final program, it's not worth it. Chez Scheme strikes a balance between compilation speed and the performance of the generated code.

In later engineering practice, I've come to appreciate this key insight multiple times.
