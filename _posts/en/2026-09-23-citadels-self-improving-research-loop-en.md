---
audio: false
generated: true
image: false
lang: en
layout: post
title: Citadel's Self-Improving Research Loop
translated: false
type: note
---

Question: **What is the “self-improving trading machine” Ken Griffin / Citadel has been talking about recently?**

Answer: I think you’re referring to the **agentic AI + quantitative research loop** Griffin described in his 2026 Goldman Sachs interview. He didn’t literally call the system a “self-improving trading machine,” but that is a reasonable shorthand for the idea he was describing.

The interesting part is that **Citadel is not simply using an LLM to predict stock prices**.

### The architecture is closer to this

```text
                    ┌─────────────────────┐
                    │   Market / Papers   │
                    │   Data / Research   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Research Agent    │
                    │                     │
                    │ hypothesize         │
                    │ code                │
                    │ backtest            │
                    │ analyze              │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Evaluator         │
                    │                     │
                    │ OOS tests           │
                    │ risk                │
                    │ costs               │
                    │ statistical tests  │
                    └──────────┬──────────┘
                               │
                         validated result
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Memory / Dataset  │
                    │                     │
                    │ what worked         │
                    │ what failed         │
                    │ under what regime   │
                    └──────────┬──────────┘
                               │
                               └──────► next hypothesis
```

The **self-improvement is in the research loop**, not necessarily in the neural network weights.

Griffin said that Citadel built an agent that could take a finance research paper, **reproduce its methodology, verify the results, and test whether the result continued to hold on data outside the original sample**. Work that traditionally took teams of master's/PhD researchers **6–8 weeks** could reportedly be done in roughly **2–3 hours**. ([Goldman Sachs][1])

That's a much more interesting system than:

```python
prediction = model.predict(market_data)
```

It's more like:

```python
while True:
    hypothesis = researcher.propose(
        data=data,
        previous_results=memory
    )

    implementation = researcher.implement(hypothesis)

    result = evaluator.run(
        implementation,
        train=train,
        validation=validation,
        test=test,
        transaction_costs=costs
    )

    memory.append({
        "hypothesis": hypothesis,
        "implementation": implementation,
        "result": result,
    })
```

Then the next researcher gets the accumulated evidence.

### And Citadel has been doing the non-LLM version for a long time

This is the part that's easy to miss.

Griffin says Citadel has used **machine learning for ~10 years**, including TensorFlow. He has described how engineers adopted TensorFlow extremely quickly and put it into production for U.S. equity quoting. ([Bishop Rock Capital][2])

In his 2026 discussion, he specifically said newer transformer-based models have improved Citadel Securities' ability to **price and manage risk**. ([Goldman Sachs][1])

So the evolution is roughly:

```text
2000s
  │
  ├── human-designed quantitative models
  │
  ▼
2010s
  │
  ├── ML models
  ├── automated feature discovery
  ├── automated pricing
  └── automated risk models
  │
  ▼
2020s
  │
  ├── transformers
  ├── foundation models
  └── LLM-assisted research
  │
  ▼
2026
  │
  ├── agents
  ├── code generation
  ├── autonomous experiment execution
  ├── automated statistical validation
  └── persistent research feedback loop
```

And **that last step is the important one**.

---

## Why this is genuinely “self-improving”

Suppose you give the machine:

```text
Universe: US equities
Data: 20 years
Objective: predict 5-minute returns
```

A normal ML pipeline might be:

```text
data → features → model → prediction → trading
```

An agentic research system can instead do:

```text
          ┌──────────────┐
          │  hypothesis  │
          └──────┬───────┘
                 ↓
          ┌──────────────┐
          │ write code   │
          └──────┬───────┘
                 ↓
          ┌──────────────┐
          │ backtest     │
          └──────┬───────┘
                 ↓
          ┌──────────────┐
          │ diagnose     │
          └──────┬───────┘
                 ↓
          ┌──────────────┐
          │ modify idea  │
          └──────┬───────┘
                 ↓
          ┌──────────────┐
          │ OOS test     │
          └──────┬───────┘
                 ↓
          ┌──────────────┐
          │ record result│
          └──────┬───────┘
                 │
                 └──────────→ next experiment
```

