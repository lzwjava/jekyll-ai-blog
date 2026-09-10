---
audio: false
generated: true
image: false
lang: en
layout: post
title: The Limits of Unrestricted Models
translated: false
type: note
---

Question: Is an uncensored/abliterated Qwen3-8B model actually interesting if there aren't many illegal questions worth asking?

Answer: **Yes, mostly.** If your main reason for downloading `Qwen3-8B-abliterated-q4_k_m.gguf` is “now I can ask illegal questions,” the novelty wears off very quickly.

The more interesting distinction is **not illegal vs. legal**, but **what behaviors the model refuses or permits**:

* **Creative writing:** darker fiction, horror, violence, controversial characters, etc.
* **Security research:** discussing malware concepts, exploit mechanics, reverse engineering, CTF-style problems, etc., within safe boundaries.
* **Model behavior experiments:** compare the base Qwen3 against the abliterated model and measure refusal rate.
* **Prompt-following:** see whether it follows unusual system/user instructions that a safety-tuned model rejects.
* **Roleplay / unrestricted conversation:** fewer “I can't help with that” interruptions.
* **Local/private inference:** this is probably the biggest practical reason to run it on your 4070.

Also, **“abliterated” does not mean “knows more.”** Usually it means some refusal/safety behavior has been modified or suppressed. The underlying Qwen capabilities are largely inherited from the base model.

For your RTX 4070 12 GB, I'd consider this more interesting as a **controlled model-behavior experiment** than as an “illegal-question machine”: run the same ~100 prompts through Qwen3-8B-Instruct and the abliterated version and measure refusal rate, answer quality, and hallucination rate.

I can also help you build a tiny local benchmark that compares the two models automatically with `llama.cpp`.