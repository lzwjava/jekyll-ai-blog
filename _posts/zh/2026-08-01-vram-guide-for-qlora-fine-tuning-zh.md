---
audio: false
generated: true
image: false
lang: zh
layout: post
title: QLoRA微调显存指南
translated: true
type: note
---

问题：LoRA/QLoRA微调Qwen或DeepSeek模型需要什么GPU机器？24GB显存够用吗？

回答：

是的，**24GB显存对许多LoRA/QLoRA微调任务来说是足够的**，但模型大小很重要。关键区别：

* **LoRA**：基础模型权重保留在GPU内存中（通常为FP16/BF16），仅训练适配器。
* **QLoRA**：基础模型被量化（通常为4位NF4），大幅降低显存使用。

内存预算大致为：

```
显存 ≈ 模型权重 + 激活值 + 梯度 + 优化器状态 + KV/缓存 + 开销
```

对于QLoRA：

```
4位权重：
参数数量 × 0.5字节

LoRA适配器：
小（通常小于模型参数的1-2%）

优化器：
仅LoRA参数，而非完整模型
```

### 实际GPU需求

| 模型                           | 参数量 | LoRA       | QLoRA     | 24GB GPU        |
| ----------------------------- | ------ | ---------- | --------- | --------------- |
| Qwen2.5-3B                    | 3B     | ~8GB       | ~5GB      | ✅ 轻松          |
| Qwen2.5-7B                    | 7B     | ~16-20GB   | ~10-14GB  | ✅ 轻松          |
| Qwen2.5-14B                   | 14B    | ~30GB+     | ~18-22GB  | ✅ 良好          |
| Qwen2.5-32B                   | 32B    | ~70GB+     | ~22-30GB  | ⚠️ 紧张        |
| Qwen3-8B                      | 8B     | ~18GB      | ~12-16GB  | ✅ 轻松          |
| DeepSeek-R1-Distill-Qwen-7B   | 7B     | ~16-20GB   | ~10-14GB  | ✅ 轻松          |
| DeepSeek-R1-Distill-Qwen-14B  | 14B    | ~30GB      | ~18-22GB  | ✅ 良好          |
| DeepSeek-R1-Distill-Qwen-32B  | 32B    | 不可能      | ~24-32GB  | ⚠️ 需要技巧      |

单个：

* RTX 3090 24GB
* RTX 4090 24GB
* RTX A5000 24GB
* RTX 6000 Ada 48GB

是非常常见的QLoRA配置。

---

## 示例：RTX 3090 24GB上运行Qwen2.5-14B QLoRA

典型配置：

```yaml
model: Qwen/Qwen2.5-14B-Instruct

quantization: 4bit
bnb_4bit_quant_type: nf4

lora:
  r: 16
  alpha: 32
  dropout: 0.05

training:
  batch_size: 1
  gradient_accumulation: 16
  max_seq_length: 4096
```

内存：

```
Qwen 14B FP4：

14B参数 × 0.5字节
≈ 7GB

+
CUDA开销
≈ 2GB

+
激活值
≈ 8-10GB

+
LoRA
<1GB

-----------------
~18-20GB
```

可在24GB内适配。

---

## 对于DeepSeek模型

需要区分：

### DeepSeek-R1-Distill

这些是基于Qwen/Llama的普通密集模型。

示例：

```
DeepSeek-R1-Distill-Qwen-14B
```

轻松运行。

24GB显卡可用。

---

### DeepSeek-V3 / R1完整版

情况不同。

```
DeepSeek-V3：
671B总参数量
37B激活参数量
```

即使QLoRA也不是普通的单GPU任务。

你需要：

* 多GPU
* 分布式训练
* 大显存

示例：

```
8 × H100 80GB
或
8 × MI300X 192GB
```

---

## 你的RTX 4070 12GB

你当前的RTX 4070：

```
12GB显存
```

可运行：

✅ Qwen2.5-3B
✅ Qwen2.5-7B QLoRA
✅ DeepSeek-R1-Distill-7B

可能：

⚠️ 14B使用激进设置：

```
batch=1
seq_len=2048
梯度检查点
CPU卸载
```

但不太舒适。

---

## 2026年最佳家用AI微调GPU选择

### 预算型

二手RTX 3090 24GB

```
$600-800美元
24GB显存
优秀的CUDA支持
```

可能是最佳性价比选择。

### 全新型

RTX 4090 24GB

```
24GB
最快的消费级显卡
```

### 严肃本地研究

二手RTX A6000

```
48GB显存
ECC内存
```

非常适合：

* Qwen 32B QLoRA
* 更大上下文
* 更大批次

---

## 推荐技术栈

对于QLoRA：

```bash
pip install transformers
pip install peft
pip install bitsandbytes
pip install trl
```

最小化训练代码：

```python
from transformers import AutoModelForCausalLM, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model

bnb = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype="bfloat16"
)

model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-14B-Instruct",
    quantization_config=bnb,
    device_map="auto"
)

lora = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=[
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj"
    ]
)

model = get_peft_model(model, lora)
```

---

鉴于你的配置（RTX 4070 + 对训练GPT/nanochat感兴趣），最实用的升级路径是：

1. 保留RTX 4070用于推理和小型实验。
2. 购买二手RTX 3090 24GB。
3. 运行：

   * Qwen3-8B完整LoRA
   * Qwen2.5-14B QLoRA
   * DeepSeek-R1-Distill-14B QLoRA
4. 构建数据集和评估流程。

对于实际的LLM工程经验，**单块24GB GPU已经足够学习生产中使用的几乎所有LoRA/QLoRA工作流程。**