---
audio: false
generated: true
image: false
lang: en
layout: post
title: KDD 2027 CFP Scope and Submission Guide
translated: false
type: note
---

Question: **What does the KDD 2027 Research Track CFP actually require, and what should you pay attention to?**

Answer:

I read the official CFP. The important part is that **KDD Research is much broader than classic “data mining.”** The 2027 CFP explicitly includes modern LLM/reasoning work, scalable AI systems, RL, generation, and foundation models. ([KDD 2027][1])

### 1. The scope is very relevant to your work

The CFP explicitly lists:

* **In-context learning**
* **Prompt engineering**
* **Continual learning**
* **Few-shot adaptation**
* **Reinforcement learning**
* **Generation and reasoning**
* **LLMs**
* **Multimodal foundation/frontier models**
* **Emergent reasoning**
* **Neural-symbolic integration**
* **Hypothesis generation**
* **Scalable AI systems / infrastructure**
* Distributed computing
* Scheduling/orchestration
* ML systems

So things like **reasoning models, RL with verifiable rewards, Lean/code-based verification, inference systems, agent systems, training infrastructure**, etc. can absolutely fit the Research Track if there is a genuine research contribution. ([KDD 2027][1])

The key phrase is:

> **“innovative research”**

A paper cannot simply be *“I built an agent using GPT-5 and it works.”* You need a technical idea that advances knowledge.

---

### 2. The biggest constraint: 8-page main paper

The submission is:

```text
PDF
├── 8 pages main paper       <-- reviewers are expected to judge this
├── References
└── Appendix                  <-- unlimited pages
```

The first **8 pages must be self-contained**. The appendix can contain proofs, implementation details, pseudocode, reproducibility material, etc. ([KDD 2027][1])

This is actually a useful way to think about KDD papers:

```text
Problem
   ↓
Observation
   ↓
New idea
   ↓
Method
   ↓
Experiments
   ↓
Evidence
   ↓
Why this changes our understanding
```

You don't get 30 pages to slowly explain the project.

---

### 3. They care about research contribution, not just engineering

Their decision factors include:

```text
technical merit
originality
potential impact
quality of execution
quality of presentation
related work
reproducibility
ethics
```

([KDD 2027][1])

For example, compare:

**Weak research framing**

> We trained a 7B reasoning model with RL and got 5% better performance.

versus:

**Research framing**

> We discover that reward sparsity in verifiable reasoning tasks causes a particular failure mode. We introduce X, which changes the distribution of exploration trajectories in a measurable way. Across N reasoning environments, X improves sample efficiency by Y% and we provide an analysis explaining why.

The second has an actual **scientific claim**.

---

### 4. Your RL + Lean idea fits the scope very naturally

Your previous idea:

```text
LLM
 ↓
generate reasoning / proof / code
 ↓
Lean / compiler / execution
 ↓
verifiable reward
 ↓
RL
 ↓
better reasoning policy
```

is almost literally inside the CFP's listed topics:

```text
reinforcement learning
generation
reasoning
LLMs
neural-symbolic integration
```

([KDD 2027][1])

But the interesting paper isn't:

> "We used Lean as a reward function."

That is already an obvious direction.

The research question needs to be something deeper, e.g.:

```text
Why does verifier-based RL work?

What kind of verifier produces the best learning signal?

How sparse can the verifier reward be?

Does partial proof verification provide better credit assignment?

Can failed proofs be converted into useful dense rewards?

How does verifier feedback change the model's exploration distribution?

Can we predict which generated trajectories are worth RL training on?

What happens when the verifier has different levels of granularity?
```

Those are **research questions**.

---

### 5. There is also a Systems angle

Given your interest in LLM infrastructure, another possible KDD direction is:

```text
Reasoning model
      ↓
trajectory generation
      ↓
verifier
      ↓
reward extraction
      ↓
RL training
```

and optimize the actual system:

```text
GPU utilization
↓
trajectory throughput
↓
verification throughput
↓
KV-cache reuse
↓
distributed rollout
↓
RL training efficiency
```

