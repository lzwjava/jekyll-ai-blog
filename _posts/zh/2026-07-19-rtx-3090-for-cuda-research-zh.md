---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RTX 3090 用于 CUDA 研究
translated: true
type: note
---

问题：用于本地MoE/注意力架构研究、复现Kimi K2 Thinking技术、以及将前沿技巧移植到小型模型时，应选择RX 7900 XT还是RTX 3090？考虑到RTX显卡二手价格更贵（8000-10000元人民币）？

答案：购买3090。对于你的具体用例，两者差距明显，无需犹豫。

**具体原因如下：**

1. **你将要复现的所有前沿仓库都优先支持CUDA。** Kimi K2 Thinking、DeepSeek-V3/R1的MoE内核、任何FlashAttention-3变体、Mamba/线性注意力仓库——全都假设使用`torch.cuda`、自定义CUDA内核（通常用原生CUDA或面向NVIDIA的Triton编写），以及用于量化的`bitsandbytes`/`exllamav2`。ROCm的移植版本落后好几个月，而且对于研究代码（与Ollama/vLLM等已移植的生产推理栈不同）常常无法编译。

2. **NVLink对你的MoE探索至关重要。** 两块3090通过NVLink可提供约112 GB/s的带宽，而AMD侧仅通过PCIe提供约32 GB/s。3090配备NVLink，而7900 XTX在多GPU场景下受限于PCIe——因为没有跨厂商的张量并行，Radeon也没有NVLink的等效方案。对于在两块显卡上进行专家并行或张量并行的MoE-on-small-models实验，这是一个真正的瓶颈差异，而非基准测试中的脚注。

3. **你实际会用到的生态工具仅支持CUDA。** AMD侧没有TensorRT-LLM，也没有ExLlamaV2——你无法在那里使用最快的单卡INT4推理路径。对于“在拼凑的硬件上探索最佳可用本地模型”（你的第4点），ExLlamaV2 + GPTQ/AWQ在CUDA上仍然是每美元最快的路径。

4. **AMD真正有优势的地方——并不适用于你。** MoE模式（如Qwen3-Coder、Gemma 4风格）在24GB的Radeon显卡上表现良好，因为每个token只激活几十亿参数——这纯粹是推理层面的论点。而你要做的是研究复现和内核级实验，CUDA的工具成熟度在此占据主导地位。

5. **对照你的人民币价格进行现实检验：** 二手RTX 3090在美国市场售价约749美元（约5400元人民币），比二手RX 7900 XTX便宜100美元，且在美国二手市场上推理速度约快32%。你提到的8000-10000元人民币是中国的市场价格（NVIDIA的进口/关税溢价），因此你听到的“AMD更便宜”的说法并不像看起来那么有力——在假设AMD有折扣之前，请先核对当地实际报价。

**你关于“ROCm了解肤浅”的判断是正确的，这并非坏事**——ROCm当前真正的价值在于生产环境下的*推理*服务（vLLM/Ollama），以更低的每GB显存成本运行，而非研究复现。对于你列表中的目标1、2、3、5，你需要的是论文代码所针对的显卡。目标4（老旧显卡本地模型“捡垃圾”）是AMD真正值得日后尝试的领域，但不要将其作为你的主力卡。

**实用建议：** 先买一块3090，运行以下命令验证：

```bash
python -c "import torch; print(torch.cuda.get_device_name(0), torch.cuda.get_device_capability(0))"
nvidia-smi --query-gpu=name,memory.total,power.limit --format=csv
```

如果后续你的MoE/注意力实验需要多GPU专家并行，再添加第二块3090通过NVLink连接——在大多数市场仍比一块4090便宜，而且你列出的整个技术栈（Kimi验证、内核移植、注意力架构对比）都能保持CUDA原生工具链。

参考链接：
- [ROCm vs CUDA for Local AI in 2026: The Software Gap](https://insiderllm.com/guides/rocm-vs-cuda-local-ai-2026/)
- [Radeon RX 7900 XTX for Local AI 2026 — Local AI Master](https://localaimaster.com/blog/radeon-7900-xtx-local-ai)
- [AMD vs NVIDIA for Local AI Inference in 2026 — GPU Hunter](https://www.gpuhunter.io/blog/amd-vs-nvidia-local-ai-2026)