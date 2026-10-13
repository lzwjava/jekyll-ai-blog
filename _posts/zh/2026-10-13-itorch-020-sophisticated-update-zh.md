---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Itorch 0.2.0：精致更新
translated: true
type: note
---

完成 — **itorch 0.2.0**，所有三个测试套件全绿。以下是“更复杂”所换来的成果：

## 更新内容

**引擎**（`tensor.py`）
- `backward(retain_graph=True)` — 在遍历后释放计算图；对已释放的图再次调用 `backward()` 会抛出 `RuntimeError`（类似 torch），而叶张量仍可重用于新的计算图
- `y.grad_fn` → `"matmul((3,4),(4,5)) -> (3,5)"` 用于调试
- `no_grad` 现在也可用作装饰器（`@no_grad`）
- `gelu` 操作 + `Tensor.__array__`，使 numpy 能干净地互操作（期间发现了两个真正的遮蔽 bug：`Module.__call__` 错误切片多参数前向传播，以及内置 `sum` 与函数式 API 的冲突）

**层**（`nn.py`）
- 归一化：`LayerNorm`、`GroupNorm`、`AvgPool2d`（以及已有的 BatchNorms）
- 循环网络：`LSTM` 和 `GRU`（batch-first，返回 `(outputs, state)`），直接沿 autograd 图展开
- 注意力：`MultiHeadAttention`、`TransformerBlock`（pre-norm + 残差）、`Transformer`（因果堆叠）、`causal_mask`、`GELU`
- `Module.freeze()/unfreeze()`（修复了“冻结参数对 unfreeze 不可见”的循环陷阱）、`nn.Sequential` 等

**训练**
- `schedulers/`：`StepLR`、`MultiStepLR`、`CosineAnnealingLR`、`ReduceLROnPlateau`
- 损失函数：`l1`、`huber`、`nll_loss`；`cross_entropy` 重构为基于 `nll_loss`
- `count_parameters`、`DataLoader(drop_last=...)`

**亮点**：`examples/04_tiny_gpt.py` — 一个约 40k 参数的字符级 GPT（token + 位置嵌入 → 2 个因果 transformer 块 → LM 头）在数秒内完成训练：
```
step   20  loss=2.37  →  step 400  loss=0.13
"to be or not tr be, thanoure is the questististion..."  ← Shakespeare-sounding
```

## 验证
- `tests/test_sophisticated.py`（新增）：gelu/归一化/池化/GRU/LSTM/注意力/transformer/损失函数的梯度均与中心有限差分对照检查；调度器学习率曲线、retain-graph 语义、freeze/unfreeze 以及一个小型 transformer 训练循环均有断言。
- 所有之前的测试套件仍然通过——无回归。

需要我将其提交并推送为 v0.2.0 吗？