---
audio: false
generated: true
image: false
lang: en
layout: post
title: Parallel Probabilistic Decision Model
translated: false
type: note
---

Question: **What is TypeSafe AI’s “System One Models” / Jev?**

Answer:

This is a pretty interesting architectural idea. The key insight is:

> **Don’t make an AI generate text if the software only needs a decision.**

TypeSafe calls this a new class of **System One Models**, and **Jev** is their first public model. ([TypeSafe AI][1])

### 1. Normal LLM

Suppose your application receives:

```text
Customer:
"I was charged twice for the same order. Can you refund one of them?"
```

With GPT/Claude, you might ask:

```text
Classify this request.

Output JSON:
{
  "intent": "...",
  "urgency": "...",
  "refund_likelihood": ...
}
```

Conceptually:

```text
text
 ↓
LLM
 ↓
tokens → JSON string
 ↓
parser
 ↓
validation
 ↓
your program
```

The LLM is fundamentally a **next-token generator**:

$$
P(x_1,x_2,\ldots,x_n)
=
\prod_i P(x_i|x_{<i})
$$

Even if you force JSON/schema output, underneath you're still generating a sequence of tokens.

---

### 2. Jev changes the target

Jev says:

```text
unstructured state
        ↓
      Jev
        ↓
typed probabilities
```

For example, you could define:

```python
questions = {
    "intent": [
        "payment_problem",
        "refund_request",
        "technical_problem",
        "other",
    ],
    "urgency": [
        "low",
        "medium",
        "high",
    ],
}
```

Then Jev might return something conceptually like:

```json
{
  "intent": {
    "payment_problem": 0.91,
    "refund_request": 0.84,
    "technical_problem": 0.03,
    "other": 0.01
  },
  "urgency": {
    "low": 0.02,
    "medium": 0.18,
    "high": 0.87
  }
}
```

Your program then decides:

```python
if result["urgency"]["high"] > 0.8:
    escalate_to_human()

if result["intent"]["refund_request"] > 0.8:
    route_to_refund_team()
```

So **the model doesn't generate the action**.

The model generates **probabilistic information**, while ordinary software determines what to do.

This is why TypeSafe describes Jev as:

> “a frontier-intelligence function call: unstructured state in, typed probabilistic decisions out.” ([TypeSafe AI][1])

---

## 3. The really important part: parallel sampling

This is probably the most interesting technical difference.

An autoregressive LLM does:

```text
token 1
  ↓
token 2
  ↓
token 3
  ↓
...
token N
```

Every token depends on previous tokens.

If you only need:

```text
A = 0.8
B = 0.1
C = 0.1
```

generating a string such as:

```text
{"A": 0.8, "B": 0.1, "C": 0.1}
```

is arguably wasteful.

Jev instead claims to produce the structured decisions **in parallel**, rather than autoregressively generating every output token. TypeSafe says this is a major reason for its latency/efficiency advantage. ([TypeSafe AI][1])

Conceptually:

```text
             ┌── P(A)
state ───────┼── P(B)
             ├── P(C)
             ├── P(D)
             └── ...
```

rather than:

```text
state
 ↓
token
 ↓
token
 ↓
token
 ↓
token
...
```

That's a very different optimization target.

---

# 4. Why does this matter so much?

Because **software doesn't actually need prose most of the time**.

Consider:

```python
if model.says_something_about_customer:
    ...
```

You don't need:

```text
"Based on my analysis, I believe that the customer is probably..."
```

You need:

```python
customer_is_churning = 0.83
```

or:

```python
route = "fraud_review"
confidence = 0.97
```

or:

```python
should_escalate = 0.91
```

This makes Jev look less like:

```text
ChatGPT
```

and more like:

```text
ML inference primitive
```

embedded inside normal software.

TypeSafe explicitly targets things like classification, routing, scoring, extraction, branching, verification, guardrails and real-time applications. ([TypeSafe AI][1])

---

# 5. The confidence is actually a big deal

This is arguably more important than the speed.

Imagine:

```text
fraud = 0.99
```

versus:

```text
fraud = 0.51
```

Your application can do:

```python
if fraud > 0.95:
    block()
elif fraud > 0.70:
    human_review()
else:
    allow()
```

So instead of:

```text
AI → decision
```

you have:

```text
AI → probability
          ↓
       software
          ↓
       decision
```

That's a much more composable architecture.

TypeSafe specifically trains Jev using **Reinforcement Learning for Calibrated Decisions (RLCD)**, where the objective is calibrated probabilities rather than merely producing answers humans prefer. ([TypeSafe AI][1])

---

# 6. “Zero hallucinations” needs an important qualification

Their statement is technically interesting but easy to misunderstand.

They don't mean:

> Jev can never make a wrong decision.

They mean something closer to:

> **Jev cannot hallucinate an output outside the allowed type/schema.**

