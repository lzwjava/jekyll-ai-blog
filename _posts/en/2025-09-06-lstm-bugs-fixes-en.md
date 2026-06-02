---
audio: false
date: 2025-09-06
generated: true
image: false
lang: en
layout: post
title: LSTM Implementation Bugs and Fixes
translated: false
type: note
---

Got it—here’s a clear, end-to-end walkthrough of what this LSTM-from-scratch script is doing, plus the subtle bugs that will break training and how to fix them. I’ll keep it linear and easy to scan (no wide tables).

# What the code tries to do

You’re implementing a minimal character/word-level LSTM language model in NumPy:

1. **Setup & sizes**

* `hidden_size`, `vocab_size`, datasets (`training_set`, `validation_set`, `test_set`), token↔index maps, and functions like `sigmoid`, `tanh`, `softmax`, `one_hot_encode_sequence` are expected to come from `data.py` / `utils.py`.
* Each time step’s input is a one-hot vector `x ∈ R^{vocab_size×1}`.
* You concatenate previous hidden state and current input:
  `z = [h_{t-1}; x_t] ∈ R^{(hidden_size+vocab_size)×1}`.
  That’s why `W_f, W_i, W_g, W_o ∈ R^{hidden_size×(hidden_size+vocab_size)}`.

2. **Parameter initialization**

* `init_lstm(...)` allocates weights for the four gates (forget f, input i, candidate g, output o), plus the output projection `W_v` to vocabulary.
* `init_orthogonal` makes each weight matrix orthonormal (via QR). That’s a decent choice for RNNs/LSTMs.

3. **Forward pass (per sequence)**
   For each time step:

* Build `z = [h_prev; x]`.
* Compute gates:

  * `f_t = σ(W_f z + b_f)`
  * `i_t = σ(W_i z + b_i)`
  * `g_t = tanh(W_g z + b_g)`
  * `C_t = f_t ⊙ C_{t-1} + i_t ⊙ g_t`
  * `o_t = σ(W_o z + b_o)`
  * `h_t = o_t ⊙ tanh(C_t)`
* Project to vocab and softmax:

  * `v_t = W_v h_t + b_v`
  * `ŷ_t = softmax(v_t)`
* The code stores lots of intermediates (`z_s, f_s, i_s, g_s, C_s, o_s, h_s, v_s, output_s`) for backprop.

4. **Loss**

* Cross-entropy at each step with a one-hot target:
  `L_t = − log ŷ_t[target]`
  (The code uses an elementwise `-mean(log(ŷ)*one_hot)`, which is equivalent to `-log(ŷ[target])` up to a constant scaling.)

5. **Backward pass (BPTT through LSTM)**

* Classic LSTM gradients, accumulated from `t = T−1 → 0`.
* Clip global gradient norm, then SGD update.

6. **Training loop**

* For each epoch: evaluate on validation set (just loss), then train on training set (loss + grads + update). Finally, plot training/validation losses.

---

# Critical issues (these will silently break learning)

## 1) Off-by-one indexing for `h` and `C` in backprop

In `forward`, you push the *initial* states first:

* `h_s[0] = h_init`, then after step 0 you append `h_0` → so `h_s` has length `T+1` with `h_s[t+1] = h_t`.
* Same for `C_s`: `C_s[0] = C_init`, then `C_s[t+1] = C_t`.

But in `backward(...)` you use `h[t]` and `C[t]` as if they were `h_t` and `C_t`. They aren’t; they’re shifted by one.

**Fix (simple rule of thumb):**

* Use `h[t+1]` where you want `h_t`.
* Use `C[t+1]` where you want `C_t`.
* For “previous cell state” you want `C_prev = C[t]` (not `C[t-1]`).

So inside the `for t in reversed(range(T)):` loop:

* Current state: `h_t = h[t+1]`, `C_t = C[t+1]`
* Previous state: `C_{t-1} = C[t]`

Your current line:

```python
C_prev = C[t - 1]
```

is wrong for `t==0` (wraps to the last element) and off by one in general. It must be:

```python
C_prev = C[t]       # previous cell state
# and use C_t = C[t+1] as "current"
```

And anywhere you use `h[t]` intending the current hidden state, change to `h[t+1]`.

## 2) Wrong derivatives for several gates

You sometimes apply the nonlinearity again instead of its derivative, or forget the derivative flag.

* **Cell state path:**
  Correct:
  `dC_t += dh_t ⊙ o_t ⊙ (1 - tanh(C_t)^2)`
  Your code:

  ```python
  dC += dh * o[t] * tanh(tanh(C[t]), derivative=True)
  ```

  That’s `tanh` applied twice. Replace with:

  ```python
  dC += dh * o_t * (1 - np.tanh(C_t)**2)
  ```

* **Forget gate:**
  Correct: `df = dC_t ⊙ C_{t-1} ⊙ f_t ⊙ (1 - f_t)`
  Your code:

  ```python
  df = dC * C_prev
  df = sigmoid(f[t]) * df
  ```

  Missing the derivative term. Should be:

  ```python
  df = dC * C_prev
  df *= f[t] * (1 - f[t])      # if f[t] stores σ pre-activation output
  ```

* **Input gate:**
  You did:

  ```python
  di = dC * g[t]
  di = sigmoid(i[t], True) * di
  ```

  This is fine **if** `sigmoid(x, True)` returns σ’(x) *not* σ(x). More robust (matching how you stored `i[t]` as the gate output) is:

  ```python
  di = dC * g[t]
  di *= i[t] * (1 - i[t])
  ```

