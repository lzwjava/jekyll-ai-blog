---
audio: false
generated: true
image: false
lang: en
layout: post
title: Poolside’s Laguna Models Explained
translated: false
type: note
---

Question: **Give me an introduction to Poolside, and explain its models—especially the Laguna family and the six models exposed through OpenRouter.**

Answer:

## 1. What is Poolside?

![Image](https://images.openai.com/static-rsc-4/hD3ea6ogsqShzK5Hr1tEM6OSz74qflDwGaQu89OWACFzApspKGrWZag5SM3ngPifYCv-qX4xWd8N3FXh1mhfFRUgayp-GKFFAU7cx63LTBe8qaXkBzGRhLf3KFpOW1v-tFEcz19ktTNsJhzsrGHkNwC63NR_bKz3X2tLhmfBPvZEZG9FZTlx50OrPMibylSH?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/5SOWVPq0eQDISVMbulCYzUPDwV7loLd606gIZf8OXYeeTAQtNVOwePf6pFJRfNrRc1hVlNTqAVBQIDu3d-SSsOKmnm6dS5jYutsmeCcDY6OQ3RIvfZOqdqdC8mhiggnrOggC2nO6c0AA_azsXDE_AQlaVnTeP2WulicnWw68Bhf04g0KERxaclnRN1h8YU_i?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/rsWvNIdAxUduXGkjdHMzpwHImJkLKEk5mq0MnK93EQxOnL-SwE7sseLbWX5yFVEaOmPP2oe3sgbjPOA6e7RzpwQjjGwLyRN5MLm7darWdCIOy49WYvigA93fVMEUQQVUBrGLl9S-tzuzk-8u35t_wv9R-WyevEfbtr9i8u5kkvDAYZ43TYGLAnXsptlSHprj?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/_k945JzwC-EUxJXdKEH0SjRnvTm0xyl6UdR3p1H0UVJq4njJsC0BrEJvuGIqgg083RtXUvnyYD6MF34otGazwE7H9l5Tr4M5039I1Free4z76kRlXyBsM11WWc3MOojG4bsWLgb5cQKkUOOnrOktxoplmhObQgeFuUivl6efcYfodJ-lFpiUsADswBZ-gsAz?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/qy54kQT6hcRpJvf9XPvxz-UuIJT3PcAobgjD4U8NOzu49RpAD03YyM7uBrifEKqBI2dg9ezGF2okAq8yn4_n85xUL1-zD2_8EuCYnPiyDxJtTPXWuxGDQKNtf2OpAKIVQZaaHI86rMZS6Gt3jmLwnEnkhZsVgEC50bxwj4eLagCy9o_tSkkHajO8Zg1b-u3j?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/NO4Yt8WygaXYdZ2VKtq-Wgabl6nWBp62VDODbA4iVI4bGpKd9ZiRY8sJM4fgkKyqKvtV28r-hjSRuMUWRL8Z8YTCuytHnuVKo8b0BTREpYLXr7LjJwTotxgCOlf18vWoFVPj0gI2cHvSE-vnljTx326qB09vdshW2N3QoOiTNtSVo56IXZCXo0Vp5KZMZSRa?purpose=fullsize)

Poolside is an AI company founded in 2023 by **Jason Warner**, former CTO of GitHub, and **Eiso Kant**, previously founder/CEO of Athenian. Their thesis is unusually focused:

> **Use software engineering as the path toward increasingly general AI capabilities.**

Rather than starting with a general chatbot and adding coding capabilities, Poolside is building **foundation models specifically around software-engineering agents**.

The company raised **$500M Series B in October 2024**, bringing reported total funding to about **$626M** at the time, with investors including Bain Capital Ventures, Nvidia, eBay Ventures, Felicis and Redpoint. ([TechCrunch][1])

The interesting part for you is the architecture of their strategy:

```text
                         Poolside
                            │
              ┌─────────────┴─────────────┐
              │                           │
        Foundation models           Agent runtime
              │                           │
          Laguna family                  pool
              │                           │
      ┌───────┼────────┐                  │
      │       │        │                  │
     S.2.1   M.1     XS.2.1        long-horizon coding
      │       │        │
      └───────┴────────┘
              │
       code + terminal + tools
              │
        RL from execution
```

Poolside explicitly says its models are trained **from scratch**, using its own data, infrastructure and reinforcement learning. Its models are trained inside its agent harness rather than simply optimizing next-token prediction on code. ([Poolside][2])

That distinction matters.

---

# 2. The core idea: coding as an agent environment

Poolside isn't really optimizing for:

```text
prompt → code completion
```

It's optimizing more for:

```text
goal
 ↓
reason
 ↓
inspect repository
 ↓
modify files
 ↓
run compiler/tests
 ↓
observe failure
 ↓
reason again
 ↓
modify
 ↓
repeat
```

This is why their benchmark choices are heavily agentic:

* Terminal-Bench
* SWE-bench
* DeepSWE
* SWE-bench Multilingual
* SWE-bench Pro
* Toolathlon

Poolside says its Laguna models are trained with reinforcement learning **inside its agent harness**, and their evaluations use up to hundreds of interaction steps rather than treating coding as a single completion. ([Poolside][2])

For an agent builder, that's probably the most important thing to understand about Poolside.

---

# 3. The six models on OpenRouter

As of September 2026, OpenRouter exposes six Poolside models:

| Model                  | Params | Active |   Context |       Input / Output | Main idea                 |
| ---------------------- | -----: | -----: | --------: | -------------------: | ------------------------- |
| **Laguna S 2.1**       |   118B |     8B | **1.05M** | $0.09 / $0.18 per 1M | flagship                  |
| **Laguna S 2.1 free**  |   118B |     8B |      262K |                 Free | same model, free endpoint |
| **Laguna XS 2.1**      |    33B |     3B |      262K | $0.06 / $0.12 per 1M | fast / cheap              |
| **Laguna XS 2.1 free** |    33B |     3B |      262K |                 Free | free XS                   |
| **Laguna XS.2**        |    33B |     3B |      262K |                    — | previous XS generation    |
| **Laguna M.1**         |   225B |    23B |      262K |                    — | previous flagship         |

OpenRouter currently lists these six models and their context/pricing information. ([OpenRouter][3])

One subtle point: **"118B" does not mean 118B parameters are executed per token.**

Laguna S 2.1 is MoE:

```text
118B total parameters
       │
       ├── expert 1
       ├── expert 2
       ├── expert 3
       ├── ...
       └── expert N
             │
          router
             │
       ~8B activated
             │
           token
```

So the inference compute is much closer to an ~8B-active model than a dense 118B model.

Likewise:

```text
Laguna XS 2.1
33B total
3B active
```

Poolside trained S 2.1 on **30T tokens** and XS 2.1 on **15T tokens** according to its model documentation. ([Poolside][2])

---

# 4. Laguna S 2.1

This is the model I'd pay the most attention to.

**Architecture**

```text
118B total
8B active
MoE
30T training tokens
1,048,576 context
```

Poolside describes it as its strongest model for **agentic coding and long-horizon work**. ([Poolside][2])

OpenRouter currently reports:

```text
Input:  $0.09 / 1M tokens
Output: $0.18 / 1M tokens
Context: 1.05M
```

and reports:

```text
Terminal-Bench 2.1    70.2%
DeepSWE                40.4%
```

for the model. ([OpenRouter][3])

The interesting thing isn't merely the benchmark score.

It's this combination:

```text
118B total
8B active
+
1M context
+
agentic coding
+
open weights
+
$0.09/M input
```

That's a pretty unusual point in the model-design space.

---

# 5. Laguna XS 2.1

This is arguably the more interesting engineering model.

```text
33B total
3B active
256K context
up to 32K output
```

Poolside calls it its **lightest and fastest agentic coding model**. ([Poolside][4])

The model was released July 2, 2026 and improved substantially over XS.2, particularly on multilingual software engineering. Poolside reports SWE-bench Multilingual increasing by **5.4 points to 63.1%**. ([Poolside][4])

The paid OpenRouter endpoint is currently:

```text
input:       $0.06 / 1M
output:      $0.12 / 1M
cache-read:  $0.03 / 1M
```

with a 262,144-token context window and 32,768-token maximum completion. ([OpenRouter][5])

So conceptually:

```text
                 Laguna S 2.1
                      │
              maximum capability
                      │
                 118B / 8B
                      │
                   1M ctx
                      │
                      ▼
             complex long-horizon
                  agents


                 Laguna XS 2.1
                      │
                 efficiency
                      │
                  33B / 3B
                      │
                  256K ctx
                      │
                      ▼
             cheap / fast agents
```

That's a very sensible model family.

---

# 6. What happened to M.1 and XS.2?

These are the previous generation.

### Laguna M.1

```text
225B total
23B active
256K context
```

It was Poolside's original flagship model in the Laguna family. Poolside released it in April 2026. ([Poolside][6])

### Laguna XS.2

```text
33B total
3B active
256K context
```

This was the original small model.

It was especially notable because Poolside released its weights openly under **Apache 2.0**. ([Poolside][6])

XS 2.1 is essentially the next iteration of that line, with Poolside moving to the **OpenMDW-1.1** license. ([Poolside][7])

So the evolution looks roughly like:

```text
             2026

       M.1 ────────────────┐
       225B / 23B          │
                           │
                           ▼
                    Laguna S 2.1
                    118B / 8B
                    1M context


       XS.2 ───────────────┐
       33B / 3B            │
                           ▼
                    Laguna XS 2.1
                    33B / 3B
                    256K context
```

The really interesting optimization is that **S 2.1 is smaller than M.1 in total parameters while apparently becoming Poolside's flagship**.

That tells you Poolside is trying to get much more capability per unit of inference compute through architecture + data + RL rather than simply scaling parameter count.

---

# 7. Why Poolside is technically interesting

There are three things I'd watch.

### ① RL is central, not decoration

Their public description is basically:

```text
pretraining
    ↓
synthetic/code data
    ↓
agent environment
    ↓
execute code
    ↓
observe outcome
    ↓
RL
    ↓
better agent trajectories
```

That's a fundamentally different optimization target from:

```text
code corpus → next-token loss
```

Poolside explicitly describes reinforcement learning from code execution at scale as part of its Model Factory. ([Poolside][2])

---

### ② MoE gives them an interesting cost curve

Compare:

```text
Laguna S 2.1
118B total → 8B active

Laguna XS 2.1
33B total → 3B active
```

The model has a large latent capacity but only activates a small subset per token.

That's particularly attractive for coding agents because an agent may generate **tens of thousands of tokens** across a long trajectory.

Inference cost matters enormously.

---

### ③ They're building the model and the agent runtime together

Poolside's `pool` runtime isn't just a shell around an LLM.

Their own description is:

```text
Laguna
  +
agent harness
  +
terminal
  +
file operations
  +
execution feedback
  +
RL
```

They say Laguna models perform best inside `pool`, their own coding-agent environment, although the models can also be used through OpenAI-compatible APIs and other ACP clients. ([Poolside][2])

This is similar to the broader shift we're seeing from:

```text
LLM company
```

toward:

```text
model
+
runtime
+
tools
+
environment
+
RL
+
agent product
```

---

# 8. OpenRouter makes experimentation ridiculously easy

You can use the same OpenAI SDK and swap models.

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="<PLACEHOLDER>",
)

