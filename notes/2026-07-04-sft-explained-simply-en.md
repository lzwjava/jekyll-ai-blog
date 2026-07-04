---
audio: false
generated: true
image: false
lang: en
layout: post
title: SFT Explained Simply
translated: false
type: note
---

**Question:** What is SFT? I just saw a PyTorch call, but how does it work underneath?

**Answer:**

**SFT** stands for **Supervised Fine-Tuning**. It is the simplest and most common way to train or adapt a large language model (LLM).

At its core, SFT is just **next-token prediction** on a dataset of instruction-response pairs. There is no magic algorithm—it is essentially the same training procedure used during pretraining, except on a much smaller, curated dataset.

For example, suppose your dataset contains:

```text
User: What is 2 + 2?
Assistant: 4
```

The model actually sees something like:

```text
<user>
What is 2 + 2?
</user>

<assistant>
4
</assistant>
```

The tokenizer converts this into IDs:

```
[123, 456, 789, 234, ...]
```

The model predicts:

```
Input:
What is 2 +

Predict:
2

Next step:

Input:
What is 2 + 2

Predict:
?

...

Eventually:

Input:
Assistant:

Predict:
4
```

It learns by minimizing the prediction error for the assistant's response.

---

## Under the hood

Suppose you have

```python
input_ids = tokenizer(text).input_ids
```

The model does

```python
logits = model(input_ids)
```

where

```
input_ids
     ↓
Embedding
     ↓
Transformer blocks
     ↓
Linear projection
     ↓
logits
```

The output shape is

```
(batch, sequence_length, vocab_size)
```

For a 50k-token vocabulary:

```
(8, 512, 50000)
```

Each position predicts the next token.

---

## Loss computation

PyTorch typically uses

```python
loss = F.cross_entropy(
    logits.view(-1, vocab_size),
    labels.view(-1)
)
```

Internally this is

```
Softmax
↓
Negative log likelihood
↓
Average over tokens
```

The loss is

[
-\log(p(\text{correct token}))
]

If the correct next token is

```
"dog"
```

and the model predicts

```
cat : 0.20
dog : 0.60
bird: 0.10
```

then

```
loss = -log(0.6)
```

If instead it predicts

```
dog : 0.99
```

the loss becomes very small.

---

## Why is it called "Supervised"?

Because humans provide the desired output.

Example:

```
Question:
How do I sort a list?

Desired answer:
Use Python's sorted() function...
```

The model is directly told what the correct response should be.

This is unlike reinforcement learning, where the model receives only a reward signal rather than the exact target output.

---

## Masking the prompt

One important detail in modern SFT is that we usually **do not train on the user's prompt**. Instead, we compute the loss only on the assistant's reply.

For example:

```text
User:
Tell me a joke.

Assistant:
Why did the chicken cross the road?
```

The labels might look like:

```
User tokens       -> -100
Assistant tokens  -> actual token IDs
```

In PyTorch:

```python
labels = input_ids.clone()
labels[user_part] = -100
```

The `-100` value tells `CrossEntropyLoss` to ignore those positions.

This means the model is **conditioned on the prompt**, but it is only penalized based on how well it predicts the assistant's response.

---

## Backpropagation

Once the loss is computed:

```
loss
 ↓
backward()
 ↓
compute gradients
 ↓
optimizer.step()
 ↓
update weights
```

Every weight in the Transformer is adjusted slightly using gradient descent.

---

## The actual PyTorch training loop

A simplified version looks like this:

```python
for batch in dataloader:
    outputs = model(
        input_ids=batch["input_ids"],
        labels=batch["labels"]
    )

    loss = outputs.loss

    loss.backward()

    optimizer.step()

    optimizer.zero_grad()
```

Inside

```python
outputs = model(...)
```

the Hugging Face model typically does something equivalent to:

```python
logits = transformer(input_ids)

shift_logits = logits[:, :-1]
shift_labels = labels[:, 1:]

loss = F.cross_entropy(
    shift_logits.reshape(-1, vocab_size),
    shift_labels.reshape(-1),
    ignore_index=-100
)
```

The labels are shifted by one position because the model predicts the **next** token.

---

## How Hugging Face hides the complexity

When you write:

```python
outputs = model(
    input_ids=input_ids,
    labels=labels
)
```

the model automatically:

1. Runs the forward pass through the Transformer.
2. Shifts logits and labels for next-token prediction.
3. Computes the cross-entropy loss.
4. Applies `ignore_index=-100` to masked positions.
5. Returns both the `loss` and the `logits`.

This is why an SFT training script can look deceptively simple.

---

## Overall pipeline

```
Instruction dataset
        │
        ▼
Tokenizer
        │
        ▼
Token IDs
        │
        ▼
Transformer forward pass
        │
        ▼
Logits
        │
        ▼
Shift by one token
        │
        ▼
Cross-entropy loss
        │
        ▼
Backpropagation
        │
        ▼
AdamW optimizer
        │
        ▼
Updated model weights
```

In summary, **SFT is fundamentally the same next-token prediction objective used during pretraining**, but applied to high-quality instruction-following examples. The key differences are the data (instruction-response pairs instead of raw text) and the common practice of masking the prompt so that only the assistant's response contributes to the training loss.
