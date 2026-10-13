---
audio: false
generated: true
image: false
lang: zh
layout: post
title: v0.3.0 新增生成模型
translated: true
type: note
---

完成 — **v0.3.0** 已提交并推送：

- **提交** `8b7d333` — 12 个文件变更，+835 / -81
- **推送** 到 `github.com:lzwjava/itorch.git`（`main` 分支上的 `0ac3959..8b7d333`）

历史：
```
fb588c4  itorch: minimal autograd deep learning library (tinygrad-style, numpy only)   [v0.1.0]
0ac3959  itorch 0.2.0: transformer/RNN support, schedulers, gradcheck suite           [v0.2.0]
8b7d333  itorch 0.3.0: generative models (col2im/ConvTranspose2d), 4 optimizers,
         nn.init, VAE example                                                         [v0.3.0]
```

生成的 `examples/grid_vae.png` 和 MNIST 缓存已被 git 忽略。该库现在涵盖 CNN、transformer、RNN 和 generative models——全部通过 numeric-gradient 和 end-to-end training tests 验证。随时可以继续！