---
audio: false
generated: true
image: false
lang: en
layout: post
title: Self-Host Analytics Without Exposing Home IP
translated: false
type: note
---

**Question:** But to self-host analytics on my workstation, I need to expose it to the outside internet, right?

**Answer:**

Yes — the tracking script runs in your visitors' browsers, so it needs a publicly reachable URL to POST events to. Your blog is on the public internet; the analytics endpoint must be too. But "expose" doesn't mean opening ports on your home router. Better options:

**Cloudflare Tunnel (recommended)** — outbound-only connection from your workstation to Cloudflare's edge. No port forwarding, no exposed home IP, free, gives you a real HTTPS domain. The `cloudflared` daemon dials out, so your firewall stays fully closed inbound.

```bash
# on lzw@192.168.1.36
brew install cloudflared   # or apt
cloudflared tunnel login
cloudflared tunnel create umami
# map a hostname (needs a domain on Cloudflare) to local Umami
cloudflared tunnel route dns umami analytics.yourdomain.com
cat > ~/.cloudflared/config.yml <<'EOF'
tunnel: umami
credentials-file: /home/lzw/.cloudflared/<UUID>.json
ingress:
  - hostname: analytics.yourdomain.com
    service: http://localhost:3000
  - service: http_status:404
EOF
cloudflared tunnel run umami
```

Requires a custom domain on Cloudflare (~$10/yr for a `.com`). Then your script src is `https://analytics.yourdomain.com/script.js`.

**Tailscale Funnel** — similar outbound model, gives you a `*.ts.net` HTTPS hostname with zero domain purchase. Simplest if you don't want to buy a domain.

```bash
tailscale funnel 3000   # exposes local :3000 publicly over HTTPS
# → https://your-machine.tailXXXX.ts.net
```

Caveat: Funnel hostnames are ugly and Tailscale rate-limits Funnel bandwidth — fine for a personal blog's analytics volume, not for high traffic.

**The honest tradeoff:** running this on a home workstation means your analytics uptime is tied to your machine being on, your home internet, and the tunnel staying up. For a *blog*, that's annoying — you'll miss data whenever the box reboots or your ISP blips.

**My revised recommendation:** For analytics specifically, the self-hosting purity isn't worth the fragility. Either:

1. **Umami Cloud** free hobby tier or **GoatCounter** hosted — zero infra, always up, still privacy-friendly. Save the self-hosting energy for workloads that actually benefit from your GPU (model training, inference serving).
2. If you *do* want to self-host, put Umami on a $4–6/mo VPS (Hetzner/Fly.io), not your home box — cheap, always-on, no tunnel needed, public IP included.

The workstation is your ML rig. Don't burn its uptime and your tunnel-debugging hours on a pageview counter. Reserve home self-hosting for things where the 192GB-class hardware or data locality is the point.
