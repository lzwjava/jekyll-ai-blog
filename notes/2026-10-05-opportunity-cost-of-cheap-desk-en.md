---
audio: false
generated: true
image: false
lang: en
layout: post
title: Opportunity Cost of Cheap Desk
translated: false
type: note
---

Question: Is spending ~1 hour physically finding/picking up a cheap second-hand desk actually expensive when an AI agent can potentially use that hour to produce useful work?

Answer: **Yes — especially for you, the opportunity cost can easily exceed the price of the desk.**

The important equation is:

$$
\text{True cost} =
\text{purchase price}
+ \text{transport}
+ \text{time} \times \text{value of your time}
+ \text{context switching}
$$

Suppose:

* Desk: ¥100
* Transport: ¥20
* Pickup: 1 hour
* Your productive value: even ¥100/hour

Then the "¥120 desk" is economically closer to:

$$
120 + 1\times100 = \mathbf{¥220}
$$

And that's before considering the fact that **1 hour of uninterrupted agent orchestration can potentially create an artifact that keeps generating value**.

The deeper change with agents is that your scarce resource becomes increasingly **human attention**, not raw execution time.

For example, instead of:

```text
You
 │
 ├── search Xianyu
 ├── message seller
 ├── travel
 ├── inspect desk
 ├── carry desk
 └── return
       ↓
    ¥100 desk
```

you increasingly want:

```text
You
 │
 └── Agent
      ├── search listings
      ├── compare prices
      ├── estimate transportation
      ├── filter scams
      ├── negotiate
      └── give you 3 candidates
                ↓
          You make final decision
```

And the same principle applies to software:

```text
1 hour manually:
    implement feature
    debug
    write tests
    documentation

1 hour with agents:
    specify goal
    supervise
    review
    merge
```

So **yes, the opportunity cost of doing low-value physical errands is becoming more visible**.

But there is one important correction: don't conclude that *every* hour should be spent coding. Sometimes the desk is worth getting because it improves your workspace for the next 1,000 hours. The correct calculation is **lifetime return on the activity**, not simply "desk pickup vs coding."

A useful personal rule could be:

$$
\boxed{
\text{Delegate/automate if }
C_{\text{delegation}} < C_{\text{your time}}
}
$$

And with agents, the threshold for delegation gets dramatically lower because software execution is becoming extremely cheap.

I can also help you build a simple **"should I do this myself or delegate it to an agent?" calculator** based on your actual hourly opportunity cost.