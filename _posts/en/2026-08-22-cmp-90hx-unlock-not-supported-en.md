---
audio: false
generated: true
image: false
lang: en
layout: post
title: CMP 90HX Unlock Not Supported
translated: false
type: note
---

Question: Can `amoghmunikote/cmpunlocker` be used to unlock a NVIDIA CMP 90HX?

Answer:

No, **the original `amoghmunikote/cmpunlocker` cannot directly unlock CMP 90HX**. It is specifically written for **CMP 170HX (GA100)**. The original project targets PCI ID `10de:20c2` / `10de:2082` (CMP 170HX variants), and its unlock logic is for GA100 HBM2e geometry + SM unlock. ([GitHub][1])

CMP 90HX is a different GPU:

* CMP 170HX → **GA100** (A100 silicon)
* CMP 90HX → **GA102** (RTX 3080-class silicon) ([GitHub][2])

The exploit path is different because the Falcon/GSP firmware is different. The original ROP payload and register offsets do not transfer. ([GitHub][2])

For CMP 90HX, you need a **90HX-specific fork/tool**. There are community ports:

* `WildFlash1st/cmp90hx-unlock` — research port for CMP 90HX. It adds GA102 support (`PCI ID 10de:220d`), but the full unlock is still experimental; the README says the exploit chain activates but PLM unlock still needs ROP gadget work. ([GitHub][2])
* `pearlfortune/cmpunlocker` — newer fork that adds CMP 90HX support and provides a `compute90hx-v67` path. It lists tested CMP 90HX environments and commands such as:

```bash
sudo ./cmpunlocker-rs compute90hx-v67 run \
  --all-cmp90hx \
  --acknowledge I-ACCEPT-90HX-V67-COMPUTE-UNLOCK

sudo ./cmpunlocker-rs compute90hx-v67 verify \
  --all-cmp90hx \
  --expect full
```

([GitHub][3])

For an AI workstation, CMP 90HX is interesting because it is basically a crippled GA102 card:

* 10GB GDDR6X
* 320-bit memory bus
* ~760 GB/s bandwidth
* RTX 3080-class silicon ([VideoCardz.com][4])

But the value proposition is different from CMP 170HX:

* CMP 170HX unlock → potentially 40/64GB VRAM, huge gain for LLM
* CMP 90HX unlock → mostly compute/feature unlock, **VRAM remains 10GB** ([GitHub][2])

For your AI use case (Qwen/DeepSeek inference, LoRA, training experiments), a CMP 90HX is still limited by 10GB VRAM. A cheap 3090 24GB, RTX A5000 24GB, or unlocked CMP 170HX is much more attractive.

References:

* amoghmunikote/cmpunlocker (CMP 170HX) ([GitHub][1])
* WildFlash1st/cmp90hx-unlock (CMP 90HX research) ([GitHub][2])
* pearlfortune/cmpunlocker (CMP 90HX support) ([GitHub][3])

[1]: https://github.com/amoghmunikote/cmpunlocker?utm_source=chatgpt.com "GitHub - amoghmunikote/cmpunlocker: A tool to unlobotomize your NVIDIA card! · GitHub"
[2]: https://github.com/WildFlash1st/cmp90hx-unlock?utm_source=chatgpt.com "GitHub - WildFlash1st/cmp90hx-unlock: Unlocking NVIDIA CMP 90HX (GA102): kernel 6.12 port + Falcon ROP exploit research. Contributors wanted! · GitHub"
[3]: https://github.com/pearlfortune/cmpunlocker/blob/main/README.en.md?utm_source=chatgpt.com "cmpunlocker/README.en.md at main · pearlfortune/cmpunlocker · GitHub"
[4]: https://videocardz.com/newz/nvidia-crypto-mining-processor-90hx-card-is-based-on-ampere-ga102-100-gpu?utm_source=chatgpt.com "NVIDIA Crypto Mining Processor 90HX card is based on Ampere GA102-100 GPU - VideoCardz.com"
