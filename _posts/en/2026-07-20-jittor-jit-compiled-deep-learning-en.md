---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Jittor: JIT-Compiled Deep Learning"
translated: false
type: note
---

Question: What's Jittor (github.com/Jittor/jittor)?

Answer: Jittor is a DL framework out of Tsinghua's CSCG group, key difference vs PyTorch/TF is that the **entire framework is JIT-compiled at runtime**, not just the ops.

Core idea:
- Python front-end, dynamic graph (imperative, like PyTorch's `nn.Module`/autograd style), but every op call generates and compiles C++/CUDA code on the fly and caches it.
- **Meta-operators**: instead of hand-writing each fused kernel (conv, pooling, etc.), they define a small set of primitive meta-ops that get combined and JIT-fused into specialized kernels per shape/dtype/device. Their claim: this gets close to hand-tuned CUDA perf without writing CUDA for every op combo.
- Unified compute graph across ops (not eager per-op dispatch like PyTorch), so the compiler can fuse and optimize across multiple ops before running.

API-wise it mimics PyTorch pretty closely:

```python
import jittor as jt
from jittor import Module, nn

class Model(Module):
    def __init__(self):
        self.layer1 = nn.Linear(1, 10)
        self.relu = nn.Relu()
        self.layer2 = nn.Linear(10, 1)
    def execute(self, x):   # forward() -> execute()
        x = self.layer1(x)
        x = self.relu(x)
        return self.layer2(x)

model = Model()
optim = nn.SGD(model.parameters(), 0.1)
jt.flags.use_cuda = 1
```

Notable things:
- `execute()` instead of `forward()`.
- `Var` instead of `Tensor`, computation is async — `.data` forces sync.
- Custom ops: write the op in C++/CUDA, JIT-compiled inline, no separate `setup.py build_ext` step like PyTorch extensions.
- Backend: g++/clang++, supports CUDA >=10, AMD ROCm >=4.0, and even Hygon DCU (Chinese domestic GPU).
- License Apache 2.0, ~3.2k stars, actively maintained (latest release 1.3.10.0), Python 54% / C++ 39% split.

Where it fits: mostly used in Chinese academic CV/graphics research (differentiable rendering, geometric learning are explicitly called out) — niche compared to PyTorch/JAX, but the JIT meta-operator design is a legit alternative angle to `torch.compile`/XLA fusion if you want to dig into compiler-level DL framework design.

References:
- [Jittor/jittor](https://github.com/Jittor/jittor)
- [Jittor Website](https://cg.cs.tsinghua.edu.cn/jittor/)
