---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Home Lab Chaos and Learning
translated: false
type: note
---

**Question:** Suppose I have a Mac and 2 Ubuntu laptops at home. What programs or funny projects can I do? Just Kafka and ZooKeeper for learning purposes? What other cool things can I do?

**Answer:**

You have a nice heterogeneous setup (macOS + Linux) that's perfect for a small home lab / distributed playground. Kafka + ZooKeeper (or the modern KRaft mode without ZooKeeper) is a solid start for learning streaming / event-driven systems, but there are tons of more fun, silly, or practical projects you can build with these three machines.

Here are some ideas ranked roughly from "quick & funny" to "more serious learning / useful":

### Funny / Silly / "Why not?" Projects

- **Distributed useless computing cluster**
  Turn the three machines into a mini "supercomputer" that wastes electricity together: run BOINC (SETI@home style), Folding@home across all three, or Mine some joke cryptocurrency (or just simulate mining with silly scripts). Bonus: write a Python script that pings between machines and shows fake "processing power" stats on the Mac screen.

- **Over-engineered home meme / notification system**
  One Ubuntu runs ntfy.sh or Gotify server. Write tiny scripts on all machines (including Mac) that send ridiculous notifications: "Dad's Mac just opened Reddit again", "Ubuntu-2 CPU at 0.1% – it's napping", or meme quotes every hour via cron. Add sound effects on the Mac using `say` or `afplay`.

- **Multi-room chaotic music / sound server**
  Run Mopidy or Jellyfin + Snapcast on one Ubuntu (server), control from Mac/iPhone, and sync audio playback across all three laptops (if they have speakers). Play the same song everywhere → instant annoying home surround system. Or make one machine the "DJ troll" that randomly changes volume/playlist.

- **Fake smart home with zero IoT**
  Use Home Assistant (on one Ubuntu) but control fake "devices": scripts that pretend to be lights (change terminal color), coffee maker (print ASCII coffee), or robot vacuum (move mouse cursor randomly on Mac).

### Cool & Actually Useful Learning Projects

- **Mini Kubernetes / container orchestration playground**
  Install k3s (lightweight Kubernetes) on all three machines → one as master (maybe Mac with multipass VMs or kind), two Ubuntu as workers. Deploy silly things like 404-game, Minecraft server pods that auto-scale, or a distributed "fortune" teller service.

- **Self-hosted personal cloud stack**
  - Ubuntu-1: Nextcloud or Immich (photos) + PostgreSQL/MariaDB
  - Ubuntu-2: MinIO (S3-compatible object storage) or TrueNAS SCALE in a VM
  - Mac: Use it as client + Time Machine backup target to one Ubuntu via SMB/NFS
  Sync files/photos across all devices privately.

- **Distributed task queue fun**
  Beyond Kafka/ZooKeeper:
  - Set up Celery + Redis/RabbitMQ across machines
  - Or use Dask.distributed: Mac as scheduler, two Ubuntu as workers → run embarrassingly parallel Python tasks (image processing, ML training chunks, password cracking demo, rendering Mandelbrot sets across nodes).

- **Monitoring & observability overkill**
  Prometheus + Grafana on one Ubuntu, node-exporter on all three → beautiful dashboard showing CPU, funny metrics like "number of open Safari tabs on Mac", temperature if sensors work, uptime bragging rights.

- **GitLab / Gitea + CI/CD playground**
  Self-host Gitea or full GitLab on one Ubuntu. Set up GitLab Runner on all three machines (including Mac runner). Practice pipelines: build Docker images, deploy joke websites, or auto-backup your dotfiles.

- **Media & backup fortress**
  Jellyfin / Plex on Ubuntu-1 (media server), sync media folders with Syncthing or rsync from Mac. Use restic/BorgBackup on all machines → encrypted backups to each other (3-2-1 rule on a budget).

- **Learning modern data/streaming beyond basic Kafka**
  - Redpanda (Kafka-compatible, easier setup)
  - Apache Flink or Spark cluster (tiny scale) for processing fake streaming data (e.g., Twitter-like feed simulator)
  - Temporal.io or n8n for workflow orchestration across machines

- **Network security playground**
  One Ubuntu as pfSense/OPNsense router/firewall (needs second NIC), Mac and other Ubuntu behind it → experiment with VLANs, WireGuard VPN between machines, intrusion detection (Suricata), or Pi-hole for ad-blocking.

Start small: pick one project, use Docker/Podman everywhere for consistency (Mac supports both), Ansible from Mac to manage the two Ubuntu boxes. Most fun comes from over-engineering something stupid — that's the spirit of home labs!

**References:**

- [https://github.com/mikeroyal/Self-Hosting-Guide](https://github.com/mikeroyal/Self-Hosting-Guide)
- [https://awesome-selfhosted.net/](https://awesome-selfhosted.net/)
- [https://www.youtube.com/watch?v=prg6-sYlijM](https://www.youtube.com/watch?v=prg6-sYlijM)
- [https://b3n.org/homelab-ideas](https://b3n.org/homelab-ideas)
- [https://selfh.st/apps](https://selfh.st/apps)
