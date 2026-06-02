---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Underestimating Experts and Deeper Understanding
translated: false
type: note
---

### Context of the Post

This excerpt is from a blog post (or social media reflection) by Yin Wang, a prominent software engineer, programming language enthusiast, and blogger known for his insightful critiques of programming languages, type systems, and software design. Wang has worked at companies like Google and is the author of the Yinwang.org blog, where he often dives deep into topics like functional programming, Lisp dialects, and the philosophy behind language design. The post reflects on his personal growth in understanding experts' perspectives, using Dan Friedman as a case study. It's a humble admission of confirmation bias—how we (including Wang himself) can misjudge someone's expertise based on surface-level disagreements.

The tone is introspective and philosophical, starting with a general observation about "human thinking patterns" (likely referring to how people form prejudices quickly) and tying it to Wang's own experience. He uses this anecdote to illustrate that deep criticism often comes from profound understanding, not ignorance.

### The Story in the Anecdote

Yin Wang recounts a time when he underestimated Dan P. Friedman, a legendary computer science professor at Indiana University and a pioneer in functional and logic programming. Friedman is best known for co-authoring the iconic *The Little Schemer* book series (with Matthias Felleisen), which teaches programming through a playful, question-and-answer style using Scheme, a minimalist dialect of Lisp.

- **Wang's Initial Misjudgment**: Friedman has long been vocal about his preference for dynamic languages like Scheme, which don't enforce types at compile time (allowing more flexibility but risking runtime errors). He often critiques static type systems in languages like Haskell, arguing they can be overly rigid, verbose, or limit expressiveness without delivering proportional benefits in real-world software. Wang, who respected Friedman's intellect (especially his mastery of advanced concepts like *continuations*—a powerful mechanism for manipulating control flow, akin to "capturing" the rest of a program's execution as a function), still dismissed him as "biased" because Friedman "only knew dynamic languages." Wang saw this as a blind spot, much like how people today might stereotype experts based on their tool preferences.

- **The Turning Point**: Wang's view shifted when Friedman demonstrated his depth. In a teaching session (likely in a course or workshop), Friedman used *miniKanren*—a lightweight, embedded domain-specific language for logic programming (think relational queries, like in Prolog, but integrated into Scheme)—to implement the *Hindley-Milner type system*. This is the polymorphic type inference algorithm powering languages like ML and Haskell, which automatically deduces types without annotations while ensuring safety. Implementing it in a dynamic language like Scheme via miniKanren elegantly shows how logic programming can model type checking as "search" for solutions, bridging dynamic and static worlds.

  Later, Friedman dove into *dependent types*—an advanced extension of type systems where types can depend on runtime values (e.g., a function that only accepts lists of length exactly 5). This enables even stronger guarantees, like proofs within code, as in languages like Idris or Agda. Friedman co-authored *The Little Typer* (2018, with David Thrall), a beginner-friendly book that introduces these ideas through a simple, typer-like language, echoing the style of his Schemer books but for typed programming.

Wang realized Friedman wasn't dismissive out of ignorance; he *understood* static types (including Haskell's sophisticated system, which combines Hindley-Milner with extensions for laziness and monads) better than most proponents. Friedman's critiques stem from seeing their limitations—e.g., how they can complicate simple programs or fail to capture domain-specific invariants without dependent types. This "seeing through" the hype leads to a more nuanced, sometimes contrarian view.

### Why This Matters

The post is a meta-commentary on expertise in programming languages: True mastery often looks like skepticism, not blind enthusiasm. It resonates with debates in the PL community (e.g., static vs. dynamic typing wars). Wang uses it to caution against snap judgments, drawing a parallel to how he sees others (and himself) reacting to contrarians today.

For a full read, the original post is on Yin Wang's blog: [Yin Wang's Blog Post on Dan Friedman](http://www.yinwang.org/blah?blog=2019/10/01/dan-friedman). Friedman's work is foundational—check *The Little Schemer* for Scheme basics or *The Little Typer* for dependent types.