* **Candidate gate:**
  You did:

  ```python
  dg = dC * i[t]
  dg = tanh(g[t], derivative=True) * dg
  ```

  If `g[t]` stores `tanh(preact)`, then `tanh’(preact) = 1 - g[t]^2`. So:

  ```python
  dg = dC * i[t]
  dg *= (1 - g[t]**2)
  ```

* **Output gate:**
  You did:

  ```python
  do = dh * tanh(C[t])
  do = sigmoid(o[t], derivative=True) * do
  ```

  With the indexing fix (`C_t = C[t+1]`, `o_t = o[t]`) and derivative as above:

  ```python
  do = dh * np.tanh(C_t)
  do *= o[t] * (1 - o[t])
  ```

* **Next cell gradient:**
  Correct:

  ```python
  dC_next = dC * f[t]
  ```

## 3) Using `h[0]` / `C[0]` to size `dh_next` and `dC_next`

You want shapes of the **current** h/C (end-of-sequence), not the initial zeros. Use:

```python
dh_next = np.zeros_like(h[-1])
dC_next = np.zeros_like(C[-1])
```

## 4) Cross-entropy arithmetic stability

`loss += -np.mean(np.log(outputs[t]) * targets[t])` will be fine if `softmax` clamps/epsilons internally. If not, add a small epsilon:

```python
eps = 1e-12
loss += -np.sum(targets[t] * np.log(outputs[t] + eps))
```

## 5) Training stability tweaks

* **Forget-gate bias:** initialize `b_f` to a positive value (e.g., `1.0`) so early in training the LSTM tends to keep memory:

  ```python
  b_f = np.ones((hidden_size, 1)) * 1.0
  ```

* **Learning rate:** `lr=1e-1` with raw SGD is aggressive. Start `1e-2` or use Adam.
* **Gradient clipping:** Good. Consider per-matrix norms if needed.

---

# A corrected core for the backprop loop

This sketch shows the indexing and derivative fixes. It assumes `f[t], i[t], g[t], o[t]` are *outputs* of their nonlinearities (as in your forward):

```python
T = len(outputs)
dh_next = np.zeros_like(h[-1])
dC_next = np.zeros_like(C[-1])

for t in reversed(range(T)):
    # Short names with correct indexing
    y_hat = outputs[t]                 # softmax output
    y_true = targets[t]
    h_t   = h[t+1]
    C_t   = C[t+1]
    C_tm1 = C[t]

    # Output layer
    dv = y_hat.copy()
    dv[np.argmax(y_true)] -= 1
    W_v_d += dv @ h_t.T
    b_v_d += dv

    # Backprop into h
    dh = W_v.T @ dv
    dh += dh_next

    # Output gate
    do = dh * np.tanh(C_t)
    do *= o[t] * (1 - o[t])
    W_o_d += do @ z[t].T
    b_o_d += do

    # Cell state
    dC = dC_next + dh * o[t] * (1 - np.tanh(C_t)**2)

    # Candidate (g), Input (i), Forget (f)
    dg = dC * i[t]
    dg *= (1 - g[t]**2)               # since g[t] = tanh(preact)

    di = dC * g[t]
    di *= i[t] * (1 - i[t])

    df = dC * C_tm1
    df *= f[t] * (1 - f[t])

    # Accumulate gate weight/bias grads
    W_g_d += dg @ z[t].T;  b_g_d += dg
    W_i_d += di @ z[t].T;  b_i_d += di
    W_f_d += df @ z[t].T;  b_f_d += df

    # Propagate to z and split to h_{t-1} part
    dz = (W_f.T @ df) + (W_i.T @ di) + (W_g.T @ dg) + (W_o.T @ do)
    dh_next = dz[:hidden_size, :]
    dC_next = dC * f[t]
```

---

# Smaller but important details & recommendations

* **Orthogonal init:** Good for recurrent weights. For input parts, you could also scale by `1/√fan_in`. Not critical here.
* **Batching:** The code trains on 1 sequence at a time (no batching). Fine for clarity, but slow/noisy. Mini-batching would require careful shape changes.
* **Teacher forcing:** You’re using ground-truth next token as the target; all good. If you ever do free-running generation, sample from `softmax` outputs and feed back into the model.
* **Loss reporting:** You sum per-time-step losses across sequences and then average by dataset length; that mixes scales if sequences vary in length. Consider normalizing by total tokens.
* **Plotting:** Works locally. In headless environments, remember to switch backends or savefig.

---

# TL;DR of the fixes you should make right now

1. **Indexing**: Replace every `h[t]` with `h[t+1]`, every `C[t]` with `C[t+1]`, and set `C_prev = C[t]` in backprop.
2. **Derivatives**:

   * Use `(1 - tanh(C_t)**2)` for the cell state path.
   * Use `gate * (1 - gate)` for the σ-gates since you stored gate outputs.
   * Use `(1 - g[t]**2)` for the candidate gate since `g[t]=tanh(preact)`.
3. **Init**: Set `b_f` to \~`1.0`.
4. **LR**: Drop to `1e-2` (or switch to Adam).
5. **Stability**: Add `eps` in `log`.

Make those changes and your loss should start decreasing in a much more sensible way. If you want, paste your updated `backward(...)` and I’ll sanity-check it.
