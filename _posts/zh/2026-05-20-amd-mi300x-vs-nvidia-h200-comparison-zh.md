---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD MI300X 对比 NVIDIA H200
translated: true
type: note
---

**问题：** AMD MI300X 与 NVIDIA H200 相比如何？

**回答：**

## 规格对比：MI300X vs H200

| 指标 | AMD MI300X | NVIDIA H200 | 优胜者 |
|---|---|---|---|
| 架构 | CDNA 3 | Hopper | — |
| 显存 | **192 GB HBM3** | 141 GB HBM3e | **AMD** |
| 显存带宽 | **5.3 TB/s** | 4.8 TB/s | **AMD** |
| FP32 TFLOPS | **163** | 67 | **AMD** |
| FP16 TFLOPS | **326** | 134（含稀疏性为 989） | AMD 原始 / NVIDIA 实际 |
| INT8 TOPS | ~2,600 | **2,680** | **NVIDIA** |
| 热设计功耗 | 750W | 700W | NVIDIA |
| 云服务价格 | ~2.50美元/小时 | ~2.25美元/小时 | NVIDIA |

纸面规格上 AMD 明显占优，但实际情况更为复杂。

## 实际基准测试数据

### 推理（LLM 吞吐量）

在采用 Llama 3.1 8B 的多 GPU vLLM 基准测试中，MI300X 单 GPU 达到约 18,752 tokens/秒——约为 **H200 吞吐量的 74%**。2 GPU 时缩放效率为 95%，但 4 GPU 时降至 81%。

在低并发（约 250 个并发查询以下）场景下，H200 每次查询的输出速度更快、延迟更低。但在**高并发**下，MI300X 反超——峰值系统吞吐量更高，每 token 成本更低。

### 延迟

在所有测试配置中，H200 的延迟持续比 MI300X 低 37–75%。在 DeepSeek R1 上，H200 离线吞吐量为 6,311 tokens/秒，而 MI300X 为 4,574 tokens/秒。

### 训练

SemiAnalysis 长达 5 个月的深入分析表明：在公开稳定的 AMD 软件环境下，MI300X 的实际训练性能远落后于 H100/H200。在稳定版本上，**MI300X 每 TCO 的训练表现更差**——但使用 AMD 定制开发版本后情况有所改观。

Clarifai 的工程师发现，由于软件开销，MI300X 仅能达到 **H100/H200 性能的 37–66%**——但在内存密集型任务上可超越 H100，延迟降低高达 40%，某些模型吞吐量翻倍。

## 真实情况：软件是瓶颈

这是核心论点。MI300X 硬件具有竞争力或更优。ROCm 是需要付出的代价：

```
硬件规格：          AMD 胜出或持平
实际训练：          AMD 约为 H200 的 65-75%（稳定版 ROCm）
实际推理：          AMD 吞吐量约 74%，延迟比 H200 差 37-75%
内存密集型任务：    AMD 有时胜出（192GB 显存优势巨大）
每 token 成本：     高并发下 AMD 胜出
```

要让 MI300X 的训练性能达到 H100/H200 的 75% 以内，SemiAnalysis 付出了巨大努力——包括在 AMD 工程团队直接支持下从源码构建定制 Docker 镜像。

## MI300X 的真正优势领域

1. **192GB 显存**——可在单卡上以 BF16 运行 70B 模型。H200 无法做到（141GB）。
2. **高并发推理**——在大批次下，MI300X 反转成本方程
3. **内存密集型工作负载**——长上下文窗口、大型 KV 缓存
4. **可用性**——H200 稀缺；MI300X 库存充足（正如你所见）
5. **成本**——每小时价格更低，且通过 DigitalOcean 可访问 AMD Developer Cloud

## AMD 的发展路线图（对决策至关重要）

MI325X（2024 年第四季度上市）升级至 256GB HBM3e + 6TB/s 带宽。MI350X/MI355X（CDNA 4，台积电 3nm，2025 年出货）FP8 性能约达 4,600 TOPS——约为 **MI300X 的 1.8 倍**，在某些 FP8 训练基准测试中与 B200 基本持平。

ROCm 也在快速改进。在 Llama-2 70B LoRA FP8 上，MI355X 将训练时间从约 28 分钟（MI300X）缩短至略超 10 分钟——加速 2.8 倍，且结果与 B200/GB200 提交数据相差约 10% 以内。

## 你的决策矩阵

| 使用场景 | 推荐选择 |
|---|---|
| LoRA 微调（HF 栈） | MI300X ✅（可用且更便宜） |
| nanoGPT 规模训练 | MI300X ✅（PyTorch ROCm 没问题） |
| 自定义 CUDA 内核 | H200（别碰 ROCm） |
| 70B 模型推理 | **MI300X 胜出**（192GB 可容纳） |
| 低延迟服务 | H200 |
| 高吞吐批量推理 | 大规模下选 MI300X |
| 当前可用性 | **MI300X 胜出** |

## 结论

之前提到的“70%”数据对于与 H200 的推理吞吐量对比仍大致成立（约 74%）。训练方面可能更差（37–66%），也可能接近持平，具体取决于 ROCm 版本和工作负载。192GB 显存优势真实存在，对于大型模型工作至关重要。针对你的使用场景——LoRA 微调、Agent 工具、nanoGPT 规模的模型训练——**通过 AMD Developer Cloud 使用 MI300X 是一个务实的优质选择**，尤其考虑到 H200 的稀缺性。

**参考资料：**

- [AMD MI300X vs NVIDIA H200 — Spheron Blog](https://www.spheron.network/blog/amd-mi300x-vs-nvidia-h200/)
- [MI300X vs H100 vs H200 Benchmark: Training — SemiAnalysis](https://newsletter.semianalysis.com/p/mi300x-vs-h100-vs-h200-benchmark-part-1-training)
- [Multi-GPU Benchmark: B200 vs H200 vs H100 vs MI300X — AIMultiple](https://research.aimultiple.com/multi-gpu/)
- [Independent GPU Performance Analysis — Artificial Analysis](https://artificialanalysis.ai/articles/independent-analysis-of-leading-gpus-amd-nvidia)
- [MI300X vs B200 — Clarifai](https://www.clarifai.com/blog/mi300x-vs-b200)
