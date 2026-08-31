---
audio: false
generated: true
image: false
lang: en
layout: post
title: HM Inference Trade-Off Analogy
translated: false
type: note
---

Question: **How should I understand the argument in this Weibo post, especially the washing-machine physics → Haskell Hindley–Milner analogy?**

Answer:

The post is making **one big argument through two very different examples**:

> **An optimization made for convenience can constrain the original capability so much that the “automation” is actually a bad trade.**

There are two layers here: the **washing-machine claim** and the **Haskell analogy**.

### 1. Washing-machine part

The author's reasoning is roughly:

```text
wave/pulsator
    ↓
accelerates water
    ↓
water develops rotational flow
    ↓
clothes move relative to water + each other
    ↓
friction / collision
    ↓
cleaning
```

The key physical idea is that **water has inertia**.

If you suddenly reverse the pulsator, the water doesn't instantly reverse with it. You need to apply torque/force over some time to change the water's velocity.

The post summarizes this as:

> Δv = a × Δt

So, very roughly:

```text
longer one-direction run
        ↓
water has more time to accelerate
        ↓
stronger / larger-scale water motion
```

Whereas:

```text
3 sec forward
→ reverse
→ 3 sec backward
→ reverse
...
```

may prevent the water from ever developing the same large-scale circulation.

**But there is an important caveat:** the Weibo post is presenting this as if it proves that dual-tub machines wash better. It doesn't. Real washing performance depends on pulsator geometry, water level, load, fabric motion, detergent, mechanical energy delivered to clothes, etc. Also, modern fully automatic machines have their own wash algorithms specifically designed around these constraints.

So don't take:

> "7 seconds > 3 seconds → therefore cleaner"

as a rigorous conclusion.

The more interesting point is actually the **design trade-off**.

---

## 2. Why does the author bring up Haskell?

This is the clever part.

The author sees the washing-machine design as:

```text
Goal A: wash clothes effectively
Goal B: make the entire process automatic
```

The automatic machine introduces a constraint:

```text
Clothes must not become badly tangled
        ↓
because later the machine must automatically spin
        ↓
therefore washing motion must be constrained
```

So the machine optimizes:

```text
wash + automatic spin + no human intervention
```

rather than:

```text
maximum washing performance
```

The author's complaint is basically:

> **You optimized for automation, and in doing so constrained the underlying operation.**

Then he says Haskell's Hindley–Milner type inference has a similar pattern.

---

# 3. HM type inference

Imagine a language where you write:

```haskell
f x = x + 1
```

You don't explicitly write:

```haskell
f :: Int -> Int
```

The compiler figures it out.

That's awesome.

The compiler essentially derives constraints:

```text
x + 1
```

requires `x` to support `+`.

Then:

```text
x :: Num a => a
```

and therefore:

```text
f :: Num a => a -> a
```

This is **type inference**.

The beautiful part of Hindley–Milner is that you can write relatively little type information and let the compiler infer a lot.

---

# 4. But there is a fundamental constraint

HM inference works extremely well because it deliberately restricts the type system.

Conceptually, it wants types to have a form that can be inferred algorithmically:

```text
a
a -> b
[a]
(a, b)
...
```

and polymorphism such as:

```haskell
id :: a -> a
```

is very elegant.

The compiler can perform something like:

```text
expression
    ↓
generate type constraints
    ↓
unification
    ↓
infer principal type
```

For example:

```haskell
\x -> x
```

Start with:

```text
x :: α
```

The function returns `x`, so:

```text
return :: α
```

Therefore:

```text
\x -> x :: α -> α
```

No annotation required.

That's the "automation" the author likes initially.

---

# 5. Where does the author's criticism come from?

As type systems become more expressive, you encounter things like:

```text
GADTs
dependent types
higher-rank polymorphism
type families
type-level computation
existentials
```

Now type inference becomes substantially harder.

You can get into situations where:

```text
the programmer knows exactly what type they mean
```

