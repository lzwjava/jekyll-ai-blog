---
audio: false
generated: true
image: false
lang: en
layout: post
title: Code Model Evaluation Accuracy Assessment
translated: false
type: note
---

**Question:** Is this inference results summary and explanation accurate?

**Answer:**

Overall, **yes, the conclusion is mostly correct**, but a few statements are oversimplified or not strictly true.

Here's my assessment.

| Statement                                             | Accuracy         | Comments                                                                                    |
| ----------------------------------------------------- | ---------------- | ------------------------------------------------------------------------------------------- |
| 124M model produces mostly garbage on code completion | ✅ True           | This is exactly what most 124M GPT-2 style models do.                                       |
| Model learned Java/Python syntax but not semantics    | ✅ Mostly true    | Good high-level explanation.                                                                |
| Short prompts perform much worse                      | ✅ True           | Very common with autoregressive LMs.                                                        |
| Code-specific training beats web-text training        | ✅ True           | GitHub-trained GPT-2 almost always outperforms FineWeb or WebText on coding tasks.          |
| 124M is "far too small" for coherent coding           | ⚠ Mostly true    | Depends on task. Small functions are possible, larger reasoning isn't.                      |
| Hidden state (768-dim) is the reason                  | ❌ Oversimplified | Hidden size is not the primary bottleneck.                                                  |
| Need 7B+ for vibe coding                              | ⚠ Mostly true    | Today this is generally accurate, although 1–3B modern models can already do useful coding. |

---

## The inference observations are believable

The outputs you showed are exactly what researchers would expect from a GPT-2 124M model.

For example,

Java:

```java
public void put(K key, V value) {
    return this).Size;
    assertEquals(...)
```

is classic **syntactic mimicry**.

The model knows

* methods begin with `{`
* `return` appears frequently
* `assertEquals` often appears near Java code
* variables often end with `.size`

but it never forms a coherent algorithm.

Likewise

```python
def quicksort(arr):
                                     class
```

is also typical.

A one-line prompt provides almost no context.

The model predicts tokens purely from local statistics.

---

## Your comparison between models makes sense

A GitHub-trained 124M model should outperform a web-text GPT-2 of similar size.

Typical ranking would be

```
GitHub-trained 124M
      >
FineWeb 124M
      >
OpenAI GPT-2 124M
```

for coding.

That matches your observations.

---

## Where the explanation is slightly inaccurate

### 1. "768-dimensional hidden state is too compressed"

This is probably the weakest claim.

The model does **not** fail primarily because

```
hidden size = 768
```

It fails because **everything scales together**:

* only 124M parameters
* only 12 transformer layers
* only 12 attention heads
* relatively few neurons
* limited representational capacity

The hidden size is only one component.

A better explanation would be

> The overall model capacity is insufficient to represent the long-range dependencies and algorithmic structure required for coherent code generation.

---

### 2. "No semantic understanding"

This is slightly too strong.

Even 124M models learn some semantics.

For example they know

```
for
if
return
while
```

They often learn

* variable naming conventions
* common library APIs
* matching braces
* recursion patterns
* simple arithmetic

What they cannot do consistently is

* maintain a multi-step algorithm
* track variable state
* reason over dozens of tokens
* preserve invariants

So I'd say

> It has limited semantic understanding rather than none.

---

### 3. "124M is far too small"

Mostly true.

But there are exceptions.

124M models can often generate

```python
def square(x):
    return x*x
```

or

```java
public int add(int a,int b){
    return a+b;
}
```

or

```python
for i in range(n):
    ...
```

They simply break down on anything requiring sustained reasoning.

---

### 4. "Need CodeLlama-7B"

Today (2026), I'd adjust this.

Approximate capabilities are:

| Model size | Coding ability                  |
| ---------- | ------------------------------- |
| 124M       | Mostly syntax imitation         |
| 350M       | Tiny helper functions           |
| 1.3B–1.5B  | Simple algorithm completion     |
| 3B         | Usable for small coding tasks   |
| 7B         | Good practical coding assistant |
| 14B+       | Strong coding                   |
| 30B+       | Very capable                    |

Modern architectures like Qwen3-Coder or DeepSeek-Coder achieve much better coding quality than older GPT-2-based models at similar parameter counts because of improved architectures, training data, tokenization, and optimization.

---

## One thing that is actually encouraging

Your GitHub-trained model **did** learn something useful.

Compared with a generic GPT-2, it learned:

* Java formatting
* Python formatting
* API names
* common identifiers
* language-specific token distributions

That means your training worked.

It just hit the expected ceiling of a 124M GPT-2 architecture.

This is exactly why projects like GitHub Copilot, based initially on much larger models, were trained with billions of parameters.

---

## Final assessment

I'd rate the report:

* **Observed results:** **10/10** — they are entirely believable for a GitHub-trained GPT-2 124M model.
* **Overall explanation:** **8.5/10** — the main conclusions are correct.
* **Technical precision:** **7.5/10** — I'd soften claims about "no semantic understanding" and avoid attributing the limitation primarily to the 768-dimensional hidden state.

The central takeaway is sound: a GitHub-trained 124M GPT-2 model can learn the statistical structure of code and produce syntactically plausible fragments, but it generally lacks the capacity to sustain coherent algorithmic reasoning over longer completions.
