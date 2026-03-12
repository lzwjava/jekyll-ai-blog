---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hot Diffusion & FaceSwap Projects 2025
translated: false
type: note
---

I'll search for hot diffusion and face swap projects on GitHub that work with vision transformers and image generation.Now let me search for face swap projects:Now let me search more specifically for trending projects and recent releases:---

## Question

What are the hot diffusion projects or faceswap projects that can learn vision transformer and image generation on GitHub?

## Answer

Based on current research and trending projects on GitHub, here are the most notable diffusion and face swap projects with vision transformer and image generation capabilities:

### **Top Diffusion Projects with Vision Transformers**

**1. DiffiT (Diffusion Vision Transformers for Image Generation)**

DiffiT is an official NVIDIA repository that combines the expressive power of diffusion models with Vision Transformers (ViTs), introducing Time-dependent Multihead Self Attention (TMSA) for fine-grained control over denoising at each timestep, achieving state-of-the-art performance on class-conditional ImageNet generation with an FID score of 1.73 on ImageNet-256. The code and pretrained models are publicly released.

**2. Latte (Latent Diffusion Transformer for Video Generation)**

Latte is accepted by Transactions on Machine Learning Research (TMLR) 2025 and is now integrated into diffusers library, supporting inference with 4/8-bit quantization to reduce GPU memory from 17 GB to 9 GB. It enables both text-to-image and text-to-video generation with transformer architecture.

**3. Diffusion-4K (Ultra-High-Resolution Image Synthesis)**

Diffusion-4K is a CVPR 2025 project that presents a novel framework for direct ultra-high-resolution image synthesis using text-to-image diffusion models, introducing the Aesthetic-4K Benchmark for evaluating 4K image generation with metrics like GLCM Score and Compression Ratio.

**4. DiT4SR (Diffusion Transformer for Real-World Image Super-Resolution)**

DiT4SR is an ICCV 2025 official PyTorch implementation for real-world image super-resolution using diffusion transformers.

**5. Diffusion Forcing Transformer (History-Guided Video Diffusion)**

This ICML 2025 project introduces the Diffusion Forcing Transformer (DFoT), a novel video diffusion model designed to generate videos conditioned on arbitrary numbers of context frames, with an interactive demo available on HuggingFace Spaces for generating videos from images or extending single images into long videos.

---

### **Top Face Swap Projects**

**1. DeepFuze (ComfyUI Integration)**

DeepFuze is a state-of-the-art deep learning tool that seamlessly integrates with ComfyUI to provide facial transformations, lipsyncing, face swapping, lipsync translation, video generation, and voice cloning, supporting 17 languages for voice cloning including English, Spanish, French, German, Chinese, Japanese, and more.

**2. Wunjo CE (Open Source, All-in-One Solution)**

Wunjo CE is an open-source, locally-run tool offering face swap, lip sync, object removal, text and background removal, restyling, audio separation, voice cloning, and video generation, with version 2.0 introducing a redesigned interface, enhanced face swap functionality, a non-existent people face generator, and a deepfake analyzer.

**3. REFace (Diffusion-Based Face Swapping)**

REFace is the official implementation of "Realistic and Efficient Face Swapping: A Unified Approach with Diffusion Models" accepted at WACV 2025 as an oral presentation, reframing face-swapping as a self-supervised train-time inpainting problem and introducing multi-step Denoising Diffusion Implicit Model (DDIM) sampling during training to reinforce identity and perceptual similarities.

**4. FaceSwap (Comprehensive Framework)**

A comprehensive face swapping system using deep learning with training pipeline, production API, and dataset management tools, supporting multi-face handling, enhanced face detection with retry mechanisms, video processing with temporal consistency, and Docker containerization with GPU support.

---

### **Key Learning Resources**

The GitHub repository "Transformer-in-Computer-Vision" maintains a categorized collection of diffusion and vision transformer papers including recent works like DiTCtrl for multi-prompt video generation, GS-DiT for pseudo 4D Gaussian fields, Magic Mirror for ID-preserved video generation, and ConceptMaster for multi-concept video customization.

These projects represent the cutting edge of vision transformer integration with diffusion models and face manipulation technology, offering both research implementations and production-ready tools for image generation, video synthesis, and face swapping applications.

---

## References

- [DiffiT - NVIDIA GitHub](https://github.com/NVlabs/DiffiT)
- [Latte - Video Diffusion Transformer GitHub](https://github.com/Vchitect/Latte)
- [Diffusion-4K GitHub](https://github.com/zhang0jhon/diffusion-4k)
- [DiT4SR GitHub](https://github.com/Adam-duan/DiT4SR)
- [Diffusion Forcing Transformer GitHub](https://github.com/kwsong0113/diffusion-forcing-transformer)
- [DeepFuze ComfyUI GitHub](https://github.com/SamKhoze/ComfyUI-DeepFuze)
- [Wunjo CE GitHub](https://github.com/wladradchenko/wunjo.wladradchenko.ru)
- [REFace GitHub](https://github.com/sanoojan/reface)
- [FaceSwap Comprehensive GitHub](https://github.com/kobewangSky/FaceSwap)
- [Transformer-in-Computer-Vision GitHub](https://github.com/Yangzhangcst/Transformer-in-Computer-Vision)