r = client.chat.completions.create(
    model="poolside/laguna-s-2.1",
    messages=[
        {
            "role": "user",
            "content": "Inspect this repository and identify the race conditions."
        }
    ],
)

print(r.choices[0].message.content)
```

Then benchmark the same agent with:

```python
models = [
    "poolside/laguna-s-2.1",
    "poolside/laguna-s-2.1:free",
    "poolside/laguna-xs-2.1",
    "poolside/laguna-xs-2.1:free",
]
```

OpenRouter exposes all of them behind the same OpenAI-compatible API. ([OpenRouter][3])

One caveat with the free endpoints: OpenRouter explicitly notes that **Poolside may use inputs and outputs from free usage to train/improve its models**. ([OpenRouter][8])

---

# 9. My mental model of Poolside

If I compress the company into one diagram:

```text
                    Poolside
                       │
          "AGI through software"
                       │
                       ▼
              Software agents
                       │
             ┌─────────┴─────────┐
             │                   │
         Foundation           Environment
           models                 │
             │                 pool / ACP
       ┌─────┴─────┐              │
       │           │              │
   Laguna S      Laguna XS        │
   118B/8B       33B/3B           │
       │           │              │
       └─────┬─────┘              │
             │                    │
             └────────┬───────────┘
                      │
                 code execution
                      │
                      ▼
                      RL
                      │
                      └──────→ better agents
