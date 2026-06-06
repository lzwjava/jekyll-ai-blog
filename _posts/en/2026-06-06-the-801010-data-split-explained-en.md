---
audio: false
generated: true
image: false
lang: en
layout: post
title: The 80/10/10 Data Split Explained
translated: false
type: note
---

Question: Can you explain the 80/10/10 train/validation/test split used in nanoGPT and nanochat, and why this separation matters?

Answer:

Yes, exactly. The **8/1/1 split** (80% train, 10% val, 10% test) is standard in nanoGPT/nanochat. Here's the principle and implementation:

## Why Three Sets?

**Train set (80%)**: Learn the parameters. Gradient updates only happen here.

**Validation set (10%)**: Tune hyperparameters and detect overfitting. You evaluate on val during training (every N steps) to watch loss diverge between train and val — that's your overfitting signal.

**Test set (10%)**: Final evaluation. You touch this *once* at the end, after all hyperparameter tuning is locked. This gives an unbiased estimate of generalization performance.

The critical thing: **val and test must be completely separated from train**. If you touch test during training (to pick hyperparams), you leak information and your final number is meaningless.

## Implementation in nanoGPT

```python
# Typical split in nanoGPT
data = np.memmap('data.bin', dtype=np.uint16, mode='r')
n = len(data)

train_data = data[:int(0.8*n)]      # 80% for training
val_data = data[int(0.8*n):int(0.9*n)]   # 10% for validation
test_data = data[int(0.9*n):]       # 10% for test

def get_batch(split, batch_size=32):
    """Sample a batch during training"""
    if split == 'train':
        ix = torch.randint(len(train_data) - context_length, (batch_size,))
        x = torch.stack([torch.from_numpy((train_data[i:i+context_length]).astype(np.int64)) for i in ix])
        y = torch.stack([torch.from_numpy((train_data[i+1:i+1+context_length]).astype(np.int64)) for i in ix])
    else:  # val or test
        ix = torch.randint(len(val_data) - context_length, (batch_size,))
        x = torch.stack([torch.from_numpy((val_data[i:i+context_length]).astype(np.int64)) for i in ix])
        y = torch.stack([torch.from_numpy((val_data[i+1:i+1+context_length]).astype(np.int64)) for i in ix])
    return x, y
```

## The Training Loop Pattern

```python
for iter in range(max_iters):
    # Sample from train, compute loss, backprop
    logits, loss = model(get_batch('train'))
    loss.backward()
    optimizer.step()

    # Every eval_interval, check validation loss (no gradients)
    if iter % eval_interval == 0:
        with torch.no_grad():
            val_loss = estimate_loss('val')  # Forward pass only on val set
        print(f"iter {iter}: train_loss {train_loss:.4f}, val_loss {val_loss:.4f}")
```

The **validation loss tells you if you're overfitting**:
- If `val_loss >> train_loss`: Model memorized training data, not generalizing
- If they track together: Good generalization, keep going

## For Language Models Specifically

The split philosophy shifts slightly at scale:

1. **For small models (nanoGPT scale)**: 8/1/1 is fine. Val and test are comparable.

2. **For large models**: Validation becomes more important than test:
   - You do 10-100x more steps on val during training (gradient decisions)
   - Test is only evaluated once at the end (not used for tuning)
   - Some teams use 9/0.5/0.5 or even larger train ratios because more data always helps

3. **For production models**: You might use a held-out **test distribution** (different domain/time period) to catch distribution shift that val didn't catch.

## Practical Consideration for Large Datasets

If you're training on billions of tokens (like you're exploring with MI300X), the 10% val/test can be gigabytes of data. You can be more aggressive:

```python
# For multi-billion token datasets, 5% val/test is acceptable
train_split = 0.90
val_split = 0.95  # 5% val, 5% test
```

The absolute size of val/test matters more than the percentage — you need enough tokens to get stable loss estimates, but beyond ~1GB of validation data, diminishing returns set in.

---

**Bottom line**: Keep val and test strictly separated. Use val loss during training to detect overfitting and tune LR/dropout/etc. Touch test once, after everything is locked. This is non-negotiable if your results are credible.
