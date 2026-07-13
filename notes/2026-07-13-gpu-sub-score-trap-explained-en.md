---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPU Sub-Score Trap Explained
translated: false
type: note
---

Question: The 1617 is from 鲁大师's individual GPU sub-test (显卡性能), not the combined system score — does that change the verdict?

Answer: No — it makes it worse, not better.

The "40万" (400,000) number people quote for MI50/Radeon Pro VII **is itself the GPU sub-score** — confirmed directly: the card scored close to 400,000 in 鲁大师 testing, with 3DMark Time Spy around 9000, performance surpassing the 3060. So "单独性能评测" and the "40W" ad number are the **same category**, both GPU-only. There's no unit-confusion escape hatch here — 1617 vs ~400,000 in the identical test bucket is a ~250x gap, not a units mismatch.

The single most common cause of this exact symptom is well documented: when the discrete GPU driver isn't properly hooked, 鲁大师 silently benchmarks the integrated graphics instead, tanking the GPU sub-score while CPU/RAM/disk scores stay normal. This happens a lot with MI50/crossflashed cards because ROCm/AMD Vega20 driver stacks are finicky and can silently fail to bind, or Windows falls back to "Microsoft Basic Display Adapter."

So before writing this card off entirely, make the shop do this in front of you:

1. Open **Device Manager** → confirm it shows `AMD Radeon Pro VII` (or Vega 20), not "Microsoft Basic Display Adapter" / "Standard VGA."
2. **Windows Settings → System → Display → Graphics** → explicitly force high-performance/discrete GPU for 鲁大师's process.
3. Re-run the GPU sub-test watching **Task Manager → Performance → GPU** engine usage — it should spike to ~100% during the run.
4. If it's Linux, just skip 鲁大师 entirely and run something you trust:
```bash
rocm-smi --showclocks --showtemp --showpower
rocminfo | grep -A3 "Marketing Name"
# or actually stress it
python3 -c "import torch; x=torch.randn(8192,8192,device='cuda'); print((x@x).sum())"
```

If after forcing the dGPU it jumps to ~380k-420k, the card's fine and the first test was just a driver/detection fluke — common, not a scam. If it's still stuck near 1617 with the dGPU confirmed active, the card is genuinely broken (dead HBM channel, bad crossflash, damaged core) — don't buy it, no negotiation.

References:
- [魔改水冷！神卡MI50-16G - 知乎](https://zhuanlan.zhihu.com/p/1927675999115543912)
- [鲁大师性能跑分科普 - 知乎](https://zhuanlan.zhihu.com/p/35588135)
- [MI50 32G版vbios汇总及通用驱动安装办法 - CSDN](https://blog.csdn.net/dwd112358/article/details/153295770)
