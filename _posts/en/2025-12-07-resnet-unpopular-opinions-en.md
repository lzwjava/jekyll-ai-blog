---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Unpopular Opinions About ResNet
translated: false
type: note
---

Question: What are some unpopular opinions about ResNet?

Answer:

ResNet (Residual Network), introduced in 2015, revolutionized deep learning by enabling the training of very deep neural networks through skip connections. However, despite its widespread adoption as a backbone for computer vision tasks, it has sparked several contrarian views in the machine learning community. These "unpopular opinions" often challenge the hype around ResNet's universality, depth obsession, and perceived simplicity. Below, I've compiled key ones drawn from discussions in forums like Reddit's r/MachineLearning, academic papers, and expert commentary on platforms like X (formerly Twitter). These highlight debates on its limitations, overreliance, and evolving relevance.

### 1. **ResNet's Success Isn't Primarily About Better Gradient Flow—That's a Misconception**

- Many cite skip connections for "improving gradient flow" to solve vanishing gradients, but this contradicts the original ResNet hypothesis. The core issue was optimization degradation in deep plain networks (higher training error despite more capacity), not just signal vanishing. Batch normalization already handled norms, but noise buildup drowned signals. Skip connections make learning identity mappings trivial (F(x) ≈ 0), easing optimization without needing to "flow" gradients perfectly. Tutorials and papers often oversimplify this, leading to cargo-cult implementations.

### 2. **You Don't Actually Need Skip Connections—ResNets Without Them Work Fine with Careful Initialization**

- The "ResNet hypothesis" (that residuals are essential for depth) has been questioned. Papers like "Fixup Initialization: Residual Learning Without Normalization" (ICLR 2019) show plain networks (no skips) can train effectively to good results if initialized properly. Skips help, but they're not magic; they're a crutch for lazy optimization. This implies ResNet's hype overlooks simpler fixes, making it overengineered for many use cases.

### 3. **ResNets Are Overrated for Most Real-World Tasks—Vision Transformers (ViTs) or Simpler Models Are Often Better**

- For training from scratch on modest compute, ResNets are "as good as it gets" but not revolutionary—Vision Transformers (e.g., via DINO self-supervision) match or beat them with similar resources, especially on diverse datasets. ViTs scale better with data and avoid ResNet's inductive biases (like locality), which can hurt on non-natural images. ResNets feel "stuck in 2015" when alternatives like RegNets offer similar performance with less fuss. Hot take: 99% of CV apps could use a basic ResNet, but that's a bug, not a feature—it's lazy engineering.

### 4. **Deeper Isn't Always Better—Wider ResNets Outperform Deeper Ones, Challenging the Depth Obsession**

- The push for ultra-deep ResNets (e.g., ResNet-152) ignores evidence that width (more channels) often yields better accuracy with fewer parameters and faster training. A 2016 arXiv paper ("Wider or Deeper") showed shallower, wider variants beating deep ResNets on ImageNet and semantic segmentation, while using less memory. Depth adds complexity without proportional gains, especially post-50 layers—it's diminishing returns fueled by benchmark chasing.

### 5. **ResNets Aren't Ideal for GANs or Non-Classification Tasks—Custom Architectures Win**

- In GAN discriminators, standard ResNets (e.g., ResNet-50) shatter data distributions, creating step-function decision boundaries with useless gradients for generators. SOTA GANs (StyleGAN, BigGAN) use bespoke designs instead. This extends to other domains: ResNets excel at ImageNet-style classification but falter in generative or low-data scenarios without heavy tweaks, making them a poor default.

### 6. **ResNets Are Too Simple and Reliable—They Stifle Innovation**

- Their ease (pre-trained in minutes, quick to train) makes them a crutch: Start with ResNet-50, fine-tune, done. But this reliability hides deeper issues—why innovate when "good enough" works? Critics argue it props up mediocre research; you'd get similar results with LSTMs for NLP or shallower CNNs. Even fans admit: "ResNets still don't make sense to me—the input addition stabilizing training is bafflingly ad-hoc."

These opinions reflect a maturing field where ResNet is respected but no longer untouchable. For practitioners, it's still a solid starting point, but experimenting with hybrids (e.g., ResNeXt for multi-path) or alternatives pays off for edge cases.

References:

- [Has the ResNet Hypothesis been debunked? (Reddit r/MachineLearning)](https://www.reddit.com/r/MachineLearning/comments/px3hzd/d_has_the_resnet_hypothesis_been_debunked/)
- [Are ResNets as good as it gets? (Reddit r/MachineLearning)](https://www.reddit.com/r/MachineLearning/comments/nbgb6a/d_are_resnets_as_good_as_it_gets/)
- [Why don't people use ResNet as GAN discriminator? (Reddit r/MachineLearning)](https://www.reddit.com/r/MachineLearning/comments/esj4m7/d_why_dont_people_use_typical_classification/)
- [Why do residual networks work? (Cross Validated)](https://stats.stackexchange.com/questions/237152/why-do-residual-networks-work)
- [Wider or Deeper: Revisiting the ResNet Model (arXiv)](https://arxiv.org/abs/1611.10080)
- [ResNets still don't make sense to me (X post)](https://x.com/_notapenguin/status/1995480100322586677)
- [99% of CV apps can be handled with simple ResNet (X post)](https://x.com/tunguz/status/1580594479211216900)
- [ViTs over classic ConvNets like ResNet (X post)](https://x.com/ZRozsypalek/status/1996217103246885243)
