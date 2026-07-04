---
audio: false
generated: true
image: false
lang: en
layout: post
title: SFT Turns Next-Token Models into Chatbots
translated: false
type: note
---

Question: How does SFT (Supervised Fine-Tuning) turn a next-token prediction model like nanoGPT into a chatbot? Do we train on JSON conversations, or do we convert them into `User:` / `Assistant:` text and train the model to predict the assistant's response?

Answer:

Yes, that's essentially the idea. The key insight is:

> **Even chat models are still just next-token prediction models.**

Nothing about the neural network fundamentally changes. The only thing that changes is **the training data format**.

## Step 1. Pretraining (nanoGPT)

In nanoGPT, you might have plain text:

```text
The capital of France is Paris.
```

The model sees

```
Input:  The capital of France is
Target: capital of France is Paris .
```

or more precisely

```
Input tokens:
The capital of France is Paris .

Predict:

The -> capital
capital -> of
of -> France
France -> is
is -> Paris
Paris -> .
```

Every token predicts the next token.

---

## Step 2. SFT dataset

Suppose you have JSON like

```json
{
  "messages": [
    {
      "role": "user",
      "content": "What is 2+2?"
    },
    {
      "role": "assistant",
      "content": "4."
    }
  ]
}
```

**The model is not trained directly on JSON objects.**

Instead, the JSON is converted into text.

For example,

```text
<|user|>
What is 2+2?

<|assistant|>
4.
```

or

```text
User: What is 2+2?
Assistant: 4.
```

or for some models:

```text
<|im_start|>user
What is 2+2?
<|im_end|>

<|im_start|>assistant
4.
<|im_end|>
```

Every model family has its own **chat template**.

---

## Step 3. Tokenization

After formatting,

```text
User: What is 2+2?

Assistant: 4.
```

becomes tokens like

```
[User]
[:]
[What]
[is]
[2]
[+]
[2]
[?]

[Assistant]
[:]

[4]
[.]
```

The transformer doesn't know these are "roles" in a semantic sense. It only sees tokens.

---

## Step 4. Loss masking (the important part)

Most SFT training does **not** compute loss on the user's tokens.

Example:

```
User: What is 2+2?
Assistant: 4.
```

Internally it becomes

```
Input:

User:
What
is
2
+
2
?
Assistant:
4
.
```

The labels are masked like

```
User        -> ignore
:           -> ignore
What        -> ignore
is          -> ignore
2           -> ignore
+           -> ignore
2           -> ignore
?           -> ignore
Assistant   -> ignore

4           -> predict
.           -> predict
```

In many implementations:

```
labels =
[-100,
 -100,
 -100,
 ...
 -100,
 token("4"),
 token(".")]
```

where `-100` tells the loss function (such as cross-entropy in PyTorch) to ignore those positions.

This teaches:

> Given the conversation so far, generate the assistant's reply.

---

## Step 5. Inference

During inference you type

```text
User: Tell me a joke.

Assistant:
```

The model predicts

```
Why
did
the
chicken
...
```

because during SFT it saw millions of examples ending with

```
Assistant:
```

followed by an answer.

So it has learned the pattern.

---

## Multi-turn conversations

Training data can also look like

```text
User: Hi

Assistant: Hello!

User: Who invented Python?

Assistant: Guido van Rossum.
```

The loss is usually computed **only on the assistant messages**.

Conceptually:

```
User: Hi                     ignore

Assistant: Hello!            train

User: Who invented Python?   ignore

Assistant: Guido ...         train
```

This teaches the model how to maintain context across turns.

---

## Why JSON is still useful

The JSON format is mainly for organizing the dataset:

```json
[
  {"role":"system","content":"You are helpful."},
  {"role":"user","content":"Hello"},
  {"role":"assistant","content":"Hi!"}
]
```

Before training, a preprocessing step applies the model's chat template and produces a single text sequence such as

```text
<System>
You are helpful.

<User>
Hello

<Assistant>
Hi!
```

That text is then tokenized and used for next-token prediction.

---

## Connection to nanoGPT

This is the key connection:

**Pretraining**

```
Wikipedia article

↓

Predict next token
```

**SFT**

```
User:
Question

Assistant:
Answer

↓

Predict the next assistant token
```

The training objective is still exactly the same: **next-token prediction**. The only differences are:

* The input now includes role markers (`User`, `Assistant`, or special chat tokens).
* The loss is usually masked so only assistant tokens contribute to training.
* The dataset consists of conversations instead of plain text.

So your understanding is correct: the conversation JSON is converted into a formatted text sequence, tokenized, and the model is trained again using next-token prediction. The main additional technique in SFT is **loss masking**, which ensures the model learns to generate assistant responses rather than simply predicting every token in the prompt.