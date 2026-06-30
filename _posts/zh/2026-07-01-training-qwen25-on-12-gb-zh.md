---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在12GB上训练Qwen2.5
translated: true
type: note
---

问题：除了推理，我能否在 RTX 4070（12 GB）上实际*训练*（或微调）Qwen2.5-1.5B-Instruct？SGLang 仅用于推理，那么在这张卡上真正的训练选项有哪些？

回答：

可以——但我们需要精确理解在 12 GB 显存下“训练”意味着什么。SGLang 是一个推理/服务引擎（RadixAttention、连续批处理），不进行梯度计算。训练需要 PyTorch 加上优化器，而显存计算非常严苛。

12 GB 显存瓶颈

一个 1.5B 模型以 bf16 权重存储仅需约 3 GB。关键在于优化器状态。使用 AdamW 进行全参数微调时，每个参数需要：

- 权重（bf16）：2 字节
- 梯度（bf16）：2 字节
- Adam m + v（fp32）：8 字节
- fp32 主副本：4 字节

合计约 16 字节/参数 → 1.5B × 16 ≈ **24 GB**，这还只是静态状态，尚未计算激活值。全参数微调在 4070 上完全不可行。因此实际选项是 LoRA/QLoRA。

QLoRA 显存计算（这是可行的方案）

QLoRA 将冻结的基座模型量化到 4 位（NF4），仅训练小型低秩适配器：

- 基座权重（4-bit）：1.5B × 0.5 字节 ≈ 0.75 GB
- LoRA 适配器（r=16，约 0.3% 参数）：几 MB 的可训练参数
- 优化器状态仅作用于适配器：可忽略
- 激活值 + 梯度检查点：可变成本

总计约 **4–7 GB**，取决于序列长度和批次大小。在 12 GB 上非常充裕。普通 LoRA（基座为 bf16，约 3 GB）也能容纳，且有余量。

最小 QLoRA 训练脚本

这是优先构建的路径——使用 `trl` + `peft` + `bitsandbytes`：

```python
# pip install -U trl peft bitsandbytes transformers datasets accelerate
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig
from trl import SFTConfig, SFTTrainer
from datasets import load_dataset

model_id = "Qwen/Qwen2.5-1.5B-Instruct"

bnb = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,   # 可再节省约 0.4 GB
)

model = AutoModelForCausalLM.from_pretrained(
    model_id, quantization_config=bnb, device_map={"": 0},
    attn_implementation="flash_attention_2",  # 若未安装 FA2 则改用 "sdpa"
)
tok = AutoTokenizer.from_pretrained(model_id)

peft_cfg = LoraConfig(
    r=16, lora_alpha=32, lora_dropout=0.05, bias="none",
    task_type="CAUSAL_LM",
    target_modules=["q_proj","k_proj","v_proj","o_proj",
                    "gate_proj","up_proj","down_proj"],  # 注意力 + MLP
)

ds = load_dataset("trl-lib/Capybara", split="train[:2000]")

cfg = SFTConfig(
    output_dir="qwen-qlora",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,        # 有效批次 16
    gradient_checkpointing=True,          # 最大的激活节省手段
    bf16=True,
    max_length=1024,
    learning_rate=2e-4,
    num_train_epochs=1,
    logging_steps=10,
    optim="paged_adamw_8bit",             # paged = 在显存峰值时存活
)

trainer = SFTTrainer(model=model, args=cfg, train_dataset=ds, peft_config=peft_cfg)
trainer.train()
trainer.save_model("qwen-qlora/adapter")
```

实际控制是否 OOM 的杠杆，按影响程度排序：`gradient_checkpointing=True`（以约 30% 计算开销换大幅激活节省）、`max_length`（激活值与长度线性相关——若紧张可降至 512）、`per_device_train_batch_size`，以及 `paged_adamw_8bit`（分页优化器在显存峰值时将数据卸载到 CPU 内存而非崩溃）。

知识 → 显存对照表

| 方法 | 基座精度 | 能否适配 12 GB？ | 训练内容 |
|---|---|---|---|
| 全参数微调 | bf16 | ❌ ~24 GB | 所有参数 |
| LoRA | bf16（~3 GB） | ✅ ~6–9 GB | 适配器 |
| QLoRA | 4-bit（~0.75 GB） | ✅ ~4–7 GB | 适配器 |

你的两块 GPU 如何分工

在 4070 上原型验证 QLoRA 流程——在 `max_length=512`、批次 1–2 的条件下，完善数据管道、对话模板和适配器配置。当需要进行全参数微调、更长上下文或真正的大范围调参时，将其推送到 MI300X（192 GB），在那里对 1.5B 模型进行全 bf16 微调远低于 30 GB，并且你可以提高批次大小和序列长度。4070 是你的正确性检查环境；MI300X 是你的规模扩展环境。

训练完成后，合并适配器并通过 SGLang 提供服务：

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM
base = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype="bfloat16")
merged = PeftModel.from_pretrained(base, "qwen-qlora/adapter").merge_and_unload()
merged.save_pretrained("qwen-merged")
# 然后：python -m sglang.launch_server --model-path qwen-merged
```

关于 flash-attention-2 的一个注意事项：针对 4070（Ada, sm_89）预编译的 wheel 可能不稳定——如果 `flash_attention_2` 在加载时报错，请切换到 `attn_implementation="sdpa"`，它使用 PyTorch 内置的融合注意力机制，在此规模下速度几乎一样快。

参考资料：

- [QLoRA 论文（Dettmers 等）](https://arxiv.org/abs/2305.14314)
- [PEFT LoRA 文档](https://huggingface.co/docs/peft/main/en/developer_guides/lora)
- [TRL SFTTrainer 文档](https://huggingface.co/docs/trl/main/en/sft_trainer)
- [bitsandbytes（分页优化器）](https://huggingface.co/docs/bitsandbytes/main/en/index)
- [Qwen2.5 模型](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct)