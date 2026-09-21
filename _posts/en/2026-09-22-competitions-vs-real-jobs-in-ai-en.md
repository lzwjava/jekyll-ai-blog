---
audio: false
generated: true
image: false
lang: en
layout: post
title: Competitions vs Real Jobs in AI
translated: false
type: note
---

Question: **If AI can heavily assist Codeforces/Kaggle, what actually remains hard in real jobs—and which credentials/competitions still signal ability?**

Answer:

The key distinction is:

> **Competitions measure “can you solve a well-defined problem under controlled constraints?” Real jobs measure “can you discover, own, and ship the right problem despite ambiguity?”**

AI makes the first category cheaper. It arguably makes the second category **more important**, not less.

### 1. What AI destroys first

A lot of traditional skill signals are becoming weaker:

| Signal                              | AI impact |
| ----------------------------------- | --------- |
| LeetCode/Codeforces problem solving | High      |
| Boilerplate coding                  | Very high |
| Syntax/API knowledge                | Very high |
| Kaggle feature engineering          | High      |
| Take-home implementation            | High      |
| “I know React/PyTorch/K8s”          | High      |
| Memorized algorithms                | High      |

This doesn't mean these skills become useless. It means **the correlation between the skill and the ability to produce software is weaker**.

Codeforces itself has already responded: its current rules explicitly prohibit using AI to generate core algorithms, reason through problems, or debug rejected solutions during rated contests. ([Codeforces][1])

That's basically an admission of the fundamental issue: **if the model is allowed to do the reasoning, the contest no longer measures the intended human capability.**

---

# 2. What becomes harder in real life

There are several layers that AI doesn't eliminate.

### A. Problem selection

Real job:

> “Our inference cost is too high.”

This is not:

```text
input → algorithm → output
```

You have to discover:

```text
Why is it expensive?
What does "too high" mean?
Which users are affected?
Can we tolerate latency?
Can we cache?
Should we distill?
Should we change the model?
Should we change the product?
Is this even the bottleneck?
```

A great engineer might discover:

> Don't optimize inference. The real problem is that we're calling the model 47 times per request.

That is much harder to benchmark with a static problem statement.

---

### B. System ownership

An AI can generate:

```python
async def foo():
    ...
```

But production asks:

```text
Who owns this service?
What happens when Redis dies?
What's the rollback procedure?
Why did latency go from p95 300ms → 4s?
Why did GPU utilization collapse?
Why is the database bill $80k/month?
Why did this migration corrupt 0.1% of users?
```

The difficult unit is no longer **a function**.

It's:

> **a system + its state + its users + its failure modes + its economics.**

---

### C. Verification

This is probably the biggest AI-era engineering skill.

LLM:

```text
"Here is a great solution."
```

Engineer:

```text
prove it
benchmark it
red-team it
inspect the generated code
find counterexamples
measure production behavior
```

The asymmetry is interesting:

> **Generation gets cheap; verification becomes expensive.**

This is already very visible in AI engineering.

If I ask an agent to modify a 100k-line repository, generating the patch isn't particularly impressive.

The hard part is knowing whether the patch is **actually correct**.

---

### D. Taste

Suppose an agent gives you 10 architectures:

```text
Kafka + Flink
Postgres + workers
Redis streams
Temporal
Ray
serverless
...
```

Someone still has to decide:

> Which one should we build?

That's not pure algorithmic competence.

It's accumulated understanding of:

* failure modes
* operational complexity
* team capability
* latency
* cost
* future requirements
* product constraints
* organizational constraints

This is why experienced engineers can still be dramatically more productive than inexperienced engineers **even when both have exactly the same AI tools**.

---

# 3. So are offline competitions useful?

**Yes—but for a very specific reason.**

ICPC is actually a fascinating credential in the AI era because it creates an environment where the model is deliberately removed from the loop.

The 2026 ICPC rules give each team **one workstation shared among the team**, and prohibit contestants from bringing their own computers/electronic devices into the contest area. ([ICPC Global][2])

The point isn't that ICPC resembles a software job.

It doesn't.

The value is that it gives a relatively clean measurement of:

```text
human reasoning
+
algorithmic knowledge
+
implementation under pressure
+
team communication
+
debugging
+
time management
```

And because the environment is controlled, the credential remains interpretable.

That's fundamentally different from:

> “I got 98th percentile on an online coding platform.”

---

# 4. The interesting credential hierarchy is changing

I'd roughly think about credentials as **evidence**, not prestige.

### Strong evidence of raw technical reasoning

```text
ICPC World Finals / Regional
IMO / IOI / similar olympiad-level results
Top-tier research results
```

ICPC explicitly describes its purpose around teamwork, programming and problem-solving ability. ([ICPC][3])

These are unusually difficult for AI to fake **when the competition itself excludes AI assistance**.

---

