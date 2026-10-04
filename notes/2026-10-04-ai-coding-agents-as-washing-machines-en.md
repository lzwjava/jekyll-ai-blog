---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI Coding Agents as Washing Machines
translated: false
type: note
---

Question: Is AI coding agents today like washing machines — helping humans but not replacing the whole process?

Answer:

Yes, that analogy is quite accurate.

A washing machine did not eliminate the entire laundry workflow. It automated the **most repetitive, mechanical, low-value parts**:

```
Before:
human:
  collect clothes
  wash
  scrub
  rinse
  squeeze water
  dry
  fold

After:
machine:
  wash
  rinse
  spin dry

human:
  put clothes in
  move clothes out
  hang / dry
  fold
```

AI coding agents are similar:

```
Before:
human:
  understand requirement
  design architecture
  write code
  debug
  test
  deploy
  maintain

With agents:
AI:
  generate code
  refactor
  write tests
  search docs
  debug simple errors
  create boilerplate

human:
  define goals
  judge architecture
  review output
  handle ambiguity
  make product decisions
  own responsibility
```

The key difference is that software has a much higher "semantic" component than laundry.

A washing machine works because:

* clothes are physical objects
* the process is well-defined
* success criteria are obvious

Software is harder because:

* requirements are vague
* users change their minds
* tradeoffs exist
* bugs can hide for years
* architecture decisions affect future systems

So current agents are closer to a **very fast junior engineer / pair programmer** than a fully autonomous software company.

A good mental model:

```
1990s:
compiler = machine that turns human intent into machine instructions

2010s:
frameworks = machine that removes repetitive engineering

2020s:
LLM agents = machine that turns high-level intent into many engineering actions
```

The likely future is not:

> "Human says: build Facebook. Agent does everything."

More likely:

> "Human founder/engineer says: build this product, explains constraints, reviews decisions. Agents operate like a team of developers."

Similar to construction:

```
architect -> decides building
workers -> execute construction

future:
human -> product/architecture/quality
agents -> implementation workforce
```

The human role shifts upward:

* less typing code
* more specifying what should exist
* more evaluating whether the result is correct
* more customer interaction

For someone building AI consulting/software factories, the leverage is exactly here: one person with agents can potentially operate like a small engineering team, but the bottleneck becomes **finding valuable problems and controlling quality**, not writing every line.

I can also map this to the "AI software factory" idea you mentioned before (100 computers + agents + humans supervising projects) and where the realistic bottlenecks are.
