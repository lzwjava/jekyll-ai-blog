---
audio: false
generated: true
image: false
lang: en
layout: post
title: π0.7 Robotic Model Overview
translated: false
type: note
---

**Question:** What is π0.7, and what are its key capabilities?

**Answer:**

π0.7 is the latest robotic foundation model from **Physical Intelligence (π)**, published April 16, 2026. It represents a meaningful step forward in general-purpose robotics — here's what makes it notable:

**What it is**

π0.7 is a general-purpose model that can perform a wide range of dexterous tasks with the same performance as fine-tuned specialist models, and crucially, it can follow new language commands and perform tasks that were never seen during training.

**Key breakthrough: Compositional Generalization**

π0.7 exhibits the first signs of *compositional* generalization — recombining skills from various tasks to solve new problems, such as using new kitchen appliances or enabling a new robot to fold laundry despite having no laundry-folding training data for that specific robot. This is analogous to how LLMs can combine concepts (e.g., "translate to French" + "format as JSON") — something prior robotic models couldn't reliably do.

**How it achieves this: Diverse Conditioning**

The key to π0.7's broad generalization is training with diverse multimodal prompts that describe not just *what* to do but *how* to do it — including language instructions, metadata (speed, quality), control modality labels, and visual subgoal images. This lets the model incorporate even suboptimal or autonomous training data without being corrupted by it.

**Cross-Embodiment Transfer**

π0.7 can fold laundry on a bimanual UR5e robot system even though no laundry-folding data was collected with that robot. Its success rate on this task matches the "zero-shot" success rate of expert human teleoperators attempting the same task on an unfamiliar platform — people with a mean of 375 hours of teleoperation experience.

**Matching Specialist Performance**

Rather than requiring separate fine-tuned specialist models for each task, the single π0.7 model can perform laundry folding, espresso making, and box folding to the same or even higher performance level as task-specific RL-trained specialists.

**References:**

- [π0.7: A Steerable Model with Emergent Capabilities](https://www.pi.website/blog/pi07) — Physical Intelligence
