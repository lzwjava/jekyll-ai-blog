---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Deep Learning Pioneers Before Hinton
translated: false
type: note
---

### Alexey Ivakhnenko's Work

Alexey Grigoryevich Ivakhnenko, a Ukrainian-Soviet cyberneticist, is often called the "godfather of deep learning" for his pioneering efforts in the 1960s and 1970s. Working under resource constraints during the Cold War era—when computing power was millions of times more limited than today—he focused on multilayer neural networks that could automatically learn hierarchical representations of data.

- **1965: Group Method of Data Handling (GMDH)**: Alongside Valentin Lapa, Ivakhnenko published the first general, working learning algorithm for supervised deep feedforward multilayer perceptrons (MLPs). This method trained networks layer by layer using regression analysis on input-output data pairs. It incrementally grew layers, trained them sequentially, and included pruning of unnecessary hidden units via validation sets. Crucially, it enabled the networks to learn distributed, internal representations of input data— a core idea in modern deep learning—without manual feature engineering. This predated similar concepts in Western AI by decades and was applied to real-world problems like pattern recognition and forecasting.

- **1971: Deep Network Implementation**: Ivakhnenko demonstrated an 8-layer deep neural network using GMDH principles, showcasing scalable depth for complex tasks. His approach treated deep networks as a form of polynomial approximation, allowing automatic model selection and avoiding the "curse of dimensionality" in high-layer architectures.

Ivakhnenko's GMDH evolved into a broader inductive modeling framework, influencing fields like control systems and economics. Despite its impact, much of his work was published in Russian and overlooked in English-language AI circles.

### Shun-ichi Amari's Work

Shun-ichi Amari, a Japanese mathematician and neuroscientist, made foundational contributions to neural network theory in the 1960s and 1970s, emphasizing adaptive learning and geometric perspectives on information processing. His research bridged neuroscience and computation, laying groundwork for self-organizing systems.

- **1967-1968: Adaptive Pattern Classification and Stochastic Gradient Descent (SGD)**: Amari proposed the first method for end-to-end training of deep MLPs using SGD, a optimization technique dating back to 1951 but newly applied to multilayer networks. In simulations with a five-layer network (two modifiable layers), his system learned to classify nonlinearly separable patterns by adjusting weights directly across layers. This enabled internal representations to emerge through gradient-based updates, a direct precursor to backpropagation-like methods, all under compute constraints billions of times harsher than modern standards.

- **1972: Adaptive Associative Memory Networks**: Building on the 1925 Lenz-Ising model (a physics-based recurrent architecture), Amari introduced an adaptive version that learned to store and recall patterns by tuning connection weights based on correlations. It handled sequence processing and retrieved stored patterns from noisy or partial inputs via neural dynamics. Published first in Japanese in 1969, this work is seen as the origin of the "Hopfield network" for associative memory.

Amari also founded information geometry, a field using differential geometry to analyze statistical models and neural dynamics, which underpins modern probabilistic neural networks.

### Context in the 2024 Nobel Backlash

In his 2024 report "A Nobel Prize for Plagiarism," Jürgen Schmidhuber argues that Hinton and Hopfield's Nobel-winning ideas—such as the Boltzmann machine (1985) for learning representations and the Hopfield network (1982) for associative memory—repackaged Ivakhnenko's layer-wise deep learning and Amari's SGD/adaptive recurrent models without attribution. For instance, the Boltzmann machine omitted citations to Ivakhnenko's 1965 internal representation learning and Amari's 1967 SGD, while Hopfield's network ignored Amari's 1972 adaptive Ising model. Schmidhuber claims this omission persisted in later surveys and the Nobel's scientific background document, highlighting a Western-centric bias in AI history.

[Alexey Ivakhnenko - Wikipedia](https://en.wikipedia.org/wiki/Alexey_Ivakhnenko)
[Deep Learning in a Nutshell: History and Training - NVIDIA Developer](https://developer.nvidia.com/blog/deep-learning-nutshell-history-training/)
[Shun-ichi Amari | Kyoto Prize](https://www.kyotoprize.org/en/laureates/shun-ichi_amari/)
[Japanese scientists were pioneers of AI, yet they're being written out of history](https://modernsciences.org/japanese-ai-pioneers-history-shuninchi-amari-kunihiko-fukushima-december-2024/)
[A Nobel Prize for Plagiarism - Technical Report IDSIA-24-24](https://people.idsia.ch/~juergen/physics-nobel-2024-plagiarism.pdf)
[Machine Learning Stirs Controversy in Nobel Prize in Physics - Harvard Technology Review](https://harvardtechnologyreview.com/2024/11/18/machine-learning-stirs-controversy-in-nobel-prize-in-physics/)
