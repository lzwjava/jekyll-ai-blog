---
audio: false
generated: true
image: false
lang: en
layout: post
title: OpenAI Millennium Prize Credit Dispute
translated: false
type: note
---

Question: **What’s the story behind OpenAI’s recent Millennium Prize math breakthrough, and is OpenAI “stealing credit”?**

Answer:

Yes — **there is a real credit/independence controversy**, but it is more precise to say **“possible use of unpublished research / questionable research ethics”** than “OpenAI definitely stole the proof.”

### 1. What OpenAI claims

OpenAI announced on September 8, 2026 that an internal AI system had produced a solution to the **Navier–Stokes existence and smoothness problem**, one of the seven Millennium Prize Problems.

The system reportedly:

* used ~**10,000 AI agents**
* ran for about **88 hours**
* consumed **millions of dollars of compute**
* produced a ~**165-page mathematical argument**
* had another AI system formalize/check parts of the argument

The core claim is roughly that **3D Navier–Stokes can develop a finite-time singularity** under the relevant formulation. If mathematically correct, this would be an enormous result. ([The Guardian][1])

But important distinction:

> **OpenAI saying “we solved it” ≠ mathematicians accepting that the Millennium Problem is solved.**

The proof still needs serious independent mathematical scrutiny. ([The Washington Post][2])

---

### 2. Why people are angry about the credit

This is the interesting part.

Two researchers were already working on the problem:

* **Tristan Buckmaster**, NYU mathematician
* **Levent Alpöge**, mathematician/researcher associated with Anthropic

They had been using AI systems including **Claude, Codex and Astra** in their research.

They had apparently made substantial progress and were preparing to publish.

Then OpenAI learned — through rumors — that researchers had made progress on Millennium Prize problems.

OpenAI says it started its serious Navier–Stokes attack around **September 1**.

Buckmaster claims that information about their unpublished work reached OpenAI, after which OpenAI rapidly launched a huge compute campaign and produced its own result. ([TechCrunch][3])

So the suspicious timeline is basically:

```text
Buckmaster + Alpöge
        │
        │ unpublished research
        ▼
   AI-assisted work
        │
        │ information reaches OpenAI?
        ▼
     OpenAI learns
   "they may have solved it"
        │
        ▼
  10,000-agent swarm
        │
        │ ~88 hours
        ▼
 OpenAI's own proof
```

That's why people are asking:

> **Did OpenAI independently solve the problem, or did it discover the direction from somebody else's private research and then use vastly more compute to beat them to publication?**

---

### 3. The particularly uncomfortable part: Codex

This is where the story becomes much more serious.

Buckmaster and Alpöge had apparently put parts of their **unpublished mathematical work into OpenAI's Codex** while using it as a research tool.

Buckmaster therefore worried that OpenAI could potentially have learned something about their research through its own products.

OpenAI says it **did not access their specific private user data** in order to solve the problem.

But OpenAI also reportedly acknowledged something much more nuanced:

> it **cannot completely rule out** that de-identified data from their product usage contributed indirectly to model improvement. ([Axios][4])

That's an important distinction.

There are two very different accusations:

```text
A. "OpenAI engineers opened Buckmaster's private Codex
    session and copied the proof."

       ↓

    OpenAI says NO.


B. "Buckmaster's interaction with OpenAI products
    could have indirectly influenced models that OpenAI
    subsequently used."

       ↓

    OpenAI says it cannot completely rule this out.
```

There is currently **no established evidence that OpenAI literally copied his proof**.

---

### 4. And there is another credit dispute

There was apparently also tension over whether **Alpöge**, who works with Anthropic, should receive credit.

Buckmaster alleges that OpenAI researcher Sébastien Bubeck pushed against crediting Alpöge because of his affiliation with Anthropic.

That's especially awkward because this isn't merely:

> "AI vs humans."

It's:

> **OpenAI vs Anthropic + academic researchers + ownership of unpublished scientific ideas.**

TechCrunch reports Buckmaster's account of this dispute, while OpenAI disputes the broader implication that its result depended on their work. ([TechCrunch][3])

---

### 5. Is this actually "stealing"?

