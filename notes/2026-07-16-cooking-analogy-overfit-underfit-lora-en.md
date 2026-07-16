---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Cooking Analogy: Overfit, Underfit, LoRA"
translated: false
type: note
---

Question: Does the cooking analogy hold — stem position/doneness ≈ data distribution effects, dry-roast vs steam ≈ different training regimes causing overfit/underfit, and "soy sauce" fine-tuning after pretraining ≈ post-training adjustment?

Answer: Mostly right, with one correction on the fine-tuning metaphor.

**Overfit/underfit ≈ cooking method mismatch — correct.**

Steaming (moist heat) vs dry-roasting (no water) changes how heat transfers into the tissue — too much moisture and the veg turns mushy (overfit to noise in the water), too little heat/time and it's still raw (underfit). Same bias-variance story:

```python
import numpy as np

def fit_poly(x, y, degree):
    coeffs = np.polyfit(x, y, degree)
    return np.poly1d(coeffs)

np.random.seed(0)
x = np.linspace(0, 1, 15)
y_true = np.sin(2 * np.pi * x)
y = y_true + np.random.normal(0, 0.2, size=x.shape)  # noisy "wet" data

for deg, label in [(1, "underfit"), (3, "good fit"), (14, "overfit")]:
    f = fit_poly(x, y, deg)
    train_err = np.mean((f(x) - y) ** 2)
    print(f"degree={deg:2d} ({label:9s}) train_mse={train_err:.4f}")
```

Degree 1 can't capture the sine shape (underfit — undercooked, structure never developed). Degree 14 nails every noisy point exactly, including the noise (overfit — the veg absorbed the seasoning-water and turned soggy, memorized irrelevant fluctuation). Degree 3 tracks the true `sin` shape without chasing noise — that's the "properly cooked" model, low bias AND low variance.

**Soy sauce fine-tuning ≈ post-pretraining — partially right, needs a correction.**

Soy sauce implies *surface* seasoning: base ingredient's internal structure untouched, only flavor layered on top. Full fine-tuning isn't that gentle — it updates every weight, and can cause catastrophic forgetting (the base "flavor" gets partially cooked out, not just added to). The metaphor that actually matches "soy sauce" (light surface coating, base untouched) is **LoRA / adapter fine-tuning** — you freeze the pretrained weights (the cooked base) and add a small low-rank delta (the sauce) on top:

```python
# conceptually: W' = W_frozen + BA   (B, A low rank, W frozen)
# full fine-tune:  W' = W - lr * grad(W)   -> base itself changes
```

So:
- pretraining = cooking the base ingredient (structure/flavor baked in, expensive, slow, ~2B tokens/mo scale for you)
- full fine-tune = re-cooking with new seasoning mixed into the ingredient itself — changes the base
- LoRA/adapter fine-tune = literally soy sauce — cheap, reversible, doesn't touch the base weights
- distillation = passing the flavor to a smaller pot (student model) via the teacher's outputs

Karpathy's own "recipe" post uses this exact cooking framing for training dynamics — worth the reread given you're training GPT-2 760M yourself.

References:
- [A Recipe for Training Neural Networks — Karpathy](http://karpathy.github.io/2019/04/25/recipe/)
- [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685)
- [Bias–variance tradeoff — overfitting/underfitting formalism](https://en.wikipedia.org/wiki/Bias%E2%80%93variance_tradeoff)
