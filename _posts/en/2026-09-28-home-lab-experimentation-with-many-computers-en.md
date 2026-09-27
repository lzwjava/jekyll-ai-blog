---
audio: false
generated: true
image: false
lang: en
layout: post
title: Home Lab Experimentation with Many Computers
translated: false
type: note
---

Question: Is it a good approach to buy many computers (10-20) for home lab use and experiment freely without fear of breaking them — installing things like OpenWrt, Docker, Kubernetes, etc. — as a way to learn a lot?

Answer: Yes, that's a solid and pretty common approach among people who want to genuinely learn systems, networking, and infrastructure. A few thoughts on why it works and how to do it well:

**Why this works**
- Real learning happens when you can break things safely. If you're always worried about breaking your one important machine, you'll avoid the exact experiments that teach you the most (bad configs, failed upgrades, corrupted partitions, botched network changes).
- Having multiple machines lets you simulate real-world scenarios: clusters, distributed systems, failover, load balancing — things you literally cannot learn on a single machine.
- OpenWrt, Docker, and Kubernetes are exactly the kind of tools where hands-on breakage teaches you more than tutorials. Bricking a router with OpenWrt and recovering it teaches you more about networking than reading 10 articles.

**Practical suggestions to make this sustainable**
- You don't need 10-20 *powerful* machines — old thin clients, mini PCs (like used Dell/HP/Lenovo tiny form factor), Raspberry Pis, or old laptops work great and are cheap/replaceable.
- Keep at least one "stable" machine or environment (could even be a VM) for anything you actually depend on (work, important files), separate from your experimental fleet.
- Learn to use **snapshots/backups/imaging** (e.g., Clonezilla, Proxmox snapshots) so "breaking" something is fast to recover from — this actually lets you break things *more* boldly, not less.
- Label/document your devices' baseline configs so you always have a known-good state to return to.
- A common progression: single Linux box → Docker containers → multiple VMs (via Proxmox/ESXi) → Kubernetes cluster (k3s is great for home use) → dedicated hardware like OpenWrt routers, NAS, Pi-hole, etc.

**One caution**
- Don't let "not being afraid to break things" become "never really understanding *why* it broke." The value comes from diagnosing and fixing, not just reinstalling from scratch every time. Try to understand root causes when you can, even if the fix is just reflashing.

So overall: yes, your instinct is right. A home lab with disposable/cheap hardware, where you're free to experiment aggressively with networking, containers, and orchestration, is one of the best ways to build real systems skills.

References:
- [r/homelab community wiki](https://www.reddit.com/r/homelab/wiki/index/)
- [OpenWrt documentation](https://openwrt.org/docs/start)
- [k3s - Lightweight Kubernetes](https://k3s.io/)
