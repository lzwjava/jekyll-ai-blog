---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Config Files Evolve Into Bad Languages
translated: false
type: note
---

### Explaining "The Logic Indestructibility Law" and Why Config Files Become Bad Programming Languages

The post you're referencing is from Yining Wang (also known as Yin Wang), a computer science researcher and blogger. It's a thoughtful piece building on an observation by programming legend Guy Steele: **as configuration files grow more complex, they inevitably evolve into a crappy programming language**. Wang uses a concept he coined—"the Logic Indestructibility Law"—to explain *why* this happens almost every time. It's a clever analogy to physics' conservation of energy: logic doesn't vanish; it just relocates.

#### What Is the "Logic Indestructibility Law"?

Wang defines it simply: **The logic that people need to express will always appear somewhere, in essentially the same form.**

- In essence, if you have some decision-making or rule-based thinking (e.g., "if this condition is true, do that"), it *has* to show up in your system. It won't evaporate just because you try to hide it or offload it.
- This logic might end up in your main program code, a config file, a spreadsheet, or even a whiteboard sketch—but it persists, unchanged in its core structure.
- It's "indestructible" because human needs (like customizing behavior) demand it. Ignoring this leads to awkward workarounds.

Think of it like water finding its level: logic flows to where it's needed, no matter how you try to contain it.

#### How Does This Explain Config Files Turning into "Bad Languages"?

Configuration files start innocently—as a way to tweak settings without touching the core code. But as needs grow, they bloat into something more sinister. Here's the step-by-step breakdown, tied to the law:

1. **The Simple Start: Just Variables**
   At first, configs are basic key-value pairs:
   - `enable_optimization = true`
   - `max_requests = 1000`
   These are like "variables" in programming (e.g., `let x = 5;`). The program reads them and plugs the values into its logic.
   *Why?* No deep logic yet—just placeholders. But variables are a fundamental building block of *any* programming language. Per the law, this logic (assigning and using values) has already snuck into the config.

2. **The Creep: Adding Branches**
   As users demand more flexibility (e.g., "enable feature X only for premium users"), devs start embedding *conditional logic* in the config:
   - Something like: `if user_type == "premium" then enable_feature_X else disable`.
   This is straight-up "if-then-else" branching—another core programming primitive.
   *Why?* Devs subconsciously shift logic from the main code to the config for easier tweaking. But the law kicks in: the logic doesn't disappear from the program; it just migrates. Now the config isn't just data—it's making decisions.

3. **The Tipping Point: Full-Blown Logic Overload**
   Over time, configs accumulate loops, functions, error handling, and custom rules. What began as a flat file (YAML, JSON, etc.) ends up with syntax that's Turing-complete (able to express any computation).
   - Result: A "language" that's powerful but terrible—missing good tooling, error messages, debugging, or libraries. It's like programming in a half-baked dialect of code.
   *Why inevitable?* Logic Indestructibility. If the logic exists (and it must, to solve real problems), it'll manifest *somewhere*. Pushing it out of the main code shoves it into the config, where it festers.

Steele's quip nails it: configs don't *want* to be languages, but complexity forces them to be. And they're always "bad" because they're designed for simplicity, not expressiveness.

#### Tie-In to Domain-Specific Languages (DSLs)

Wang references his earlier essay, ["The Pitfalls of DSLs"](https://yinwang1.substack.com/p/dsl-misconceptions) (specifically the "Dynamic Logic Loading" section), to extend this. Many DSLs (custom mini-languages for specific tasks) arise from the same urge: loading rules or behaviors at runtime without recompiling.

- **The Mistake:** Teams think they need a bespoke language for "dynamic logic," so they invent one—reinventing if-then-else in a clunky wrapper.
- **The Fix:** Most of this boils down to simple conditionals. Just embed snippets from an existing language (e.g., JavaScript's `if` statements) into your config. No need for a whole new DSL—it's overkill and leads to the same "bad language" trap.
- *Law in Action:* The logic (e.g., "check if X, then Y") had to go somewhere. A snippet in JS keeps it in a *good* language, avoiding config bloat.

#### Why Does This Matter?

This isn't just theory—it's a warning for software design. It explains why tools like Kubernetes YAML or webpack configs feel like coding nightmares. The lesson? Embrace logic where it thrives (in proper languages), rather than exiling it to configs. Design systems that make logic *visible and manageable*, or it'll haunt you in spectral form.

If you want to dive deeper, the full post is a quick read with more nuance.

[Original Post: Configuration Files and the Logic Indestructibility Law](https://yinwang1.substack.com/p/224)
[Related: The Pitfalls of DSLs](https://yinwang1.substack.com/p/dsl-misconceptions)
