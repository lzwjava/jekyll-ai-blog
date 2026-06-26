---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPT-2 on SEC-EDGAR Data
translated: false
type: note
---

Done. Paper created at:

  ~/projects/jekyll-ai-blog/latex/en/sec-edgar-gpt/sec-edgar-gpt.tex

Structure:

- Abstract — 124M GPT-2 on 1.55B SEC-EDGAR tokens, val_loss 2.45
- Introduction — motivation, contributions
- Related Work — BloombergGPT, FinGPT, small LMs, EDGAR data
- Methodology — data (1.55B tokens, 16 shards), model (12-layer GPT-2), training (RTX 4070, 5 days)
- Results — all 5 prompts analyzed with observations
- Analysis — echo vs generate, loop attractors, numerical coherence, domain drift, grammar vs logic
- Discussion — applications, limitations, comparison with larger models, future work
- Conclusion
- References (6 citations: BloombergGPT, FinGPT, GPT-2, TinyStories, EDGAR sentiment/extraction)

No LaTeX on this server — you'll need to compile on your MacBook:

  cd ~/projects/jekyll-ai-blog/latex/en/sec-edgar-gpt
  xelatex sec-edgar-gpt.tex

Or if you want me to install texlive here, I can do that. The paper uses standard packages (graphicx, hyperref, tabularx, booktabs, amsmath, listings) so it should compile cleanly.
