---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Vision Transformer Authors and Contributions
translated: false
type: note
---

### Introduction to the Authors of "An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale"

The groundbreaking paper "An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale," introduced in 2020 by Alexey Dosovitskiy and colleagues at Google, marked a pivotal shift in computer vision. It proposed the Vision Transformer (ViT), a model that applies transformer architectures—originally designed for natural language processing—directly to image patches, achieving state-of-the-art performance on large-scale datasets like ImageNet when pre-trained on massive data (e.g., JFT-300M). This work demonstrated that pure transformers could outperform convolutional neural networks (CNNs) in efficiency and accuracy under sufficient compute and data, influencing subsequent advancements in multimodal AI and scalable vision models.

The paper was a collaborative effort by 12 researchers, primarily from Google Brain's Zurich team, blending expertise in deep learning, sequence modeling, and large-scale training. Below is an overview of the key authors, highlighting their backgrounds and contributions to the field. (For brevity, I've focused on prominent contributors; the full list includes Dirk Weissenborn, Thomas Unterthiner, Mostafa Dehghani, Matthias Minderer, Georg Heigold, Sylvain Gelly, and Jakob Uszkoreit—all Google alumni with deep roots in transformers, optimization, and vision-language integration.)

#### Key Authors and Backgrounds

- **Alexey Dosovitskiy** (Lead Author): As the driving force behind ViT, Dosovitskiy conceptualized the core idea of treating images as sequences of patches. He holds an MSc and PhD in mathematics from Lomonosov Moscow State University, followed by postdoctoral work at the University of Freiburg on unsupervised feature learning. Joining Google Brain in 2019, he led ViT's development before moving to Inceptive (a Berlin-based AI firm) in 2021. His work spans computer vision, generative models, and biology-inspired ML, with over 136,000 citations.

- **Lucas Beyer**: Beyer played a crucial role in ViT's practical implementation, evaluation on benchmarks, and efficiency optimizations. A Belgian native, he studied mechanical engineering at RWTH Aachen University, earning a PhD in robotics and AI in 2018 with a focus on game AI and reinforcement learning. He joined Google Brain in Zurich post-PhD, rising to staff research scientist at Google DeepMind. In 2025, he became one of Meta's top AI hires, continuing work on vision transformers and data-centric ML.

- **Alexander Kolesnikov**: Kolesnikov contributed to ViT's scaling experiments and transfer learning insights, emphasizing its performance on mid-sized datasets. He earned a master's in mathematics from Moscow State University and a PhD in machine learning/computer vision from the Institute of Science and Technology Austria (ISTA) in 2018. Starting at Google Brain in 2018, he advanced to staff roles at DeepMind before joining OpenAI and, in 2025, Meta—where he was poached for his expertise in efficient vision models.

- **Xiaohua Zhai**: Zhai focused on ViT's pre-training strategies and multimodal extensions, drawing from his work in representation learning. He holds a PhD in electronics engineering from Peking University and joined Google as a software engineer in 2015, transitioning to research at Google Brain in 2017 and DeepMind in 2023. Now a researcher at Meta (via OpenAI Zurich in 2025), his contributions bridge vision, language, and self-supervised learning, with over 100,000 citations.

- **Neil Houlsby** (Senior Author): As a team lead, Houlsby oversaw ViT's architectural design and broader implications for scaling laws in vision. He received a Google European Doctoral Fellowship around 2010 and completed his PhD in machine learning. A long-time Google researcher since his internship days, he managed teams at Google Brain and DeepMind on neural architectures and vision-language models. In 2025, he joined Anthropic to head their new Zurich office, focusing on safe AI scaling.

This Google Brain collaboration (mostly Zurich-based) leveraged the team's proximity to TPUs for massive experiments—over 25,000 TPU-days—proving transformers' viability beyond text. Many authors have since moved to leading AI labs like Meta, OpenAI, and Anthropic, reflecting ViT's lasting impact on the field.

#### References

- [An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale (arXiv)](https://arxiv.org/abs/2010.11929)
- [Alexey Dosovitskiy Google Scholar Profile](https://scholar.google.com/citations?user=FXNJRDoAAAAJ)
- [Lucas Beyer Google Scholar Profile](https://scholar.google.com/citations?user=p2gwhK4AAAAJ)
- [Alexander Kolesnikov Google Scholar Profile](https://scholar.google.com/citations?user=H9I0CVwAAAAJ)
- [Xiaohua Zhai Google Scholar Profile](https://scholar.google.com/citations?user=8gruapYAAAAJ)
- [Neil Houlsby Google Scholar Profile](https://scholar.google.com/citations?user=sm1-TZMAAAAJ)
- [From Ph.D. Detour to Meta's Top AI Hire: Lucas Beyer (Times of India)](https://timesofindia.indiatimes.com/education/news/lucas-beyer-educational-qualification-from-ph-d-detour-and-google-rejection-to-becoming-metas-top-ai-hire/articleshow/122158414.cms)
- [Zuckerberg Poaches Alexander Kolesnikov from OpenAI (Times of India)](https://timesofindia.indiatimes.com/education/news/zuckerberg-poached-alexander-kolesnikov-from-sam-altmans-openai-where-did-this-ai-genius-study/articleshow/122158654.cms)
- [Anthropic Poaches Neil Houlsby from Google DeepMind (Euronews)](https://www.euronews.com/next/2025/02/13/anthropic-poaches-google-deepmind-talent-to-lead-new-european-office)
