---
audio: false
generated: true
image: false
lang: en
layout: post
title: Detach Volume Before Destroying Droplet
translated: false
type: note
---

Yes, but do it in the right order:

## Before Destroying

**1. Check if anything is still running:**

```bash
# are you mid-training?
tmux ls

# any processes writing to volume?
lsof /mnt/data
```

**2. Unmount the volume cleanly:**

```bash
umount /mnt/data
```

**3. Verify unmounted:**

```bash
df -h  # /mnt/data should be gone
```

## Then from Your MacBook

```bash
# get droplet ID
doctl compute droplet list

# detach volume first
doctl compute volume-action detach <volume-id> <droplet-id> --wait

# then destroy
doctl compute droplet delete <droplet-id> --force
```

## Or Just Via DigitalOcean UI

Since you're already in the UI:

1. Go to your droplet → **Volumes** tab → **Detach** the volume
2. Then **Destroy** the droplet

---

**Key rule:** always detach before destroy. Destroying with volume still attached usually works but it's risky — potential for filesystem corruption on the volume, which has your precious `train.bin` and checkpoints.

Volume stays, droplet dies, $2/hr stops. ✅
