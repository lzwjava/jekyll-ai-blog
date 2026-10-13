---
audio: false
generated: true
image: false
lang: en
layout: post
title: itorch 0.4.0 DCGAN and Faster Conv
translated: false
type: note
---

Done — **v0.4.0** committed and pushed:

- **Commit** `d19ef9c` — 7 files changed, +424 / -35
- **Pushed** to `github.com:lzwjava/itorch.git` (`8b7d333..d19ef9c` on `main`)

History:
```
fb588c4  itorch: minimal autograd deep learning library (tinygrad-style, numpy only)     [v0.1.0]
0ac3959  itorch 0.2.0: transformer/RNN support, schedulers, gradcheck suite             [v0.2.0]
8b7d333  itorch 0.3.0: generative models (col2im/ConvTranspose2d), 4 optimizers, VAE    [v0.3.0]
d19ef9c  itorch 0.4.0: DCGAN example, gradcheck/profile utils, 17x faster conv grads    [v0.4.0]
```

The library now trains CNNs, transformers, RNNs, VAEs, and GANs — all numpy, ~3,600 lines, 5 green test suites. Natural next candidates whenever you're ready: the `einsum`/`scatter` op-completeness round, or the Function-IR refactor that would enable a true lazy `@jit`.
