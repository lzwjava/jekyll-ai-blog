---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fast Conv and Adversarial Training
translated: false
type: note
---

**Round 4 complete → itorch 0.4.0** (~3,560 lines). This round was "make it fast and prove it trains adversarially":

## What landed

**1. Conv engine perf — 17× faster gradients**

- Replaced the 6-D `np.add.at` scatter in `im2col`/`col2im` with **per-tap strided adds** (`gp[..., i : i+s·(oh−1)+1 : s] += tap`)
- Measured: **185 ms → 10.6 ms** per conv backward on a realistic shape (equivalence verified by existing gradchecks + new identity/adjoint/overlap-add tests)

**2. Basic-slice backward optimization**

- Found via profiling that `ConvTranspose2d`'s output crop (`canvas[:, :, p:p+oh, ...]`) was paying for generic `np.add.at`. Basic slice/index backprops now use unique `zero[idx] = g` placement (fast zero-pad). **DCGAN step went 700 ms → 100 ms.**

**3. `tt.gradcheck()`** — user-facing gradient validation

```python
tt.gradcheck(lambda x: (x.silu()**2).sum(), tt.randn(4, 3, requires_grad=True))
```

Passes silently on good gradients, `ValueError`s on bad ones (test proves it catches an intentionally wrong backward).

**4. `tt.profile()`** — per-op backward profiler (`with tt.profile() as p: loss.backward(); p.report()`). Dogfooded on DCGAN: showed matmul 47% / im2col 16% / getitem 11%, which is exactly how I found the slicing issue.

**5. Showpiece: `examples/06_dcgan_mnist.py`** — adversarial min-max training on our own `ConvTranspose2d`/`LeakyReLU`:

```
step 1000  D=1.207 (real 0.852, fake 0.355)  G=0.772
```

**256/256 generated digits with healthy ink coverage** (median 9.8%, like real MNIST).

## Verification

- New `tests/test_round4.py`: gradcheck utility (positive + negative), profiler, conv identities (exact round-trip for non-overlapping windows, finite-difference adjoint for arbitrary params, overlap-add semantics), slicing backprop offsets, DCGAN smoke
- All **5 suites green**

Shipped as v0.4.0. Want me to commit and push?
