---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PyTorch训练循环中的tqdm
translated: true
type: note
---

问题：在 PyTorch/LLM 训练循环中，tqdm 有什么作用？

答案：`tqdm` 仅仅是一个围绕任意可迭代对象的进度条包装器。在训练循环中，它包裹数据加载器（或步骤范围），从而提供迭代速度、预计剩余时间以及实时更新的后缀（显示损失/学习率/梯度范数）——仅此而已，不涉及框架魔法。

```python
from tqdm import tqdm

for epoch in range(epochs):
    pbar = tqdm(train_loader, desc=f"epoch {epoch}")
    for batch in pbar:
        x, y = batch
        optimizer.zero_grad()
        logits = model(x)
        loss = F.cross_entropy(logits.view(-1, vocab_size), y.view(-1))
        loss.backward()
        optimizer.step()

        pbar.set_postfix(loss=loss.item(), lr=optimizer.param_groups[0]['lr'])
```

关键机制：
- `tqdm(iterable)` 返回一个生成器包装器——它会事先对可迭代对象调用 `len()`（如果可用）（数据加载器通过 `len(dataset)/batch_size` 提供 `__len__`），从而计算进度条及预计剩余时间的总数。
- `set_postfix(**kwargs)` 在不换行的情况下更新进度条尾部的 `{...}` 字典——这正是用于实时显示损失、学习率、每秒 token 数的方法。
- `set_description(str)` 更新前导标签（例如 `f"loss {loss:.4f}"`）。
- 内部会对刷新进行限流（默认 `mininterval=0.1s`），以避免在快速循环中频繁输出到 stdout——当你在 H100/MI300X 上每秒执行数千个微批次时，这一点很重要，否则 stdout 刷新本身会成为瓶颈。
- 在多 GPU/分布式（DDP）场景下，应将 `tqdm` 放在 `if rank == 0:` 后面——每个 rank 都输出自己的进度条会造成混乱。
- 嵌套进度条：外层用 `tqdm(range(epochs))`，内层用 `tqdm(train_loader, leave=False)`——`leave=False` 会清除内层进度条，避免每个 epoch 都堆积。
- 对于 token 吞吐量样式的日志记录（常见于你的 GPT-2 预训练运行中），人们会手动计算 `tokens/sec` 并将其塞入 `set_postfix`——tqdm 本身只跟踪 `it/s`，不跟踪领域特定的吞吐量。

它纯粹是外观/可观测性方面的工具——对梯度、分布式通信或实际训练数学没有任何影响。如果在高步率下它拖慢了你的速度（很少见，但在使用小批量的超快 H100 循环中可能发生），可以通过 `disable=True` 禁用它，或者增大 `mininterval`。

参考资料：
- [tqdm 文档](https://tqdm.github.io/)
- [tqdm GitHub](https://github.com/tqdm/tqdm)