The **optimization target isn't just model loss**.

It can be something like:

$$
J =
\text{Sharpe}
-\lambda_1\text{Turnover}
-\lambda_2\text{Drawdown}
-\lambda_3\text{Costs}
-\lambda_4\text{Complexity}
$$

The agent searches over:

$$
\theta_{t+1}
=
\text{ResearchAgent}
(\theta_t,\;D,\;R_t)
$$

where \\(R_t\\) is the accumulated experimental record.

That's much closer to **automated scientific discovery** than conventional ML.

---

## The really hard part: avoiding fake improvement

This is where finance makes the problem nasty.

If an agent can run 1 million experiments, eventually it will discover:

```text
strategy #837,421
Sharpe = 4.7
```

which is probably bullshit.

You've just created an enormous **multiple-testing / overfitting machine**.

So a serious self-improving trading system needs a hard boundary between:

```text
agent-controlled
────────────────────────
hypothesis
code
features
architecture
hyperparameters
experiment selection
```

and:

```text
evaluator-controlled
────────────────────────
data split
future holdout
transaction costs
risk limits
evaluation metric
execution simulator
```

The agent **must not be able to move the goalposts**.

Interestingly, there is now academic work explicitly exploring this architecture. A 2026 paper called **AQuA** describes “recursively self-improving quantitative trading research agents”: the agents retain validated experimental evidence and use it to guide subsequent proposals, while operating inside sealed evaluation environments with fixed data splits and evaluators. ([arXiv][3])

That's basically the concept you're asking about.

### One important distinction

Don't interpret Griffin as saying:

> “We built AGI that continuously rewrites itself and therefore prints money.”

His actual comments are considerably more grounded.

He has also said that generative AI hasn't yet been revolutionary for much of finance because investing involves predicting a changing future, whereas standard ML is particularly strong when the underlying relationship is relatively stable. He distinguishes short-horizon trading from longer-horizon investing in this respect. ([Bishop Rock Capital][4])

So the near-term thesis is more:

> **AI makes the research/engineering loop dramatically faster → humans and machines can explore a much larger hypothesis space → better models/strategies can emerge.**

rather than:

> **LLM predicts tomorrow's stock price.**

And that's why I think **“self-improving trading research machine”** is actually a better description than “AI trader.”

If you're thinking about building one yourself, the interesting next step is to map this into a **minimal autonomous quant-research loop**—LLM + Python sandbox + backtester + experiment DB + OOS gate—and see exactly where the self-improvement comes from. I can sketch that architecture and a ~200-line prototype.

[1]: https://www.goldmansachs.com/insights/goldman-sachs-exchanges/citadels-ken-griffin-on-ai-us-china-tensions-and-us-data-centers?utm_source=chatgpt.com "Citadel's Ken Griffin on AI, US-China Tensions, and US Data Centers | Goldman Sachs"
[2]: https://www.bishoprockcap.com/assets/library/ken-griffin/May%202026%20Ken%20Griffin%2C%20Founder%20and%20CEO%20of%20Citadel%20-%20In%20Good%20Company%20%28NBIM%20Investment%20Conference%202026%20stage%29%20%28transcript%29?utm_source=chatgpt.com "Ken Griffin, Founder and CEO of Citadel - In Good Company (NBIM Investment Conference 2026 stage)"
[3]: https://arxiv.org/abs/2608.12841?utm_source=chatgpt.com "AQuA: Recursively Self-Improving Quantitative Trading Research Agents"
[4]: https://www.bishoprockcap.com/assets/library/ken-griffin/April%202025%20View%20From%20The%20Top%20with%20Ken%20Griffin%2C%20Founder%20and%20CEO%20of%20Citadel%20%28transcript%29?utm_source=chatgpt.com "View From The Top with Ken Griffin, Founder and CEO of Citadel"