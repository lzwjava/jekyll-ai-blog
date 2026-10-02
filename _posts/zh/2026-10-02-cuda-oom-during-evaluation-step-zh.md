---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 评估步骤中的CUDA内存不足
translated: true
type: note
---

找到了。没有名为 `a` 的 tmux 会话（你的会话是 `0` = mihomo 代理 和 `1` = 训练 shell），但错误出现在 **会话 1** 中——训练运行在 **评估期间因 CUDA 内存不足错误而崩溃**。

## 错误信息

```
torch.OutOfMemoryError: CUDA out of memory. Tried to allocate 1.51 GiB.
GPU 0 has a total capacity of 11.56 GiB of which 1.16 GiB is free.
...
File ".../nanochat/gpt.py", line 515, in forward
    logits = softcap * torch.tanh(logits / softcap)   # squash the logits
```

## 发生了什么

1. 训练本身正常——它进行到了 **第 ~116 步**，损失值健康下降（约 4.12）。
2. 然后一个周期性的 **核心评估** 被触发。它顺利完成了 `coqa` 和 `boolq`。
3. 在 `bigbench_language_identification (10-shot)` 期间，评估对 **一个长输入/批量输入** 执行了前向传播，并在 `gpt.py:515` 的 logits-squash 行处发生了 OOM。
4. 进程终止并退回到 shell 提示符（`lzw@to:/mnt/data/nanochat$`）。

## 内存分布（GPU 0 总计 11.56 GiB）

- PyTorch 已分配：7.81 GiB
- PyTorch 预留但未分配：1.34 GiB（内存碎片）
- 当尝试再分配 1.51 GiB 时，仅剩 1.16 GiB 空闲

## 可能的修复

1. **减少内存碎片**（错误信息本身也建议这样做）：

   ```bash
   export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
   ```

2. **降低评估内存**——例如限制 `max_per_task`（`--core_metric_max_per_task` 标志），减小评估批大小，或对评估使用梯度/激活卸载。
3. **在评估前释放内存**——评估运行时训练状态（优化器/激活值）仍然驻留；评估虽然会在 `torch.no_grad()`（确实如此）下运行，但模型权重和训练缓冲区可能仍会竞争资源。考虑在 CPU 或独立进程中运行评估。

需要我查看 `base_train.py` / `core_eval.py` 以找到最简洁的修复方式（例如限制评估批长度或添加 `expandable_segments`）吗？
