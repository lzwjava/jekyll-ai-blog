---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Large Language Model Reasoning Techniques
translated: false
type: note
---

### Overview

Denny Zhou (likely the intended "Danny Zhou") delivered a lecture titled "Large Language Model Reasoning" as part of Stanford's CS25: Transformers United course (Version 5). In it, he provides a comprehensive overview of reasoning in large language models (LLMs), emphasizing practical techniques, theoretical foundations, and ongoing challenges. Below is a structured summary of his key points, drawn directly from his slides and accompanying notes.

### Definition of Reasoning in LLMs

- Reasoning in LLMs is fundamentally about **generating intermediate tokens** (or steps) between the input prompt and the final output, rather than jumping straight to an answer. This process enables the model to break down complex problems.
- It doesn't need to mimic human reasoning exactly—the goal is effective problem-solving. For example, solving "What is the last two letters of 'artificial intelligence'?" by concatenating word endings step-by-step yields "le," showing how intermediates aid computation.
- Theoretical backing: For problems solvable by boolean circuits of size *T*, constant-sized transformers can handle them by producing *O(T)* intermediate tokens, avoiding the need for massive model scaling.

### Motivations

- Pretrained LLMs are inherently capable of reasoning without special prompting or fine-tuning; the myth that they can't is debunked—issues arise from decoding methods that fail to surface reasoned outputs.
- This approach aligns with "The Bitter Lesson": Leverage computation (via token generation) over human-like shortcuts, enabling emergent human-like behaviors through next-token prediction.
- Focus on optimizing for end-goal metrics like correctness, using model-generated data instead of expensive human annotations.

### Core Ideas

- **Chain-of-Thought (CoT) Decoding**: Generate multiple candidate responses and select the one with highest confidence on the final answer. Reasoned paths often have higher confidence than direct guesses (e.g., counting apples in a scenario).
- **Scaling via Length, Not Depth**: Train models to generate longer sequences (*O(T)* tokens) for serial problems, making them arbitrarily powerful without bloating model size.
- **Aggregation Over Single Shots**: Generating and combining multiple responses (e.g., via majority vote) outperforms single outputs; retrieval of similar problems + reasoning beats reasoning alone.
- Example: Gemini 2.0's "thinking mode" solves puzzles like forming 2025 with numbers 1-10 by prioritizing operations (e.g., 45 × 45 = 2025).

### Key Techniques

- **Prompting**: Use few-shot examples or phrases like "Let's think step by step" to elicit intermediates (e.g., for math word problems). Zero-shot works but is less reliable.
- **Supervised Fine-Tuning (SFT)**: Train on human-annotated step-by-step solutions to boost likelihood of reasoned paths.
- **Self-Improvement**: Generate your own training data by filtering correct reasoned solutions from model outputs.
- **RL Fine-Tuning (ReFT)**: Iteratively reward correct full responses (reasoning + answer) and penalize incorrect ones, using a verifier. This generalizes best for verifiable tasks; credit to team members like Jonathan Lai.
- **Self-Consistency**: Sample multiple paths, then aggregate (e.g., most frequent answer). Universal variant for open-ended tasks lets the model self-select.
- **Retrieval + Reasoning**: Pull in related examples to bootstrap (e.g., recalling distance formulas for area queries).
- **Other Enhancers**: "Take a Step Back" for abstraction; marginalization to fix probabilistic decoding biases.

### Limitations

- **Prompting**: Simple but brittle—needs task-specific examples; generic prompts underperform.
- **SFT**: Doesn't generalize well to out-of-distribution problems (e.g., fails on novel "strawberry" letter-counting despite training).
- **RL**: Relies on reliable verifiers, which aren't available for all tasks (e.g., creative writing).
- **General Challenges**: LLMs are probabilistic predictors, so greedy decoding favors fluent-but-wrong answers. Aggregation helps but doesn't solve non-verifiable domains.
- Decoding misalignment: Even strong models may not rank reasoned outputs highest without intervention.

### Future Directions

- Push beyond benchmarks to real-world apps, especially non-verifiable tasks (e.g., translation optimization without perfect metrics).
- Scale aggregation and retrieval for bigger gains.
- Improve decoding (e.g., via marginalization) to better align probabilistic outputs with correctness.
- Build toward systems that "remember" successful reasoning paths across sessions.

This lecture highlights RL fine-tuning as the current powerhouse, with a shift toward viewing reasoning as a scalable generation problem.

### References

- [LLM Reasoning Slides (PDF)](https://dennyzhou.github.io/LLM-Reasoning-Stanford-CS-25.pdf)
- [Denny Zhou's X Post on Key Points](https://x.com/denny_zhou/status/1948499173986201915)
- [Lecture Video on YouTube](https://www.youtube.com/watch?v=ebnX5Ur1hBk)
- [CS25 Course Page](https://web.stanford.edu/class/cs25/)
