---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Nanochat和nanoGPT实验总结
translated: true
type: note
---

## nanochat — 训练运行

### d8（~40M参数）— 初步验证概念

**配置：** depth=8, batch=32,768, seq_len=1,024, 5k次迭代
**数据：** 来自fineweb-edu分片的约1.64亿token（8个分片，约20亿字符）
**流程：** 预训练 → SFT（Karpathy的identity_conversations）→ 评估

检查点位于 `base_checkpoints/d8/`，步骤1k和5k。SFT步骤也已运行（chatsft_checkpoints/d8/）。

**结果：** 语言建模损失约3.0，ARC-Easy 25.6%，MMLU 25.3%，GSM8K/HumanEval 0%。这是预期的——40M参数在1.64亿token下，数据与参数比例约为4倍（Chinchilla建议约20倍），因此模型学习了语言结构但完全没有推理能力。

### d12（286M参数）— 重要尝试

**配置：** depth=12, dim=768, heads=6, seq_len=2,048, batch=65,536 tokens/step

**阶段1 — Fresh 10k（MLflow追踪）：** `run_d12_10k_mlflow.sh`。约6.55亿token。验证BPB：0.9349（约验证损失2.87）。样本输出显示模型生成了交替重复的内容（"法国首都在该国南部。它是法兰西共和国的首都"）——它学习了表面结构，但尚未看到足够的数据来实现事实绑定。

**阶段2 — Chinchilla运行（87k→200k步骤）：** `run_rtx4070_chinchilla.sh` 计划87k步（约57亿token），然后 `run_d12_130k.sh` 从87k恢复至130k。实际进行了更远：

每10k步的检查点位于 `base_checkpoints/d12/`：
| 步骤 | 日期 |
|------|------|
| 130k | 6月7日 |
| 140k | 6月9日 |
| 150k | 6月9日 |
| 160k | 6月10日 |
| 170k | 6月10日 |
| 180k | 6月10日 |
| 190k | 6月10日 |
| 200k | 6月10日 |

总计约131亿token（200k × 65,536）。每个检查点792MB（模型）+ 1.2GB（优化器）。损失在约3.0处趋于平稳——模型仍在学习，但损失曲线变平，这意味着要么（a）数据多样性已耗尽，（b）学习率调度需要调整，或者（c）286M容量在此数据分布上已饱和。

**阶段3 — 评估结果（约10k新模型）：**
- ARC Easy: 25.63% — 接近随机（25%）
- ARC Challenge: 25.77% — 接近随机
- MMLU: 25.26% — 接近随机（25%）
- GSM8K: 0.00% — 无算术推理
- HumanEval: 0.00% — 无代码生成

评估是在10k步的新模型上运行的。200k步的模型可能得分略高，但仍远未达到实用——这些基准测试对于286M模型需要比当前多10倍以上的数据。

### d4分布式测试

跨2个rank的极小20步运行。CPU/DDP测试，除了验证分布式训练路径外没有其他意义。

### d24 MI300X（约760M参数）

**配置：** depth=24, dim=1,536, heads=12, batch=524,288, seq_len=2,048, 计划29k步
**数据：** ClimbMix-400B，目标约152亿token

在AMD MI300X（192GB HBM3）上运行。测试了多种配置变体（FP8, FA2+FP8）。日志位于 `run_mi300x_d24.log`、`run_mi300x_d24_fa2_fp8.log`、`run_mi300x_d24_fp8.log`。`run_mi300x_d24_pretrain.sh` 脚本是仅预训练变体。

这是你最具雄心的运行——760M参数在云端GPU上以2美元/小时运行。

---

## nanoGPT — 训练运行

除非另有说明，所有运行均基于Karpathy的原始nanoGPT，采用GPT-2 124M架构（n_layer=12, n_head=12, n_embd=768）。

### fineweb-gpt3（124M，目标100亿token）

**配置：** `config/train_fineweb_gpt3.py` — batch=4 × grad_accum=128 = 有效每步524,288 token，max_iters=19,073
**数据：** `/mnt/data/nanoGPT/data/fineweb/edu_fineweb100B`

训练在约15,180步处停止（训练损失3.05，验证损失3.03）——train.log显示 `Command 'python3.13' not found` 错误。实际运行使用了错误的Python二进制文件。在崩溃前达到了约79亿token。检查点保存于该点。

### fineweb（124M）

相同架构的标准运行。检查点位于 `out-fineweb/ckpt.pt`（约1.4GB）。似乎是完成的单次运行，但未保留train.log。

### github-code-124m（124M，目标140亿token）

**配置：** `config/train_github_code_124m.py` — 有效batch=32,768, max_iters=427,000
**数据：** `/mnt/data/zz/datasets/github-code-tok/`（27GB token化的GitHub代码）

