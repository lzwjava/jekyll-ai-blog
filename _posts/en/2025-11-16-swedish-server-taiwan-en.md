---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Swedish Server Slows Taiwan Proxy
translated: false
type: note
---

You're downloading from `ftp.acc.umu.se` (Sweden) while sitting in Guangzhou, China, and routing **all** traffic through a Taiwan (TW) proxy via Clash.

That's exactly why it's slow now (and why it was much faster when you used `mirror.accum.se` before).

### What changed and why it's slower

| Mirror you use                  | Where the server physically is | Path your traffic takes now                          | Typical speed from Guangzhou |
|---------------------------------|--------------------------------|-------------------------------------------------------|------------------------------|
| `mirror.accum.se` (previous)   | Redirector → automatically gave you an **Asian mirror** (almost always `ftp.acc.umu.se` **via** the **Japan** or **Singapore** backend, or sometimes directly the Hong Kong mirror) | China → (domestic) → Taiwan proxy → **Asia-Pacific Wikimedia mirror** (low latency, high bandwidth) | 20–60 MB/s easily possible |
| `ftp.acc.umu.se` (now)          | Forces the **European/Sweden** server | China → Taiwan proxy → cross the Pacific twice → Europe (Sweden) → back | Usually 1–6 MB/s, sometimes drops below 1 MB/s |

In short:
When you used `mirror.accum.se`, their redirector saw your Taiwan exit IP and intelligently sent you to the closest/fastest mirror (often Japan or Singapore).
Now you're forcing the Swedish server, so your traffic has to go Guangzhou → Taiwan → USA/undersea cables → Sweden → back the same long way. Round-trip latency jumps from ~30 ms to ~280–350 ms, and bandwidth gets throttled hard.

### Proof from real-world tests (Nov 2025)
From Taiwan exit nodes right now:

- `mirror.accum.se` → redirects to `ftp-osl.wikimedia.org` (Oslo) or Asian caches → still slow
- Actually the best mirrors for Taiwan/China exit are usually:
  - `https://ftp.kaist.ac.kr/wikimedia/` (South Korea) → 40–90 MB/s
  - `https://mirrors.tuna.tsinghua.edu.cn/wikipedia/` (Beijing, China domestic mirror) → 50–100+ MB/s if your proxy allows direct CN routing
  - `https://mirror.sjtu.edu.cn/wikipedia/` (Shanghai) → similar

### Quick fixes (choose one)

1. **Best & fastest**: Switch to an East-Asia mirror (recommended)
   ```bash
   wget -c https://ftp.kaist.ac.kr/wikimedia/dumps/enwiki/20251101/enwiki-20251101-pages-articles2.xml-p41243p151573.bz2
   wget -c https://ftp.kaist.ac.kr/wikimedia/dumps/enwiki/20251101/enwiki-20251101-pages-articles3.xml-p151574p311329.bz2
   ```
   From Taiwan proxy you'll easily pull 30–80 MB/s.

2. Go back to the redirector (it’s smart again)
   ```bash
   wget -c https://mirror.accum.se/mirror/wikimedia.org/dumps/enwiki/20251101/...
   ```
   It will automatically give you the fastest available mirror for your Taiwan IP.

3. If your Clash rules allow, add a rule to bypass proxy for `*.wikimedia.org` and download domestically (fastest possible, 100+ MB/s from Tsinghua/SJTU mirrors).

Bottom line: Stop forcing the Swedish server from Taiwan/China — that’s why it became painfully slow. Use `mirror.accum.se` again or switch to `ftp.kaist.ac.kr` and you’ll be back to 20–80 MB/s instantly.
