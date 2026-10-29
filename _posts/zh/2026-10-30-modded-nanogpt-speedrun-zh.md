---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 改装版NanoGPT速通
translated: true
type: note
---

这是 **modded-nanogpt** — NanoGPT 速通项目。以下是项目状态和操作指南：

## 项目内容
目标是以最少的墙钟时间在 8×H100 上将 GPT-2-small 训练到 **≤3.28 FineWeb 验证损失**。当前纪录：**0.665 分钟（39.9 秒）** — ANVIL2（`records/track_1_short/2026-08-30_ANVIL2`）。

- `train_gpt.py` + `track_1_short/` — 赛道 1 训练器（模型、优化器、调度、内核）
- `train_gpt_medium.py` — 赛道 2（GPT-2 Medium，目标 2.92）
- `records/track_3_optimization/` — 赛道 3（最小化步数，不限时间）
- `run.sh` — 启动 `torchrun --standalone --nproc_per_node=8 train_gpt.py`

Git 工作区干净，已与 `origin/master` 同步。

## 你的环境
- ✅ 已安装 torch 2.10.0+cu128，CUDA 可用，`torchrun` 在 PATH 中
- ⚠️ 只有 **1× RTX 4070（12GB）** — 不是 8×H100，因此无法在此进行官方纪录计时
- ❌ 训练数据尚未下载（缺少 `fineweb10B/`）
- ❓ FlashAttention-3 内核缓存（`devenpzak/flash-attn3-12864`）未验证

## 按目标分类的操作指引

**A. 本地运行当前纪录（冒烟测试）：**
```bash
pip3 install -r requirements.txt
python3 data/cached_fineweb10B.py 9        # ~9 亿 tokens
sed -i 's/nproc_per_node=8/nproc_per_node=1/' run.sh
./run.sh
```
注意：在 12GB 显存上可能需要缩短注意力序列长度（README：PR #38 指南）——这会改变训练行为，因此结果与纪录不可比。首次运行还需支付约 7 分钟的 `torch.compile` 时间。

**B. 竞争新纪录**（实际的"项目任务"）：
1. 阅读 `README.md` 中的 **规则** 部分（固定数据管道，p<0.01 时验证损失 ≤3.28，无额外 inductor 标志，必须在相同硬件上击败先前纪录）
2. 找到改进点——算法方面（架构/优化器/调度）或系统方面（内核、CUDA graphs、通信）
3. 在 8×H100 上验证（例如 PrimeIntellect，用于官方运行），提供运行日志，提交 PR

**C. 在不打破纪录的情况下贡献：** 接手开放的 PR，改进文档/可读性，或参与赛道 2/3。

你想追求哪个目标？如果是 A，我现在就可以开始下载数据并准备运行。