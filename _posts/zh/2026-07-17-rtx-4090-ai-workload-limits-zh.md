---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RTX 4090 AI工作负载限制
translated: true
type: note
---

**问题：RTX 4090（24GB）在训练/推理负载方面实际有何优势，其真实规格/限制是什么？**

**答案：**

**芯片**：AD102（Ada Lovelace），台积电 4N（5nm 级）。16384 个 CUDA 核心，512 个第四代 Tensor Core，128 个第三代 RT Core。无 NVLink —— 这一点很关键，意味着如果将来使用多块 4090，将无法实现快速的 GPU 间互联，跨 GPU 通信只能依赖 PCIe 4.0 x16（双向约 32GB/s）。

**内存**：24GB GDDR6X，384-bit 位宽，带宽约 1008 GB/s。与你的 MI300X（192GB HBM3，约 5.3TB/s）相比，4090 的带宽约为其 1/5.3，容量为其 1/8。两者完全属于不同级别：4090 是准专业级推理/微调设备，MI300X 则是训练节点。

**算力**：密集 FP32 约 82.6 TFLOPS，密集 FP16 Tensor 约 165 TFLOPS（稀疏模式可达 330 TFLOPS），无实际意义的原生 FP64（1:64 比例，对科学计算无用）。TDP 450W，PCIe 4.0 x16。

**24GB 实际能承载的模型规模**：

```
# 经验法则：参数 * 每参数字节数 + KV缓存 + 激活值

# 7B 模型，fp16 推理
7e9 * 2 字节 = 14GB 权重
+ KV 缓存（随上下文增长，7B 模型 4k 上下文约需 1-2GB）
+ 激活值/开销
→ 轻松容纳，且有空间支持合理批大小

# 7B QLoRA 微调（4-bit 基座 + fp16 适配器）
7e9 * 0.5 字节 = 3.5GB 基座
+ 仅 LoRA 参数的优化器状态（很小）
+ 激活值
→ 轻松容纳，也可扩展到 13B QLoRA

# 13B 全参数 fp16 微调（权重 + 梯度 + Adam 状态）
13e9 * 2（权重）+ 13e9 * 2（梯度）+ 13e9 * 4*2（Adam m,v fp32）
≈ 26 + 26 + 104 = 远超 24GB
→ 若无卸载（DeepSpeed ZeRO-Offload / CPU）或 LoRA 则无法实现
```

因此，在单块 4090 上：全参数微调上限约为 1-3B 参数（使用梯度检查点可提升），QLoRA/LoRA 可舒适地支持 13B-34B 模型，纯推理（尤其是量化版本，如 GGUF/AWQ/GPTQ 4-bit）则能运行 30B-70B 模型，只需对速度有耐心，并使用 CPU 卸载溢出部分。

对于你的技术栈——训练 GPT-2 760M 对于这张卡来说简直是小菜一碟，即使在 fp32 精度下也能容纳大批量。如果在扩展到 MI300X 之前需要原型验证架构更改，4090 是合适的开发设备：迭代快、功耗低，且对于任何能容纳的模型，计算结果与数据中心显卡完全一致。

**实际注意事项**：4090 上的 GDDR6X 相比 HBM，每 GB 发热更大、功耗更高。在持续满载 Tensor Core 负载下，如果设备安装密集，需留意散热；若运行 24/7 无人值守训练任务，可使用 `nvidia-smi -pl` 限制功耗。

```bash
nvidia-smi --query-gpu=name,memory.total,memory.used,utilization.gpu,power.draw,temperature.gpu --format=csv
```

参考资料：
- [NVIDIA RTX 4090 规格](https://www.nvidia.com/en-us/geforce/graphics-cards/40-series/rtx-4090/)
- [Ada Lovelace 架构白皮书](https://images.nvidia.com/aem-dam/Solutions/geforce/ada/nvidia-ada-gpu-architecture.pdf)