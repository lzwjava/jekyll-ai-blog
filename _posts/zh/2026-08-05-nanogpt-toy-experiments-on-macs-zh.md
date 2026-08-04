---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Mac 上的 nanoGPT 玩具实验
translated: true
type: note
---

问题：我可以在 M2 Air 或 2017 款 Mac Pro（Intel）上运行 nanoGPT 风格的小型实验吗（例如 1000 步、小模型）？

答案：两者都可以很好地用于玩具级运行——你训练的并不是 GPT-2，而是一个几百K到几M参数的字符级模型。这对应的是 KB 到 MB 级别的激活值，FLOP 量微不足道。

**M2 Air**：使用 `--device=mps`。以下是某人运行完全相同的 nanoGPT shakespeare_char 配置的实际数据：使用 `--device=cpu` 时，每次迭代约需 410-550ms；切换到 `--device=mps` 后，每次迭代降至约 140-250ms，利用片上 GPU 获得了约 2-3 倍的加速。按此速度，1000 步只需 2-5 分钟。

**2017 款 Mac Pro（Intel，AMD GPU）**：不支持 MPS，macOS 上也没有 CUDA。只能使用 `--device=cpu`。在这个规模下仍然没问题——即使在 M2 上，纯 CPU 路径对一个 4 层/64 嵌入维度的模型也只需要约 410-550ms/迭代，因此在任何现代 x86 CPU 上，1000 步的玩具运行也只需几分钟。不要指望 torch.compile 能起作用（Triton 在这里意义不大，而且经常在非 CUDA 环境下出问题），所以始终传递 `--compile=False`。

设置与具体命令：

```bash
git clone https://github.com/karpathy/nanoGPT
cd nanoGPT
pip install torch numpy transformers datasets tiktoken wandb tqdm

# 小型字符级数据集，几秒钟即可完成分词
python data/shakespeare_char/prepare.py

# M2 Air（MPS）
python train.py config/train_shakespeare_char.py \
  --device=mps --compile=False \
  --n_layer=4 --n_head=4 --n_embd=128 --block_size=64 --batch_size=12 \
  --max_iters=1000 --lr_decay_iters=1000 --eval_iters=20 --log_interval=1 --dropout=0.0

# 2017 款 Mac Pro（仅 CPU）
python train.py config/train_shakespeare_char.py \
  --device=cpu --compile=False \
  --n_layer=4 --n_head=4 --n_embd=64 --block_size=64 --batch_size=8 \
  --max_iters=1000 --lr_decay_iters=1000 --eval_iters=1 --log_interval=1 --dropout=0.0
```

注意事项：
- 在 M2 上运行前，设置环境变量 `PYTORCH_ENABLE_MPS_FALLBACK=1` ——某些操作在 MPS 上仍未实现，否则会直接报硬错误，而不是静默回退到 CPU。
- 如果你希望结果比“损失下降”更有说服力，可以将 `max_iters` 提高到约 3000-6000；一次 MPS 运行在 6184 次迭代后达到损失 3.25，耗时 3.5 分钟——此时生成的文本开始呈现类似莎士比亚的结构，而不是噪声。
- 如果你想完全跳过 Python，使用更底层的方案，Karpathy 的 `llm.c` 可以在纯 C 环境下编译并运行在 CPU 上，完全不需要 PyTorch 依赖——既然 Mac Pro 上也没有 GPU 路径，不妨一试。

参考资料：
- [Running nanoGPT on a MacBook M2 — Simon Willison](https://til.simonwillison.net/llms/nanogpt-shakespeare-m2)
- [karpathy/nanoGPT](https://github.com/karpathy/nanoGPT)
- [PyTorch training on Apple Silicon — Hugging Face](https://huggingface.co/docs/transformers/v4.47.1/perf_train_special)