The CFP explicitly welcomes **systems and infrastructure for large-scale AI**, including distributed computing, orchestration and scheduling. ([KDD 2027][1])

So a paper could potentially be about something like:

> **Efficient Verifier-Guided Reinforcement Learning for Large-Scale Reasoning Models**

where the novelty is actually in the training/rollout/verifier architecture.

---

### 6. Important: KDD doesn't want a survey

The CFP explicitly says survey papers whose purpose is simply to comprehensively summarize an existing topic are **out of scope**. ([KDD 2027][1])

So:

```text
❌ "A Survey of RL for Reasoning Models"

❌ "A Comprehensive Review of Lean + LLM"

❌ "The State of AI Agents in 2027"
```

would not fit the Research Track merely because they're interesting.

But:

```text
✅ new algorithm
✅ new training method
✅ new empirical discovery
✅ new model/system architecture
✅ new theoretical insight
```

can.

---

### 7. Double-blind is strict

Your submission cannot reveal:

```text
author names
affiliations
identifying information
acknowledgements
obvious self-identification
```

They specifically recommend:

```latex
\documentclass[sigconf,anonymous,review]{acmart}
```

([KDD 2027][1])

Interestingly, an anonymized GitHub repository **is allowed and recommended**, although it isn't mandatory. ([KDD 2027][1])

---

### 8. One thing that matters a lot for you: OpenReview profile

Every author needs a sufficiently complete OpenReview profile.

The CFP says missing required profile information can itself lead to **desk rejection**.

Required information includes things like:

```text
current/past affiliations (5 years)
homepage
DBLP
ORCID
advisors
recent publications
```

as applicable. ([KDD 2027][1])

New OpenReview accounts without institutional email can also take **up to two weeks** to be moderated. ([KDD 2027][1])

So if you're seriously targeting KDD, this is something to set up early rather than the week before submission.

---

### 9. Current timeline

For **KDD 2027 Cycle 1**:

| Event        | Date                        |
| ------------ | --------------------------- |
| Abstract     | **July 19, 2026**           |
| Paper        | **July 26, 2026**           |
| Rebuttal     | **Sep 29 – Oct 13, 2026**   |
| Notification | **Nov 14, 2026**            |
| Conference   | **Aug 1–5, 2027, San Jose** |

All submission deadlines are **Anywhere on Earth (AoE)**. ([KDD 2027][1])

Given today's date, **the Cycle 1 paper deadline has already passed**. The CFP says KDD has two submission cycles per year, so the relevant opportunity for a new paper would be the subsequent cycle rather than trying to submit to Cycle 1 now. ([KDD 2027][1])

### 10. The most important distinction

I'd reduce the whole CFP to this:

```text
             KDD Research
                  │
        ┌─────────┴─────────┐
        │                   │
    Engineering          Research
        │                   │
"we built X"          "we discovered X"
        │                   │
benchmark             hypothesis
implementation        mechanism
system                 algorithm
                       evidence
                       analysis
```

For **you**, I would think in terms of:

```text
idea
 ↓
minimal implementation
 ↓
run experiments
 ↓
discover something surprising
 ↓
formulate hypothesis
 ↓
design controlled experiments
 ↓
turn discovery into algorithm
 ↓
write KDD paper
```

rather than:

```text
pick KDD topic
 ↓
build something
 ↓
write paper
```

That first workflow is much more aligned with what this CFP is asking for.

**Official CFP:** [KDD 2027 Research Track — Call for Papers](https://kdd2027.kdd.org/research-track-call-for-papers/?utm_source=chatgpt.com) 

References:

* [KDD 2027 Research Track CFP](https://kdd2027.kdd.org/research-track-call-for-papers/?utm_source=chatgpt.com) 
* [KDD 2027 official site](https://kdd2027.kdd.org/?utm_source=chatgpt.com) 

[1]: https://kdd2027.kdd.org/research-track-call-for-papers/ "Research Track: Call for Papers – KDD 2027"
