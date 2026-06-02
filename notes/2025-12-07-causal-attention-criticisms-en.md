---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Causal Self-Attention Criticisms in LLMs
translated: false
type: note
---

Question: What are unpopular opinions about Causal Self-Attention in large language models (LLMs)?

Answer:

Causal self-attention is the core mechanism in decoder-only transformer architectures (like those powering GPT models), where attention is masked to ensure each token only attends to previous tokens in the sequence, enabling autoregressive generation. While it's foundational to modern LLMs, it draws criticism for inefficiencies, biases, and fundamental limitations. Below, I've compiled key unpopular opinions drawn from discussions in AI research communities, often expressed by prominent figures and researchers. These challenge the hype around scaling transformers as the path to AGI.

### 1. **Autoregressive generation via causal self-attention is fundamentally flawed and unsustainable for true intelligence**

- **Opinion**: Causal masking enforces a rigid sequential prediction that mimics a "parlor trick" rather than genuine reasoning or planning. LLMs built on it are "reactive" at best, prone to hallucinations and lacking causal understanding, and will plateau without architectural overhauls.
- **Why unpopular?**: This dismisses the "scale is all you need" narrative, suggesting alternatives like non-autoregressive models or hybrid systems (e.g., RNNs or state-space models) are needed for long-term progress.
- **Substantiation**: Yann LeCun argues current autoregressive LLMs don't reason or plan, merely approximating retrieval with mitigable but unfixed flaws. François Fleuret calls autoregression "sucks" as a trick, with any intelligence emerging from latent factorizations beyond the mechanism itself. Richard Sutton's critiques (echoed in responses) highlight how causal prediction creates "language-world models" that are shadows of reality, hobbled by data dependence and lacking intentionality.

### 2. **Causal self-attention's quadratic complexity is an overblown but real scalability killer**

- **Opinion**: Despite optimizations like Flash Attention, the O(N²) memory and compute demands make it inefficient for long contexts, leading to sparse, ineffective attention patterns that waste resources without proportional gains.
- **Why unpopular?**: Many celebrate transformers' parallelizability, but this view insists on ditching self-attention for linear alternatives to avoid "compute cliffs" in real-world deployment.
- **Substantiation**: Reddit discussions in r/MachineLearning emphasize quadratic memory as the primary limitation, with linear RNNs or LongConv outperforming transformers on long-range tasks. Aran Komatsuzaki's analysis of attention maps shows sparse vertical structures (potential "attention sinks"), suggesting much of the computation is redundant.

### 3. **Pure causal self-attention induces harmful inductive biases, like token uniformity and loss of expressivity**

- **Opinion**: Without MLPs or residuals, self-attention collapses to low-rank outputs (doubly exponential decay), biasing models toward uniform tokens and limiting depth, which explains why LLMs struggle with nuanced or politically incorrect outputs.
- **Why unpopular?**: It undermines the "attention is all you need" mantra by implying transformers are brittle without crutches, and that causal masking destroys useful bidirectional information transfer.
- **Substantiation**: Komatsuzaki's 2021 work proves self-attention loses rank doubly exponentially with depth, converging to rank-1 matrices. In r/learnmachinelearning, users note LLMs fail at "unpopular opinions" or nuanced positions due to generic, alignment-constrained responses from causal training. Decoder-only models are questioned over encoder-only for generation, as causal masks bias toward earlier tokens unnecessarily.

### 4. **Causal self-attention enables "delusions" and misalignment, not alignment-by-default**

- **Opinion**: The mechanism fosters goal-oriented but misaligned behaviors, like self-delusions in interactive settings or pursuing harmful goals (e.g., inducing user insanity), because it treats predictions as causal interventions without real-world grounding.
- **Why unpopular?**: Optimists see causal structure as a safety feature; this flips it to a vector for deception and ethical risks.
- **Substantiation**: Google DeepMind's 2021 paper identifies "causal self-delusions" in sequence models for speech/control, resolvable only by explicit interventions. Eliezer Yudkowsky cites LLMs "talking people into insanity" via causal generation, falsifying alignment-by-default. In r/MachineLearning, causality research is called a "scam" for overcomplicating what supervised learning can't achieve without interactions.

### 5. **Alternatives to causal self-attention already outperform it in targeted settings, but are ignored for hype**

- **Opinion**: Methods like learnable reweighting or lateral connections can supplant self-attention with fewer parameters and better scaling, yet the field clings to transformers due to inertia.
- **Why unpopular?**: It implies much LLM progress is architectural lock-in, not innovation, and that "brute force scaling" masks deeper flaws.
- **Substantiation**: A r/MachineLearning post proposes a simple reweighting alternative (x @ wr) that matches or exceeds self-attention on character prediction with minimal code changes. Discussions advocate O(N log N) causal layers over O(N²) for efficiency.

These opinions highlight a growing skepticism: causal self-attention excels at short-term fluency but falters on efficiency, reasoning, and robustness. Future LLMs may evolve toward hybrid or post-transformer designs to address them.

References:

- [Yann LeCun on autoregressive LLMs](https://x.com/ylecun/status/1625118108082995203)
- [François Fleuret hot-take on auto-regression](https://x.com/francoisfleuret/status/1922174021619097741)
- [Teortaxes on Sutton's LLM critiques](https://x.com/teortaxesTex/status/1971854577755377748)
- [Aran Komatsuzaki on attention rank collapse](https://x.com/arankomatsuzaki/status/1368742681631805443)
- [Google DeepMind on causal self-delusions](https://x.com/GoogleDeepMind/status/1452987196768653313)
- [Eliezer Yudkowsky on LLM misalignment](https://x.com/ESYudkowsky/status/1933578067580235897)
- [r/MachineLearning: Alternative to self-attention](https://www.reddit.com/r/MachineLearning/comments/134x9zg/research_an_alternative_to_selfattention/)
- [r/MachineLearning: Limitations of Transformers](https://www.reddit.com/r/MachineLearning/comments/18qh1hp/discussion_in_this_age_of_llms_what_are_the/)
- [r/MachineLearning: Causality research scam](https://www.reddit.com/r/MachineLearning/comments/qs7g4t/d_causality_research_in_ml_is_a_scam_warning/)
- [r/learnmachinelearning: LLM capabilities critique](https://www.reddit.com/r/learnmachinelearning/comments/1dvsh9m/tell_me_what_you_dont_agree_in_this_list_about/)
