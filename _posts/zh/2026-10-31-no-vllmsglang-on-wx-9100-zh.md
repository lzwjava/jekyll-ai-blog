---
audio: false
generated: true
image: false
lang: zh
layout: post
title: WX 9100上不支持vLLM/SGLang
translated: true
type: note
---

简短回答：**不，实际上不行。** WX 9100（Vega 10，`gfx900`）不在 vLLM 和 SGLang 的受支持硬件范围内，并且这台机器的 ROCm 7.1 缺少它们所依赖的内核。

## 证据

**1. vLLM 官方 ROCm 支持列表**（来自上游文档）：
> GPU：MI200s（gfx90a）、MI300（gfx942）、MI350（gfx950）、Radeon RX 7900（gfx1100/1101）、RX 9000（gfx1200/1201）、Ryzen AI MAX / AI 300（gfx1151/1150）

`gfx900` 不在其中。同样地，SGLang 的 ROCm 路径也仅限于 CDNA（MI210/250/300）加上 RDNA3。

**2. 此机器上的 rocBLAS 没有 gfx900 内核** — 我们在 llama.cpp 中已经遇到了同样的障碍：

```
available TensileLibrary: gfx908, gfx90a, gfx942, gfx1030, gfx1100, gfx1101, gfx1151, gfx1200, gfx1201
```

没有 `gfx900`。vLLM/SGLang 依赖于 PyTorch → hipBLAS/rocBLAS，因此它们会以相同的方式（或更早）失败。

**3. 没有适用于 gfx900 的 PyTorch ROCm wheel。** 官方 `torch` ROCm wheel 不包括 `gfx900`，因此即使是在此处开箱即可使用的普通 PyTorch on GPU 也不可用（已确认：未安装 `torch`）。

**4. 没有矩阵核心。** MFMA（矩阵引擎）随着 `gfx908`/CDNA1 出现；WMMA 随着 RDNA 出现。Vega 的 GCN **两者都没有**，vLLM/SGLang 的 paged attention 和 GEMM 内核是为这些单元编写的。即使从源代码构建也无法生成可工作的内核。

## 这意味着什么

| 选项 | WX 9100 (gfx900) |
| -------- | ------------------ |
| llama.cpp (HIP, MMQ) | ✅ **已正常工作** |
| Ollama | ✅ （底层是 llama.cpp） |
| vLLM | ❌ 不支持 |
| SGLang | ❌ 不支持 |
| PyTorch GPU（官方 wheel） | ❌ 没有 gfx900 版本 |
| PyTorch 从源代码构建 + 旧版 ROCm | ⚠️ 可能但工作量巨大，仍然没有 vLLM |

好消息：您已经在运行的 `llama-server` **就是** 此 GPU 的 vLLM 风格服务路径——它提供了一个与 OpenAI 兼容的 `/v1` API、Web UI、连续批处理（多个插槽）和 32K 上下文。这涵盖了实际用例。

如果您特别需要 vLLM/SGLang（paged attention、非常高的并发性、tensor parallel across many GPUs），那么您需要更换为 **CDNA 卡**——MI210/MI250（gfx90a）或 MI300（gfx942）。您提到的 MI25 也是 `gfx900`，因此尽管有“Instinct”名称，但它将具有相同的限制。
