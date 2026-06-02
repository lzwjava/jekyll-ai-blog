---
audio: false
generated: true
image: false
lang: en
layout: post
title: Other Image Models on Vertex AI
translated: false
type: note
---

While Imagen is the flagship family of image generation models from Google on Vertex AI, there are other options available, particularly if you're looking for different capabilities or open-source alternatives.

Here's a breakdown of other image-related models you can use on Vertex AI:

### Gemini Models (for multimodal use cases)

The Gemini family of models are multimodal, meaning they can process and understand multiple types of data, including text, images, video, and audio. While they are primarily known for their text-based outputs, some Gemini models have specific features for image-related tasks. For example, some Gemini models can:

* **Generate images** from a text prompt.
* **Edit images** using conversational instructions.
* **Perform visual question answering (VQA)**, where you can ask a question about an image and receive a text-based answer.
* **Generate descriptions** for a given image (image captioning).

This is a great option if you're building an application that needs to handle both text and images in a conversational or integrated way, rather than just generating an image from a simple prompt.

### Open-Source Models from Model Garden

Vertex AI's **Model Garden** is a centralized hub where you can discover, test, customize, and deploy a wide range of models, including both Google's proprietary models and a curated selection of open-source models. This is where you'll find alternatives to Imagen, such as:

* **Llama 3-Vision**: A family of multimodal models that are optimized for visual recognition, image reasoning, and captioning.
* **Flux**: A rectified flow transformer model that generates high-quality images from text descriptions.
* **Instant ID**: An identity-preserving, text-to-image generation model. This is useful for generating new images of a specific person or subject while maintaining their key identity features.

These open-source models often come with different licensing terms, performance characteristics, and customization options, giving you more flexibility for specific use cases.

### Other Vision-Related Models

Beyond image generation, Vertex AI offers pre-trained models for a variety of vision tasks, which you might find useful:

* **Multimodal Embeddings**: Generates vector representations of images, which you can use for tasks like image search (finding similar images), classification, or clustering.
* **Vertex AI AutoML Image**: Allows you to train your own custom machine learning models for image classification, object detection, and image segmentation without writing any code.
* **Video models (Veo)**: While not an image model, Veo allows you to generate high-quality videos from text or image prompts. It's a powerful tool for media creation that extends beyond still images.