If your schema is:

```text
{
    route: "sales" | "support" | "fraud"
}
```

the model can't suddenly output:

```text
"route": "banana"
```

or generate 500 words of irrelevant prose.

TypeSafe says this is mathematically guaranteed by the constrained output space. ([TypeSafe AI][1])

But:

```text
type-safe ≠ correct
```

This distinction is crucial.

It can still produce:

```text
route = fraud
confidence = 0.93
```

when the correct answer was support.

That's a **model error**, not a type error.

---

# 7. The architecture is actually quite beautiful

You can think of a future agent like this:

```text
                   ┌──────────────┐
user/event ───────>│    Jev       │
                   │ intelligence │
                   └──────┬───────┘
                          │
                 typed probabilities
                          │
                          ▼
                   ┌──────────────┐
                   │ normal code  │
                   └──────┬───────┘
                          │
             ┌────────────┼────────────┐
             ▼            ▼            ▼
          tool A       tool B       human
```

This is very different from:

```text
user
 ↓
LLM
 ↓
LLM decides what to do
 ↓
tool call
 ↓
LLM interprets result
 ↓
...
```

The second architecture gives the LLM much more freedom.

The first architecture gives **the programmer control over the state machine**, while AI supplies the fuzzy judgment.

That's why TypeSafe calls them **“smart if-statements.”** ([TypeSafe AI][1])

---

# 8. Why is it potentially 100× cheaper/faster?

Their published numbers are aggressive:

* Jev: **$0.042 / million input tokens**
* reported latency: **70–500 ms**
* their workflow benchmark claims up to **193.6× faster**
* and **444.6× cheaper** than the compared LLM setup. ([TypeSafe AI][1])

But don't interpret this as:

> “Jev is 400× cheaper than GPT at everything.”

That's **not** what their evaluation demonstrates.

Their advantage comes from restricting the problem:

```text
LLM:
general intelligence
+
text generation
+
reasoning
+
structured output
+
token-by-token decoding

Jev:
decision intelligence
+
fixed output space
+
parallel output
+
calibrated probabilities
```

They are comparing **System-One-shaped workloads**, not arbitrary ChatGPT workloads.

TypeSafe itself acknowledges that its workflow benchmarks were constructed by its model-capabilities team and that the comparisons have methodological limitations. ([TypeSafe AI][1])

---

# 9. This is very relevant to agents

This is the part I'd pay attention to given what you're building.

Today's agent:

```text
LLM
 ↓
reason
 ↓
choose tool
 ↓
generate arguments
 ↓
tool
 ↓
read result
 ↓
reason
 ↓
...
```

A more sophisticated architecture could become:

```text
              ┌─────────────┐
state ───────>│     Jev     │
              └──────┬──────┘
                     │
              probabilities
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
       action A   action B   human
```

And then reserve a powerful autoregressive model for the parts that actually require **generation/reasoning**:

```text
               ┌── Jev ── cheap/fast decisions
agent state ───┤
               └── LLM ── expensive reasoning/generation
```

So instead of calling a $5–10/MTok frontier model for every tiny decision:

```text
"Should I retry?"
"Should I call this tool?"
"Is this result suspicious?"
"Does this output violate policy?"
"Which route?"
"Is confidence sufficient?"
"Should I ask the user?"
```

you can potentially use a specialized decision model.

That is the deeper idea behind System One.

---

## 10. My mental model

I'd summarize the distinction like this:

```text
                 Traditional LLM

   world ──> tokens ──> reasoning ──> tokens ──> world
                    expensive
                    sequential
                    flexible
                    difficult to constrain
```

versus:

```text
                 System One

   world ──> state ──> probabilities ──> program ──> world
                       parallel
                       typed
                       calibrated
                       cheap
```

And the really interesting research question is:

> **How much of “intelligence” actually requires language generation?**

TypeSafe's bet is: **much less than we currently assume.**

Their founder Diogo Almeida describes this as a deliberate departure from the RLHF/chat direction; TypeSafe is building architecture + sampler + RLCD specifically around machine-consumable decisions. ([TypeSafe AI][1])

So I would **not** think of Jev as simply “a smaller LLM.”

Think of it as:

> **a learned probabilistic decision engine that happens to have frontier-model-level capability on a constrained class of problems.**

[TypeSafe's original announcement](https://typesafe.ai/blog/introducing-system-one-models-and-jev?utm_source=chatgpt.com)
[TypeSafe AI homepage](https://typesafe.ai/?utm_source=chatgpt.com)

I can next break down **how Jev could actually be trained from an LLM/RL perspective—especially what RLCD might look like mathematically and why parallel sampling is possible**, which is probably the most interesting technical part.

[1]: https://typesafe.ai/blog/introducing-system-one-models-and-jev "Introducing System One Models & Jev - TypeSafe AI Blog"
