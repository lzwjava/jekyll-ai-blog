---
audio: false
generated: true
image: false
lang: en
layout: post
title: v0.3.0 Adds Generative Models
translated: false
type: note
---

Done — **v0.3.0** committed and pushed:

- **Commit** `8b7d333` — 12 files changed, +835 / -81
- **Pushed** to `github.com:lzwjava/itorch.git` (`0ac3959..8b7d333` on `main`)

History:

```
fb588c4  itorch: minimal autograd deep learning library (tinygrad-style, numpy only)   [v0.1.0]
0ac3959  itorch 0.2.0: transformer/RNN support, schedulers, gradcheck suite           [v0.2.0]
8b7d333  itorch 0.3.0: generative models (col2im/ConvTranspose2d), 4 optimizers,
         nn.init, VAE example                                                         [v0.3.0]
```

The generated `examples/grid_vae.png` and MNIST cache are gitignored. The library now spans CNNs, transformers, RNNs, and generative models — all validated by numeric-gradient and end-to-end training tests. Keep going whenever you want!
