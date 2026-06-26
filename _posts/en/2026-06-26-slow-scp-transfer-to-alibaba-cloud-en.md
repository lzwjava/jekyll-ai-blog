---
audio: false
generated: true
image: false
lang: en
layout: post
title: Slow SCP Transfer to Alibaba Cloud
translated: false
type: note
---

Question: Why is the SCP transfer to my Alibaba Cloud HK box (47.86.12.246) so slow at ~270–370 KB/s, even though the test upload to HF from there was faster than from my Mac?

Answer:

Quick clarification of what your log actually shows, because two different transfers are being conflated:

1. **Mac → Alibaba HK (SCP)**: ~270–370 KB/s. This is the slow one.
2. **Alibaba HK → HuggingFace (hf upload)**: ~515 KB/s, 2.7x faster than Mac → HF.

So Alibaba isn't fast — the HK box is just a *better-positioned relay* to HF than your Mac is. The bottleneck in step 1 is the **Mac → HK leg**, and it's almost certainly your home/office upstream + the GFW path to Alibaba's public IP, not Alibaba itself.

Why the Mac → HK SCP crawls:

- **SCP is single-stream TCP.** One connection, so throughput is capped by `window_size / RTT`. On a cross-border path with loss, BBR-vs-CUBIC mismatch and a small receive window murder you. You're not saturating bandwidth — you're RTT/loss-bound.
- **SCP/SSH has cipher + framing overhead** and no parallelism. The 15ms "link" figure in the log is misleading; real China→HK paths jitter and drop under the GFW.
- **Your home upstream** is likely the hard ceiling (~2–5 Mbit/s up = ~300–600 KB/s). 370 KB/s ≈ 3 Mbit/s. That smells like your ISP upload cap, not Alibaba.

What to do instead — kill the single-stream bottleneck:

```bash
# 1. rsync over multiple isn't native, but compress + resume:
rsync -avP --partial /Users/lzwjava/projects/sec-edgar-gpt-124m/model.safetensors \
  root@<IP_ADDRESS>:/tmp/

# 2. Parallel streams — the real fix. Use rclone with chunked parallel transfer:
rclone copy model.safetensors hk:/tmp/ --transfers 8 --multi-thread-streams 8

# 3. Or just skip the relay entirely — upload Mac → HF directly with
#    hf's built-in xet/multipart, which already does parallel chunks:
hf upload lzwjava/sec-edgar-gpt-124m model.safetensors model.safetensors
```

The AI-native move here: **stop relaying.** The only reason the HK box helped was HF endpoint proximity. But `hf upload` already does parallel multipart + xet dedup. Your Mac → HF direct path with `--transfers` parallelism will likely beat Mac → SCP → HK → HF, because SCP's single stream is the actual villain — you're paying the slow Mac→HK leg *plus* a copy, to save on a leg that hf parallelizes anyway.

If the HK relay genuinely wins (worth measuring), at least make the Mac→HK leg parallel:

```bash
# split + parallel scp, reassemble on HK
split -b 50M model.safetensors model.part.
ls model.part.* | xargs -P8 -I{} scp {} root@<IP_ADDRESS>:/tmp/
ssh root@<IP_ADDRESS> 'cat /tmp/model.part.* > /tmp/model.safetensors'
```

8 parallel streams typically gets you 4–6x on a loss-bound cross-border path.

Bottom line: Alibaba isn't fast. SCP is slow because it's one TCP stream over a lossy China→HK path bounded by your home upstream. Parallelize, or cut the relay and let `hf upload` do the chunking direct from your Mac.
