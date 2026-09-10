---
audio: false
generated: true
image: false
lang: en
layout: post
title: CMP 170HX Unlock Paper Found
translated: false
type: note
---

Question: **You mean the recent CMP 170HX unlock paper, not the GitHub implementation.**

Answer: **Yes — you were right. I found it.**

The paper is:

**“A Canary in the Crypto Mine: Defeating Stack Protection in a GPU Secure Coprocessor” — Jon Pry, June 2026.** It was uploaded on **June 26, 2026**, and is explicitly about the CMP 170HX. ([ResearchGate][1])

[Paper — A Canary in the Crypto Mine](https://www.researchgate.net/publication/408132536_A_Canary_in_the_Crypto_Mine_Defeating_Stack_Protection_in_a_GPU_Secure_Coprocessor?utm_source=chatgpt.com)

The paper's core result is much more interesting than simply “unlocking VRAM”:

```text
CMP 170HX
   │
   ├── GA100 / A100 silicon
   │
   ├── SM rate: 1/32
   ├── VRAM: 8/10 GB exposed
   └── PCIe: Gen1
          │
          ▼
   SEC2 / Heavy-Secure Falcon
          │
          ▼
   stack-protection bypass
          │
          ▼
   arbitrary code execution
          │
          ▼
   modify privileged GPU state
          │
          ├── restore SM throughput
          ├── restore memory geometry
          └── defeat PCIe restriction
```

The paper claims that the three commercial restrictions are **software-defeatable from a rooted host**, without NVIDIA signing keys, debug fuses, or physical access. The key vulnerability is the GPU secure coprocessor's stack-protection mechanism. ([ResearchGate][1])

And the chronology is quite clear now:

* **June 26:** `A Canary in the Crypto Mine` circulated as a preprint.
* **July 1:** raw `booter_load` disassembly appeared.
* **July 3:** annotated disassembly.
* **July 10:** register/gadget research.
* **July 14:** initial `cmpunlocker` commit.
* **July 16:** paper posted into the research server as `main.pdf`.
* **July 18:** working memory-unlock commit. ([GitHub][2])

So **the paper you're remembering is almost certainly Jon Pry's paper**. The later `cmpunlocker` project is the implementation/reproduction layer built around this research. ([GitHub][3])

I can also trace **the paper → exact exploit → exact register writes → 8 GB → 64 GB transformation** and map the whole thing technically.

[1]: https://www.researchgate.net/publication/408132536_A_Canary_in_the_Crypto_Mine_Defeating_Stack_Protection_in_a_GPU_Secure_Coprocessor?utm_source=chatgpt.com "(PDF) A Canary in the Crypto Mine: Defeating Stack Protection in a GPU Secure Coprocessor"
[2]: https://github.com/Consensus-Protocol/cmp170hx/blob/main/docs/history/clean-room-and-provenance.md?utm_source=chatgpt.com "cmp170hx/docs/history/clean-room-and-provenance.md at main · Consensus-Protocol/cmp170hx · GitHub"
[3]: https://github.com/WebForks/cmpunlocker/blob/main/README.md?utm_source=chatgpt.com "cmpunlocker/README.md at main · WebForks/cmpunlocker · GitHub"