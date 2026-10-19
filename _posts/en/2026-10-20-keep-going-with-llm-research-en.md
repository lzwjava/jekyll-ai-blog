---
audio: false
generated: true
image: false
lang: en
layout: post
title: Keep Going with LLM Research
translated: false
type: note
---

## Question: Should I keep pursuing LLM research, model training, and inference instead of giving up?

**Answer: Yes. I think you should keep going. But don't pursue it merely because you love AI. Build a life and a business around becoming increasingly capable of understanding, training, and deploying AI systems.**

Looking at your background, I see a consistent direction: you want to understand computers deeply, build real products, explore new technologies, and eventually operate your own company.

LLM research and engineering sit at the intersection of these ambitions.

### 1. Your long-term technical direction should cover the entire LLM stack

Don't limit yourself to application development or a single specialization. Build expertise across the model lifecycle.

| Area | What to explore | Why it matters |
| --- | --- | --- |
| **Pretraining** | Tokenization, data pipelines, distributed training, scaling laws, optimization | Understand how models acquire capabilities |
| **Post-training** | SFT, preference optimization, RL, synthetic data, evaluations | Understand how base models become useful assistants and agents |
| **Inference** | KV cache, batching, quantization, speculative decoding, serving systems | Make models faster, cheaper, and more accessible |
| **Model architecture** | Transformers, MoE, attention, MTP, novel architectures | Understand the fundamental mechanisms and research opportunities |
| **AI infrastructure** | GPU kernels, CUDA, Triton, distributed computing, memory optimization | Make increasingly capable models practical to train and serve |
| **AI agents** | Tool use, coding agents, planning, memory, evaluation | Turn model capabilities into products that accomplish real work |

You have already trained a 760M-parameter GPT-2 model on an MI300X and worked with modern LLM tooling. You have a starting point from which to deepen your expertise.

The important thing is to keep moving from *using models* toward *understanding and improving models*.

### 2. Don't choose between research and building a business

I would structure your work around three interconnected activities.

**A. Research: Build your technical depth.**

Continue experimenting with pretraining, post-training, and inference.

For example, take a small model and systematically investigate:

- How data quality affects training outcomes.
- How training tokens and model size affect loss.
- Whether a particular post-training technique improves task performance.
- How different inference optimizations affect throughput, latency, and memory consumption.
- How much capability you can obtain from limited compute.

Don't merely reproduce other people's results. Develop the ability to formulate a hypothesis, run an experiment, measure the outcome, and explain what you learned.

**B. Products: Turn your knowledge into something people use.**

Continue developing your CLI agents, open-source projects, and Fun Live.

Your research can feed your products. Your products can generate revenue, usage data, and real-world problems that motivate your research.

You don't need to train a frontier model to build a valuable AI company. You can create significant value by making existing models more useful, cheaper to operate, easier to deploy, or better at particular tasks.

**C. Business: Build financial independence.**

This is particularly important when you're operating your own company.

Research can have a long feedback loop. Revenue gives you the freedom to continue researching without depending entirely on an employer, investor, or research grant.

My preferred strategy for you would be:

- **Consulting:** Sell AI engineering, agent development, model adaptation, and inference optimization.
- **Open source:** Publish your experiments and tools to demonstrate your capabilities.
- **Products:** Develop solutions around problems you repeatedly encounter with customers.
- **Research:** Reserve consistent time for deeper experiments that might not generate immediate revenue.

These activities should reinforce each other rather than compete for your attention.

### 3. Don't confuse persistence with doing the same thing indefinitely

There is an important distinction between giving up on your direction and changing your strategy.

You should not give up on learning how models work simply because a particular experiment fails, a job application is rejected, or the market changes.

But you should be willing to abandon an ineffective approach.

For example:

- If training large models from scratch is too expensive, work on smaller models, data efficiency, or training infrastructure.
- If you cannot compete with frontier labs on model scale, investigate inference efficiency, specialized models, or post-training.
- If AI research alone doesn't pay your bills, sell engineering services while continuing your research.
- If a particular project attracts no users, publish what you learned and try a better hypothesis.

**Preserve the long-term direction; change the short-term strategy when the evidence tells you to.**

That is different from blindly persisting with one project.

### 4. Your advantage is the combination of research, engineering, and entrepreneurship

You don't need to become a conventional academic researcher.

Your background gives you another possible trajectory:

1. Understand the fundamentals of deep learning.
2. Train and fine-tune models yourself.
3. Build efficient inference systems.
4. Develop agents and AI-native software.
5. Find real problems through customers and users.
6. Turn the most valuable solutions into products.
7. Use the resulting revenue, experience, and distribution to support more ambitious research.

This creates a potentially powerful feedback loop.

Research improves your engineering. Engineering improves your products. Products reveal real problems. Revenue funds further experimentation.

You can also explore hardware, GPU architecture, compilers, and systems software as your interests develop. These fields connect directly to the economics of AI.

You don't have to decide today whether your ultimate identity will be researcher, engineer, or founder.

You can become a founder whose technical judgment comes from doing the work yourself.

### 5. What I would do over the next 12 months

I would choose one primary technical research track and one commercial track.

**Technical track: Build a serious, measurable LLM project.**

For example, investigate efficient post-training or inference for a small open-weight model.

Publish:

- The problem and hypothesis.
- The baseline.
- The experimental setup.
- The code and reproducible results.
- The performance and cost measurements.
- The limitations and lessons learned.

Build a sequence of experiments that compounds into genuine expertise, rather than jumping between every new model release.

**Commercial track: Find paying customers for your AI engineering capabilities.**

Offer specific services such as:

- LLM inference optimization.
- Fine-tuning and post-training.
- AI coding agents and business agents.
- Evaluation pipelines.
- Model deployment and GPU infrastructure.

Use customer problems to identify opportunities for reusable software.

Review your progress every month. Measure technical progress, user adoption, revenue, and financial runway. Don't judge the entire direction by a single month or a single experiment.

---

### My fundamental advice

You have already invested years in software engineering, built a product with 30,000 users, and experimented with model training. You don't need to throw away that accumulated experience and start from zero in a completely different field.

Your next step is to compound it.

Keep learning the mathematics. Keep reading papers. Keep training models. Keep profiling inference. Keep building software that real people use.

But also take care of your financial situation and build a business that gives you the freedom to keep doing this.

**You don't need to prove that you can become the best LLM researcher in the world. You need to keep becoming more capable, produce work that others can verify, and build a sustainable life around the problems you genuinely want to solve.**

And remember: research does not always mean inventing a new architecture. Reproducing a result, discovering why an optimization works, identifying a failure mode, or making an existing technique substantially cheaper can all be meaningful technical contributions.

Your long-term goal can be to understand the entire process—from raw data and pretraining to post-training, inference, and products—while becoming increasingly independent in your ability to experiment and build.

**Don't give up on that direction just because the path is uncertain. Build the financial and technical foundation that allows you to pursue it for a long time.**
