---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在MI300X上运行Qwen3.5-122B
translated: true
type: note
---

问题：`unsloth/Qwen3.5-122B-A10B-MTP-GGUF` 模型能否在 AMD MI300X GPU 上使用 llama.cpp 运行？

答案：

让我们用数据仔细分析一下：

---

### **1. 模型规格**

* **Qwen3.5-122B** → 1220亿参数
* **A10B-MTP** → 可能指混合精度量化（可能是10位或自定义） + MTP（多任务预训练）
* **GGUF格式** → 与 `llama.cpp` 兼容

**预估内存占用：**

* 密集 FP16：122B × 2 字节 ≈ 244 GB
* 使用 **Q4_K / 4位量化**：约为 FP16 的 30–35% → ~73–85 GB
* 使用 **A10B-MTP（10位 + 压缩）**：可能降低至 **~90–95 GB**，根据 KV 缓存和上下文长度可能略高

> MI300X 拥有 **192 GB 显存**，因此 **理论上单实例可将此模型装入 GPU 内存**。

---

### **2. Token 上下文考量**

* `llama.cpp` 需要额外显存用于：

  * **KV 缓存** → 随 `上下文长度 × 隐藏层大小 × 层数` 增长
  * **中间激活值 / 工作内存**
* 在 **典型 4K–8K 上下文**下，可能需要 **~30–50 GB 额外显存**。

**预估总显存用量：**

```
模型权重（~90–95 GB）+ KV 缓存与缓冲区（~50 GB）≈ 140–145 GB
```

* 剩余约 50 GB 余量 → 适合 8K–16K 上下文
* 对于 **极长上下文（>50K tokens）**，将触及内存上限

---

### **3. 吞吐量（tg128）预期**

* MI300X 的 token 生成受 **内存带宽限制**
* 基于 70B 级别基准测试（40–45 GB 权重 → 45 t/s）粗略估算：

  * 模型大小约 2 倍 → 吞吐量大致减半 → **20–25 tokens/秒**
* 因此，**Qwen3.5-122B-A10B-MTP 在 MI300X 上的实际吞吐量**：**单 GPU 实例约 20–25 t/s**

---

### **4. 实用建议**

1. **使用 Q4_K 或 A10B-MTP 量化** → 减少显存占用
2. **保持合理的上下文长度**（≤16K tokens）以确保稳定运行
3. **在 llama.cpp 中启用 flash attention** → 减少内存压力，提升速度
4. **多实例 / 批处理** → MI300X 显存足够同时运行 2–3 个较小序列以提高吞吐量

> ✅ 结论：**在单块 MI300X 上使用 llama.cpp 运行 unsloth/Qwen3.5-122B-A10B-MTP-GGUF 是可行的**，但预期吞吐量为 **中等水平（约 20–25 t/s）**，并需相应规划上下文长度。

---

参考链接：

* [llama.cpp GGUF 格式](https://github.com/ggml-org/llama.cpp)
* [AMD ROCm MI300X llama.cpp 基准测试](https://github.com/ggml-org/llama.cpp/discussions/14640)
* [Hugging Face：Qwen3.5-122B-A10B-MTP](https://huggingface.co/unsloth/Qwen3.5-122B-A10B-MTP-GGUF)

---

如果您需要，我可以专门针对此 122B GGUF 模型在 MI300X 上，制作一份 **不同上下文长度的显存映射 + token 吞吐量预估表**，以便您精确规划使用。需要我这么做吗？
