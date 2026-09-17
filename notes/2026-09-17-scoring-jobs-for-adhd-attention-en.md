---
audio: false
generated: true
image: false
lang: en
layout: post
title: Scoring Jobs for ADHD Attention
translated: false
type: note
---

Question: What kinds of jobs tend to fit someone with ADHD?

Answer: The key variable is **not “ADHD = certain jobs.”** It is whether the job gives you the conditions under which your attention system works well.

For an engineer, jobs often work better when they have:

* **High novelty:** new problems, technologies, customers, incidents.
* **Fast feedback loops:** you can see within hours/days whether your work works.
* **Autonomy:** you decide how to solve the problem rather than following a rigid process.
* **Deep technical problems:** enough complexity to trigger sustained interest.
* **Urgency / real consequences:** deadlines and production problems can provide external activation.
* **Variety:** several projects rather than maintaining the same system for years.
* **Visible ownership:** “this thing is mine” rather than one tiny ticket in a huge organization.
* **Low bureaucracy:** fewer meetings, approvals, status reports, and repetitive administrative work.

For **your particular engineering profile**, I would investigate these directions:

| Work                                   | ADHD-friendly characteristics                          | Potential downside                      |
| -------------------------------------- | ------------------------------------------------------ | --------------------------------------- |
| **LLM/Agent Engineer**                 | Novelty + experimentation + rapid feedback             | Research can become open-ended          |
| **AI Infrastructure Engineer**         | Hard technical problems + debugging + systems thinking | Some maintenance/on-call                |
| **ML Systems / Inference Engineer**    | Performance optimization, GPUs, kernels, serving       | Requires sustained deep work            |
| **AI Consultant / Solutions Engineer** | New customer/problem every few days                    | Context switching                       |
| **Startup Engineer**                   | Huge autonomy + variety + urgency                      | Ambiguity and workload                  |
| **Developer Tools / CLI Engineer**     | Immediate feedback + strong ownership                  | Smaller market                          |
| **GPU repair / hardware engineering**  | Physical feedback + troubleshooting + novel failures   | Business volume can be unpredictable    |
| **SRE / Production Engineering**       | Incidents create strong urgency and feedback           | On-call stress                          |
| **Research Engineer**                  | Novel problems + experimentation                       | Long periods without external deadlines |
| **Traditional enterprise maintenance** | Predictable                                            | Often lots of repetitive work           |

One particularly interesting pattern for you is:

**LLM engineer + consulting + hardware**

rather than trying to find one perfectly optimized job.

For example:

```text
                 AI systems
                    │
        ┌───────────┼───────────┐
        │           │           │
     LLM infra   Agents      GPU/hardware
        │           │           │
     kernels     products    repair/debug
        │           │           │
        └───────────┼───────────┘
                    │
                 Consulting
```

That gives you **problem novelty without requiring you to abandon engineering depth**.

The opposite pattern is worth recognizing too. Jobs involving:

```text
same system
    ↓
same tickets
    ↓
same meetings
    ↓
same approval process
    ↓
same technology
    ↓
repeat for 3 years
```

can be particularly frustrating for someone whose attention is strongly driven by novelty and challenge.

But there is an important distinction: **ADHD-friendly ≠ easy**. A difficult debugging problem can be highly engaging, while an objectively easy task can be almost impossible to start if there is no novelty or urgency.

A useful way to choose work is therefore to score the **job environment**, not the job title:

```python
factors = {
    "novelty": 0.20,
    "autonomy": 0.20,
    "feedback_speed": 0.15,
    "technical_depth": 0.15,
    "urgency": 0.10,
    "variety": 0.10,
    "ownership": 0.10,
}

# Rate each from 1–10 based on the actual job.
fit = sum(factors[k] * rating[k] for k in factors)
```

I'd actually use this on **real job descriptions**, because two companies hiring for “Senior AI Engineer” can have completely opposite day-to-day environments.

I can also take your current background and build a **10-role ADHD/work-style matrix** showing novelty, autonomy, deep-work potential, income ceiling, startup compatibility, and boredom risk.
