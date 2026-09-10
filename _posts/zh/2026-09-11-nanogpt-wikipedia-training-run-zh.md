---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NanoGPT维基百科训练运行
translated: true
type: note
---

运行顺畅。以下是总结。

## 数据已复制
`nanoGPT/data/wikipedia_local/` → **`/mnt/data/igpt/data/wikipedia/`**

| 文件 | 大小 | 内容 |
|---|---|---|
| `train.bin` | 172 MB | **85,970,233** 个 GPT-2 BPE token |
| `val.bin` | 118 KB | 59,058 个 token |
| `meta.pkl` | 73 B | 由我创建（之前缺失）— `{tokenizer: bpe, encoding_name: gpt2}` |

与现有的 char-level `data/` 保持分离，因此 `--data_dir data` 仍能正常工作。

## 对 `train.py` 的两处修复（长期运行均需要）
1. **`estimate_loss()` 缺少 `torch.no_grad()`** — 评估时构建了反向计算图导致 OOM。已添加装饰器（与 `generate()` / `sample_and_print()` 一致）。
2. **最终保存覆盖了 `ckpt.pt` 的最新状态**，破坏了 README 中宣称的最佳验证检查点。现在最终状态保存为 `ckpt_last.pt`，而 `ckpt.pt` 保留最佳验证检查点。

## 训练已启动（系统 `python3.12`，torch 2.11+cu130）
```
PID 670206   日志: /mnt/data/igpt/out-wikipedia/train.log
data_dir=data/wikipedia  tokenizer=bpe  out_dir=out-wikipedia
n_layer=6 n_head=6 n_embd=384（29.95M 参数） block_size=256 dropout=0.1
batch_size=8 × grad_accum=16 → 32,768 tok/iter
max_iters=30000（约 983M token ≈ 11 个 epoch） lr=6e-4 cosine→6e-5 warmup=1000
```
当前进度：**验证损失 6.26 @ 迭代 500**，约 325 ms/iter → **预计剩余时间 ≈ 2.7 小时**（完成时间约 06:03）。每 500 次迭代保存最佳检查点。

监控 / 停止 / 采样：
```bash
tail -f /mnt/data/igpt/out-wikipedia/train.log
kill $(cat /mnt/data/igpt/out-wikipedia/train.pid)
/usr/bin/python3.12 train.py --data_dir data/wikipedia --tokenizer bpe \
  --out_dir out-wikipedia --sample --prompt "The history of" --max_new_tokens 200
```

## 一个值得注意的注意事项
你的 `llama-server`（Qwen3-8B）占用了 12 GB 显存中的 **5.9 GB**，桌面占用约 3.5 GB，因此仅剩约 2.4 GB 可用——我不得不将模型缩小到 30M 参数，微批次大小为 8，空闲显存仅约 **330 MiB**。如果你停止 `llama-server`，我可以使用更大的模型（例如 `n_embd=768, n_layer=12`）和更大的批次重新运行，这样能更好地利用显卡。nanoGPT 中还有一个 3.7B token 的 `fineweb/train.bin`，如果你更倾向于使用它进行训练。