but

```text
the inference algorithm cannot determine it
```

So you have to write annotations or restructure the program.

The author's philosophical complaint is:

```text
Without inference:

programmer
    ↓
explicitly specifies types
    ↓
maximum expressive freedom
```

With aggressive inference:

```text
programmer
    ↓
writes less
    ↓
compiler infers more
    ↓
language/type system imposes restrictions
```

So he sees the same pattern:

### Washing machine

```text
automatic spin
      ↓
must prevent tangled clothes
      ↓
constrains washing motion
```

### Type system

```text
automatic type inference
      ↓
must keep inference decidable/manageable
      ↓
constrains type-system expressiveness
```

That's the analogy.

---

# 6. But there is a major technical problem with the post

I would **not** conclude:

> "HM is badly designed because inference reduces expressiveness."

That's too simplistic.

The trade-off is more like:

```text
                 Expressiveness
                      ↑
                      |
                      |          dependent types
                      |       /
                      |     /   richer systems
                      |   /
                      | /
                      +----------------→ inference automation
                         HM
```

There is a genuine engineering trade-off between:

* expressive type systems
* decidable inference
* predictable compiler behavior
* concise source code
* understandable error messages
* compilation complexity

HM is extremely successful precisely because it occupies a very useful point in this design space.

And modern Haskell isn't simply:

> "HM and nothing else."

GHC has accumulated many extensions far beyond classical Hindley–Milner.

For example, you can explicitly guide inference:

```haskell
f :: forall a. ...
```

or use richer type features when necessary.

So the real situation is closer to:

```text
simple cases
    ↓
let compiler infer everything

hard cases
    ↓
programmer supplies constraints
```

rather than:

```text
inference = inherently bad
```

---

# 7. The deeper idea is actually interesting

I think the valuable idea in the post is **not** "dual-tub washing machines are better" or "Haskell is bad."

It's this:

> **Every automation mechanism introduces assumptions about the problem. Those assumptions can become constraints on what the system is capable of doing.**

This is a very useful engineering lens.

You see the same thing everywhere.

### Garbage collection

```text
automatic memory management
        ↓
no manual free()
        ↓
less programmer burden
        ↓
less precise control over lifetime
```

### ORM

```text
automatic SQL mapping
        ↓
less SQL boilerplate
        ↓
convenient CRUD
        ↓
awkward expression of unusual queries
```

### Kubernetes

```text
automatic scheduling / reconciliation
        ↓
declarative operations
        ↓
huge operational convenience
        ↓
sometimes harder to express unusual infrastructure behavior
```

### LLM agents

```text
automatic planning
        ↓
less explicit workflow code
        ↓
more flexibility for unknown tasks
        ↓
less deterministic control
```

And interestingly, this is very close to a principle in programming-language design:

> **Automation isn't free. It works by restricting the space of things that need to be reasoned about.**

That's the strongest interpretation of the Weibo post.

---

## 8. The part I would challenge

The author jumps from:

```text
automation creates constraints
```

to:

```text
therefore the automation is bad
```

That does **not** follow.

Engineering is optimization under constraints.

Suppose:

```text
Manual washing:
    cleaning = 10
    convenience = 2

Automatic washing:
    cleaning = 8
    convenience = 10
```

Someone may rationally choose the second one.

Likewise:

```text
Explicit types:
    expressiveness = 10
    verbosity = 8

HM inference:
    expressiveness = 8
    verbosity = 2
```

That can be an excellent trade.

So I'd rewrite the author's thesis as:

> **Don't confuse reducing human effort with improving the underlying capability. Whenever you automate something, inspect what constraints the automation introduces.**

That is a much stronger and more general engineering principle.

And it's particularly relevant to **AI agents**: an agent that "automates everything" can easily become less controllable, less debuggable, and less expressive than a small explicit program. The interesting question is not *automation or no automation*, but **where to put the boundary between automation and explicit control**.
