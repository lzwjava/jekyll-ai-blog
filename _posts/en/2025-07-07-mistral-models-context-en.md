---
audio: false
generated: true
lang: en
layout: post
title: Mistral AI's 2025 Model Context Lengths
translated: false
type: note
---

As of June 2025, Mistral AI has released several models with varying context lengths. Here's a summary of some of the key models and their context windows:

* **Magistral Small (magistral-small-2506):** This open-weight model has a 128k context window, though performance might degrade past 40k, so a recommended maximum length is 40k tokens.
* **Magistral Medium (magistral-medium-2506):** This API-only reasoning model also has a recommended context window of 40k.
* **Mistral Small 3.1 (mistral-small-2503) / Mistral Small 3.2 (mistral-small-2506):** These models feature a context window of up to 128,000 tokens.
* **Codestral (codestral-2501):** This code-focused model boasts a significant context window of 256,000 tokens.
* **Mistral Large 2 (mistral-large-2407 / mistral-large-2411):** Mistral's flagship large model has a 128k context window.
* **Mistral NeMo (open-mistral-nemo-2407):** This 12B model, developed in collaboration with NVIDIA, offers a large context window of up to 128,000 tokens.
* **Mistral Medium 3 (mistral-medium-2505):** This multimodal model also supports a 128k context window.

It's important to note that while some models advertise very large context windows (e.g., 128k), the practical performance might be optimized for a slightly smaller range (e.g., 40k for Magistral models).
