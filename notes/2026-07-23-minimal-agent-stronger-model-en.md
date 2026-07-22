---
audio: false
generated: true
image: false
lang: en
layout: post
title: Minimal Agent, Stronger Model
translated: false
type: note
---

Question: Why is pi-agent so strong? Is it because LLMs already contain most knowledge, so a minimal-agent approach with precise instructions can outperform heavily prompted agents?

Answer:

Your intuition is largely correct. The core idea is **moving intelligence from the agent framework back into the base model**.

A modern LLM already has:

* billions/trillions of tokens of pretraining knowledge
* learned coding patterns
* learned tool-use patterns
* learned reasoning heuristics
* broad world models

So the agent layer does not need to "teach" the model everything again. The agent layer mainly needs to provide:

1. **Current task state**
2. **Available tools**
3. **Constraints**
4. **A good execution loop**

A small agent like pi-agent can work well because the forward pass is already very capable:

```
User intent
    |
    v
small system prompt
    |
    v
LLM latent knowledge + reasoning
    |
    v
tool call
    |
    v
observe result
    |
    v
next action
```

The model itself fills in the gaps.

---

The tradeoff is basically:

## Minimal agent

Example:

```
You are a coding agent.
Use tools when needed.
Solve the user's task.
```

Advantages:

* smaller context window usage
* faster inference
* cheaper
* more creative
* less constrained
* lets frontier models decide strategy

The model has more "degrees of freedom".

This is closer to:

```
strong model + thin orchestration
```

---

## Heavy agent (Claude Code style)

A heavier agent often has:

```
system prompt
+ coding rules
+ safety rules
+ workflow rules
+ tool descriptions
+ examples
+ memory
+ conventions
+ policies
```

Advantages:

* more predictable
* easier for millions of users
* fewer catastrophic mistakes
* consistent workflow

But cost:

Every rule consumes attention budget.

The model now has to solve:

```
original task
+
follow 100 instructions
+
avoid violating constraints
```

Sometimes the optimization target becomes:

"follow the framework"

instead of:

"solve the user's problem".

---

A useful analogy:

### GPT-4 era:

The model was weaker.

You needed:

```
agent framework = external brain
```

So more prompts, more chains, more scaffolding.

---

### 2026 frontier model era:

The model is stronger.

You want:

```
agent framework = nervous system
model = brain
```

Too much nervous system control can actually reduce intelligence.

---

This is similar to programming language design.

A huge framework:

```
Spring Boot
+ 200 annotations
+ conventions
+ lifecycle hooks
+ dependency injection
```

is great for enterprise stability.

But sometimes a small Go/Rust program wins because:

```
less abstraction
closer to metal
more freedom
```

Agent design has the same spectrum.

---

The interesting future direction is probably:

```
tiny agent runtime
+
excellent model
+
excellent tools
+
long-term memory
+
evaluation loop
```

not:

```
giant prompt
+
hundreds of rules
+
rigid workflow
```

The winning agent may look more like an operating system kernel:

```
10k lines of code
```

not:

```
1 million lines of agent instructions
```

---

One important caveat:

The reason pi feels powerful is also because you are an advanced user. A 12-year engineer naturally provides:

```
high-quality task specification
good debugging feedback
correct constraints
```

The agent doesn't need to compensate for bad input.

For average users, more opinionated agents often perform better because they transform vague intent into executable steps.

So the real formula is:

```
Expert user + frontier model + thin agent
        >
Heavy agent + average user
```

but:

```
Average user + heavy agent
        >
Average user + minimal agent
```

The interesting research question is finding the smallest possible "agent kernel" that maximizes model capability without fighting it. pi-agent is exploring that point on the curve.