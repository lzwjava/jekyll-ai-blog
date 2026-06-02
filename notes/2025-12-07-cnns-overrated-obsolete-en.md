---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: CNNs Are Overrated and Obsolete
translated: false
type: note
---

Question: What are some unpopular opinions about Convolutional Neural Networks (CNNs)?

Answer:

Here are several genuinely unpopular or contrarian opinions about CNNs that you’ll rarely see celebrated in the deep-learning community:

- **CNNs are overrated for most real-world vision tasks today**
  Vision Transformers (ViTs) and MLP-based architectures (e.g., ConvNeXt, MLP-Mixer) consistently outperform CNNs on large datasets when given the same compute and data. Many people still treat “CNN = best for images” as gospel, but since ~2021 the evidence shows inductive biases like translation invariance and locality are often unnecessary or even harmful when you have enough data.

- **The convolution operation itself is largely obsolete**
  Modern high-performing “CNNs” (ResNet-50→ConvNeXt, ResNeXt→Swin Transformer, etc.) have replaced almost every 3×3 convolution with either depthwise separable convs, large-kernel convs, or straight-up attention. The classic stacked 3×3 convs that made AlexNet/VGG famous are rarely the optimal building block anymore.

- **CNNs succeeded mostly because of historical accidents, not because convolution is magically suited to images**
  In the early 2010s, convolutions were computationally cheap on GPUs (shared weights → fewer MACs), fit neatly into cuDNN kernels, and worked well with small datasets + heavy regularization (dropout, data aug). If transformers had matured five years earlier, CNNs might have remained a niche idea.

- **Most theoretical justifications for CNNs are post-hoc rationalizations**
  Claims like “convolutions enforce translation invariance” or “hierarchical receptive fields mimic the visual cortex” sound nice but don’t hold up. Real CNNs are not translation-invariant without pooling/data aug, and the visual cortex analogy has been heavily criticized by neuroscientists.

- **For small/medium datasets, hand-crafted features (SIFT, HOG) + linear SVM or random forests still beat lightweight CNNs in many industrial settings**
  People forget this because academic benchmarks use huge labeled datasets, but in medical imaging, remote sensing, or defect detection with <10k images, classic methods are often more robust and interpretable.

- **CNNs are responsible for a huge amount of wasted compute in the last decade**
  The community spent years scaling ResNets to 1000+ layers and ensembling giant CNNs when a simple ViT or even a well-tuned MLP would have been more sample-efficient and faster to train with modern optimizers.

- **The term “CNN” has become almost meaningless**
  Today it just means “whatever ImageNet winner we had before transformers.” Calling Swin Transformer or ConvNeXt a “CNN” is mostly marketing/legacy terminology.

In short: CNNs were revolutionary from 2012–2018, but clinging to them as the default vision architecture in 2025 is increasingly seen (in some circles) as a form of intellectual inertia.

References:

- [Dosovitskiy et al., “An Image is Worth 16x16 Words” (ViT paper)](https://arxiv.org/abs/2010.11929)
- [Liu et al., “A ConvNet for the 2020s” (ConvNeXt)](https://arxiv.org/abs/2201.03545)
- [Tolias et al., “What Neural Network Architects Can Learn from Neuroscience (and vice versa)”](https://www.nature.com/articles/s42256-021-00354-y)
- [Touvron et al., “Training data-efficient image transformers” (DeiT)](https://arxiv.org/abs/2012.12877)
