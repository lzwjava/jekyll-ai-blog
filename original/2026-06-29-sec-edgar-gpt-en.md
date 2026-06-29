---
audio: false
generated: false
image: true
lang: en
layout: post
title: "SEC-EDGAR-GPT: A 124M Language Model Trained on SEC Filings"
translated: false
---

**Disclaimer:** All training data is publicly available on Hugging Face. All experiments and training were conducted on my personal devices or cloud platforms using my personal accounts — no bank resources were used.

---

I trained a 124M-parameter GPT-2 from scratch on 1.55B tokens of SEC-EDGAR financial filings using a single RTX 4070. SEC-EDGAR is the U.S. Securities and Exchange Commission's public database of corporate filings — 10-K annual reports, 10-Q quarterly reports, and other disclosures from publicly traded companies. Training took ~8 hours and converged to a validation loss of 2.28.

The model generates convincing SEC boilerplate — risk factors, MD&A sections, business descriptions — but struggles with numerical consistency and long-range coherence, as expected at this scale.

**Code:** [github.com/lzwjava/sec-edgar-gpt](https://github.com/lzwjava/sec-edgar-gpt) | **Paper:** [sec-edgar-gpt.pdf](https://github.com/lzwjava/sec-edgar-gpt/raw/main/sec-edgar-gpt.pdf)

This entire 124M model — training, deployment, paper, and website — was done in 3 days using Hermes Agent. With AI agents, LLM research and practice has become genuinely accessible.

Thanks to Andrej Karpathy's nanoGPT for the training framework, the kapilrao/SEC-EDGAR dataset on Hugging Face, and Ming Jian Wei, Du Chun, and Parjanya Mudunuri for helpful discussions.

---

**About me:** I'm a contractor engineer at GFT working with a global bank. Over the past year I've consumed ~3B LLM tokens and trained ~15 small models (up to 760M) across RTX 4070, H200, B200, and AMD MI300X. I've made 5,000+ contributions on the bank's internal GitHub and 11,000+ on public GitHub. I've done 2.5 years as a contracting engineer in the bank, working in WPB and GFT. I've given an AI talk to 80 bank peers to share hands-on experience. Recently, I am also working with Principal Engineer Parjanya Mudunuri and my lead Ming Jian Wei for about a month on a project involving large Excel file handling and a join/union tool to compare gaps and differences across multiple banking systems.

As the bank's CEO put it, AI is becoming one of the defining technologies in our time. I hope this work can help the bank adopt AI tech a bit more.

---

**Scan to try:**

![QR: Demo](assets/images/sec-edgar-gpt-workers-demo.png)

[sec-edgar-gpt.lzwjava.workers.dev](https://sec-edgar-gpt.lzwjava.workers.dev/)

**Website:**

![SEC-EDGAR-GPT website](assets/images/sec-edgar-gpt/website.png)

**Chat interface:**

![SEC-EDGAR-GPT chat](assets/images/sec-edgar-gpt/chat.png)

**Scan for model:**

![QR: HuggingFace](assets/images/sec-edgar-gpt-huggingface.png)

[huggingface.co/lzwjava/sec-edgar-gpt-124m-hf](https://huggingface.co/lzwjava/sec-edgar-gpt-124m-hf)
