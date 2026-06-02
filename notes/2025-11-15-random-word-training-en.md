---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Training on Random Word Salad
translated: false
type: note
---

If you train a small model like nanoGPT (or any transformer similar to GPT-2 small) on 2–3 GB of completely **random English-like words** (i.e., sequences of real English words picked uniformly at random, no grammar, no meaning, just word salad), here’s what will actually happen:

### The model will learn that there is **no structure** to learn
- It will very quickly figure out the token distribution (the unigram frequencies of words).
- It will realize that the next word is essentially independent of previous words (or very close to independent).
- Perplexity on the training data will bottom out extremely fast (after a few epochs it will already be close to the entropy of the uniform word distribution).
- The model will essentially turn into a **unigram sampler** — it will just output words according to their marginal frequency in the training data, with almost zero context dependence.

### Generated text will be slightly better than pure nonsense, but still complete garbage
Example of what you’ll get after training:

> the cat quickly under yesterday apple banana elephant running purple however tomorrow cheese lightning quickly zebra sandwich forever mountain bicycle orange elephant yesterday banana

It will:
- Use real English words ✓
- Respect word frequencies (common words like “the”, “and”, “to” will appear a lot) ✓
- Have perfect spelling ✓
- Be 100% grammatically and semantically incoherent ✗

It will **not** learn:
- Grammar or syntax
- Any phrase structure
- Function words placement
- Any kind of meaning or topic coherence
- Even bigrams/trigrams beyond weak statistical noise

### Comparison to training on real text
When you train nanoGPT on real text (e.g., Shakespeare or OpenWebText), even with just 2–3 GB, you start seeing real sentences emerge surprisingly quickly because there’s rich predictable structure.

With purely random words, you’ll never cross the threshold into coherence — no matter how long you train. The model converges almost immediately to “next word is random according to frequency” and stops improving.

### Fun experiment you can actually try
You can generate such a dataset easily:

```python
import random
words = open('big-wordlist.txt').read().splitlines()  # e.g., 300k English words
with open('random_3gb.txt', 'w') as f:
    for _ in range(500_000_000):  # ~3 GB
        f.write(random.choice(words) + ' ')
```

Train nanoGPT on it for a few hours. You’ll see loss drop to ~4–5 nats (which is basically the entropy of English word distribution) and then flatten completely. Sampling afterward will give exactly the word salad above.

### Bottom line
Yes, the generated text will be almost pure nonsense — just slightly more “natural-looking” nonsense than if you sampled words uniformly from a dictionary, because it will match real word frequencies. But it will never say anything remotely meaningful or grammatical.

It’s actually a great way to prove to yourself how much real language relies on long-range dependencies and structure — because when you remove all of it, even a powerful architecture like GPT learns essentially nothing useful.
