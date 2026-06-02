---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: P2P Speed Unleashed by Swarms
translated: false
type: note
---

Question: Why is BitTorrent download so fast, and why can P2P downloads easily exceed 10 MB/s?

Answer:

BitTorrent (and modern P2P protocols in general) can achieve very high download speeds — often 10–100+ MB/s on good connections — because of how the protocol fundamentally works compared to classic direct (HTTP/FTP) downloads. Here's why it's often dramatically faster:

### 1. You download from **many sources at the same time** (not just one server)
- In normal downloads (e.g. from a website), you connect to **one single server**.
  - Your max speed = that one server's upload speed to you + your download bandwidth.
  - Most home servers or even cloud servers rarely give >50–100 Mbps per connection to one user.
- In BitTorrent:
  - You connect to **dozens or hundreds of other peers** (people who already have parts of the file).
  - You download **small pieces (typically 256 KB–4 MB each)** from many different people simultaneously.
  - Your total speed = sum of upload speeds **from all those peers** to you.
  → If 50 peers each give you just 200–500 KB/s, you already reach 10–25 MB/s easily.

### 2. The more popular the torrent = the faster it goes (swarm effect)
- Popular torrents (Linux ISOs, new movies, big games) often have **hundreds or thousands of seeders**.
- More seeders → more parallel connections → more bandwidth available to you.
- On well-seeded torrents it's common to saturate a 1 Gbit/s (≈125 MB/s) home connection completely.

### 3. You give back while downloading ( Tit-for-Tat / reciprocal uploading)
- BitTorrent clients upload pieces to others while downloading.
- This "helps the swarm" → other peers prioritize **you** ( unchoke you) because you're uploading to them.
- Good upload speed from you → you get unchoked by more peers → even higher download speed.
- This creates a **positive feedback loop**: fast uploaders get the fastest downloads.

### 4. Very efficient piece selection & rarest-first strategy
- BitTorrent uses **rarest-first** piece selection: you first download the pieces that fewest people have.
- This spreads rare pieces quickly across the swarm → prevents bottlenecks.
- Combined with **end-game mode** (when almost finished, it aggressively requests missing blocks from everyone) → final pieces arrive very fast.

### 5. Multiple TCP connections = better bandwidth utilization
- Modern home internet (especially fiber) can be asymmetric or have per-connection limits.
- BitTorrent opens **50–500 simultaneous connections** (configurable).
- Many small TCP connections often achieve higher total throughput than one big HTTP connection (due to TCP window scaling, congestion control, ISP QoS, etc.).

### Real-world examples of 10+ MB/s
- 100 Mbps fiber (~12.5 MB/s theoretical max) → easily saturated with 20–40 good peers.
- 1 Gbps fiber (~125 MB/s) → very common to hit 50–120 MB/s on popular Linux distro torrents, game updates, or new movie releases.
- Gigabit connections with good routing and 200+ seeders → peaks of 150–200+ MB/s are reported regularly in 2025–2026.

### Comparison table: HTTP vs BitTorrent

| Aspect                  | Single HTTP/FTP server          | BitTorrent (P2P)                          |
|-------------------------|----------------------------------|--------------------------------------------|
| Number of sources       | 1                               | 10–1000+                                  |
| Speed limit             | Server's upload + your line     | Sum of many peers' uploads                |
| Scales with popularity  | No (server can throttle)        | Yes — more seeders = faster               |
| Can saturate gigabit    | Rarely                          | Very often on popular content             |
| Upload contribution     | None (download only)            | Required — improves your download speed   |

**Bottom line**: BitTorrent is fast because it turns downloading into a massively parallel, cooperative process instead of depending on one central point. The protocol is specifically engineered to scale with the number of participants — the more people share, the faster everyone gets the file.

References:

- [BitTorrent protocol specification (bittorrent.org)](http://bittorrent.org/beps/bep_0003.html)
- [How BitTorrent Works (Cloudflare explanation)](https://www.cloudflare.com/learning/cdn/what-is-bittorrent/)
- [Why torrents are faster than direct downloads (Reddit ELI5 threads)](https://www.reddit.com/r/explainlikeimfive/comments/related-to-bittorrent-speed)