I'd separate **three levels**:

| Situation                                                                                                   | My assessment                              |
| ----------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| OpenAI independently discovers the proof after hearing rumors someone is close                              | **Not stealing**                           |
| OpenAI learns a general research direction from public information and independently solves it              | **Aggressive competition, but legitimate** |
| OpenAI uses unpublished private research from its users to guide its own research without permission/credit | **Serious research-ethics problem**        |
| OpenAI literally copies their proof and publishes it as its own                                             | **Academic plagiarism**                    |

Right now, the evidence publicly available establishes **the controversy**, but **not the strongest version of the plagiarism accusation**.

Nature also reports that OpenAI explicitly launched the effort after hearing rumors that Buckmaster and Alpöge had made progress. ([Nature][5])

---

### 6. But there's a deeper issue here

I think the most interesting thing isn't actually the $1M prize.

It's this:

**What happens when the company that provides your AI research assistant is also capable of competing against you?**

Imagine you're a mathematician:

```python
research = """
Here is my unpublished proof idea.
I think Lemma 7 may solve Navier-Stokes.
"""

codex(research)
```

Historically, you'd worry about:

```text
advisor
competitor
conference
journal
reviewer
```

With frontier AI, you now have another entity:

```text
        Your research
             │
             ▼
        AI assistant
             │
      ┌──────┴──────┐
      ▼             ▼
  helps YOU      improves MODEL
                    │
                    ▼
              AI company
                    │
                    ▼
              competing lab
```

That creates a **structural conflict of interest** that didn't really exist with traditional mathematical software.

Axios makes essentially this point: the episode raises the question of whether frontier labs can compete with the scientists who use their products. ([Axios][4])

---

### 7. And there's an even bigger AI implication

This event demonstrates something important about **AI research economics**.

Buckmaster's team might have:

```text
2 researchers
+ Claude/Codex
+ mathematical insight
```

OpenAI can respond with:

```text
10,000 agents
+ enormous inference budget
+ massive parallel search
+ specialized verification
+ frontier model
```

So scientific competition may increasingly become:

$$
\text{research capability}
=
\text{human insight}
\times
\text{model capability}
\times
\text{compute}
\times
\text{agent parallelism}
$$

And **compute becomes a competitive weapon in scientific priority**.

That is probably the most important story here for someone building agents like you.

Also, OpenAI says it **does not intend to claim the $1M Clay prize**, which makes the dispute primarily about **scientific priority and credit**, rather than the money itself. ([The Washington Post][2])

[Nature's report on the breakthrough](https://www.nature.com/articles/d41586-026-02842-5?utm_source=chatgpt.com)

[TechCrunch's account of the credit dispute](https://techcrunch.com/2026/09/08/openai-fought-dirty-on-career-making-math-problem-says-nyu-mathematician/?utm_source=chatgpt.com)

I can also break down **the actual Navier–Stokes mathematical claim and what the AI supposedly proved**, from the PDE level rather than the news-story level.

[1]: https://www.theguardian.com/science/2026/sep/08/openai-claims-to-have-solved-maths-problem-that-stumped-humans-for-decades?utm_source=chatgpt.com "OpenAI claims to have solved maths problem that stumped humans for decades"
[2]: https://www.washingtonpost.com/technology/2026/09/09/openai-claims-it-solved-elusive-math-problem-with-1-million-prize/?utm_source=chatgpt.com "OpenAI claims it solved elusive math problem with a $1 million prize - The Washington Post"
[3]: https://techcrunch.com/2026/09/08/openai-fought-dirty-on-career-making-math-problem-says-nyu-mathematician/?utm_source=chatgpt.com "OpenAI fought dirty on career-making math problem, says NYU mathematician | TechCrunch"
[4]: https://www.axios.com/2026/09/08/openai-math-solution-navier-stokes-credit?utm_source=chatgpt.com "OpenAI's historic math solution overshadowed by credit controversy"
[5]: https://www.nature.com/articles/d41586-026-02842-5?utm_source=chatgpt.com "OpenAI claims huge maths breakthrough on a famed ‘Millennium Problem’ | Nature"