检查点位于 `out-github-code-124m/ckpt.pt`（约1.4GB）。配置目标为140亿token。需要检查训练进展到哪一步。

### sec-edgar-124m（124M，目标15.5亿token）

**配置：** `config/train_sec_edgar_124m.py` — 有效batch=32,768, max_iters=47,400（1个epoch）
**数据：** `/mnt/data/zz/datasets/sec-edgar-tok/`（3.1GB token化的SEC文件）

检查点位于 `out-sec-edgar-124m/ckpt.pt`（约1.4GB）。应该已完成约1个epoch。

### gpt2-200m（200M参数）

更大的架构。检查点位于 `out-gpt2-200m/ckpt.pt`（约2.5GB）。train.log为空（0字节）——要么运行立即崩溃，要么日志记录在其他地方。

### 小规模运行

`out-helloworld`（随机初始化），`out-shakespeare`（空），`out-shakespeare-char`（基于字符的GPT在莎士比亚上），`out-wikipedia`（Wikipedia预训练，362MB检查点）。这些是原始的nanoGPT演示运行。

### 可用数据集

| 数据集 | 大小 | Token数 |
|---------|------|---------|
| github-code-tok | 27GB | 约70-80亿token |
| sec-edgar-tok | 3.1GB | 约15亿token |
| edu_fineweb100B | 约15GB | 跨分片分割 |
| openwebtext | 可变 | 约9GB |

---

## 当前实际值得关注的内容

### 1. nanochat d12 — 完成评估循环

你从130k到200k有8个检查点，但从未进行过适当的评估扫描。d12训练达到了200k步（约130亿token），这大约是数据与参数比的45倍——对于286M而言低于Chinchilla最优（约20倍），因此从技术上来说模型在其容量下训练不足。但平坦的损失曲线（约3.0）表明收益递减。

**先做这个：** 在200k检查点上运行 `scripts.base_eval`，看看损失改善是否转化为任何基准测试相对于10k检查点的提升：
```bash
cd /mnt/data/nanochat && source .venv/bin/activate
python -m scripts.base_eval --device-batch-size=8 --model-tag=d12-fresh
```

### 2. nanochat d12 — 对200k检查点进行SFT

286M的d12模型从未进行过SFT。d8的SFT证明了管道的有效性。SFT将为你提供一个具备聊天能力的本地286M模型。

```bash
python -m scripts.chat_sft --max-seq-len=2048 --device-batch-size=8 --total-batch-size=32768 --run=rtx4070-d12-sft
```

这是最高杠杆率的行动：一个经过SFT的286M聊天模型可用于快速本地推理、代理子角色以及无需API成本的提示实验。

### 3. nanoGPT github-code-124m — 检查训练状态

27GB的GitHub代码数据集是你最大的精心策划数据集。如果427k步的运行已完成，你将拥有一个124M代码模型。如果没有，则恢复训练。这直接服务于你的代理工具开发工作（ww, iclaw）。

### 4. nanoGPT fineweb-gpt3 — 从15k步恢复

可轻松修复——运行因 `python3.13` 不存在而失败。使用正确的Python（`.venv/bin/python` 或 `python3.11`）恢复。距离达到19,073步仅剩约4k步。

### 5. 在相同数据上比较nanochat与nanoGPT

两个框架都可以训练GPT-2 124M架构。你有相同的github-code数据集已为两个框架token化。在相同模型配置下比较nanochat和nanoGPT的训练速度（token/秒）。这回答了：未来实验应该使用哪个框架？

### 6. GGUF量化 → 本地服务

sec-edgar-124m检查点足够小，可以转换为GGUF格式用于llama.cpp推理。你已经在 `~/projects/llama.cpp/build/bin/` 构建了llama.cpp。这将为你提供一个本地服务的模型，用于SEC EDGAR任务，无需API调用。

```bash
cd /mnt/data/nanoGPT
python3 scripts/convert_hf_to_gguf.py --outfile out-sec-edgar-124m/ggml-model-q4_0.gguf --model out-sec-edgar-124m/ckpt.pt
```

### 7. 在124M上的RL/GRPO是可行的但为时过早

你具备TRL技能和PEFT工具链。一个使用GRPO在GSM8K上微调的124M模型将是一个很好的学习练习——你将实时看到RL奖励塑造动态在你训练的模型上。但基础模型首先需要处于合理的损失区间（124M在100亿token下约3.0对于RL来说仍然较高）。

---

**总结：** 每小时的最高投资回报率是（1）对d12进行评估扫描，（2）对d12 200k检查点进行SFT。这将为你提供一个可工作、可评估、可比较并使用的聊天模型。然后（3）评估github-code-124m的状态。