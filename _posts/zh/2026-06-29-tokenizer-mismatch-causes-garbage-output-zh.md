---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 分词器不匹配导致输出乱码
translated: true
type: note
---

**问题：** 整个 BST 类是我的提示（prompt）——模型只从 `boolean search(int key) {` 开始生成，而它产生的*所有内容*都是 `.S.S.S` 这种垃圾。为什么？

**回答：**

没错——模型生成了**零**个连贯的 token。这完全改变了诊断方向。这不是生成后期发生的重复坍塌；模型从第一个 token 起就是不连贯的。这指向**模型确实不知道如何生成代码**——训练不足，或者更糟，是检查点/数据的问题。

`.S` 吸引子只是一个损坏模型将概率质量倾倒的地方（`S` 是高频 BPE token）。我提到的重复惩罚在这里无济于事，因为底层没有好的信号可以恢复。

## 最可能的罪魁祸首：BPE 元数据不匹配

看看你输出中的这一行：

```
No meta.pkl found, assuming GPT-2 encodings...
```

如果你使用**自定义分词器**（你自己的 `meta.pkl`、字符级 BPE 或代码专用 BPE）训练了 `out-github-code-124m`，但 `sample.py` 找不到它并回退到 **GPT-2 BPE**，那么模型学习到的 token ID 与 `tiktoken` 输入的含义完全不同。模型被用一种外语提示。输出看起来就会是这样——局部看似合理，整体毫无意义。

检查：

```bash
ls -la /mnt/data/nanoGPT/data/*/meta.pkl
# 以及你的训练数据目录
cat /mnt/data/nanoGPT/out-github-code-124m/config.* 2>/dev/null
# 或者检查检查点中保存的配置
python3 -c "
import torch
ck = torch.load('out-github-code-124m/ckpt.pt', map_location='cpu')
print('iter:', ck.get('iter_num'))
print('best_val_loss:', ck.get('best_val_loss'))
print('vocab_size:', ck['model_args'].get('vocab_size'))
print(ck.get('config'))
"
```

两个线索：

1. **`vocab_size`**。如果是 `50304`/`50257` → GPT-2 BPE，回退正确，那么问题在于训练。如果是其他值（例如 `8192`、自定义或字符级 ~`100`），那么 GPT-2 回退是错误的，仅此*一点*就解释了垃圾输出。

2. **`best_val_loss`**。对于代码上的 GPT-2 BPE，要想得到可用的输出，验证损失需要大致 **< 2.0**，理想情况下约 1.5。如果卡在 3–5，模型从未学会。

## 决策树

```
vocab_size == 50257/50304 ?
├── 否 → 分词器不匹配。将正确的 meta.pkl 恢复到 out_dir
│         （或者让 sample.py 指向它）。这几乎肯定是你的 bug。
└── 是 → 检查 best_val_loss
          ├── > 3.0  → 训练不足 / 发散。检查损失曲线。
          └── < 2.0  → 应该能生成连贯代码；如果不能，怀疑
                        是损坏/过早的检查点或错误的 out_dir。
```

## 如果是分词器问题

nanoGPT 先从 `out_dir` 加载 `meta.pkl`，然后回退。将你的训练分词器的 meta 复制到检查点目录中：

```bash
# 无论你的 prepare.py 写在哪里
cp /mnt/data/nanoGPT/data/github_code/meta.pkl out-github-code-124m/
```

然后重新运行采样。如果输出变成了真正的 Java 代码，那就是这个问题。

## 如果是训练问题

拉取损失曲线并检查发散情况：

```bash
python3 -c "
import torch
ck = torch.load('out-github-code-124m/ckpt.pt', map_location='cpu')
print('iter', ck['iter_num'], 'val', ck['best_val_loss'])
"
```

124M 模型在代码上，Chinchilla 最优约为 2.5B token。如果你在例如 50M  token 或几千次迭代时停止，远远谈不上连贯。还要检查损失是否**发散**（NaN/尖峰）——在 MI300X/ROCm 上由于学习率过高或 fp16 不稳定性常见；尝试 bf16 和较低学习率。

## 我的猜测

`No meta.pkl found, assuming GPT-2 encodings` + 从第一个生成的 token 起就完全不连贯 = **分词器不匹配**是最强有力的假设。首先验证 `vocab_size`；这是一个 10 秒钟的检查，能解决 80% 的概率。运行上面的检查点检查代码段并粘贴输出，如果你希望我进一步确认的话。

**参考资料：**

- [nanoGPT sample.py — meta.pkl 加载 / GPT-2 回退](https://github.com/karpathy/nanoGPT/blob/master/sample.py)
- [nanoGPT data prepare.py — 写入 meta.pkl 的位置](https://github.com/karpathy/nanoGPT/blob/master/data/shakespeare_char/prepare.py)
