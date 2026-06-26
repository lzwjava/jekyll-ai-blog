---
audio: false
generated: true
image: false
lang: en
layout: post
title: Guangzhou-HK Proxy for ML Workloads
translated: false
type: note
---

Your VPN/proxy routing is going Guangzhou → Hong Kong, and yes — for HuggingFace and most international ML traffic, this is a good setup.

Here's why it works in your favor:

**Geography + peering.** Guangzhou to Hong Kong is ~140km. The 1.6ms ping you're seeing means your traffic hits a CloudFront HKG edge node almost immediately. Hong Kong sits outside the GFW, so once your packets reach the Alibaba Cloud HK instance (AS45102), they have unrestricted, well-peered routes to AWS/CloudFront/HuggingFace CDN endpoints.

**The bottleneck isn't HK→HuggingFace, it's Mainland→HK.** The 5.7 MB/s you measured is the HK box's own egress to HuggingFace — that's clean. Your real constraint is the Guangzhou→HK leg crossing the border. That's where throttling, packet loss, and jitter happen. So the smart architecture is: do the heavy pulling *on the HK box*, not on your Mac through a tunnel.

For your actual workflow this means:

```bash
# On the HK Alibaba box — pull/cache models here
export HF_HUB_ENABLE_HF_TRANSFER=1
pip install -U "huggingface_hub[hf_transfer]" hf_transfer
hf download deepseek-ai/DeepSeek-V3 --local-dir ./models/dsv3

# Then sync to your Mac / workstation over the border once, compressed
rsync -avz --progress lzw@<HK_IP>:./models/dsv3 ~/models/
```

`hf_transfer` (Rust-based) saturates the link with parallel chunked downloads — it'll push that 5.7 MB/s higher if HuggingFace's CDN gives you more concurrent connections. Worth benchmarking with it on vs off.

One caveat on "good": 5.7 MB/s (~45 Mbps) is *fine* but not great for a HK datacenter box — Alibaba Cloud HK instances can usually do 100+ Mbps to AWS edges. If you're pulling a 600GB MoE checkpoint, 5.7 MB/s is ~30 hours. Check whether your instance has a bandwidth cap (the 1.6GB RAM / 2-core suggests a small/burstable instance, which often caps egress):

```bash
# Quick raw-throughput test, bypassing HF app layer
curl -o /dev/null -w "%{speed_download}\n" \
  https://cdn-lfs.huggingface.co/<some-large-file>
```

So: routing through Guangzhou→HK is the right call for hitting international ML infra. Just make the HK box the workhorse and treat the cross-border leg as a one-time sync, not the hot path.
