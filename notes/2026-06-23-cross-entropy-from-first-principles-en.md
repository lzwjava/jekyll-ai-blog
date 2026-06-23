---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cross-Entropy from First Principles
translated: false
type: note
---

**Question:** Explain cross-entropy from first principles using math.

**Answer:**

## Cross-Entropy: Full Mathematical Derivation

---

### 1. Start from Information Theory

For an event with probability `p`, the **surprisal** (self-information) is:

```
I(x) = −log p(x)
```

Units depend on log base: base-2 = bits, base-e = nats. PyTorch uses `ln` (nats).

**Why negative log?** Three axioms force this form:

- Certain event `p=1` → zero surprise: `−log(1) = 0` ✓
- Impossible event `p→0` → infinite surprise: `−log(0) = ∞` ✓
- Independent events multiply in probability, add in surprise: `−log(p·q) = −log p − log q` ✓

---

### 2. Shannon Entropy H(p)

Expected surprisal under the **true** distribution:

```
H(p) = 𝔼_{x∼p}[−log p(x)] = −Σₓ p(x) log p(x)
```

This is the **minimum average code length** achievable when you know the true distribution. It's a lower bound — you can't do better.

---

### 3. Cross-Entropy H(p, q)

Now suppose you **don't** know `p`. You design your code assuming distribution `q`, but reality samples from `p`:

```
H(p, q) = 𝔼_{x∼p}[−log q(x)] = −Σₓ p(x) log q(x)
```

Break it down:

| Term | Meaning |
|------|---------|
| `−log q(x)` | code length you assigned to event x (wrong assumption) |
| `p(x)` | true weight — how often x actually occurs |
| `Σₓ p(x) · [−log q(x)]` | expected cost under reality |

---

### 4. The KL Decomposition (most important identity)

```
H(p, q) = H(p) + D_KL(p ∥ q)
```

**Proof:**

```
D_KL(p ∥ q) = Σₓ p(x) log [p(x) / q(x)]
             = Σₓ p(x) [log p(x) − log q(x)]
             = Σₓ p(x) log p(x)  −  Σₓ p(x) log q(x)
             = −H(p)             +  H(p, q)

→ H(p, q) = H(p) + D_KL(p ∥ q)    □
```

Since `D_KL ≥ 0` always (Gibbs' inequality), this gives:

```
H(p, q) ≥ H(p)
```

Equality iff `p = q`. **This is why minimizing cross-entropy works** — `H(p)` is constant during training (labels fixed), so:

```
argmin_q H(p, q)  =  argmin_q D_KL(p ∥ q)
```

---

### 5. One-Hot Collapse (language modeling case)

In LM training, `p` is one-hot over vocabulary: `p(y=k) = 1`, all others `= 0`.

The sum over all classes collapses to a single term:

```
H(p, q) = −Σₓ p(x) log q(x)
         = −[0·log q(x₁) + ··· + 1·log q(y_true) + ··· + 0·log q(xₙ)]
         = −log q(y_true)
```

**That's the entire loss** — just the negative log-probability the model assigned to the correct token. Every other class contributes zero because `p(x≠y_true) = 0`.

---

### 6. The Softmax + Log-Sum-Exp Chain

Your model outputs logits `z ∈ ℝᶜ`. The softmax gives:

```
q(y=k) = exp(zₖ) / Σⱼ exp(zⱼ)
```

Plugging into cross-entropy for one-hot target class `c`:

```
L = −log q(y=c)
  = −log [ exp(zc) / Σⱼ exp(zⱼ) ]
  = −zc + log Σⱼ exp(zⱼ)
  = −zc + LogSumExp(z)
```

This is what `F.cross_entropy` computes **directly** — no intermediate softmax. The gradient is clean:

```
∂L/∂zₖ = q(y=k) − 𝟙[k=c]
```

= predicted probability minus the one-hot truth. For the correct class `k=c`:

```
∂L/∂zc = q(y=c) − 1
```

Negative when model is underconfident → gradient pushes `zc` up. For wrong classes:

```
∂L/∂zₖ = q(y=k)   (k ≠ c)
```

Positive → gradient pushes `zₖ` down. The gradient **is** the residual between prediction and truth. Beautiful.

---

### 7. Full Picture

```
Reality (true labels p)
        │
        │ samples x with prob p(x)
        ▼
Cost assigned by model: −log q(x)    ← depends on q only
        │
        │ weight by p(x), sum
        ▼
H(p,q) = H(p) ──────────────────┐
               + D_KL(p‖q) ◄────┘ ← this is what training minimizes
                    ↑
                    └── zero only when q = p (perfect model)
```

---

### Intuition in one sentence

> Cross-entropy is the average number of nats your model wastes by being wrong about the distribution — entropy is the unavoidable floor, KL is the fixable gap.
