---
audio: false
generated: true
image: false
lang: en
layout: post
title: Add Both Links to Paper
translated: false
type: note
---

Question: Should I add the GitHub repo link (https://github.com/lzwjava/sec-edgar-gpt) and the Hugging Face model link (https://huggingface.co/lzwjava/sec-edgar-gpt-124m-hf) into the paper (.tex), given the content won't change much in the near future — or should I skip the paper and just add them to a Twitter post instead?

Answer:

Yes, put both links in the paper. This is the right call, and the reasoning is concrete:

**A paper is the canonical, archival artifact. A tweet is ephemeral.** Six months from now, someone who finds your `.tex`/PDF (via arXiv, Google Scholar, a citation, or your notes site) needs the code and weights reachable *from the document itself*. Twitter posts decay — they're unsearchable after a week, die if the account changes, and nobody cites a tweet. The paper is what gets indexed, forwarded, and referenced. Reproducibility links belong where the claims live.

**Convention strongly supports it.** Modern ML papers routinely include `\footnote{Code: ...}` on the first page and a dedicated reproducibility/artifacts section. Reviewers and readers expect "Code available at" and "Weights available at." A GPT-2 124M reproduction paper without a repo + checkpoint link is strictly weaker.

**The "content won't change" point actually argues *for* adding it, not against.** Stable links are exactly what you want in an archival document. The risk with papers is linking to something that rot-changes; since your repo and the HF model are stable, the paper link stays valid. If you're worried about future churn, pin a release tag and a specific HF revision:

- `https://github.com/lzwjava/sec-edgar-gpt/tree/v1.0`
- `https://huggingface.co/lzwjava/sec-edgar-gpt-124m-hf/tree/<commit-sha>`

That way the paper points at an immutable snapshot even if `main` evolves.

**Concrete placement in the `.tex`:**

First-page footnote on the title (most visible):

```latex
\title{SEC-EDGAR-GPT: ...%
\thanks{Code: \url{https://github.com/lzwjava/sec-edgar-gpt} \quad
Model: \url{https://huggingface.co/lzwjava/sec-edgar-gpt-124m-hf}}}
```

And a short reproducibility section near the end:

```latex
\section{Code and Model Availability}
The training code, configuration, and dataset pipeline are released at
\url{https://github.com/lzwjava/sec-edgar-gpt}. Pretrained weights
(124M parameters, HF format) are available at
\url{https://huggingface.co/lzwjava/sec-edgar-gpt-124m-hf}.
```

Make sure you have `\usepackage{hyperref}` (and `url` is pulled in by it) so the links are clickable in the PDF.

**Do both — it's not either/or.** Paper = canonical record (must have the links). Twitter = distribution/marketing (drives traffic *to* the paper and repo). The tweet links to the paper; the paper links to the artifacts. That's the correct directionality. Cross-link them: the GitHub README should also link the paper PDF and the HF model, so each entry point reaches the other two.

So: add both links to the `.tex` now, pin them to a tag/revision if you want immutability, then announce on Twitter with a link back.
