---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RAG中的两种GPU消费者
translated: true
type: note
---

## `rag/` 如何使用 GPU

此代码库中**恰好**有两个 GPU 消费者，且都**不是**检索计算。

**1. 嵌入模型（`build_index.py` + `retriever.py`）**

- `build_index.py` → `load_encoder()`（`retriever.py:239`）调用 `SentenceTransformer(model, device=device)`。`--device` 默认为 `None`，因此 sentence-transformers 在可用时自动选择 `cuda:0`（探测日志确认 `dim=1024, device=cuda:0`）。
- 以 **fp32** 运行（无 `model.half()`），使用 `--batch-size 32`。`--fp16` 仅控制写入 `embeddings.npy` 的数据类型，不涉及计算数据类型。
- 在 RTX 4070 上测得（`logs/probe_bge_m3.log`）：使用 bge-m3、批大小 32 时，**63–67 块/秒**。完整构建 186,263 块约需 **50 分钟** GPU 时间。
- 查询时，`Retriever.encode_query()` 懒加载*相同*编码器到 GPU，并嵌入单个查询。

**2. 答案生成（`rag_chat.py`）**

- `--backend llama`（默认）：llama.cpp 加载 `lzw-notes-merged.Q4_K_M.gguf`（2.5 GB），使用 `--n-gpu-layers -1` → **所有**层在 GPU 上。
- `--backend hf`：`AutoModelForCausalLM.from_pretrained(..., torch_dtype=bfloat16, device_map="auto")` → 整个 Qwen3-4B 以 bf16（约 8 GB）在 GPU 上。
- `--backend vllm`：`gpu_memory_utilization=0.85`。

**不在 GPU 上：**

- 稠密搜索使用 **`faiss-cpu` 1.15.1** 中的 `faiss.IndexFlatIP`（`has_gpu=False`），以及 NumPy 回退——两者均在 CPU 上。BM25 同样为纯 NumPy CPU 计算。
- 索引本身（`embeddings.npy` 286 MB，`index.faiss` 286 MB，`chunks.jsonl` 294 MB）位于**系统 RAM**，而非 VRAM。`Retriever.__init__` 将全部 186k 条 JSON 记录解析为 Python 字典列表——这才是真正的主机 RAM 开销（约 1–1.5 GB 堆）。

## VRAM 使用取决于什么

| 组件 | 取决于 | 当前数值 |
| --- | --- | --- |
| 嵌入权重 | 模型 × 数据类型 | e5-small 118M → **0.47 GB** fp32；bge-m3 568M → **2.27 GB** fp32（4.3 GB 缓存目录包含重复的 `pytorch_model.bin`） |
| 嵌入激活 | 批大小 × 序列长度 × 隐藏维度 × 深度 | 块平均 458 字符 ⇒ 较短；批大小 32 ⇒ 数百 MB（bge-m3 fp32 峰值约 2.5–3.5 GB） |
| LLM 权重 | 参数 × 量化 | Qwen3-4B Q4_K_M = **2.5 GB**；bf16 HF = **约 8 GB** |
| KV 缓存 | `2 × 层数 × KV 头数 × 头维度 × 上下文 × 2 B` | 36 × 8 × 128 ⇒ **每 token 144 KiB** ⇒ 8k 时 1.2 GB，16k 时 2.4 GB，40k 时 6 GB |
| 计算缓冲/开销 | 后端 | llama.cpp 约 0.5–1 GB；vLLM 预留 85% 显存 |
| 共存 | 两个模型同时加载 | e5 0.5 **+** LLM 约 4.5 ≈ **5 GB**；bge-m3 2.5 **+** LLM ≈ **7–8 GB** |

因此 VRAM ≈ `嵌入权重 + 嵌入激活 + LLM 权重 + KV 缓存（上下文）+ 缓冲`。影响最大的两个旋钮是 **`--ctx`**（与 KV 缓存线性相关）和 **`--batch-size`**（索引期间激活）。这就是 README 目标为 12 GB 的原因——当前 `nvidia-smi` 显示已用 8.2 GB，仅剩约 3.2 GB 空闲。

## 更强的 GPU 有帮助吗？

有，但仅对两个 GPU 阶段有效——而且提升幅度差异很大：

- **索引构建：~线性扩展。** 4070 上 63 块/秒 → 4090（约 2 倍带宽/计算）≈ 2 倍，H200 ≈ 4–6 倍。必须提高 `--batch-size`（64–128）以保持更大显卡饱和。切换到 `intfloat/multilingual-e5-small` 是更大、更便宜的优势（约 5 倍，见 README），优于 GPU 升级。
- **生成：真正的回报。** 4B Q4 模型的单流解码受内存带宽限制（每 token 读取 2.5 GB）：4070 = 504 GB/s，4090 ≈ 1 TB/s，H100/H200 ≈ 3.35–4.8 TB/s。预计 token/s 约提升 2 倍 / 4–6 倍，且预填充（计算受限）扩展更好。大 GPU 还能通过连续批处理使 `--backend vllm` 对并发用户更值得。
- **检索：几乎没有好处。** 186k × 384 维的 `IndexFlatIP` 为 71M MACs——CPU 上约 10–30 ms，已远低于 LLM 延迟。投入更大的 GPU 毫无意义；若未来在意，可安装 `faiss-gpu`（节省 1–2 ms）或切换到 IVF/HNSW（用于数百万块）。GPU 在检索中的唯一作用是嵌入单个查询（约 10–30 ms）。

**结论：** 对于单查询交互使用，约 90%+ 的延迟来自 LLM，因此更快的 GPU 大致按内存带宽比例加速回答。对于离线索引构建，更快的 GPU 线性提升，但更小/更快的嵌入模型或 fp16 计算是比硬件更好的杠杆。