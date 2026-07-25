---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Torch编译FLUX模型失败
translated: true
type: note
---

![Cat HD](cat_hd.png)

以下是事件经过及经验总结：

---

## 🔍 `torch.compile` 的问题出在哪里

| 方法 | 结果 | 时间 |
| ---------- | -------- | ------ |
| ❌ `pipe.to('cuda')` — 全部放到 GPU | **OOM**（54 GB > 48 GB 显存） | — |
| ❌ `enable_model_cpu_offload` — 1024×1024 | **OOM**（transformer + 激活值过大） | — |
| ✅ `enable_sequential_cpu_offload` — 512×512 | **成功** | **60.3s** |
| ❌ `torch.compile` 配合 `max-autotune` | **超时**（编译内核超过 5 分钟） | — |
| ❌ `torch.compile` 配合 `reduce-overhead` | **卡死**（首次前向传播时惰性编译，32 个工作进程，耗时数分钟） | — |
| ✅ `enable_sequential_cpu_offload` — 1024×1024 | **成功**（此次 APEX 已缓存） | **37.2s** 🚀 |

### 关键要点

1. **对于 FLUX 来说，`torch.compile` 并不值得** — 编译开销（数分钟）远超 4 步推理的生成时间（37 秒）
2. **顺序 CPU 卸载是万金油** — 通过逐个将子模块移至 GPU，将显存控制在 48 GB 以内
3. **注意力切片** 能有效降低激活值内存，使 1024×1024 分辨率得以运行
4. **第二次运行时，1024×1024 比 512×512 更快**，因为 APEX 内核已被缓存（0.22 秒 vs 20 秒编译时间）

### 最终可用的配方

```python
pipe = FluxPipeline.from_pretrained('/root/FLUX.1-schnell', torch_dtype=torch.bfloat16)
pipe.enable_sequential_cpu_offload()
pipe.enable_attention_slicing()

image = pipe("prompt", num_inference_steps=4, width=1024, height=1024).images[0]
# → 在 AMD Radeon 48 GB 上每张 4 步图像约需 37 秒
```
