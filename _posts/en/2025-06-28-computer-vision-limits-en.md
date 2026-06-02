---
audio: false
generated: true
lang: en
layout: post
title: Computer Vision Falls Short of Humans
translated: false
type: note
---

The blog post by Yin Wang argues that computer vision systems, even advanced ones in 2019, were far from achieving human-level performance. It claims that these systems struggle with basic object recognition (e.g., identifying a car) and are easily fooled by adversarial examples or minor image alterations, unlike humans who recognize objects effortlessly. Wang suggests that the field overstates its progress and that true human-level computer vision remains elusive due to fundamental limitations in how these systems process and understand images.

### Is it true?
As of the post's publication in October 2019, Wang’s argument had merit based on the state of computer vision at the time:

- **Limited Generalization**: Computer vision models, like convolutional neural networks (CNNs), relied heavily on pattern matching within training data. They often failed to generalize to new contexts or handle edge cases well, as Wang describes. For example, models could misclassify objects when lighting, angles, or backgrounds changed significantly.

- **Adversarial Vulnerability**: Wang’s point about adversarial examples—images subtly altered to mislead models—was accurate. Research, such as Goodfellow et al. (2014), showed that small, imperceptible perturbations could cause models to misclassify images with high confidence, highlighting a gap between human and machine vision.

- **Overhyped Claims**: The post criticizes the hype around computer vision. In 2019, while models like ResNet, YOLO, and early transformers showed impressive results on benchmarks (e.g., ImageNet), these were controlled datasets. Real-world applications often revealed weaknesses, such as misidentifications in autonomous driving or facial recognition systems.

However, the post’s tone is absolute, claiming “there is no human-level computer vision.” This overlooks progress in specific tasks. For instance:
- **Task-Specific Success**: By 2019, computer vision systems outperformed humans in narrow tasks like classifying certain medical images (e.g., detecting diabetic retinopathy) or recognizing specific objects in controlled settings.
- **Progress Since 2019**: By 2025, advancements like vision transformers (e.g., ViT, CLIP) and large-scale multimodal models (e.g., GPT-4o, DALL·E 3) have closed the gap. These models handle more diverse inputs, better generalize across contexts, and integrate language and vision for improved reasoning. Still, they don’t fully replicate human vision’s robustness, context awareness, or intuitive understanding.

### Critical Assessment
Wang’s core claim—that computer vision in 2019 was not human-level—is largely true. Models lacked the generalization, robustness, and intuitive understanding of human vision. However, his dismissal of progress may be overly pessimistic, as significant strides have been made since. Even in 2025, while computer vision excels in specific domains, it still falls short of human-level perception in open-world scenarios due to issues like:
- **Contextual Reasoning**: Humans integrate sensory data with world knowledge effortlessly; machines struggle with this.
- **Edge Cases**: Models can fail in rare or novel situations where humans adapt quickly.
- **Energy Efficiency**: Human vision is far more energy-efficient than computational models.

The post remains relevant as a critique of overhyping AI capabilities but doesn’t account for the rapid progress in the field. No single source confirms “human-level” vision has been achieved by 2025, but the gap has narrowed significantly.[](https://yinwang0.wordpress.com/2019/10/20/human-level-computer-vision/)
