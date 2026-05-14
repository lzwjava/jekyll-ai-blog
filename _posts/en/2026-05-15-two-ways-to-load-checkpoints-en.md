---
audio: false
generated: true
image: false
lang: en
layout: post
title: Two Ways to Load Checkpoints
translated: false
type: note
---

There are two cases, depending on what kind of checkpoint you're downloading.

## 1. OpenAI GPT-2 weights (already supported)

`model.py:229` (`GPT.from_pretrained`) already wraps HF Transformers, so you just do:

```bash
python sample.py --init_from=gpt2          # or gpt2-medium / gpt2-large / gpt2-xl
```

First run pulls the weights into `~/.cache/huggingface/` automatically. Requires `transformers` installed. Works only for those four model names because the key-remapping in `from_pretrained` is hard-coded for GPT-2.

## 2. A nanoGPT-style `ckpt.pt` someone uploaded to HF

Files like Karpathy's reproductions or community 124M/350M runs are usually a raw `torch.save({'model': ..., 'model_args': ...})` dict — i.e., what `train.py` writes. Download then point `sample.py` at the directory:

```bash
pip install huggingface_hub
huggingface-cli download <user>/<repo> ckpt.pt --local-dir out-hf

python sample.py --init_from=resume --out_dir=out-hf --start="Hello"
```

`sample.py:35-46` loads `<out_dir>/ckpt.pt`, builds `GPTConfig(**checkpoint['model_args'])`, and calls `load_state_dict`. So the repo must publish a compatible `ckpt.pt` with both `'model'` and `'model_args'` keys. If only `'model'` exists, you'll need to pass the config (n_layer, n_head, n_embd, block_size, vocab_size) yourself when building the GPT.

## 3. A Hugging Face `transformers` checkpoint (safetensors / pytorch_model.bin)

Those use different parameter names and layouts than nanoGPT. The cleanest route: reverse the mapping in `model.py:229-280`. That code copies HF → nanoGPT keys (transposing the Conv1D weights). You can write the inverse to load arbitrary GPT-2-architecture HF models into nanoGPT — same trick works for any model that's truly GPT-2-shaped (same n_layer/n_head/n_embd, same tokenizer). Different architectures (LLaMA, Mistral, etc.) won't load.

If you tell me which specific HF repo you want to run, I can give you the exact commands.