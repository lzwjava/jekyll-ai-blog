---
audio: false
generated: true
image: false
lang: zh
layout: post
title: itorch 0.4.0 DCGAN 和 Faster Conv
translated: true
type: note
---

完成 — **v0.4.0** 已提交并推送：

- **提交** `d19ef9c` — 7 个文件变更，+424 / -35
- **已推送** 到 `github.com:lzwjava/itorch.git`（`main` 分支上的 `8b7d333..d19ef9c`）

历史记录：
```
fb588c4  itorch：极简 autograd 深度学习库（tinygrad 风格，仅 numpy）     [v0.1.0]
0ac3959  itorch 0.2.0：transformer/RNN 支持、调度器、gradcheck 测试套件   [v0.2.0]
8b7d333  itorch 0.3.0：生成模型（col2im/ConvTranspose2d）、4 个优化器、VAE [v0.3.0]
d19ef9c  itorch 0.4.0：DCGAN 示例、gradcheck/profile 工具、卷积梯度快 17 倍  [v0.4.0]
```

该库现在可以训练 CNN、transformer、RNN、VAE 和 GAN——全部基于 numpy，约 3,600 行，5 套测试全绿。等你准备好后，接下来自然的候选方向是：`einsum`/`scatter` 算子完备性（op-completeness）这一轮，或者 Function-IR 重构，后者将能够实现真正的惰性 `@jit`。