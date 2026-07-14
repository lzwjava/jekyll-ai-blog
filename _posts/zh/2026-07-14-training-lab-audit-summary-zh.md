---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 培训实验室审计摘要
translated: true
type: note
---

这是对该仓库（`zz`，72 次提交）的完整审计：

---

## 总提交数：72

全部在 `main` 分支，历史记录干净。从 FineWeb 下载脚本开始，演变为一个完整的训练实验室。

---

## 使用的训练框架（2 个）

| 框架 | 用途 |
| ----------- | ---------- |
| **nanoGPT**（Karpathy） | FineWeb 125M 和 760M，OpenWebText 125M |
| **nanochat**（Karpathy） | d12 286M 预训练 + SFT |
| **transformers+peft+trl** | Notes SFT（Qwen3-4B） |
| **transformers+Whisper** | SPGISpeech（ASR） |

---

## 你尝试过的模型（9 个不同的模型/运行组合）

### nanoGPT — FineWeb 125M（n_layer=12，124M 参数，RTX 4070）

1. **运行 #1** — 20,000 步（`train_log_fineweb.txt`）
2. **运行 #2** — 约 6,000 步（`train_log_fineweb2.txt`）
3. **运行 #3** — 11,000+ 步（配置 max_iters=12000，`train_log_fineweb3.txt`）
4. **OpenWebText 125M** — 6,000 步（`train_log_openweb.txt`）
5. **FineWeb 125M（MI300X）** — 750+ 步（`train_log_do_fineweb.txt`，MFU 163%）

### nanoGPT — FineWeb 760M（n_layer=24，n_embd=1536，760M 参数，MI300X）

6. **760M** — 76,000 / 计划 445,000 步（17%，约 2.46B tokens 已见）。两个日志文件记录了同一运行的不同阶段。MFU 108–113%。推理质量审计：流畅但产生幻觉——在 val_loss 3.16 时表现为“随机鹦鹉”。

### nanochat — d12（depth=12，n_embd=768，n_head=6，约 286M 参数）

7. **fineweb-edu-d12** — 10,000 步（基础预训练）
8. **rtx4070-d12-chinchilla** — 从上述检查点恢复，总计 87,000 步，RTX 4070 上用时 28.4 小时。最终验证 bpb：0.866，平滑训练损失：2.748。完全完成。
9. **code-sec-fineweb-d12** — 在混合数据（github-code + SEC-EDGAR + FineWeb-Edu）上训练 50,000 步
10. **code-sec-sft（SFT）** — 在 d12 检查点（第 50K 步）上进行 8,985 步 SFT。验证 bpb：0.405。SFT 教会了对话格式和代码模式，但约 140M 参数太小，无法进行推理。

### nanochat — Codeparrot d12

11. **Codeparrot-clean d12** — 训练脚本存在（RTX 4070 上 device-batch-size=4，24.7B Python tokens）。流水线已编写，但没有日志证据表明它已完成。

### 其他

12. **Notes SFT（Qwen3-4B）** — 微调流水线已创建（`finetune/train.py`）
13. **SPGISpeech（Whisper）** — 训练脚本已创建（`spgispeech/train_whisper.py`）
14. **SEC-EDGAR GPT-2 124M** — 配置已添加，但未找到训练日志

---

## 汇总表

| # | 模型 | 框架 | 参数 | 硬件 | 步数 | 状态 |
| --- | ------- | ----------- | -------- | ---------- | ------- | -------- |
| 1 | FineWeb 125M run1 | nanoGPT | 124M | RTX 4070 | 20K | 已完成 |
| 2 | FineWeb 125M run2 | nanoGPT | 124M | RTX 4070 | 6K | 已完成 |
| 3 | FineWeb 125M run3 | nanoGPT | 124M | RTX 4070 | 11K | 已完成 |
| 4 | OpenWebText 125M | nanoGPT | 124M | RTX 4070 | 6K | 已完成 |
| 5 | FineWeb 125M MI300X | nanoGPT | 124M | MI300X | 750 | 冒烟测试 |
| 6 | FineWeb 760M | nanoGPT | 760M | MI300X | 76K/445K | 提前停止 |
| 7 | fineweb-edu-d12 | nanochat | 286M | RTX 4070 | 10K | 基础预训练完成 |
| 8 | rtx4070-d12-chinchilla | nanochat | 286M | RTX 4070 | 87K | **完全完成** |
| 9 | code-sec-fineweb-d12 | nanochat | 286M | H200? | 50K | 已完成 |
| 10 | code-sec-sft | nanochat | 约 140M | H200? | 8,985 | 已完成 |
| 11 | codeparrot-d12 | nanochat | 286M | RTX 4070 | ? | 仅脚本 |
| 12 | Notes SFT (Qwen3-4B) | trl/peft | 4B | RTX 4070 | ? | 仅脚本 |
| 13 | SPGISpeech (Whisper) | transformers | 变化 | ? | ? | 仅脚本 |

你已完成了 **10 次实际训练运行**（有日志证据），涵盖 **5 个不同的模型定义**（FineWeb 125M、FineWeb 760M、nanochat d12、codeparrot d12、Qwen3-4B SFT）。皇冠上的明珠是 **d12-chinchilla 运行**（87K 步，完全完成）和 **code-sec-fineweb-d12 + SFT 流水线**。
