---
audio: false
generated: true
image: false
lang: en
layout: post
title: Rust's Unforeseen AI Advantage
translated: false
type: note
---

Question: What did Fengjia Chun (Jeremy Feng), co-founder of Greptime, say in his recent reflection post about why choosing Rust for GreptimeDB was the right decision and why the team doesn't regret it?

Answer:

Jeremy Feng (冯家纯), co-founder and engineering lead for the GreptimeDB kernel, published a detailed four-year retrospective on April 21, 2026. The Rust decision is one of the central topics he reflects on. Here is a comprehensive breakdown:

---

## Background: Why Rust Was Chosen in 2022

Picking Rust for a database in 2022 was a minority choice. For the team, there was almost no debate — they had been writing Rust for nearly four years, so experience was not a concern.

The technical reasoning was grounded in the nature of database systems:

A database demands precise memory control, complex concurrency management, and stable latency under high throughput. That points squarely at a systems language with no GC and predictable performance. Go and Java's GC works fine for most scenarios, but at the storage engine level, a single GC pause can mean a latency spike — and that was unacceptable. Rust's ownership model inherently guarantees memory and thread safety, and zero-cost abstractions mean you don't have to choose between clean design and raw performance.

---

## The Good: What Rust Delivered

Jeremy outlines several concrete benefits that materialized over four years:

### 1. Elimination of Entire Bug Classes

Rust eliminated entire classes of concurrency and memory bugs. Their CI almost never produces a segfault — something hard to imagine in a C++ database project.

### 2. Unexpected Community Appeal

An unexpected bonus was community appeal. Rust developers are naturally drawn to infrastructure projects, and contributors who showed up often went beyond typo fixes to working on the engine itself.

### 3. The Surprising 2025 Dividend: Rust Is Great for AI-Assisted Coding

This was perhaps the most striking insight Jeremy shared — something the team never anticipated when they made the original choice:

In 2025, Rust gave them a gift they never anticipated: it may be the best language for vibe coding. AI writes plenty of buggy Rust, but the compiler catches errors precisely and kicks them right back, creating a tight generate-error-fix loop. In other languages, AI-generated code can "look right" while bugs hide in runtime corners. If Rust code compiles, a whole category of memory and concurrency errors is already gone. They had no idea this dividend was coming when they made the choice.

---

## The Hard: Real Costs They Had to Pay

Jeremy is candid about the downsides — he does not sugarcoat the difficulties:

The hard part was hiring. The Rust talent pool is an order of magnitude smaller than Java or Go, and the intersection of "knows databases" and "knows Rust" is smaller still. Every new team member needed patience and ramp-up time. Compile times and disk usage were also painful.

---

## The Verdict: No Regrets

Jeremy's conclusion is unambiguous:

If they had to do it over, they'd pick Rust again. The early phase is harder, but over a longer timeline, worth it.

---

## Summary Table

| Aspect | What Rust Brought |
|---|---|
| **Memory Safety** | No segfaults; entire classes of bugs eliminated by the compiler |
| **Concurrency** | Ownership model guarantees thread safety at compile time |
| **Performance** | No GC pauses; predictable latency under high throughput |
| **Community** | Rust devs are attracted to infrastructure and go deep into the codebase |
| **AI Coding (2025 bonus)** | Compiler's tight feedback loop makes AI-generated code far safer than in other languages |
| **Cost** | Smaller hiring pool; slower onboarding; long compile times |
| **Final verdict** | Would pick Rust again without hesitation |

The key philosophical takeaway from Jeremy is that the benefits of Rust compound over a long timeline — safety, performance, community, and even AI tooling synergy — far outweigh the steep initial costs. The 2025 AI-coding insight in particular was an unplanned but significant bonus that further validated their original choice.

References:

- [Four Years of GreptimeDB: Looking Back at Decisions, Detours, and the People Along the Way — Greptime Blog (April 21, 2026)](https://www.greptime.com/blogs/2026-04-21-greptimedb-four-years-retrospective)
