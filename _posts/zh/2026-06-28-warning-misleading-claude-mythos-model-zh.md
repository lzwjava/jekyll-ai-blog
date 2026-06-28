---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 警告：误导性的Claude Mythos模型
translated: true
type: note
---

让我检查一下。这是一个来自名为 `empero-ai` 的用户/组织的第三方 GGUF 模型仓库，并非 Anthropic 或 Qwen 的官方内容。有几个值得注意的地方：

**它声称是什么：** 一个名为 "Qwythos" 的 9B 参数模型——这是一个合成词，暗示它基于 Qwen（标签为 `qwen3.5`），并以某种方式与 "Claude Mythos 5" 混合或命名。它宣称具有 1M 上下文、推理能力、视觉功能（存在 `mmproj` 文件）、函数调用，并带有 "uncensored" 标签。打包为 GGUF 量化格式（BF16、Q4_K_M 至 Q8_0），用于 llama.cpp/Ollama/LM Studio。

**为什么这个名称具有误导性：** "Claude Mythos 5" 在此被用作品牌宣传。Anthropic 的权重不存在任何合法途径能进入他人 Hugging Face 账户上的社区 GGUF 中——Anthropic 根本不发布开放权重。因此，以下情况之一为真：

- 这是一个 Qwen-3.5-9B 的衍生模型，有人**通过从 Claude 风格模型中抓取的输出进行蒸馏或微调**，然后命名以蹭热度。
- 这是纯粹的名称抢占——一个带有同人小说式 "Mythos" 角色微调的 Qwen 模型，配上一个吸引眼球的仓库标题。

无论哪种情况，名称中的 "Claude" 和 "Mythos" 都是营销手段，而非来源标识。Apache-2.0 许可证和 `qwen3.5` 标签暴露了实际基础。

**对你的实际参考意义：** 该模型规模与 Qwen-3.5-9B 视觉模型一致——17.9 GB BF16 对应约 9B 参数是合理的，Q4_K_M 5.63 GB 可以轻松放入你的 RTX 4070 的 12 GB 显存。如果你想尝试一下，在你的工作站上快速运行：

```bash
# 工作站 (192.168.1.36), 4070
llama-server -hf empero-ai/Qwythos-9B-Claude-Mythos-5-1M-GGUF:Q4_K_M -c 32768 --port 8080
```

我建议对其 1M 上下文和 "Claude Mythos" 的声称持高度怀疑态度，直到你自己进行基准测试——社区仓库经常夸大上下文长度（RoPE 缩放后，超出原生长度时性能严重下降），并贴上流行名称。请检查 README 中的 `n_ctx_train`，并在信任超过约 32–64K 的上下文之前运行 needle-in-haystack 评估。另外，`uncensored` + `cybersecurity` + `biomedical` 的标签组合也是常见的模式，即通过合并/微调来优化标签而非实质内容。

如果你告诉我你真正想要的是什么（长上下文检索、视觉、无审查的本地代理），我可以推荐 7–14B 范围内经过更好验证的替代方案。