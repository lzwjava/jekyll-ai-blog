---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPU与sglang的不兼容性
translated: true
type: note
---

我已经克隆了它，但需要在这里停下，给你一个明确的答复，以免耗费10–15 GB的安装空间却无法运行。

## 我的操作
- ✅ 克隆到 `~/projects/sglang`（通过HTTPS——`git@` 的SSH克隆挂起，很可能那台机器没有配置GitHub SSH密钥）。

## 结论：sglang无法在这块GPU上运行

这块显卡是 **Tesla M40 = Maxwell架构，计算能力5.2**。sglang的安装和运行时都硬性要求更新的硬件：

| sglang 要求（来自 `python/pyproject.toml`） | 支持的最低GPU | M40 (sm_52) |
|---|---|---|
| `flashinfer_python[cu13]==0.7.0` | Ampere (sm_80+) | ❌ |
| `flash-attn-4>=4.0.0b18` | Ampere (sm_80+) | ❌ |
| `nvidia-cutlass-dsl[cu13]==4.8.0` | sm_80/90 目标 | ❌ |
| Triton（传递依赖） | Volta+ (sm_70+，实际为 sm_80+) | ❌ |
| `torch==2.13.0` (cu13) | sm_80 级别构建 | ❌/⚠️ |

整个代码库和文档都针对 **Hopper (sm_90) / Blackwell (sm_100/120)**；连Ampere在那里都算“老旧”了。Maxwell M40比最低要求落后了3–4代。

除此之外：
- **M40没有真正的FP16/BF16吞吐能力**（Maxwell的FP16速度约为常规的1/64）。现代LLM服务基于FP16/BF16，所以即使是“后备模式”也会慢得离谱。
- **12 GB显存**即使在兼容硬件上也只支持约7B-4bit模型。
- 这台机器还没有sudo权限，且只有Python 3.14（sglang/torch cu13的wheels目标为3.10–3.13）。

之前的烧机测试能运行，是因为我通过NVRTC编译了一个纯FP32的sm_52内核——但sglang的快速内核（FlashInfer/FA3/FA4/CUTLASS/Triton）完全没有sm_52的代码路径。它会在第一次内核启动时就失败，这是必然的。

## 针对这块M40的可行方案
1. **llama.cpp** — 唯一仍在Maxwell上运行的主流LLM运行时（其CUDA后端使用简单内核 + FP32/量化后备）。我可以设置它并实际服务一个小模型（如Qwen2.5-1.5B/3B、Llama-3.2-3B）——慢但可用。
2. **将M40用作FP32计算**（像烧机测试那样）——用于训练/数学工作负载，而非LLM服务。
3. 如果你非要sglang，需要 **任何Ampere+显卡**（RTX 3060 12GB或更好是最便宜的入门选择）。

需要我（a）仍然尝试完整安装，让你亲眼看到失败，还是（b）转向llama.cpp，在M40上实际服务一个模型？