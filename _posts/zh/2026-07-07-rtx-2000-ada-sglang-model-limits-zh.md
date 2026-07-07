---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RTX 2000 Ada SGLang 模型限制
translated: true
type: note
---

是的，硬件概述基本正确，但有一些 SGLang 特定的重要注意事项。

关键瓶颈是 **VRAM**，而非 CPU/内存/存储。RTX 2000 Ada 拥有：

* 16 GB GDDR6 VRAM
* 计算能力 8.9（Ada，支持 FP8 Tensor Core）
* PCIe 工作站 GPU，非数据中心显卡

对于 SGLang 推理服务，实际可行的矩阵如下：

| 模型            | 精度           | 能否容纳？           | 实际说明                              |
| --------------- | -------------- | -------------------- | ------------------------------------- |
| Llama 3 8B      | FP16           | ✅ 是                 | 不错的基准                            |
| Qwen2.5 7B      | FP16/BF16      | ✅ 是                 | 可能是最佳选择                        |
| Mistral 7B      | FP16           | ✅ 是                 | 不错                                  |
| Qwen2.5 14B     | FP16           | ❌ 否                 | 约 28GB 权重                          |
| Qwen2.5 14B     | INT8/FP8       | ⚠️ 可能              | 需要量化检查点 + KV 缓存调优          |
| Qwen2.5 32B     | AWQ/GPTQ INT4  | ✅ 是                 | 可能是甜点区间                        |
| Qwen2.5 72B     | INT4           | ⚠️ 技术上能加载       | 几乎没有 KV 缓存，推理效果差          |

原先的估算：

> FP16 7-8B
> INT4 30-34B

是实际可行的范围。

但是：

> Qwen2.5-72B-AWQ ~14GB

对 SGLang 来说具有误导性。模型权重可能装得下，但推理服务不仅仅是权重。

内存：

```
VRAM =
  模型权重
+ CUDA 内核
+ 激活缓冲区
+ KV 缓存
+ 临时工作空间
```

例如：

Qwen2.5-72B-AWQ：

```
权重：        约 14GB
运行时：      约 1GB+
KV 缓存：     几乎为零
```

你可能能加载它，但：

```
上下文长度：极短
批量大小：1
吞吐量：很差
```

它更像是一个演示，而不是一个 API 服务。

---

对于这台机器，我会测试：

### 选项 1：最佳质量 / 实用

```
Qwen2.5-32B-Instruct-AWQ
```

SGLang：

```bash
python -m sglang.launch_server \
  --model-path Qwen/Qwen2.5-32B-Instruct-AWQ \
  --quantization awq \
  --host 0.0.0.0 \
  --port 30000 \
  --max-model-len 8192
```

预期：

* 良好的推理能力
* 良好的编程能力
* 可接受的延迟

---

### 选项 2：快速生产 API

```
Qwen2.5-7B-Instruct
```

```bash
python -m sglang.launch_server \
  --model-path Qwen/Qwen2.5-7B-Instruct \
  --host 0.0.0.0 \
  --port 30000
```

你将获得：

* 更大的 KV 缓存
* 更长的上下文
* 更高的并发性

---

### 选项 3：编程模型

```
Qwen2.5-Coder-14B-Instruct-AWQ
```

或

```
DeepSeek-Coder-V2-Lite-Instruct
```

配合 AWQ/INT4。

---

启动前，检查：

```bash
nvidia-smi

python - <<EOF
import torch
print(torch.cuda.get_device_name())
print(torch.cuda.get_device_capability())
EOF
```

然后安装：

```bash
pip install "sglang[all]"
```

测试：

```bash
python -m sglang.launch_server \
  --model-path Qwen/Qwen2.5-7B-Instruct \
  --port 30000
```

健康检查：

```bash
curl http://localhost:30000/health
```

---

我需要确认一件事：**RTX 2000 Ada + SGLang 兼容性**。SGLang 大量使用 FlashInfer/Triton 内核；Ada CC 8.9 受支持，但某些优化内核可能与 A100/H100 相比性能不同。

对于 RunPod 按小时计费实例，我会使用以下命令进行基准测试：

1. Qwen2.5-7B FP16
2. Qwen2.5-14B AWQ
3. Qwen2.5-32B AWQ

命令：

```bash
python -m sglang.bench_serving \
 --backend sglang \
 --dataset-name random \
 --num-prompts 100
```

这将给出真实的 tokens/秒和并发能力。