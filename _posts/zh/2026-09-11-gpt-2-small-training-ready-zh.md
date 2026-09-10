---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPT-2小型训练就绪
translated: true
type: note
---

已完成。当前没有任务在运行；GPU 已空闲，你可以启动它了。

## `run1.sh`（`/mnt/data/igpt/run1.sh`，可执行）

```bash
tmux new -s igpt
cd /mnt/data/igpt
./run1.sh
# detach: Ctrl-b d     reattach: tmux attach -t igpt
# resume after a crash: ./run1.sh --init_from resume
```

本次运行：**124 M 参数的 GPT-2-small**（`12L/12H/768d`，block 512）在 **FineWeb** 上训练（3.68 B GPT-2 BPE tokens，memmapped —— 无需重新 tokenize），30 000 iters × 32 768 tokens ≈ **983 M tokens**，lr 6e-4 cosine → 6e-5，warmup 1000，dropout 0.1，bf16。最佳验证集 checkpoint → `out-fineweb-124m/ckpt.pt`，最终状态 → `ckpt_last.pt`，完整日志通过 tee 保存到 `out-fineweb-124m/train.log`。实测约 ~800 ms/iter ⇒ **ETA ≈ 6.5–7 小时**。

无需编辑即可覆盖：`PY=… DATA_DIR=… OUT_DIR=… ./run1.sh`，额外的 flag 会被转发（`./run1.sh --max_iters 50000`）。

环境状态：
- `llama-server` 已终止 → **约 9.0 GB 空闲**（之前是 2.4 GB）。
- 已将 `nanoGPT/data/fineweb/{train.bin,val.bin}` 复制到 `igpt/data/fineweb/`，并写入了缺失的 `meta.pkl`。
- 之前复制的 Wikipedia 数据仍在 `igpt/data/wikipedia/`（86 M tokens），如果你想跑一次更短/验证集更干净的运行，可以改用：`DATA_DIR=data/wikipedia OUT_DIR=out-wikipedia-124m ./run1.sh`。
- `train.py` 的改动已存在于你的工作树中（长训练都需要）：eval 已包裹在 `torch.no_grad()` 中，最终保存不再覆盖最佳验证集 `ckpt.pt`。

运行结束后的采样示例：
```bash
/usr/bin/python3.12 train.py --data_dir data/fineweb --tokenizer bpe \
  --out_dir out-fineweb-124m --sample --prompt "The history of" --max_new_tokens 200
```