---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Nanochat训练与SFT失败分析
translated: true
type: note
---

以下是您在 RTX 4070 工作站上训练实验的完整情况：

============================================================
NANOCHAT (Karpathy's nanochat) — /mnt/data/nanochat
============================================================

状态：已完成（2026 年 6 月 2 日）——但 SFT 阶段产生了 NaN loss。

发生了什么：

  1. 下载了 9 个 shard（约 2B 字符）的 ClimbMix 数据到 ~/.cache/nanochat/base_data_climbmix/
  2. 训练了一个 BPE tokenizer（32,503 次合并，vocab_size=32768）
  3. 基础预训练（depth=8，约 40M 参数）：
     - 5000 步，device_batch_size=4，total_batch_size=32768
     - val_bpb：3.14 -> 0.99（正常收敛！）
     - 最佳 val_bpb：0.9909（第 5000 步）
     - 模型保存：~/.cache/nanochat/base_checkpoints/d8/model_005000.pt（320MB）
     - 速度：约 103,700 tok/sec，总训练时间约 26 分钟
  4. 基础模型评估——基准测试得分：
     - ARC-Easy: 25.42%（随机水平 = 25%）
     - ARC-Challenge: 24.91%（随机水平 = 25%）
     - MMLU: 25.19%（随机水平 = 25%）
     - GSM8K: 0.00%
     - HumanEval: 0.00%
     -> 对于 40M 参数的模型来说这是预期的——基本是随机水平。
  5. SFT（监督微调）：
     - 加载了 identity_conversations.jsonl
     - 第 6 步时 loss 变为 NaN！（lr=1.0，过高）
     - 所有 188 步 SFT 的 loss 均为 nan
     - 最终 val_bpb：3.9589（从基础模型的 0.99 退化）
     - ChatCORE: 0.0012（接近零）
     - 所有评估基准：0.00%
     -> SFT 因学习率爆炸而失败

关键问题：SFT 阶段的学习率对于小型 40M 模型来说过高，立即导致 NaN loss。基础预训练实际上是正常的。

============================================================
NANOGPT (Karpathy's nanoGPT) — /mnt/data/nanoGPT
============================================================

存在多个训练记录：

数据：
  data/fineweb/         — train.bin（6.9GB）+ val.bin（12K）+ edu_fineweb100B/
  data/openwebtext/     — train.bin（旧格式 16GB）
  data/shakespeare_char/
  data/shakespeare/
  data/wikipedia_local/

输出检查点：
  out-fineweb/ckpt.pt          — 1.49 GB（4 月 30 日）
  out-gpt2-200m/ckpt.pt        — 2.63 GB（5 月 15 日）— GPT-2 200M 参数
  out-wikipedia/ckpt.pt        — 362 MB（2025 年 11 月）
  out-helloworld/ckpt.pt       — 129 MB（4 月 28 日）
  out-shakespeare-char/ckpt.pt — 129 MB（4 月 23 日）
  out-shakespeare/             — 空（无检查点）

============================================================
如何使用 NANOCHAT 进行训练
============================================================

流程为：数据 -> tokenizer -> 预训练 -> SFT -> 评估 -> 对话

1. 快速冒烟测试（5 分钟，适用于 RTX 4070）：

   cd /mnt/data/nanochat
   source .venv/bin/activate
   OMP_NUM_THREADS=1 python -m scripts.base_train --depth=8 \
     --device-batch-size=4 --num-iterations=200 --run=smoke

2. 包含 SFT 的完整运行（修复 NaN）：

   编辑 run_rtx4070.sh，修改 SFT 的学习率。基础模型已经训练好，
   因此可以跳过预训练直接进入 SFT：

   python -m scripts.chat_sft --max-seq-len=1024 \
     --device-batch-size=4 --total-batch-size=32768 \
     --num-iterations=1500 --run=rtx4070-d8

   但你需要降低学习率。查看 chat_sft.py 接受哪些 lr 参数。

3. 与训练好的模型对话：

   python -m scripts.chat_cli -p "天空为什么是蓝色的？"

   # 或使用 Web UI

   python -m scripts.chat_web

4. 扩展规模——尝试 depth=12（GPT-1 大小，约 100M 参数）：

   python -m scripts.base_train --depth=12 \
     --device-batch-size=2 --total-batch-size=32768 \
     --num-iterations=5000 --run=rtx4070-d12

============================================================
下一步做什么
============================================================

最直接的修复：SFT NaN。需要我 SSH 进去并：
  (a) 检查 chat_sft.py 中的 lr 覆盖标志
  (b) 使用合理的 lr（例如 1e-4 而不是 1.0）重新运行 SFT
  (c) 用修复后的模型测试对话 CLI？

或者如果你想尝试不同的方式，你还可以：

- 在 RTX 4070 上尝试 depth=12 或 depth=16（使用更小的 batch）
- 使用 nanoGPT 的 fineweb 检查点（约 200M）进行实际生成
- 在 SFT 成功后运行 RL 训练阶段（scripts/chat_rl.py）
