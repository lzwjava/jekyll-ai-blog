---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 昂贵的配置错误，廉价的预防测试
translated: true
type: note
---

没错，完全正确。编译时的类比非常贴切——而且问题会叠加：在第 48 小时发现的每个配置错误，都会浪费大约 48 小时的 GPU 时间加你的注意力。

**能在 10 分钟内发现此问题的低成本做法：**

1. **先冒烟测试配置**——使用 `max_iters=50, eval_interval=20, compile=False` 运行，验证：
   - 损失是否确实下降
   - 内存是否合适，峰值时无 OOM
   - Tokens/step × max_iters 是否与你预期的总预算一致
   - 检查点能否正常保存和恢复

2. **启动时打印预算**——在 `train.py` 中添加：

   ```python
   tokens_per_step = batch_size * block_size * gradient_accumulation_steps * ddp_world_size
   print(f"tokens/step = {tokens_per_step:,}")
   print(f"total tokens = {tokens_per_step * max_iters / 1e9:.2f}B")
   ```

   这一行代码在提交前就会显示“10.00B”——你会立刻注意到：“等等，我准备的是 140B。”

3. **使用 wandb**——设置 `wandb_log = True`（你已经设置了项目名称，只需切换标志即可）。你可以通过手机查看损失、学习率和梯度范数；如果损失在第 3 小时发散，你可以直接终止，而不是等到第 48 小时才发现。

4. **恢复而非重启**——`always_save_checkpoint = True` 已经开启。如果你之后决定延长训练，只需提高 `max_iters` 并从 `ckpt.pt` 恢复即可（nanoGPT 支持 `init_from='resume'`）。因此这两天并非完全浪费——你可以从第 19073 步继续，使用更多 tokens。

需要我帮你把预算打印功能添加到 `train.py` 中，并检查恢复并扩展的训练流程是否已正确配置吗？
