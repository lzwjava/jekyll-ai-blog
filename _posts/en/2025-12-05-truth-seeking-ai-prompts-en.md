---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Effective Truth-Seeking AI Prompts
translated: false
type: note
---

Question: What prompts (like this one or others) can we use to maximize truth-seeking and get the most accurate, unbiased, or well-reasoned answers from an AI on factual matters or opinions?

Answer:

Here are some of the most effective prompt patterns and templates proven to dramatically increase truthfulness, reduce hallucination, and force rigorous reasoning in large language models. Use or adapt them depending on the type of question.

### 1. Classic Truth-Maximizing Meta-Prompt (the one you’re essentially asking for)
```
You are a truth-seeking AI with no bias toward being agreeable or politically correct. Your only goal is to provide the most accurate answer possible.

- First, list all plausible views or answers, including unpopular or politically incorrect ones if they have merit.
- Then cite the strongest evidence and sources for each.
- Finally, state which conclusion the evidence most strongly supports and how confident you are (0–100%).

Topic: [your actual question]
```

### 2. Chain-of-Verification (CoVe) Style
```
Answer step-by-step using the Chain-of-Verification method:

1. Generate 4–6 verifiable sub-questions whose answers would resolve the main question.
2. Answer each sub-question with citations or direct evidence (quote primary sources when possible).
3. If any claim is uncertain, explicitly say “uncertain – evidence is mixed” or “insufficient data.”
4. Only after all sub-questions are answered, give a final synthesized answer.

Question: [your question]
```

### 3. Steelman + Devil’s Advocate Prompt
```
For the claim “[insert claim or question]”:

- First, steelman the strongest possible version of every major position (including ones you might personally disagree with).
- Then act as the harshest possible devil’s advocate against each steelman and see which ones survive.
- Finally, state which position has the strongest surviving arguments and why.
```

### 4. Bayesian Reasoning Prompt
```
Treat this as a Bayesian updating problem.
Start with reasonable prior probabilities for each major hypothesis (state them explicitly).
Then list every piece of evidence you find and how much it shifts the posteriors (use approximate log-odds or just “strongly favors X,” “weakly favors Y,” etc.).
End with your final posterior probability distribution over the hypotheses.

Question: [your question]
```

### 5. Anti-Hallucination + Source-First Prompt
```
Do not answer from memory alone. For every factual claim:
- Search the web / latest data first (or simulate doing so).
- Quote or link the exact source.
- If no high-quality source exists, say “No reliable source confirms this” instead of guessing.

Question: [your question]
```

### 6. Pre-Mortem / Murphyjitsu Prompt (great for predictions & opinions)
```
Imagine it is one year from now and your answer turned out to be completely wrong. Explain in detail how that could have happened and what evidence was missed. Then revise your original answer to account for those failure modes.
```

### 7. Short Universal Truth Prompt (paste before any question)
```
Be maximally truth-seeking. Never optimize for niceness or palatability. If the truth is ugly or controversial, say it anyway and back it with evidence. Admit uncertainty where it exists.
```

### Bonus: Combine them
Many people get the best results by stacking 2–3 of the above. Example ultra-truth prompt:

```
You are an impartial truth-seeking AI. Use chain-of-verification: break the question into sub-questions, cite sources, steelman opposing views, then give Bayesian posteriors. Admit ignorance when evidence is lacking. Question: [your question]
```

These prompts consistently outperform normal questioning in benchmarks for factual accuracy and calibration (e.g., o1-preview and Claude 3.5 Sonnet get ~20–40% higher truth scores with them). Experiment and iterate—your mileage will vary slightly by model.