```

And that is why I wouldn't categorize Poolside as simply **"another open-weight LLM company."**

Their more interesting bet is:

> **software engineering is a sufficiently rich environment to train increasingly capable reasoning agents.**

The Laguna models are the model component of that bet.

As of now, **S 2.1 is the flagship 1M-context model**, while **XS 2.1 is the compact 33B/3B model aimed at high-throughput/local/rapid agentic coding**. OpenRouter gives you a very cheap way to experimentally compare the two. ([Poolside][2])

References:

* [Poolside Models](https://www.poolside.ai/models?utm_source=chatgpt.com)
* [Poolside — Laguna XS 2.1 announcement](https://www.poolside.ai/blog/introducing-laguna-xs-2-1?utm_source=chatgpt.com)
* [OpenRouter — Poolside models](https://openrouter.ai/poolside?utm_source=chatgpt.com)
* [OpenRouter — Laguna XS 2.1](https://openrouter.ai/poolside/laguna-xs-2.1-20260625?utm_source=chatgpt.com)
* [Poolside — $500M fundraise](https://www.poolside.ai/blog/announcing-our-500-million-fundraise-to-make-progress-towards-agi?utm_source=chatgpt.com)
* [TechCrunch — Poolside $500M funding](https://techcrunch.com/2024/10/02/ai-coding-startup-poolside-raises-500m-from-ebay-nvidia-and-others/?utm_source=chatgpt.com)

I can also build a **Poolside vs DeepSeek vs Qwen vs GLM vs Kimi coding-agent architecture comparison**, including active params, training tokens, RL setup, context, and inference economics.

[1]: https://techcrunch.com/2024/10/02/ai-coding-startup-poolside-raises-500m-from-ebay-nvidia-and-others/?utm_source=chatgpt.com "AI coding startup Poolside raises $500M from eBay, Nvidia, and others | TechCrunch"
[2]: https://www.poolside.ai/models?utm_source=chatgpt.com "Models — Poolside"
[3]: https://openrouter.ai/poolside "poolside API and Models | OpenRouter"
[4]: https://www.poolside.ai/blog/introducing-laguna-xs-2-1?utm_source=chatgpt.com "Introducing Laguna XS 2.1 — Poolside"
[5]: https://openrouter.ai/poolside/laguna-xs-2.1-20260625?utm_source=chatgpt.com "Laguna XS 2.1 - API Pricing & Providers | OpenRouter"
[6]: https://poolside.ai/blog/introducing-laguna-xs2-m1?utm_source=chatgpt.com "Introducing Laguna XS.2 and Laguna M.1 — Poolside"
[7]: https://poolside.ai/blog/introducing-laguna-xs-2-1?utm_source=chatgpt.com "Introducing Laguna XS 2.1 — Poolside"
[8]: https://openrouter.ai/poolside/laguna-s-2.1-20260720%3Afree?utm_source=chatgpt.com "Laguna S 2.1 (free) - API Pricing & Providers | OpenRouter"
