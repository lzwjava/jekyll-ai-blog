---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Fineweb GPT-3训练设置
translated: true
type: note
---

加载器正常工作 — 1407 个训练分片 + 1 个验证分片，uint16，第一个 token 为 50256 (EOT)，与预期一致。

### 4) 操作步骤 — 要运行的命令

```bash
cd /mnt/data/nanoGPT
source venv/bin/activate

#（可选）确认 GPU 空闲
nvidia-smi

# 试运行：小批次运行 5 次迭代（iters），确保一切正常再正式运行
python train.py config/train_fineweb_gpt3.py \
    --compile=False --batch_size=2 --gradient_accumulation_steps=1 \
    --max_iters=5 --eval_interval=10 --log_interval=1

# 正式运行（单块 4070，12GB）。使用 tmux/screen 会话 — 这将耗时数小时。
tmux new -s nano
python train.py config/train_fineweb_gpt3.py 2>&1 | tee out-fineweb-gpt3/train.log
# 分离：Ctrl-b d   |   重新连接：tmux attach -t nano
```

### 后续可调整的注意事项/参数
- `max_iters=19073` ≈ 在 524k tokens/step 下看到约 **100 亿 tokens**。要真正使用你 tokenized 的全部约 1400 亿 tokens，请将其增加到约 267000（并将 `lr_decay_iters` 设置为相同值）。这在 4070 上需要运行数天。
- 如果试运行时出现 OOM（内存不足），请将 `batch_size` 降至 4，并将 `gradient_accumulation_steps` 加倍至 128（保持 tokens/step 不变）。
- 如果 `compile=True` 在你的 PyTorch/CUDA 组合上出错，请改用 `--compile=False`。
- 中断后恢复：`python train.py config/train_fineweb_gpt3.py --init_from=resume`。
- 我对 `train.py` 所做的补丁是向后兼容的 — 没有 `shard_dir` 的旧配置仍然可以读取 `train.bin`/`val.bin`。