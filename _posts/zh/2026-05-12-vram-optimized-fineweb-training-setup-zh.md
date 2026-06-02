---
audio: false
generated: true
image: false
lang: zh
layout: post
title: VRAM优化的FineWeb训练设置
translated: true
type: note
---

没关系——你可以运行几个小时。以下是烟雾测试的结果以及我做出的改动：

  Findings

- batch_size=8 导致显存不足（比你的12 GB多需要1.54 GiB）。已修复为 batch_size=4 +
  gradient_accumulation_steps=128 —— 保持相同的524k token/步。
- 在 batch_size=4、eager模式下：约88毫秒/微批次，约6.6 GB显存（约5.6 GB余量）。
- 损失值在4次迭代中从11.04 → 10.94 → 10.85 → 10.75 → 10.56 —— 训练连接正确，分片加载成功，词表无误。
- 按实际grad_accum=128推算每迭代时间：约11秒/迭代。

  Time budget for the real run (max_iters=19073, ~10B tokens seen)

- Eager (compile=False)：约59小时（约2.5天）
- 启用 compile=True：编译耗时1–3分钟后速度提升约20–30%，因此约40–50小时
- 如需更短运行，设置 --max_iters=5000 --lr_decay_iters=5000 → 约15小时，约2.6B token。

  Run this in another terminal

  cd /mnt/data/nanoGPT
  tmux new -s nano                 # 使其在断开连接后仍存活
  source venv/bin/activate

  PYTORCH_ALLOC_CONF=expandable_segments:True \
  python -u train.py config/train_fineweb_gpt3.py 2>&1 \
    | tee -a out-fineweb-gpt3/train.log

# detach: Ctrl-b d        reattach: tmux attach -t nano

  如果 compile=True 在你的 torch/CUDA 组合上报错，只需在末尾添加 --compile=False 重新启动即可。

  中断后恢复运行：添加 --init_from=resume。
