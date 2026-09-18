---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Jev: Selection Decision Model"
translated: false
type: note
---

Question: **Intro to the Jev model — the model designed for selection/decision-making**

Answer:

![Image](https://images.openai.com/static-rsc-4/5kqEB-_tozfNOxCG5znnHmqUzK3eVZlPTZYMFzj-iEZ60reqAn8jgucSyQOY67dUroTlTFtatsaqS8xhGWNxnhwLQ_CnfjdSPSy9Uu0C7C3NOTItAFJE_P_2pB2F421mFgNSfiZjQSz9Abh6tqI1ndMLjpkYCHZvjxdgpbnwyJb2r_FUYXwElq73ZXS95Aob?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/AYuVQENzmsodM4geyodKL7q2IsXjw22GtLZG9YRuNZu3LmS6zdrPfRbcuggqGJn3j7PmaSbdHv01mS3sFkATv2ozn1S9anmsFftkrE_5KsIC7uO8BEPiyJrxaT96XM_SPvGecvlbah6SsvWPNiwweM8u09A30YZgPBrI1NJv5TgcANJYnkBh5SnuHiptSQ10?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/PF0HiFKxeBoSoUuOMLYq6lO7IXGlDKUR6Rnt3969j9XAczDGSIWCX_5byQg_jTpx61vKijKUotfDYMGTASOAq5FDXNTwMvMl1yhvfZDSrIlGc-BC9ti6-4qtKg0OUPdlvE5OSgP4e3alS3nnrOJ-RNm2yurcEvb9uyKY9jU95ODE6LJOnyE8J_O9RbQ_Q1gw?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/hCOxyL2LG8fc_mflbvN7D3zqHPv2EVEnhc4vDXzXT3wE1-FaJgZNxLNLUYtRsMYcoSl1xN0xDEXu2_sx-r4rmY_FifM42YZCc1YZIPl3XRuH471S4E_UnxKw_Le5HJsKYf_fOCXfFxB5B70fgVhBU4JrMFZNvB8SGIxa6sY9WGM2FoQGWZZ-pvp1Y7EDWR2T?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/olx9xVOMIm9iBLyhsyYJfQ8F2JUh03zD-R6Lxy0BJikTRdpzo8vkw2xrj-hdchknFJgWLE1IvZ7R5RIPbBgPelBgA0xK_-UBsYWeyXlmOcJF0G0ETK8f-EqkTvDOcjwb59SgtBJVTShCskABd3Q0x0MalY1v0vR2OnKXDZHw-XzPzROLWk0v4ftKmAvOXmkQ?purpose=fullsize)

**Jev is a new kind of model from TypeSafe AI whose job is not to generate text, but to make small, structured decisions.** It was announced in September 2026 and is called a **“System One” model** by TypeSafe. ([System One Models][1])

The key idea is:

> **LLM:** `prompt → generated tokens`
> **Jev:** `state + question → decision + probability`

### 1. The problem it solves

Suppose your agent has 50 tools:

```text
user request
     │
     ▼
┌───────────────┐
│   LLM         │
│ "which tool?" │
└───────┬───────┘
        │
        ▼
   tool selection
```

You're using a powerful generative model to answer something that is fundamentally a **classification problem**.

For example:

```text
Input:
"Find all unread emails from yesterday."

Options:
  gmail_search
  github_search
  shell
  browser
  calendar

Output:
  gmail_search
```

Jev is designed specifically for this kind of decision. ([Jev Agent][2])

---

## 2. Jev's basic abstraction

Think of it as:

```python
decision = jev(
    state=state,
    question=question,
)
```

where:

```python
state = """
User wants to find all unread emails from yesterday.
"""

question = Choice(
    "Which tool should handle this request?",
    criteria={
        "gmail": "Search and retrieve email",
        "github": "Search GitHub repositories",
        "shell": "Execute local shell commands",
        "browser": "Browse arbitrary websites",
    }
)
```

Conceptually:

```text
                  state
                    │
                    ▼
             ┌───────────┐
             │    Jev    │
             └─────┬─────┘
                   │
       ┌───────────┼───────────┐
       ▼           ▼           ▼
    gmail       github       shell
     0.93        0.02        0.01
```

The application gets a **typed decision**, rather than a string that it needs to parse. ([System One Models][3])

---

# 3. Three important primitives

Jev currently exposes three major kinds of questions.

### Choice

**"Which one?"**

```text
Which model should handle this request?

A. small
B. medium
C. frontier
```

Output is essentially:

```json
{
  "choice": "medium",
  "probabilities": {
    "small": 0.12,
    "medium": 0.81,
    "frontier": 0.07
  }
}
```

This is the most obvious use for **model selection / routing**. ([System One Models][3])

### Score

**"Where does this fall on an ordered scale?"**

For example:

```text
How difficult is this coding task?

1 = trivial
2 = simple
3 = moderate
4 = difficult
5 = extremely difficult
```

Then your application can route:

```python
if score < 2.5:
    use_small_model()
else:
    use_frontier_model()
```

### Noul

**"Is this statement true?"**

For example:

```text
Does this request require human review?
```

Output:

```text
P(yes) = 0.87
```

This is useful for gates:

```python
if p_human_review > 0.8:
    escalate()
```

The important distinction is that the **application owns the threshold**; Jev provides the probability rather than deciding your business policy for you. ([AutoJev][4])

---

# 4. Why this is interesting for agents

This is probably the most interesting part for you.

A modern agent has lots of tiny decisions:

```text
                 Agent state
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
       Which tool?  How risky?  Which model?
          │           │           │
          ▼           ▼           ▼
         Jev         Jev         Jev
          │           │           │
          ▼           ▼           ▼
       Tool A       0.12        Haiku
```

The expensive generative model then concentrates on the genuinely generative work:

```text
                  ┌──────────────┐
                  │     Jev      │
                  │  decisions   │
                  └──────┬───────┘
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
           routing     safety     grading
              │          │          │
              └──────────┼──────────┘
                         ▼
                  ┌──────────────┐
                  │ Frontier LLM │
                  │ generation   │
                  └──────────────┘
```

That's the architectural idea: **don't use a generative LLM for every decision inside an agent.** ([Jev Agent][2])

---

# 5. Jev for model selection

This is exactly where the name "model to select" becomes interesting.

Imagine you have:

```python
models = {
    "cheap": "small-fast-model",
    "normal": "medium-model",
    "hard": "frontier-model",
}
```

Instead of:

```python
router_llm("Which model should I use?")
```

you can formulate:

```text
STATE:
    user request

QUESTION:
    Which approved model should answer this?

OPTIONS:
    cheap
    normal
    hard
```

Then:

```text
                    User request
                         │
                         ▼
                       Jev
                         │
             ┌───────────┼───────────┐
             ▼           ▼           ▼
           cheap       normal       hard
           0.61         0.31        0.08
             │
             ▼
       cheap model
```

This creates a **model cascade**:

```text
             request
                │
                ▼
              Jev
                │
       ┌────────┴────────┐
       │                 │
    easy/cheap          hard
       │                 │
       ▼                 ▼
   cheap LLM         frontier LLM
```

The router itself needs to be extremely cheap, otherwise you destroy the economics of routing. This is one of the use cases proposed for Jev. ([Jev Agent][5])

---

# 6. Jev vs a normal LLM

The conceptual difference is quite deep.

A normal autoregressive LLM does:

```text
x
↓
hidden states
↓
next-token distribution
↓
token
↓
next-token distribution
↓
token
↓
...
↓
"Use model B because..."
```

Jev instead aims for something closer to:

```text
state
  ↓
representation
  ↓
decision distribution
  ↓
Choice / Score / Noul
```

So if your application needs:

```text
"Write a Python program"
```

use an LLM.

If it needs:

```text
"Which Python tool should I call?"
```

Jev is the type of model being proposed for that job.

This is why TypeSafe describes it as **System One** rather than another general-purpose chat model. ([WorkerKit][6])

---

# 7. The really important distinction

Don't think:

> **Jev = better LLM**

Think:

> **Jev = a specialized learned decision function sitting underneath an LLM/agent.**

Your stack could become:

```text
                    ┌────────────────────┐
                    │   Application      │
                    └─────────┬──────────┘
                              │
                  ┌───────────┴───────────┐
                  │                       │
                  ▼                       ▼
             ┌─────────┐            ┌───────────┐
             │   Jev   │            │    LLM    │
             │ decision│            │ generation│
             └────┬────┘            └─────┬─────┘
                  │                       │
          ┌───────┼────────┐              │
          ▼       ▼        ▼              ▼
        route    gate     score       text/code/tool args
```

That separation is the interesting idea.

There is also an important limitation: **bounded output does not mean the judgment is necessarily correct.** A classifier can only select from your allowed choices, but it can still choose the wrong choice. Independent discussion of Jev has also noted that some published accuracy figures are based on agreement with other LLMs rather than an objective ground truth. ([Progressive Robot][7])

For someone building **agent harnesses**, I'd pay particular attention to Jev as a possible **router / verifier / tool selector**, rather than treating it as a replacement for GPT/Claude-style generation.

References:

* [TypeSafe AI — Jev overview](https://typesafe.ai/?utm_source=chatgpt.com)
* [Jev model explanation](https://systemonemodels.org/models/jev/?utm_source=chatgpt.com)
* [Jev for LLM model routing](https://jev-agent.com/use-cases/llm-model-routing?utm_source=chatgpt.com)
* [Jev for agent tool selection](https://jev-agent.com/use-cases/agent-tool-selection?utm_source=chatgpt.com)

I can next show you how **Jev could replace the model-selection/router layer inside a `ww`/`iclaw`-style agent**, with a minimal Python implementation.

[1]: https://systemonemodels.org/guides/jev-explained/?utm_source=chatgpt.com "Jev explained: TypeSafe AI's decision model | System One Models"
[2]: https://jev-agent.com/use-cases/agent-tool-selection?utm_source=chatgpt.com "Jev for agent tool selection — pick from 100 tools | Jev Agent"
[3]: https://systemonemodels.org/models/jev/?utm_source=chatgpt.com "Jev AI model: specs, pricing and use cases | System One Models"
[4]: https://autojev.ai/jev-model?utm_source=chatgpt.com "Jev Model Guide: Inputs, Outputs and Best Use Cases"
[5]: https://jev-agent.com/use-cases/llm-model-routing?utm_source=chatgpt.com "Jev for LLM routing — pick the cheap model first | Jev Agent"
[6]: https://workerkit.ai/blog/jev-and-decision-models?utm_source=chatgpt.com "Jev: TypeSafe's System One model explained - WorkerKit"
[7]: https://www.progressiverobot.com/2026/09/16/jev-model-typesafe-programmatic-logic/?utm_source=chatgpt.com "Jev Model: Proven Speed, Smart Logic Without a Chatbot"
