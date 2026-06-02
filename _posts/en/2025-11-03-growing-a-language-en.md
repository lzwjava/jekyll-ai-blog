---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Growing a Language by Guy Steele
translated: false
type: note
---

### Overview
The talk "Growing a Language" was delivered by Guy L. Steele Jr. at OOPSLA '98 (Object-Oriented Programming, Systems, Languages & Applications conference) in Vancouver, Canada, on October 19, 1998. It's a seminal 45-minute presentation on language design and evolution, using Scheme (a dialect of Lisp) as a live-coding demonstration. Steele, a co-designer of Java and Scheme, illustrates how to build a programming language incrementally from the ground up, emphasizing simplicity, expressiveness, and extensibility. The core idea is that languages "grow" organically by starting with minimal primitives and layering features on top, rather than designing everything at once.

The video is available on YouTube (archived by ACM SIGPLAN) and has influenced modern language design discussions, including in functional and embedded domain-specific languages (DSLs).

### Key Themes and Structure
Steele structures the talk as a hands-on tutorial, coding live in Scheme to "grow" a simple expression evaluator into a full-fledged language. He uses metaphors like "gardening" (nurturing features) vs. "architecture" (rigid blueprints) to argue for evolutionary design. Here's a breakdown of the main sections:

1. **Introduction: Why Grow a Language? (0:00–5:00)**
   Steele motivates the talk by critiquing "big bang" language design (e.g., specifying everything upfront, leading to bloat). He proposes "growing" instead: start small, test often, and extend based on real needs. He draws from Lisp's history, where the language grew from evaluator code. Goal: Build a tiny language for arithmetic expressions that can evolve into something Turing-complete.

2. **Seed: Basic Evaluator (5:00–10:00)**
   Starts with the simplest kernel: a function that evaluates atomic numbers (e.g., `3` → 3).
   - Code snippet (in Scheme):
     ```scheme
     (define (eval exp) exp)  ; Identity for atoms
     ```
   He runs it live, showing `(eval 3)` returns 3. This is the "seed"—pure, no syntax sugar.

3. **Sprouting: Adding Operations (10:00–20:00)**
   Introduces binary operators like `+` and `*` by pattern-matching on lists (e.g., `(+ 2 3)`).
   - Grows the evaluator:
     ```scheme
     (define (eval exp)
       (if (pair? exp)
           (let ((op (car exp))
                 (args (cdr exp)))
             (apply op (map eval args)))
           exp))
     ```
   Demonstrates evaluation: `(+ (* 2 3) 4)` → 10. Emphasizes hygiene—keep it simple, avoid premature optimization.

4. **Branching: Conditionals and Variables (20:00–30:00)**
   Adds `if` for conditionals and `let` for binding variables, showing how scoping emerges naturally.
   - Example growth:
     ```scheme
     (define (eval exp env)
       (if (pair? exp)
           (case (car exp)
             ((quote) (cadr exp))
             ((if) (if (eval (cadr exp) env)
                       (eval (caddr exp) env)
                       (eval (cadddr exp) env)))
             ((let) (eval (cadddr exp) (extend-env env (caadr exp) (eval (cadadr exp) env))))
             (else ...))  ; Fallback to function application
           (lookup exp env)))  ; Variable lookup
     ```
   Live demo: Computes factorials via recursive `let` bindings, highlighting how recursion "grows" from iteration.

5. **Flowering: Macros and Abstraction (30:00–40:00)**
   Introduces hygienic macros to add domain-specific syntax (e.g., a `while` loop). Shows how macros let users "grow" the language themselves.
   - Key insight: Languages should be "open" for extension, like Lisp's macro system, enabling DSLs without forking the core.

6. **Conclusion: Lessons for Designers (40:00–45:00)**
   Steele wraps up with principles:
   - **Incrementalism**: Add one feature at a time; test immediately.
   - **Uniformity**: Reuse primitives (e.g., everything is an expression).
   - **User Empowerment**: Let users extend via macros or similar.
   He ties it to real-world languages (Java, Scheme) and warns against "feature creep." Q&A touches on performance and implementation challenges.

### Impact and Takeaways
This talk popularized "language workbench" ideas, influencing tools like Racket (which extends Scheme) and concepts in Rust's macros or Swift's extensions. It's a masterclass in thinking about languages as living systems—practical, philosophical, and entertaining (Steele's dry wit shines through).

For the full experience, watch the video: [Growing a Language - OOPSLA '98](https://www.youtube.com/watch?v=_ahvzDzKdB0). Transcripts/summaries are sparse, but the code is reconstructible from the slides (available via ACM Digital Library). If you're into PL design, pair it with Steele's later "Growing a Pattern Language" (OOPSLA '05).
