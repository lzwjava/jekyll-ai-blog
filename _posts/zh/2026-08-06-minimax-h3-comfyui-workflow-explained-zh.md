---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MiniMax H3 ComfyUI工作流详解
translated: true
type: note
---

**问题：** 这个 MiniMax H3 ComfyUI 工作流程实际上是如何端到端工作的——模型架构、节点图机制，以及每个阶段的作用？

**答案：**

你的分析很准确。以下是底层模型和流水线的机制。

**模型架构** — MiniMax H3 是一个 331 亿参数密集单流全模态 transformer，使用 Qwen3-VL-32B 文本编码器，于 2026 年 8 月 3 日根据 MiniMax H3 社区许可协议开源。此次开源发布了两个任务检查点：FL2VA（文生视频及首/末帧条件控制）和 Ref2VA（基于参考的生成）——你的文件使用的是 Ref2VA（`minimax_h3_ref2va_pruned_int8_convrot.safetensors`），这解释了为什么工作流具有图像参考和多图像参考流水线，但没有首/末帧变体。

关键设计选择（与图结构形状相关的原因）：
- 使用三维多模态旋转位置编码（MM-RoPE）来表示跨时间维度和两个空间维度 (t, h, w) 的位置关系——这就是为什么分辨率和帧数设置会直接馈送到条件控制中，而不仅仅是采样器。
- 模态特定的自适应层归一化（AdaLN）以相对较低的额外训练和推理成本提升了生成质量——你所拥有的“经过剪枝的 INT8”检查点特别地预计算了 adaLN 曲线表，体积缩小约 40%。
- 音频并非事后添加：32 kHz 立体声与画面在同一轮次中生成，无需独立的音频模型——因此，单独的音频 VAE（`minimax_h3_audio_vae_fp32.safetensors`）从相同的潜空间解码，而不是采用后期文本转语音/拟音步骤。
- 2K 输出并非超分辨率模块：对于 H3 的 2K 分辨率输出，我们没有使用传统的专用超分辨率模块，而是让 H3 基础模型通过上下文内方式重新生成其自身的低分辨率结果。根据 ComfyUI 维基百科，该重新生成步骤（`H3-Regenerate-2K`）仅为 API 调用——H3-Context-IR 预处理系统和 H3-Regenerate-2K 升频模块仍是托管的 API——因此，除非你将数据输出到它们的托管端点，否则你的本地工作流上限是基准的 768p，而非 2K。

**图机制（每个模块存在的原因）：**

```
Models          → 加载 UNET（扩散Transformer）+ CLIP（Qwen3VL-32B 文本编码器）+ 视频 VAE + 音频 VAE
Conditioning    → 文本提示 / 图像参考 / 多图像参考 → 经由 CLIP 编码 → MM-RoPE 感知嵌入
Sampling        → 扩散Transformer去噪循环，基于以上条件 + 分辨率选择器输出进行控制
Decode+Create   → 视频 VAE 解码潜变量 → 帧；音频 VAE 解码 → 波形；通过 VideoHelperSuite/KKVideo 进行混流
User Inputs     → 提示文本、分辨率选择、帧数（124 @ 匹配模式 = 24-25fps 下约 5 秒）
Prompt templates→ 提示词模版组只是一个静态文本块，馈送到一个 LLM（外部，通过 API 节点或手动输入），
                  用于将你的简短提示扩展为 H3 期望的结构化导演风格提示
Switch (开关)   → rgthree Fast Groups Bypasser——实际上只是启用/禁用节点组，以便你可以在一个 JSON 文件中
                  维护 3 条流水线（文生视频、单参考、多参考），并通过切换运行哪个子图而无需重新布线。
```

“提示词模版”并非 ComfyUI 节点功能——它们只是纯文本块，旨在粘贴到 LLM 聊天中（或如果你有，则连接到 API 调用节点），因为 H3 对于结构化的、镜头列表风格的提示（镜头、主体、光照、运动）响应远好于单个简短的句子。鉴于提示最多可达 7000 个字符，模版的存在是为了帮助你实际填满这个预算，而不是浪费模型的上下文窗口。

**要实际运行它**，你需要：
```bash
# 自定义节点
git clone https://github.com/Comfy-Org/ComfyUI.git  # H3 支持已直接合并（PR #15224）
# 或者如果使用单独的节点包：
comfy node install rgthree-comfy
comfy node install comfyui-videohelpersuite

# 模型（来自 Comfy-Org/MiniMax-H3 重新打包的仓库）
models/diffusion_models/minimax_h3_ref2va_pruned_int8_convrot.safetensors
models/text_encoders/qwen3vl_32b_minimax_h3_int8_convrot.safetensors
models/vae/minimax_h3_video_vae_fp16.safetensors
models/vae/minimax_h3_audio_vae_fp32.safetensors
```

考虑到你已经在本地运行 MI300X——即使是在 768p/124 帧的设置下，经过剪枝的 INT8 + int8 文本编码器也应该能轻松容纳在一块 GPU 的显存中；密集的 33B transformer 是内存瓶颈，而非 VAE。

原生支持与开源同日落地：原生 ComfyUI 支持已于同一天合并（Comfy-Org/ComfyUI #15224），因此这个工作流文件是当前的，而非围绕旧 API 的过时社区支架。

参考资料：
- [MiniMax H3 开源公告](https://www.minimax.io/news/minimax-h3-open-source)
- [MiniMax H3 ComfyUI 维基百科 — 原生支持、检查点](https://comfyui-wiki.com/en/models/minimax)
- [fal.ai 上的 MiniMax H3 — 功能、提示长度](https://fal.ai/minimax-h3)
- [MiniMax H3 开发者指南](https://blog.4sapi.com/blog/minimax-h3-open-source-video-model)