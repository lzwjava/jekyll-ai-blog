---
audio: false
generated: true
image: false
lang: en
layout: post
title: From Uncensored to AI Agent
translated: false
type: note
---

Question: **Once you have an uncensored/open-weight model, what should you actually do with it?**

Answer:

The interesting part is **not merely removing the refusal layer**. The real value is that you now control the whole inference + training stack.

I’d treat it as a small research/product loop:

```text
uncensored model
      ↓
baseline evaluation
      ↓
find failure modes / capabilities
      ↓
SFT / LoRA / preference tuning
      ↓
tool use + agent loop
      ↓
benchmark against Qwen / Llama / etc.
      ↓
package into a useful local product
```

### 1. First: establish what "uncensored" actually means

Run the same prompts against:

```text
original model
    vs
uncensored model
```

Measure:

* refusal rate
* instruction following
* coding performance
* reasoning
* hallucination
* context retention
* tool calling
* multilingual behavior
* benchmark scores

Don't assume "uncensored" = "better". Often the model is simply a fine-tune with different behavioral preferences.

### 2. Then inspect the model

For a Hugging Face model:

```bash
git clone <MODEL_REPO>
cd <MODEL_REPO>

find . -maxdepth 2 -type f | sort
```

Look at:

```text
config.json
tokenizer_config.json
generation_config.json
*.safetensors
README.md
```

Especially:

```json
architectures
model_type
hidden_size
num_hidden_layers
num_attention_heads
num_key_value_heads
intermediate_size
torch_dtype
```

This tells you what you're actually running.

### 3. Run it locally

For example:

```bash
pip install -U transformers accelerate torch
```

Then:

```python
from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = "<MODEL_ID>"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype="auto",
    device_map="auto",
)

prompt = "Explain how TCP congestion control works."

inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

out = model.generate(
    **inputs,
    max_new_tokens=512,
    temperature=0.7,
)

print(tokenizer.decode(out[0], skip_special_tokens=True))
```

Then move to **vLLM/SGLang** once you care about throughput.

### 4. The really interesting thing: build your own agent

This is where an uncensored model becomes much more interesting than a chatbot.

Give it:

```text
LLM
 ├── shell
 ├── filesystem
 ├── Python
 ├── browser
 ├── GPU inspection
 ├── git
 └── your own APIs
```

Then:

```text
user
 ↓
LLM
 ↓
tool call
 ↓
observation
 ↓
LLM
 ↓
tool call
 ↓
...
 ↓
answer
```

For your setup, you could make a **local GPU-repair agent**:

```text
GPU
 ↓
nvidia-smi / lspci
 ↓
MATS/MODS output
 ↓
oscilloscope measurements
 ↓
photos
 ↓
LLM
 ↓
hypothesis
 ↓
next measurement
 ↓
LLM
 ↓
diagnosis
```

That's substantially more interesting than simply asking an uncensored model questions.

### 5. Then fine-tune it

Take your own high-quality examples:

```json
{
  "messages": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ]
}
```

Start with LoRA/QLoRA:

```text
base model
    +
your data
    ↓
adapter
    ↓
specialized model
```

Possible specializations for you:

* coding agent
* Linux/GPU debugging
* CUDA engineering
* hardware repair reasoning
* Chinese/English technical knowledge
* autonomous CLI agent
* long-running research agent

### 6. Build an evaluation harness

This is probably the highest-leverage next step.

Instead of:

```text
"I think this model is good."
```

build:

```bash
./eval.py \
    --model qwen \
    --model my-uncensored \
    --tasks coding,reasoning,agent,gpu
```

and produce:

```text
                     Qwen     My model
coding               82       84
reasoning            71       76
tool use             78       91
refusal              35%      4%
GPU diagnosis        41       67
```

Now you're doing **model engineering**, not just model downloading.

### The important mental model

An uncensored model is basically:

> **a controllable foundation for experiments where you own the behavior policy.**

The strongest workflow is:

```text
open weights
    ↓
understand architecture
    ↓
benchmark
    ↓
collect failures
    ↓
train
    ↓
evaluate
    ↓
agentize
    ↓
deploy
```

And because you already work with CLI agents, GPUs, training and inference infrastructure, I'd personally go straight toward **"uncensored model + local tools + autonomous CLI agent"**, rather than building another chat UI.

I can next help you build a minimal `uncensored-model → tool-calling CLI agent` in Python using vLLM/SGLang.
