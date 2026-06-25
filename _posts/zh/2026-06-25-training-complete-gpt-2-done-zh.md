---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 训练完成——GPT-2已完成
translated: true
type: note
---

🎉 **训练完成！** 恭喜！

检查点确认如下：

- **iter_num: 427,000** / max_iters: 427,000 — 已达到完整目标
- **best_val_loss: 3.466** — 这是最终验证损失
- GPT-2 124M (12层, 12头, 768维嵌入) 在 github-code 上训练
- 处理了约 14B tokens (427k iters × batch 4 × accum 8 × block 1024)

"train" tmux 会话已结束 — 它在完成全部 427k 次迭代并保存最终检查点后正常退出。GPU 现在空闲 (0% 利用率, 43°C, 10W)。

模型位于：
  /mnt/data/nanoGPT/out-github-code-124m/ckpt.pt (1.4 GB)

想用它做点什么吗？比如转换为 GGUF 用于 llama.cpp、运行一些代码生成示例，或推送到 HuggingFace？
