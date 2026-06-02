---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Hugging Face Download Speed Solutions
translated: false
type: note
---

Your issue is very typical for people in mainland China (especially South China like Guangzhou) when downloading large files from Hugging Face.

### Why without proxy → extremely slow (~200–300 KB/s)
- Even though you are using **hf-mirror.com** (the official Chinese mirror run by HF + 01.AI), the actual large parquet files of FineWeb are **not cached inside China**.
- hf-mirror.com only redirects you to the global CDN (now using xet-bridge on AWS us-east-1).
- From Guangzhou without proxy → your traffic goes through international gateways (China Telecom/Unicom/Mobile backbone → US AWS), and large-file downloads are heavily throttled or QoS-limited. 2 GB files easily drop to < 500 KB/s, sometimes even 100 KB/s.

### Why with Clash proxy → suddenly very fast (often 20–100 MB/s)
- Your Clash is almost certainly using a Hong Kong, Taiwan, Japan, Singapore, or Korea node (very common for Guangzhou users).
- These nodes have:
  - Direct peering or very good connectivity to AWS us-east-1 (or Cloudflare that HF also uses)
  - No GFW throttling on outbound traffic
  - Much higher bandwidth
- So even though you are “detouring” through the proxy, the actual path is much faster than the direct international exit from mainland China.

### In short
Direct (even via hf-mirror.com) from Guangzhou → slow because the real storage is still in the US, and China → US bandwidth for big files is terrible in 2025.
Clash proxy (HK/TW/JP/SG node) → fast because those nodes have excellent connectivity to US AWS.

### Recommended solutions (from fastest to slowest)

1. **Keep using Clash (or v2rayN, Surge, etc.) with a low-latency HK/TW/JP node** — this is currently the fastest way in mainland China for FineWeb, RedPajama, The Stack, etc.

2. Use **HF’s official accelerated endpoint in China** (works without any proxy for many people in 2024-2025):
   ```bash
   export HF_ENDPOINT=https://hf-mirror.com
   ```
   Then use huggingface-cli or datasets library directly (not wget). Many users in China report 50–200 MB/s this way now because HF has started caching more shards on Aliyun/ Tencent Cloud in 2025.

3. Use **FastGit + hugger** or **openi/pkulaw mirrors** (some shards are cached in China):
   Example:
   ```bash
   pip install hugger
   hugger download HuggingFaceFW/fineweb --revision main --include "CC-MAIN-2013-20/*.parquet"
   ```

4. Keep wget + hf-mirror.com but force it through your Clash proxy (what you are already doing).

### Quick one-liner to download any FineWeb shard fast from Guangzhou
```bash
# Set Clash HTTP proxy (port usually 7890)
export https_proxy=http://127.0.0.1:7890

# Then use aria2 (much faster + resume than wget)
aria2c -x16 -s16 -k1M "https://hf-mirror.com/datasets/HuggingFaceFW/fineweb/resolve/main/data/CC-MAIN-2013-20/000_00000.parquet"
```

You’ll easily get 30–100 MB/s depending on your proxy node.

So bottom line: in mainland China in 2025, for >1 GB files on Hugging Face, using a HK/TW/JP proxy is still almost always faster than direct connection, even when using hf-mirror.com. This is just the reality of international bandwidth from China right now.
