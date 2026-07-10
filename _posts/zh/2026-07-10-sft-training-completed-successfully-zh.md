---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SFT训练成功完成
translated: true
type: note
---

**SFT 完成 — 8,985 步，184.7 分钟（约 3 小时）**

### SFT 总结

| 预训练（第 50k 步） | SFT（第 8985 步） |
|---|---|
| val_bpb：**1.418** | val_bpb：**0.405** |
| 训练损失：1.06 | 训练损失：1.07 |

验证 BPB 下降 71% —— 模型学会了生成聊天格式的回复。

最终损失：~1.07，学习率衰减到 0.00（warmdown 完成）。数据集结束时第 2 个 epoch 刚刚开始。

检查点：`/home/lzw/.cache/nanochat/chatsft_checkpoints/d12/model_008985.pt`（793MB）

**下一步：** 测试 SFT 模型的生成结果并与预训练模型进行比较：

```bash
cd /mnt/data/nanochat && source .venv/bin/activate
python /mnt/data/zz/fineweb-code-sec-gpt/run_prompts.py --step 8985 --temp 0.7 --max-tokens 200
```