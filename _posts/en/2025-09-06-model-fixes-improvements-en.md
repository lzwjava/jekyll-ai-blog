---
audio: false
date: 2025-09-06
generated: true
image: false
lang: en
layout: post
title: Model Shape Fixes and Improvements
translated: false
type: note
---

Here’s what your script is doing, piece by piece, plus a couple of important fixes you’ll likely want to make.

# What the model is

* You define a tiny **character/word-level next-token predictor**:

  * `nn.LSTM(input_size=vocab_size, hidden_size=50, num_layers=1)` processes a sequence of one-hot vectors (size = `vocab_size`) and produces a hidden state of size 50 at each time step.
  * `nn.Linear(50, vocab_size, bias=False)` maps each time step’s hidden state to **logits over the vocabulary**.

# Expected tensor shapes (critical)

PyTorch LSTM’s default input shape is **(seq\_len, batch\_size, input\_size)** because you didn’t set `batch_first=True`.

* For a single sequence in a batch of 1:

  * Inputs to LSTM should be `(seq_len, 1, vocab_size)`.
  * LSTM outputs `x` with shape `(seq_len, 1, hidden_size)`.
  * You then `view(-1, hidden_size)` → `(seq_len, hidden_size)` so the linear layer produces `(seq_len, vocab_size)`.
  * `CrossEntropyLoss` expects:

    * `outputs`: `(N, C)` = `(seq_len, vocab_size)`
    * `targets`: `(N,)` = `(seq_len,)` token indices

# Where your code likely goes wrong (shape)

You do:

```python
inputs_one_hot = inputs_one_hot.permute(0, 2, 1)
```

If `one_hot_encode_sequence` returns `(batch, seq_len, vocab)`, the correct permute for default LSTM is **`permute(1, 0, 2)`** (to get `(seq_len, batch, vocab)`). Your current `permute(0,2,1)` gives `(batch, vocab, seq_len)`, which is mismatched and will either error or silently learn nonsense if the earlier shape is different than assumed.

Two clean options (pick one):

**A) Keep default LSTM (batch\_second):**

```python
# want (seq_len, batch, input_size)
inputs_one_hot = inputs_one_hot.permute(1, 0, 2)  # (seq_len, 1, vocab_size)
```

**B) Make it batch-first (often simpler):**

```python
self.lstm = nn.LSTM(input_size=vocab_size, hidden_size=50, batch_first=True)
# want (batch, seq_len, input_size)
# then DO NOT permute; leave as (1, seq_len, vocab_size)
```

# Training loop logic

* You keep two running sums per epoch: `epoch_training_loss` and `epoch_validation_loss`.
* **Validation phase** (`net.eval()` + no gradient steps):

  * For each (inputs, targets) in `validation_set`:

    * one-hot encode inputs, convert targets to indices
    * forward pass → logits `(seq_len, vocab_size)` (assuming shapes fixed)
    * CE loss against target indices of shape `(seq_len,)`
    * accumulate loss
* **Training phase** (`net.train()`):

  * Same preprocessing
  * forward → loss → `optimizer.zero_grad()` → `loss.backward()` → `optimizer.step()`
* You record average losses and print every 5 epochs.

# Inference & printout

* You pick a sample from `test_set`, run the model, get logits for each time step, take `argmax` per time step → predicted tokens.
* You print input words, target words, and predicted words.
* You plot training vs validation loss over epochs.

# Small, high-impact improvements

1. **Fix the input shape** (most important). Use one of A or B above. If you choose batch-first, change the forward pass to:

   ```python
   x, (h, c) = self.lstm(x)         # x: (batch, seq, hidden)
   x = x.reshape(-1, self.lstm.hidden_size)  # (batch*seq, hidden)
   ```

2. **Use `with torch.no_grad()` for eval/inference** to avoid tracking gradients and for speed/memory:

   ```python
   net.eval()
   with torch.no_grad():
       outputs = net(inputs_one_hot)
       loss = criterion(outputs, targets_idx)
   ```

   And for numpy conversion:

   ```python
   outputs = net(inputs_one_hot).detach().numpy()
   ```

3. **Seed PyTorch too** for reproducibility:

   ```python
   torch.manual_seed(42)
   ```

4. **Device handling** (if you use GPU):

   ```python
   device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
   net.to(device)
   inputs_one_hot = inputs_one_hot.to(device)
   targets_idx = targets_idx.to(device)
   ```

5. **Target alignment**: make sure `targets` are the **next tokens** aligned with each input time step. If your dataset pairs `(inputs, targets)` that way, you’re good. Otherwise, create `targets = inputs[1:]` and drop the last input or similar.
6. **Drop `.bias=False` unless you have a reason**; a bias on the output layer is usually harmless/helpful.
7. **Padding/variable lengths** (optional): if sequences have varying lengths, consider `pack_padded_sequence` to avoid training on padding tokens.
8. **Monitoring**: accuracy over the next-token predictions can be more interpretable than loss alone—compute `% correct argmax` on validation.

# Minimal corrected snippet (batch-first version)

```python
class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.lstm = nn.LSTM(input_size=vocab_size, hidden_size=50, num_layers=1, batch_first=True)
        self.l_out = nn.Linear(50, vocab_size)

    def forward(self, x):
        # x: (batch, seq, vocab_size)
        x, _ = self.lstm(x)                    # (batch, seq, hidden)
        x = x.reshape(-1, self.lstm.hidden_size)  # (batch*seq, hidden)
        x = self.l_out(x)                      # (batch*seq, vocab)
        return x

# ... in your loop, remove the permute; ensure inputs_one_hot is (batch, seq, vocab)
# validation/inference use `with torch.no_grad()` and `.detach()`
```

If you share the exact shape that `one_hot_encode_sequence` returns (e.g., `(seq, vocab)` vs `(1, seq, vocab)`), I can tailor the permute/reshape lines precisely for your case.
