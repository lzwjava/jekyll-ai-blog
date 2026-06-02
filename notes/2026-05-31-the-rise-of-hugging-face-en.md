---
audio: false
generated: true
image: false
lang: en
layout: post
title: The Rise of Hugging Face
translated: false
type: note
---

**Question:** What is the story of Hugging Face — when it was born, how it grew, who founded it, and how the team evolved?

---

## The Hugging Face Story

### Origin: 3 French Guys, a Chatbot, and Alanis Morissette Covers

The story starts in Paris, 2016. Julien Chaumond was a software engineer at Stupeflix when he reconnected with Thomas Wolf, who he knew from engineering school — they used to play in a rock band doing Alanis Morissette covers. Together with Clément Delangue, who Chaumond already knew, the three launched Hugging Face.

The founders' backgrounds were complementary from the start:

- Clément Delangue brought business acumen, Julien Chaumond engineering skills, and Thomas Wolf a research background.
- Thomas Wolf had a Ph.D. in physics and had authored research papers in machine learning.

The original product: an AI-powered chatbot for teenagers — they didn't set out to build the backbone of the AI revolution. They just wanted to build something fun.

### 2016–2018: Consumer Chatbot Phase

The team moved to New York after signing a $200k seed ticket from US investor Betaworks and securing a spot in their chatbot-focused accelerator program. "We could never have raised money in France with this kind of" pitch — strong signal that the French startup ecosystem wasn't ready for consumer AI bets then.

After developing their initial chatbot idea, the founders participated in the Betaworks accelerator, which provided early seed funding and helped the company establish a US presence.

### 2018: The BERT Moment — The Real Inflection Point

This is the pivotal event in HF history. A key turning point came in late 2018 when Google released BERT. The Hugging Face team rapidly produced and open-sourced a PyTorch implementation of BERT within a week. Chaumond has said this moment clarified the company's direction, leading Hugging Face to formalize its pivot in 2019 away from the consumer chatbot and toward building open-source ML infrastructure.

That weekend sprint — shipping the PyTorch port of BERT in a single week — is often cited as the moment that defined the entire company's future direction.

The insight: the founders realized that while people liked their chatbot, developers needed their tools.

### 2019: Transformers Library + Series A

After pivoting from a chatbot to a developer-first company, Hugging Face ignited rapid growth with the 2019 release of the Transformers library, which unified access to BERT, GPT-2, and other state-of-the-art models, driving explosive adoption.

Funding: Hugging Face raised $15M in a Series A led by Lux Capital in December 2019, with participation from A.Capital, Betaworks, Richard Socher (Salesforce chief scientist), Greg Brockman (OpenAI co-founder & CTO), Kevin Durant, and other angels. Greg Brockman as an early angel is a great signal — the OpenAI network saw the bet early.

### 2020–2021: Scale and Series B

By mid-2020 the team had grown across Paris and New York, recruiting talent from Google Research and FAIR, and monthly downloads hit ~1 million. Fundraising and product expansion accelerated the move into vision, audio, and biology.

Series B raised $40M in March 2021, led by Addition VC.

Revenue at this point: Hugging Face brought in $10M in revenue in 2021.

### 2022: Series C — $2B Valuation, GitHub of ML

In May 2022, Hugging Face raised $100M in a Series C led by Lux Capital, joining the double unicorn club at a $2B valuation. Investors included Sequoia, Coatue, Addition.

Revenue: $15M in 2022.

This is also when their "GitHub for ML" positioning solidified. The platform now registers 1M monthly active users, and Chaumond describes it as "the GitHub of machine learning."

### 2023: Series D — $4.5B, Backed by Every Major Tech Company

Hugging Face's most recent valuation is $4.5B, based on raising $235M in their Series D in 2023, more than double their previous $2B valuation.

Investors in the Series D include Salesforce Ventures (lead), Google, Nvidia, Amazon — essentially every hyperscaler hedging their bets on the open-source ML hub. Revenue reached ~$50M annualized as of 2023, with over 10,000 companies using the platform.

---

## Timeline Summary

| Year | Event |
|------|-------|
| 2016 | Founded in NYC (French founders), consumer chatbot for teens, Betaworks seed $200k |
| 2018 | BERT released → HF ships PyTorch port in 1 week → pivot decision |
| 2019 | Transformers library launched, Series A $15M (Lux Capital, Greg Brockman angel) |
| 2020 | Downloads hit 1M/month, team expands from Google Research + FAIR hires |
| 2021 | Series B $40M, $10M revenue, Hub launched |
| 2022 | Series C $100M, $2B valuation (Sequoia, Coatue), $15M revenue |
| 2023 | Series D $235M, $4.5B valuation, ~$50M ARR, Google/Nvidia/Amazon as investors |
| 2026 | ~731 employees, 1M+ models on Hub |

---

## Why It Worked

The strategic core: **give away the library, monetize the infra**. Teams and organizations use paid workspaces at $20/user/month; larger customers pay for compute on a usage basis with inference endpoints priced per hour, beginning at $0.033/hr for CPU instances. Enterprise plans add custom infra, SSO, audit logs.

This is the classic open-source playbook — Redis, MongoDB, Elastic — but executed at the exact right time when the transformer revolution was making ML accessible to every team. The Transformers library became the standard abstraction layer. If you control the abstraction, you own the ecosystem.

For you specifically: HF's story rhymes with what you're building. They won by being the fastest to implement BERT and open-sourcing it — speed + open source + developer trust, not a polished product. Their early moat was the same as yours should be: deep technical credibility, not marketing.

---

**References:**

- [Hugging Face Business Breakdown & Founding Story — Contrary Research](https://research.contrary.com/company/hugging-face)
- [Fundraising in the US & emerging founders factory — Sifted](https://sifted.eu/articles/hugging-face-interview-julien-chaumond)
- [From Open Source to Billion-Dollar Valuation — WeAreFounders](https://www.wearefounders.uk/from-open-source-to-billion-dollar-valuation-the-hugging-face-founders/)
- [HuggingFace Statistics — Originality.AI](https://originality.ai/blog/huggingface-statistics)
