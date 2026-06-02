---
audio: false
generated: true
image: false
lang: en
layout: post
title: Transfer Data Between DigitalOcean Droplets
translated: false
type: note
---

Question: How can I transfer 100GB of data between a normal Droplet and a GPU Droplet in DigitalOcean?

Answer:

Yes — you **can transfer 100GB between Droplets** in DigitalOcean. There are **4 common methods**, ranked from best to worst for your use case.

---

# ✅ Best Method (Recommended): Private Network + rsync/scp

If both droplets are in the **same region**, use **private networking** — fastest and free.

### Step 1 — get private IPs

On both droplets:

```bash
ip a
```

You'll see something like:

```
10.124.0.5   (droplet A)
10.124.0.8   (GPU droplet)
```

---

### Step 2 — transfer 100GB using rsync (best)

From GPU droplet:

```bash
rsync -avz --progress root@10.124.0.5:/data/ /data/
```

Or using `scp`:

```bash
scp -r root@10.124.0.5:/data /data
```

These are standard ways to copy files between droplets over SSH. ([DigitalOcean][1])

**Why this is best**

* uses internal network (fast)
* no internet bandwidth
* no extra storage
* works for 100GB easily

---

# ✅ Even Better (Fastest): Attach Volume

This is the **pro method** for large datasets.

Workflow:

1. Create volume (100GB)
2. attach to cheap droplet
3. download dataset
4. detach volume
5. attach to GPU droplet

DigitalOcean allows moving volumes between droplets in the **same region**. ([DigitalOcean Docs][2])

This avoids copying entirely.

Speed = instant (no transfer)

---

# Method 3 — snapshot droplet

If your whole droplet has data:

1. snapshot droplet
2. create GPU droplet from snapshot

This copies everything at once. ([DigitalOcean][3])

---

# Method 4 — object storage (Spaces)

Upload → download

```
cheap droplet → DO Spaces → GPU droplet
```

slower but works across regions.

---

# What I Recommend For Your Training Setup

Your plan:

> cheap droplet download 100GB
> then start H100 GPU droplet
> transfer internally

Best architecture:

### Option A (clean)

```
cheap droplet
    ↓ rsync (private IP)
GPU droplet
```

### Option B (professional)

```
cheap droplet
    ↓
volume (100GB)
    ↓
GPU droplet
```

Option B is **what serious training pipelines use**

---

# Real Speed Expectation

Inside DigitalOcean private network:

Typical:

* 1–10 Gbps internal
* 100GB transfer time:

| speed  | time    |
| ------ | ------- |
| 1 Gbps | ~15 min |
| 2 Gbps | ~7 min  |
| 5 Gbps | ~3 min  |

So **100GB is trivial**

---

# Example (Your Exact Workflow)

cheap droplet:

```
/dataset/100gb
```

GPU droplet:

```
mkdir /dataset
```

run:

```bash
rsync -avz --progress root@10.0.0.5:/dataset/ /dataset/
```

done.

---

# Conclusion

Yes — your idea is correct:

cheap droplet download → transfer → start GPU training

Use one of:

1. rsync over private IP (simplest)
2. attach volume (best)
3. snapshot (full clone)

I recommend **volume method** if you do this often.

References:

* [https://docs.digitalocean.com/products/volumes/how-to/move-between-droplets/](https://docs.digitalocean.com/products/volumes/how-to/move-between-droplets/)
* [https://docs.digitalocean.com/docs/droplets/how-to/transfer-files](https://docs.digitalocean.com/docs/droplets/how-to/transfer-files)
* [https://www.digitalocean.com/community/questions/how-do-i-copy-files-from-my-droplet-to-my-pc-for-backup](https://www.digitalocean.com/community/questions/how-do-i-copy-files-from-my-droplet-to-my-pc-for-backup)
* [https://docs.digitalocean.com/products/paperspace/machines/how-to/transfer-files/](https://docs.digitalocean.com/products/paperspace/machines/how-to/transfer-files/)

[1]: https://www.digitalocean.com/community/questions/how-do-i-copy-files-from-my-droplet-to-my-pc-for-backup?utm_source=chatgpt.com "How do I copy files from my droplet to my PC for backup | DigitalOcean"
[2]: https://docs.digitalocean.com/products/volumes/how-to/move-between-droplets/?utm_source=chatgpt.com "How to Move Volumes between Droplets | DigitalOcean Documentation"
[3]: https://www.digitalocean.com/community/questions/how-to-transfer-one-droplet-all-data-to-another-droplet?utm_source=chatgpt.com "how to transfer one droplet all data to another droplet | DigitalOcean"
