---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 热门扩散与换脸项目 2025
translated: true
type: note
---

我会搜索 GitHub 上与 vision transformers 和 image generation 相关的热门 diffusion 和 face swap 项目。现在让我搜索 face swap 项目：现在让我更具体地搜索 trending projects 和 recent releases：---

## 问题

GitHub 上有哪些热门 diffusion 项目或 faceswap 项目，可以学习 vision transformer 和 image generation？

## 回答

根据当前研究和 GitHub 上的 trending projects，以下是最值得注意的 diffusion 和 face swap 项目，这些项目具有 vision transformer 和 image generation 功能：

### **顶级 Diffusion 项目，支持 Vision Transformers**

**1. DiffiT (Diffusion Vision Transformers for Image Generation)**

DiffiT 是 NVIDIA 的官方仓库，将 diffusion models 的表现力与 Vision Transformers (ViTs) 结合，引入 Time-dependent Multihead Self Attention (TMSA)，以实现每个 timestep 的精细 denoising 控制，在 class-conditional ImageNet 生成上达到了 state-of-the-art 性能，ImageNet-256 的 FID score 为 1.73。代码和预训练模型已公开发布。

**2. Latte (Latent Diffusion Transformer for Video Generation)**

Latte 被 Transactions on Machine Learning Research (TMLR) 2025 接受，现已集成到 diffusers library 中，支持 4/8-bit quantization 推理，将 GPU 内存从 17 GB 减少到 9 GB。它使用 transformer architecture 支持 text-to-image 和 text-to-video 生成。

**3. Diffusion-4K (Ultra-High-Resolution Image Synthesis)**

Diffusion-4K 是 CVPR 2025 项目，提出了一种新型框架，用于使用 text-to-image diffusion models 直接进行 ultra-high-resolution image synthesis，引入 Aesthetic-4K Benchmark 用于评估 4K image generation，指标包括 GLCM Score 和 Compression Ratio。

**4. DiT4SR (Diffusion Transformer for Real-World Image Super-Resolution)**

DiT4SR 是 ICCV 2025 的官方 PyTorch 实现，用于真实世界 image super-resolution 的 diffusion transformers。

**5. Diffusion Forcing Transformer (History-Guided Video Diffusion)**

此 ICML 2025 项目引入 Diffusion Forcing Transformer (DFoT)，一种新型 video diffusion model，可根据任意数量的 context frames 生成视频，并在 HuggingFace Spaces 上提供 interactive demo，用于从图像生成视频或将单张图像扩展为长视频。

---

### **顶级 Face Swap 项目**

**1. DeepFuze (ComfyUI Integration)**

DeepFuze 是一款 state-of-the-art 深度学习工具，与 ComfyUI 无缝集成，提供 facial transformations、lipsyncing、face swapping、lipsync translation、video generation 和 voice cloning，支持 17 种语言的 voice cloning，包括 English、Spanish、French、German、Chinese、Japanese 等。

**2. Wunjo CE (Open Source, All-in-One Solution)**

Wunjo CE 是一款开源、本地运行的工具，提供 face swap、lip sync、object removal、text and background removal、restyling、audio separation、voice cloning 和 video generation，2.0 版本引入重新设计的界面、增强的 face swap 功能、非真实人物面部生成器，以及 deepfake analyzer。

**3. REFace (Diffusion-Based Face Swapping)**

REFace 是“Realistic and Efficient Face Swapping: A Unified Approach with Diffusion Models”的官方实现，该论文被 WACV 2025 接受为 oral presentation，将 face-swapping 重新定义为 self-supervised train-time inpainting 问题，并在训练期间引入 multi-step Denoising Diffusion Implicit Model (DDIM) sampling 以强化 identity 和 perceptual similarities。

**4. FaceSwap (Comprehensive Framework)**

一个全面的 face swapping 系统，使用 deep learning 配备 training pipeline、production API 和 dataset management tools，支持 multi-face handling、增强的 face detection（带 retry mechanisms）、带 temporal consistency 的 video processing，以及带 GPU 支持的 Docker containerization。

---

### **关键学习资源**

GitHub 仓库“Transformer-in-Computer-Vision”维护了一个分类的 diffusion 和 vision transformer 论文集合，包括最近的作品，如 DiTCtrl 用于 multi-prompt video generation、GS-DiT 用于 pseudo 4D Gaussian fields、Magic Mirror 用于 ID-preserved video generation，以及 ConceptMaster 用于 multi-concept video customization。

这些项目代表了 vision transformer 与 diffusion models 以及 face manipulation technology 的前沿集成，提供研究实现和 production-ready tools，用于 image generation、video synthesis 和 face swapping 应用。

---

## 参考文献

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
