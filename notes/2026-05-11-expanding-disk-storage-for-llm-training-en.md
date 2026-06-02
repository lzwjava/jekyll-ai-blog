---
audio: false
generated: true
image: false
lang: en
layout: post
title: Expanding Disk Storage for LLM Training
translated: false
type: note
---

Question: My current Linux machine has only 1.7 GB of disk space left on a 916 GB NVMe drive (100% full). I'm doing LLM training and need to store large datasets like FineWeb and GPT-3 scale data (~400 GB). How do I upgrade/expand the disk storage?

Answer:

## Context: Your Current Situation

```
Filesystem      Size  Used Avail Use%
/dev/nvme0n1p2  916G  868G  1.7G 100%   ← basically full
```

Your new PC build (from the parts list you shared) includes:
- **Samsung 980 SSD 1TB** (PCIe 3.0 NVMe) — your current boot drive (this is the one that's full)
- **WD Blue 2TB HDD** — also in the build (7200 RPM SATA)

You actually **already have the solution in your PC**: the **2TB WD HDD** is your expansion drive. But you may not have it mounted and set up yet.

---

## Strategy Options (Best to Simplest)

### Option A: Use the 2TB HDD (Already in Your Build) — Recommended for Training Data

This is the easiest and most practical path. Training datasets (FineWeb, etc.) are **read sequentially**, so HDD speed is acceptable for data storage/preprocessing, even if not ideal.

**Step 1 — Identify the new disk:**
```bash
lsblk
# or
sudo fdisk -l
```
Look for a device like `/dev/sdb` or `/dev/sda` that is ~2TB and unpartitioned.

**Step 2 — Partition it:**
```bash
sudo fdisk /dev/sdb
# Inside fdisk:
# n  → new partition
# p  → primary
# 1  → partition number
# (press Enter twice to use full disk)
# w  → write and exit
```

**Step 3 — Format as ext4:**
```bash
sudo mkfs.ext4 /dev/sdb1
```

**Step 4 — Create mount point and mount:**
```bash
sudo mkdir -p /data/llm
sudo mount /dev/sdb1 /data/llm
```

**Step 5 — Make it permanent (auto-mount on boot):**
```bash
# Get the UUID
sudo blkid /dev/sdb1

# Edit fstab
sudo nano /etc/fstab
# Add this line (replace UUID with your actual value):
UUID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx  /data/llm  ext4  defaults  0  2
```

**Step 6 — Set permissions so your user can write:**
```bash
sudo chown -R $USER:$USER /data/llm
```

**Verify:**
```bash
df -h /data/llm
# Should show ~1.8TB available
```

Now download your datasets there:
```bash
# Example: HuggingFace datasets
huggingface-cli download HuggingFaceFW/fineweb --repo-type dataset --local-dir /data/llm/fineweb
```

---

### Option B: Add a Second NVMe SSD (Better for Active Training I/O)

The **MSI MAG B760M Mortar** motherboard you chose has **two M.2 slots**, so you can physically add another NVMe SSD (e.g., a 2TB PCIe 4.0 drive). This gives much better read speeds (~5000 MB/s vs ~150 MB/s HDD) which matters during tokenization and DataLoader I/O.

Steps are identical to Option A after physical install — it will appear as `/dev/nvme1n1`.

---

### Option C: Immediate Relief — Clean Up the Existing NVMe

Before buying/mounting anything, reclaim space now:

```bash
# Find what's eating space
du -sh /* 2>/dev/null | sort -rh | head -20
du -sh /home/* 2>/dev/null | sort -rh
du -sh ~/.cache/* 2>/dev/null | sort -rh

# Common culprits in ML workloads:
# HuggingFace cache
du -sh ~/.cache/huggingface/

# Conda/pip cache
conda clean --all
pip cache purge

# Docker images (if using)
docker system prune -a

# Old model checkpoints
find ~ -name "*.ckpt" -o -name "*.pt" | du -sh
```

---

### Option D: Symlink Cache to the New Drive (Transparent Integration)

After mounting `/data/llm`, redirect HuggingFace's cache there seamlessly:

```bash
# Move existing HF cache to new drive
mv ~/.cache/huggingface /data/llm/hf_cache

# Symlink so tools don't notice
ln -s /data/llm/hf_cache ~/.cache/huggingface

# Or just set the env var in ~/.bashrc:
echo 'export HF_HOME=/data/llm/hf_cache' >> ~/.bashrc
echo 'export TRANSFORMERS_CACHE=/data/llm/hf_cache' >> ~/.bashrc
source ~/.bashrc
```

---

## Storage Sizing Reality Check for LLM Training Data

| Dataset | Approximate Size |
|---|---|
| FineWeb (sample-10BT) | ~10–25 GB |
| FineWeb (full) | ~44 TB (impractical locally) |
| The Pile | ~825 GB |
| OpenWebText | ~40 GB |
| GPT-3 training data equivalent | Several TB total |

**Practical recommendation**: For a local training setup, use **FineWeb sample subsets** or **OpenWebText**, stored on the 2TB HDD. The full FineWeb/GPT-3 scale data requires cloud/cluster storage.

---

## Summary: What to Do Right Now

1. `lsblk` — confirm the 2TB WD HDD appears (e.g., `/dev/sdb`)
2. Partition → format → mount it to `/data/llm`
3. Add to `/etc/fstab` so it persists across reboots
4. Set `HF_HOME=/data/llm/hf_cache` in your shell profile
5. Download datasets directly to `/data/llm/`

This gives you ~1.8 TB of usable training data space without touching your OS partition at all.

References:

- [Extending an ext4 filesystem on LVM without downtime](https://www.systutorials.com/extending-a-mounted-ext4-file-system-on-lvm-in-linux/)
- [Expand storage on Debian without LVM](https://blog.bogdancaraman.com/expand-storage-debian-no-lvm/)
- [How to add a second hard drive on Linux and increase storage pool](https://www.cyberciti.biz/faq/howto-add-disk-to-lvm-volume-on-linux-to-increase-size-of-pool/)