### Strong evidence of ML ability

Kaggle can still be useful, but there's a huge caveat:

**Kaggle is becoming heterogeneous.**

Some competitions permit AI/automated ML; others explicitly prohibit generative AI. For example, current Kaggle competitions can have rules allowing GPT/Claude/Gemini with disclosure, while other competitions explicitly prohibit LLM use. ([Kaggle][4])

So:

```text
"Kaggle Master"
```

doesn't tell the whole story anymore.

A much better signal is:

```text
Kaggle result
+ competition
+ rules
+ writeup
+ code
+ reproducibility
```

---

# 5. But there's an even stronger credential: shipped things

For someone actually hiring an engineer, this can be much more informative:

```text
GitHub repo
       ↓
real users
       ↓
real traffic
       ↓
real failures
       ↓
real revenue / impact
       ↓
you can explain every design decision
```

For example:

> “I built an inference service handling 2B tokens/month.”

is a much more interesting interview starting point than:

> “I solved 2,000 LeetCode problems.”

Because now the interviewer can ask:

```text
Why this architecture?
What was the bottleneck?
What broke?
How much did it cost?
What did you measure?
Why didn't you use X?
What would you change at 10x traffic?
```

And you either know—or you don't.

AI can't conveniently hide that gap because the interviewer can keep drilling into the system.

---

# 6. This produces a new kind of interview

I suspect the future technical interview becomes less:

```text
"Implement LRU cache."
```

and more:

```text
Here's a broken production system.

Here are:
  logs
  traces
  metrics
  source code
  customer complaints

Find the problem.

Then:

  propose a fix
  implement it
  benchmark it
  explain tradeoffs
```

Or:

```text
Here's an agent.

It passes 80% of our tests.

Get it to 98%.

You have 4 hours.
```

Or:

```text
Here's a 500k-line repository.

Add feature X.

You may use any AI tools.

We will evaluate:
  correctness
  regression rate
  tests
  architecture
  security
  performance
  explanation
```

That is much closer to actual work.

---

# 7. The weird consequence

AI doesn't necessarily make **elite humans less valuable**.

It can make the distribution more extreme.

Imagine two engineers:

```text
Engineer A:
  reasoning: 5
  coding:    8
  AI usage:  5

Engineer B:
  reasoning: 9
  coding:    7
  AI usage:  9
```

After AI:

```text
A → can produce a lot more code

B → can produce a lot more systems
```

Because B can:

```text
decompose
→ delegate to agents
→ inspect
→ reject
→ redesign
→ test
→ iterate
→ ship
```

The bottleneck moves upward.

From:

> **“Can you write the code?”**

to:

> **“Can you direct a large amount of computation toward the correct objective?”**

That's much closer to the role of an AI-native engineer.

---

# 8. So what should you actually optimize for?

I'd build a portfolio with **three orthogonal signals**:

```text
              Human reasoning
                    ↑
                    │
              ICPC / olympiad
                    │
                    │
                    │
Real-world ←────────┼────────→ AI-native
systems             │            execution
                    │
              shipped products
                    │
                    ↓
              revenue / users
```

You don't need every credential.

A particularly strong combination is:

```text
1. One hard offline credential
   ICPC / olympiad / serious research

2. One serious technical artifact
   model / distributed system / compiler / agent framework

3. One undeniable real-world result
   users / revenue / latency / scale / open-source adoption
```

The third one is increasingly important.

**A medal tells me you can solve hard problems.**

**A shipped system tells me you can survive reality.**

**An AI-native system tells me you understand the new leverage.**

And the really interesting people will eventually have all three.

### References

* [ICPC Regional Rules 2026/27](https://icpc.global/regionals/rules?utm_source=chatgpt.com)
* [ICPC World Finals Rules 2026](https://icpc.global/worldfinals/rules%23?utm_source=chatgpt.com)
* [Codeforces AI Rule](https://codeforces.com/page/30?utm_source=chatgpt.com)
* [Kaggle Competition Documentation](https://www.kaggle.com/docs/competitions?lor=19&utm_source=chatgpt.com)

I can also map this into a concrete **2026–2030 “AI-era engineering credential stack”**—ICPC vs Kaggle vs GitHub vs research vs startup/revenue vs open source—and explain what each actually proves.

[1]: https://codeforces.com/page/30?utm_source=chatgpt.com "Codeforces"
[2]: https://wf.icpc.global/2026/about/?utm_source=chatgpt.com "The 2026 ICPC World Finals Dubai hosted by Dubai Chamber of Digital Economy"
[3]: https://icpc.global/regionals/rules?utm_source=chatgpt.com "The ICPC International Collegiate Programming Contest"
[4]: https://www.kaggle.com/competitions/ai-opportunity-discovery-hackathon/rules?utm_source=chatgpt.com "AI Opportunity Discovery Hackathon | Kaggle"
