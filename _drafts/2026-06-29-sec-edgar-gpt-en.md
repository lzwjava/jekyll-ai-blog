---
audio: false
generated: false
image: false
lang: en
layout: post
title: "SEC-EDGAR-GPT: A 124M Language Model Trained on SEC Filings"
translated: false
---

I trained a 124M-parameter GPT-2 from scratch on 1.55B tokens of SEC-EDGAR financial filings using a single RTX 4070. Training took ~8 hours and converged to a validation loss of 2.28.

The model generates convincing SEC boilerplate — risk factors, MD&A sections, business descriptions — but struggles with numerical consistency and long-range coherence, as expected at this scale.

**Code:** [github.com/lzwjava/sec-edgar-gpt](https://github.com/lzwjava/sec-edgar-gpt)

Thanks to Andrej Karpathy's nanoGPT for the training framework, the kapilrao/SEC-EDGAR dataset on Hugging Face, and Ming Jian Wei, Du Chun, and Parjanya Mudunuri for helpful discussions.

---

**About me:** I'm a contractor engineer at GFT working with a global bank. Over the past year I've consumed ~1.5B LLM tokens and trained ~20 small models (up to 760M) across RTX 4070, H200, B200, and AMD MI300X. I've made 5,000+ contributions on the bank's internal GitHub and 11,000+ on public GitHub. My goal is to bring open-source frontier model practices into the bank and invite peers to learn and experiment with them.

As HSBC CEO Georges Elhedery put it, staff should be "on the journey with us, not fighting us" — that's exactly the spirit: hands-on experimentation beats sitting on the sidelines.

---

**Scan to try:**

![QR: Demo](assets/images/sec-edgar-gpt-workers-demo.png)

[sec-edgar-gpt.lzwjava.workers.dev](https://sec-edgar-gpt.lzwjava.workers.dev/)

**Scan for model:**

![QR: HuggingFace](assets/images/sec-edgar-gpt-huggingface.png)

[huggingface.co/lzwjava/sec-edgar-gpt-124m-hf](https://huggingface.co/lzwjava/sec-edgar-gpt-124m-hf)
