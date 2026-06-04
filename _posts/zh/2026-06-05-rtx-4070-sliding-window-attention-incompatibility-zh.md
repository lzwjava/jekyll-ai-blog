---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RTX 4070滑动窗口注意力不兼容
translated: true
type: note
---

问题：为什么训练运行失败，错误信息提到 `window_pattern="SSSL"` 且 RTX 4070 不支持 sliding window attention？

答案：

问题出在你脚本中使用的注意力模式与你的 GPU 支持情况不匹配。以下是详细说明：

1. **注意力模式：**
   * `L` = full context attention（完整上下文注意力，对整个序列进行标准注意力）。
   * `S` = sliding window attention（滑动窗口注意力，一种仅关注小范围 token 的内存高效近似方法）。

2. **硬件限制：**
   * 在你的 **RTX 4070** 上，框架中的 SDPA（Scaled Dot-Product Attention）实现 **不支持 sliding window attention**。
   * 这就是使用包含 sliding window `S` 的 `window_pattern="SSSL"` 时触发错误的原因。

3. **之前的运行成功：**
   * 之前的运行使用了 `"L"`（完整注意力），你的 GPU 支持该模式，因此运行正常。

4. **解决方案：**
   * 你需要在脚本中显式设置 `--window-pattern L`，使模型使用 **full context attention**，这与你的 RTX 4070 兼容。
   * 本质上，脚本默认使用了 sliding window 配置，而你的 GPU 无法处理该配置。

5. **后续步骤：**
   * 终止当前的运行（它只进行到第 10k 步，尚未开始真正的训练）。
   * 编辑你的 `run_rtx4070_chinchilla.sh` 脚本，在启动训练的命令中添加 `--window-pattern L`。
   * 重新启动运行。

这**不是代码中的 bug**——仅仅是注意力模式与硬件兼容性问题。

如果你需要，我可以提供在脚本中需要修改的具体代码片段，以确保它能无错误地运行。
