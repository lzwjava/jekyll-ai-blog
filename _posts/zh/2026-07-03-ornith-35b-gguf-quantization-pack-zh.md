---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Ornith-35B GGUF量化包
translated: true
type: note
---

**问题：** Hugging Face 上的 `deepreinforce-ai/Ornith-1.0-35B-GGUF` 是什么？

**答案：**

这是一个全新的发布（该收藏集几小时前刚更新）。Ornith-1.0 是 DeepReinforce 团队推出的自改进开源模型系列，专为智能体编程而设计，而该特定仓库是 **35B-MoE 成员的 GGUF 量化包**——即适用于本地单 GPU/CPU 混合部署的 llama.cpp/Ollama 就绪构建。

关键信息：

**谱系与家族。** 该系列提供 9B-Dense、31B-Dense、35B-MoE 和 397B-MoE 四种尺寸，基于 Gemma 4 和 Qwen 3.5 进行后训练。GGUF 元数据确认 35B 为 `qwen35moe` 架构——因此它是一个 Qwen 3.5 MoE 基座模型，经过大量的 RL 后训练以用于编码智能体。采用 MIT 许可，无区域限制。

**有趣的部分——支架生成的 RL。** 训练框架使用 RL，模型不仅学习生成解决方案的展开（rollouts），还学习生成驱动这些展开的支架（scaffold）；通过联合优化支架和最终解决方案，模型发现了更好的搜索轨迹。这超越了标准的智能体 RL（如 GRPO-on-SWE-tasks 风格）：不再是固定外部框架（系统提示、工具循环、规划结构）而只优化其内部的策略，而是策略自身也生成其外部框架。从概念上讲，这是对智能体循环本身的元 RL——奖励信号同时流经支架选择及其诱导的轨迹。鉴于你对智能体架构的兴趣，deep-reinforce.com/ornith.html 上的博客值得一读，其中包含实际的目标公式。

**基准测试（根据模型卡片，自我报告）。** 35B 在 Terminal-Bench 2.1（Terminus-2）上得分为 64.2，而 Qwen3.5-35B 为 41.4；在 SWE-bench Verified 上得分为 75.6，而 Qwen3.5-35B 为 70——大致匹配 Qwen3.5 397B 的 76.4，而尺寸仅为后者的约 1/11。这是一个推理模型：助手回复以 `thinking… response` 块开头，服务配方启用推理解析器加 qwen3 工具调用解析器，以便 `<tool_call>` 块呈现为 OpenAI 风格的 `tool_calls`。通常注意事项：发布日卡片上的供应商报告数据；需等待独立的 Terminal-Bench 跑分。

**本仓库中的量化大小：** Q4_K_M 21.2 GB，Q5_K_M 24.7 GB，Q6_K 28.5 GB，Q8_0 36.9 GB，BF16 69.4 GB。

针对你的硬件：

- **RTX 4070（12 GB）电脑：** Q4_K_M 放不进显存，但这正是 MoE + llama.cpp 混合卸载大显身手的情况——每个 token 仅激活 35B 参数中的一小部分，因此借助 62 GB 内存，你可以将专家层放在 CPU 上，注意力/共享层放在 GPU 上（使用 `--n-gpu-layers` 部分卸载，或 `--override-tensor "exp=CPU"` 风格的专家卸载）。预计可用但 tok/s 不会很快。
- **MI300X（192 GB）：** 在 vLLM 下运行完整的 BF16 safetensors（`deepreinforce-ai/Ornith-1.0-35B`，非 GGUF 仓库），并添加 `--reasoning-parser qwen3 --tool-call-parser qwen3_xml`，然后将 OpenCode/OpenHands/你自己的 `ww`/`iclaw` 智能体指向 OpenAI 兼容端点。推荐采样参数：temp 0.6，top_p 0.95。
- **MacBook Air M2 16 GB：** 跳过；即使是 Q4 也太大。

在工作站上快速测试：

```bash
llama-server -hf deepreinforce-ai/Ornith-1.0-35B-GGUF:Q4_K_M -c 32768 --port 8000
# 然后将任何 OpenAI 兼容的智能体 CLI 指向 http://localhost:8000/v1
```

鉴于它明确针对终端编码智能体进行了优化（他们甚至将其作为支架在 Claude Code 内部进行了基准测试），它自然可以成为你 CLI 智能体栈中本地/低成本层级的一个候选。

**参考文献：**

- [deepreinforce-ai/Ornith-1.0-35B-GGUF · Hugging Face](https://huggingface.co/deepreinforce-ai/Ornith-1.0-35B-GGUF)
- [Ornith 博客 — DeepReinforce](https://deep-reinforce.com/ornith.html)
