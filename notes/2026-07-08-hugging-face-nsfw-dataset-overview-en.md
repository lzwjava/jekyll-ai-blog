---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hugging Face NSFW Dataset Overview
translated: false
type: note
---

Question: Does Hugging Face host mature/erotic story datasets that could be used to fine-tune a model?

Answer:

Yes — there are community-uploaded NSFW text datasets on Hugging Face, but treat them as low-quality, legally murky, and mostly community-curated rather than "official" or vetted.

**What actually exists:**

- Several **collections** aggregate them, e.g. a collection covering nsfw text datasets, nsfw image datasets, and nsfw models/loras, and a separate collection of "NSFW Sexting Datasets" tagged for chat/roleplay and "uncensored" fine-tuning.
- Most individual repos flagged as sensitive don't show their card content in search (HF gate-blocks NSFW cards until you log in and accept the content warning) — e.g. the amaye15/NSFW dataset is marked as containing sensitive content, similarly for deepghs/nsfw_detect, edwixx/NsFW-Dataset, and utsavm/NSFW_Chat_Dataset.
- Not all "NSFW" datasets are erotica — some are classifiers, not story corpora. E.g. valurank/Adult-content-dataset is 850 article descriptions labeled Adult vs Non_Adult, scraped across platforms — that's a content classifier training set, not fiction.

**Practical notes for your use case (fine-tuning a model on erotic/mature fiction):**

1. **Quality is generally poor.** Most of these are scraped from AO3, Literotica, or roleplay logs without cleaning — expect duplicate content, broken formatting, inconsistent tagging, and copyright contamination (scraped fan-fiction/erotica is rarely public domain or explicitly licensed for ML training).
2. **License risk is real.** Datasets scraped from Literotica/AO3 etc. almost never come with redistribution or commercial-training rights. If any of your Fun Live successor products or client-facing agent work touches this, that's a legal exposure, not just an ethics one — worth flagging especially if you're doing anything HK-entity/commercial with it.
3. **HF gates these behind login + content agreement** — you'll need `huggingface-cli login` with an account that has accepted the gate, then use `datasets.load_dataset(..., token=True)`.
4. **Better alternative if your actual goal is roleplay/chat-style fine-tuning**: the "uncensored" community models (Mythomax, Nous-Hermes variants, etc.) already did the RLHF/DPO-alignment-removal work — fine-tuning on top of one of those with a small curated dataset (a few thousand well-formatted examples) will get you further than training from scratch on a noisy 200k-row scrape.

I'm not going to write or generate erotic content myself, but the dataset pointers above are real and searchable directly on HF.

References:

- [nsfw text datasets - sirsnuff Collection](https://huggingface.co/collections/sirsnuff/nsfw-text-datasets)
- [NSFW Sexting Datasets - Grumpyaloha Collection](https://huggingface.co/collections/Grumpyaloha/nsfw-sexting-datasets)
- [valurank/Adult-content-dataset](https://huggingface.co/datasets/valurank/Adult-content-dataset)
- [amaye15/NSFW](https://huggingface.co/datasets/amaye15/NSFW)