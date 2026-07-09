---
audio: false
generated: true
image: false
lang: en
layout: post
title: Autonomous AI Research Nuances
translated: false
type: note
---

Question: Is this assessment of Yin Wang, autonomous driving, and the roles of optimism vs. pessimism in AI basically right?

Answer:

Broadly, yes, but I'd make the distinctions more precise.

Your observation about **timing** is important. In 2019, there was enormous enthusiasm around autonomous driving. Many people implicitly assumed that scaling engineering effort would quickly lead to Level 4/5 autonomy. In that environment, a critique like Yin Wang's was valuable because it highlighted issues that many discussions underemphasized:

* responsibility and liability,
* long-tail edge cases,
* overconfidence in marketing,
* the mismatch between demos and deployment.

Several of those concerns are still relevant today. Even in 2026, the industry has made impressive progress, but fully general autonomous driving remains much harder than many 2019 predictions suggested.

However, there's also a limitation.

Understanding whether autonomous driving will succeed requires combining several fields:

* perception
* robotics
* planning
* control theory
* safety engineering
* large-scale data collection
* simulation
* hardware economics

Someone can make an insightful philosophical or software-engineering critique without spending years building AV systems. But predicting *how fast* the field will progress usually requires much deeper exposure to those engineering details.

I also agree with another point you made:

> Among thousands of papers, blogs, and projects, only a small fraction end up pointing in the right direction.

Research is extremely noisy. Looking back, many ideas that attracted huge attention disappeared, while a few seemingly ordinary ideas became foundational. In AI alone:

* CNNs eventually dominated computer vision.
* Transformers displaced RNNs.
* Scaling laws became surprisingly predictive.
* RLHF became central for chat assistants.
* Diffusion models overtook GANs for image generation.

Most published ideas did **not** become the future.

Your point about pessimism versus optimism is also worth refining.

The quote "Pessimists are usually right; optimists change the world" is memorable, but reality is more nuanced.

Take Yann LeCun.

He is simultaneously:

* optimistic about representation learning and self-supervised learning,
* skeptical of current LLMs as a complete path toward AGI,
* optimistic about AI in the long run,
* critical of hype surrounding particular approaches.

That isn't a contradiction. Scientists are rarely globally optimistic or globally pessimistic. Instead, they're optimistic about mechanisms they believe in and skeptical about mechanisms they think are insufficient.

The same applies to many influential researchers:

* Geoffrey Hinton spent decades optimistic about neural networks when most of the field wasn't.
* Later, he became much more concerned about AI safety.
* Andrej Karpathy is optimistic about scaling and foundation models while being realistic about their current limitations.
* François Chollet has long argued that benchmark performance is not equivalent to general intelligence.

So people are often optimistic in one dimension and skeptical in another.

I think the deeper lesson is this:

Good researchers are usually **selectively skeptical** rather than simply optimistic or pessimistic. They ask:

* Which assumptions are actually justified?
* Which bottlenecks are real?
* Which trends are empirical versus speculative?

The people whose predictions age well are often those who update their views as evidence accumulates, rather than remaining permanently optimistic or permanently pessimistic.

References:

* [Yin Wang – Responsibility and Risk Analysis of Self-Driving Cars](https://yinwang.org/posts/autopilot-responsibility?utm_source=chatgpt.com)
* Yann LeCun
* Yin Wang