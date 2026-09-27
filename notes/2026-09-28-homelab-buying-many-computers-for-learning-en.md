---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Homelab: Buying Many Computers for Learning"
translated: false
type: note
---

Question: Are there people on the internet who do this — buying many computers to build a home lab for learning/experimenting?

Answer: Yes, absolutely — it's a huge, well-established hobby with active communities. This is generally called a "**homelab**."

**Where people share this**
- **r/homelab** on Reddit — a large community (roughly 450K-800K+ members depending on the source) where people share their setups, from a single Raspberry Pi to full server racks.It's an online community for DevOps engineers and programmers, established in 2012, with both a forum and a live chat via an associated Discord server.
- **r/selfhosted** — focused more on the software side (running your own services instead of using cloud providers).
- **r/DataHoarder** — for storage-heavy setups (NAS, backups).
- Many personal blogs and YouTube channels document "homelab tours."

**What a typical homelab looks like** (from a real example someone shared publicly)
One user described their setup as a small homelab mainly used to experiment and learn new technologies and networking concepts, built mostly from refurbished and second-hand machines — including two Dell servers running Proxmox and Kubernetes, a Raspberry Pi, a Synology NAS, and a PiKVM. On it they self-host things like Pi-hole, Prometheus/Grafana for monitoring, Home Assistant, a media server, and personal VPN services for family and friends.

**The range of scale is huge**
As one community member summarized it: a homelab can be as simple as a Raspberry Pi running Pi-hole, or a single old PC running a media server — all the way up to a full rack with multiple servers, disk arrays, a custom router setup, a complete media stack in Docker, and even AI workloads. The advice from long-time members is consistently: you don't need an expensive enterprise rack with UPS, patch panels, and Cisco routers — you can start with something as small as a Raspberry Pi, or even just a laptop running virtualization software, and expand only when you actually need to.

So your instinct — buy a bunch of cheap/used machines, don't be afraid to break them, and learn by doing (Docker, Kubernetes, OpenWrt, etc.) — is exactly how a large chunk of this community operates.

References:
- [r/homelab community overview](https://thehiveindex.com/communities/r-homelab)
- [Homelab user setup example (Tildes)](https://tildes.net/user/oxtyped)
- [r/homelab "New Users Start Here" guide](https://nyc1.lr.ggtyler.dev/r/homelab/comments/15jt90s/new_rhomelab_users_start_here)
