---
audio: false
generated: true
image: false
lang: en
layout: post
title: Unsung Heroes of Word2Vec and LSTM
translated: false
type: note
---

Question: Who are the main authors of Word2Vec and LSTM, and do they receive enough credit compared to figures like Yann LeCun?

Answer:

The **Word2Vec** technique was primarily developed by **Tomáš Mikolov** (lead author), along with co-authors Kai Chen, Greg Corrado, Ilya Sutskever, and Jeff Dean at Google. It was introduced in two key 2013 papers: one on efficient estimation of word representations and the other on distributed representations of words and phrases. Mikolov is widely recognized as the main creator and driving force behind Word2Vec, which became hugely influential in NLP by enabling fast, high-quality word embeddings that captured semantic relationships (e.g., the famous "king - man + woman ≈ queen" vector arithmetic).

The **LSTM** (Long Short-Term Memory) was invented by **Sepp Hochreiter** and **Jürgen Schmidhuber**. Their seminal 1997 paper in Neural Computation introduced the architecture to solve the vanishing gradient problem in recurrent neural networks, allowing models to learn long-range dependencies effectively. This work laid critical groundwork for sequence modeling, and LSTMs powered many advances in speech recognition, machine translation, and more until transformers largely took over.

**Yann LeCun** is a pioneer in convolutional neural networks (**CNNs**), with major contributions starting in the late 1980s/early 1990s (e.g., LeNet for handwriting recognition). He shared the 2018 Turing Award with Geoffrey Hinton and Yoshua Bengio for deep learning overall.

Your point about credit is valid and commonly discussed in the AI community:

- Figures like LeCun, Hinton, and Bengio received massive public recognition (Turing Award, media coverage as "godfathers of deep learning"), high-profile roles (e.g., LeCun at Meta), and broad acclaim.
- In contrast, Mikolov's Word2Vec is one of the most cited and practically used innovations in modern NLP, yet he is less visible in mainstream AI narratives.
- Hochreiter and Schmidhuber made foundational contributions (LSTM is extremely impactful, with the 1997 paper among the most-cited in deep learning history), but Schmidhuber in particular has often voiced frustration about receiving less credit relative to the "big three" (Hinton, LeCun, Bengio), despite priority in areas like RNNs, LSTMs, and more.

Many researchers share your sentiment: the people who quietly build enabling tools and publish openly (often without aggressive self-promotion or big corporate backing at the time) frequently become the "unsung heroes" or "behind-the-scenes" contributors. Their work is freely available and powers countless applications and companies, but financial and fame rewards often go disproportionately to those with better visibility, timing, or institutional support.

That said, within the research community, Mikolov, Hochreiter, and Schmidhuber are highly respected and cited. Word2Vec and LSTM have transformed AI in very tangible ways, even if the spotlight sometimes shines elsewhere.

References:

- [Word2vec - Wikipedia](https://en.wikipedia.org/wiki/Word2vec)
- [Efficient Estimation of Word Representations in Vector Space (arXiv)](https://arxiv.org/abs/1301.3781)
- [Long short-term memory - Wikipedia](https://en.wikipedia.org/wiki/Long_short-term_memory)
- [Long Short-Term Memory (original 1997 paper)](https://www.bioinf.jku.at/publications/older/2604.pdf)
