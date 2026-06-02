---
audio: false
generated: true
image: false
lang: en
layout: post
title: Managing Dynamic IPs on DigitalOcean Droplets
translated: false
type: note
---

**Question:** Every time I create a GPU droplet or restore from a snapshot on AMD Developer Cloud (DigitalOcean), the Public IPv4 address changes — is that expected behavior?

**Answer:**

Yes, that's completely expected. Here's why:

## Ephemeral IPs on DigitalOcean Droplets

DigitalOcean assigns Public IPv4 addresses **dynamically from a pool** at droplet creation time. This means:

- **New droplet** → new IP from pool
- **Droplet destroyed + recreated** → different IP
- **Restored from snapshot** → different IP (it's a new droplet instance, just with your old disk state)
- **Powered off then on** → IP is **preserved** (the droplet still exists)

The IP is bound to the droplet's *existence*, not its *state*.

## What Stays the Same (Snapshot Restore)

When you restore a snapshot, you get:

- ✅ Same filesystem, packages, models, configs
- ✅ Same SSH keys (baked into the image)
- ❌ Different Public IPv4
- ❌ Different droplet ID

## Practical Fix: Stop Chasing IPs

Since you work terminal-first, the cleanest solutions:

**Option 1: Reserved IP (DigitalOcean's static IP)**

```bash
# Assign a reserved IP to your droplet via doctl
doctl compute reserved-ip-action assign <reserved-ip> --droplet-id <id>
```

Reserved IPs persist across droplet recreations — you reassign them. Free while assigned to a running droplet.

**Option 2: Script your SSH config update**

```bash
#!/bin/bash
# After creating droplet, grab new IP and update ~/.ssh/config
NEW_IP=$(doctl compute droplet get <droplet-name> --format PublicIPv4 --no-header)
sed -i '' "s/HostName .*/HostName $NEW_IP/" ~/.ssh/config
echo "Updated SSH config: $NEW_IP"
```

**Option 3: Use `doctl` to always resolve dynamically**

```bash
# One-liner SSH without hardcoding IP
ssh $(doctl compute droplet get amd-gpu --format PublicIPv4 --no-header) -i ~/.ssh/your_key
```

Add to your `~/.zshrc` or `~/.bashrc`:

```bash
alias amd='ssh -i ~/.ssh/amd_key $(doctl compute droplet get amd-gpu --format PublicIPv4 --no-header)'
```

**Option 4: Tailscale (best for long-term)**

Install Tailscale inside your snapshot image — it assigns a stable `100.x.x.x` address that never changes regardless of public IP:

```bash
# Inside the droplet (bake into snapshot)
curl -fsSL https://tailscale.com/install.sh | sh
tailscale up
```

Then always `ssh 100.x.x.x` — works even if DigitalOcean changes your public IP.

## Recommendation for You

Since you're spinning up expensive MI300X droplets and destroying them to save ~$2/hr, **Tailscale baked into the snapshot** is the cleanest solution. One-time setup, zero IP management forever. Reserve the DigitalOcean Reserved IP as a fallback if you need a stable public-facing endpoint.
