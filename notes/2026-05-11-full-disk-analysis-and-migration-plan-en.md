---
audio: false
generated: true
image: false
lang: en
layout: post
title: Full Disk Analysis and Migration Plan
translated: false
type: note
---

Got the whole picture. **Analysis only — nothing changed.**

## The disk

| Device                   | Size    | State                                                          |
| ------------------------ | ------- | -------------------------------------------------------------- |
| `nvme0n1` (Samsung 980)  | 931 GB  | Boot/root, 100% full (868 GB used)                             |
| `sda` (WD Blue 2 TB HDD) | 1.82 TB | **Empty, no partition table, not mounted** ← your escape hatch |

The HDD is physically installed and visible. It just needs partitioning + formatting + mounting. The blog-recommendation guide you pasted is correct on the steps — `/dev/sdb` in that guide is `/dev/sda` on this machine.

## Where the 868 GB went

Top consumers, in priority order:

| Path                                       | Size       | What it is                                                         | Verdict                                         |
| ------------------------------------------ | ---------- | ------------------------------------------------------------------ | ----------------------------------------------- |
| `~/projects/blog-source/fineweb_test_dump` | **88 GB**  | A previous FineWeb experiment dump                                 | likely **dead weight** — confirm then delete    |
| `~/.cache/huggingface`                     | **69 GB**  | HF dataset/model cache                                             | **move to HDD**, set `HF_HOME`                  |
| `~/projects/zz/datasets`                   | **72 GB**  | Current run's fineweb-edu (in progress)                            | **move to HDD** without losing progress         |
| `~/projects/llama.cpp`                     | 73 GB      | Almost certainly model files inside                                | **move to HDD**                                 |
| `~/projects/imagenet`                      | 64 GB      | Dataset                                                            | **move to HDD**                                 |
| `/var/lib/docker`                          | **43 GB**  | Docker images/volumes                                              | `docker system prune -a` if you don't need them |
| `~/projects/coco`                          | 38 GB      | Dataset                                                            | **move to HDD**                                 |
| `~/projects/llama`                         | 31 GB      | Model weights                                                      | **move to HDD**                                 |
| `~/projects/nanoGPT`, `llama2.c`           | 26 GB each | Datasets/weights inside                                            | **move to HDD**                                 |
| `~/qDownloads`                             | 14 GB      | qBittorrent movies (Friends, Dune, Oppenheimer, Leon, Linkin Park) | delete what you've watched                      |
| `~/.cache/pip`                             | 13 GB      | pip wheel cache                                                    | safe to `pip cache purge`                       |
| `~/projects/blog-source/.venv`             | 7.6 GB     | One project's venv                                                 | rebuildable                                     |
| `~/.ollama`                                | 8.4 GB     | Ollama models                                                      | move or delete                                  |

That's > 400 GB of clearly-relocatable data, all of which is just sitting on the wrong disk.

## What to do — the plan (you run, I don't touch anything)

### Step 1 — Set up the HDD (one-time, ~5 minutes)

```bash
# 1. Partition the whole disk as GPT, single ext4 partition
sudo parted /dev/sda --script mklabel gpt mkpart primary ext4 0% 100%

# 2. Format
sudo mkfs.ext4 -L data /dev/sda1

# 3. Mount point under your home so paths are short
sudo mkdir -p /mnt/data
sudo mount /dev/sda1 /mnt/data
sudo chown $USER:$USER /mnt/data

# 4. Make it persistent
echo "UUID=$(sudo blkid -s UUID -o value /dev/sda1)  /mnt/data  ext4  defaults,noatime  0  2" | sudo tee -a /etc/fstab

# 5. Verify
df -h /mnt/data    # should show ~1.8 TB available
```

> Why `parted` over `fdisk`: scriptable in one line, GPT-by-default (matters for >2 TB and modern systems), no interactive prompts.
> Why `noatime`: skips per-read timestamp writes — small win for dataset reads.

### Step 2 — Move the FineWeb download in-place (zero progress loss)

```bash
# stop the downloader if it's running
mkdir -p /mnt/data/datasets
mv ~/projects/zz/datasets/fineweb-edu /mnt/data/datasets/
ln -s /mnt/data/datasets/fineweb-edu ~/projects/zz/datasets/fineweb-edu
```

The script will resume from `progress.json` and the symlink is invisible to it. **Don't change `TARGET_TOKENS`** — you have 1.8 TB now.

### Step 3 — Redirect HuggingFace cache (one line in `.bashrc`)

```bash
mkdir -p /mnt/data/hf_cache
mv ~/.cache/huggingface/* /mnt/data/hf_cache/ 2>/dev/null
rmdir ~/.cache/huggingface
ln -s /mnt/data/hf_cache ~/.cache/huggingface
# and so it survives a fresh ~/.cache
echo 'export HF_HOME=/mnt/data/hf_cache' >> ~/.bashrc
```

I prefer the symlink **and** the env var — the symlink covers tools that hard-code `~/.cache/huggingface`, the env var covers tools that read `HF_HOME`.

### Step 4 — Move the other big project dirs

```bash
mkdir -p /mnt/data/projects
for d in llama.cpp llama imagenet coco nanoGPT llama2.c stable-diffusion-webui; do
  mv ~/projects/$d /mnt/data/projects/
  ln -s /mnt/data/projects/$d ~/projects/$d
done
```

### Step 5 — Investigate and clean (decide before deleting)

```bash
# Probably stale, check before nuking:
ls -la ~/projects/blog-source/fineweb_test_dump   # 88 GB — is this still needed?

# Safe one-liners:
pip cache purge                                   # frees ~13 GB
docker system prune -a --volumes                  # frees up to 43 GB (only if you don't need those images)
sudo journalctl --vacuum-size=500M                # trims old systemd logs
```

For `~/qDownloads`: those are clearly movies — `Dune Part Two`, `Oppenheimer`, `Leon`, `Friends S1`, `Linkin Park - Meteora`. Total ~14 GB. Delete whatever you've watched. (If qBittorrent is still seeding any of them, remove from the qBit UI first so it doesn't try to recreate the file.)

## Two clarifications on the recommendation guide

A couple of things in the answer you pasted aren't quite right for **this** machine:

- It says `/dev/sdb` — on your box the HDD is `/dev/sda` (the only SATA disk; NVMe boot drive is on the M.2 bus, separate).
- It says "FineWeb full is ~44 TB, impractical locally" — yes, but your **400 GB** target is the `fineweb-edu` subset and that absolutely fits on the new 1.8 TB drive. Don't downsize the training run on a storage argument; the HDD solves it.

## What I'd do first

Order of operations:

1. Partition + mount the HDD (Step 1) — gets you 1.8 TB headroom immediately.
2. Move `~/projects/zz/datasets/fineweb-edu` via symlink (Step 2) — unblocks the running download.
3. Move HF cache (Step 3) — frees 69 GB on NVMe.
4. Look at `blog-source/fineweb_test_dump` (Step 5) — 88 GB that's probably deletable.
5. Move the rest of `~/projects/*` (Step 4) at your leisure — these are datasets/weights, fine on a HDD for read-mostly workloads.

After steps 1–4 your NVMe will be at ~50% used and you'll have ~1.6 TB free on the HDD for future datasets. No physical hardware change needed — everything is already there.

Want me to write a single script that does Steps 1–3 atomically, or would you rather run each line by hand?
