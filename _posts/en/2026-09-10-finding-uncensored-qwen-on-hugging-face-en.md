---
audio: false
generated: true
image: false
lang: en
layout: post
title: Finding Uncensored Qwen on Hugging Face
translated: false
type: note
---

Question: **How do I find uncensored models like Qwen variants on Hugging Face?**

Answer: The easiest way is to use Hugging Face's **`uncensored` filter/search**, then inspect the model card rather than trusting the name.

### 1. Direct Hugging Face search

[Hugging Face — uncensored models](https://huggingface.co/models?other=uncensored&utm_source=chatgpt.com)

This currently surfaces models such as:

* `OBLITERATUS/Qwen3.8-27B-OBLITERATED`
* `huihui-ai/Huihui-Qwen3.8-27B-abliterated`
* `orcarouter/Qwen3.8-27B-Uncensored-GGUF`
* `JonathanColetti/Qwen3.8-27B-Uncensored-GGUF`
* `DavidAU/Qwen3.8-27B-TURBO-...-Heretic-Uncensored...`

([Hugging Face][1])

### 2. Search terms that actually work

On HF, try combinations of:

```text
qwen uncensored
qwen abliterated
qwen heretic
qwen obliterated
qwen uncensored gguf
qwen uncensored 4bit
qwen uncensored 8b
qwen uncensored 14b
qwen uncensored 32b
```

The important keywords are:

```text
uncensored
abliterated
obliterated
heretic
unfiltered
```

For example:

[Search Qwen3 + uncensored](https://huggingface.co/models?search=qwen3+uncensored&utm_source=chatgpt.com)

HF currently returns hundreds/thousands of variants depending on the query. ([Hugging Face][2])

### 3. Understand the terminology

There are several different things people call "uncensored":

**A. Fine-tuned uncensored**

```text
base Qwen
    ↓
uncensored instruction tuning
    ↓
model
```

The model was trained to be less refusal-oriented.

**B. Abliteration**

```text
Qwen
 ↓
identify refusal / safety directions
 ↓
modify weights
 ↓
abliterated Qwen
```

This is extremely common on HF. `Huihui-Qwen...-abliterated`, `Heretic`, and `OBLITERATED` are examples. ([Hugging Face][3])

**C. Merge**

For example:

```text
Qwen
 + another fine-tune
 + another model
 + refusal-removal model
 = merged model
```

This is where names can become crazy:

```text
Qwen3.8-27B
  → Fable
  → Cold Fusion
  → Heretic
  → Uncensored
  → NEO
  → CODER
  → MTP
```

Your earlier `DavidAU/...TURBO-Fable-Cold-Fusion...` is exactly this sort of community model. ([Hugging Face][2])

### 4. Filter by hardware

For your own machine, this is probably more useful than simply searching `uncensored`.

For example, with a **12 GB 4070**, search:

```text
qwen uncensored 4bit
qwen abliterated GGUF
qwen 8B uncensored
qwen 9B uncensored
```

Then choose:

```text
4B / 8B / 9B
↓
Q4_K_M / Q4_K_S / IQ4
↓
GGUF
```

For example, HF currently has `Qwen3.5-9B` and `Qwen3.5-4B` uncensored variants, as well as many 27B versions. ([Hugging Face][4])

For **27B**, you can still run quantized versions, but VRAM/RAM and speed become the constraint.

### 5. My preferred HF workflow

Instead of searching:

```text
"best uncensored model"
```

I would do:

```bash
# Search HF from CLI / browser
huggingface-cli search qwen uncensored
```

Or just use the HF search URL and then filter:

```text
Model name:       qwen3
Task:             Text Generation
Library:          GGUF
Parameter size:   4B–14B
Sort:             Downloads / Trending
```

Then inspect:

```text
README
Files
Quantization
Base model
License
Downloads
Likes
Recent updates
```

**Don't trust "UNCENSORED" in the filename alone.** Some community models are heavily merged/quantized and their behavior can differ substantially from the original model.

For you specifically, I'd start with **Qwen3/Qwen3.5/Qwen3.8 8–9B uncensored/abliterated GGUF**, benchmark them locally, and then move to 27B if the behavior is worth the extra compute. ([Hugging Face][4])

References:

* [Hugging Face Models — uncensored filter](https://huggingface.co/models?other=uncensored&utm_source=chatgpt.com)
* [Hugging Face Models — Qwen3 uncensored search](https://huggingface.co/models?search=qwen3+uncensored&utm_source=chatgpt.com)
* [Hugging Face Models](https://huggingface.co/models?utm_source=chatgpt.com)

[1]: https://huggingface.co/models?other=uncensored&utm_source=chatgpt.com "Models – Hugging Face"
[2]: https://huggingface.co/models?search=qwen+uncensored&utm_source=chatgpt.com "Models – Hugging Face"
[3]: https://huggingface.co/models?other=qwen3&utm_source=chatgpt.com "Models – Hugging Face"
[4]: https://huggingface.co/models?search=qwen3+4b+uncensored&utm_source=chatgpt.com "Models – Hugging Face"
