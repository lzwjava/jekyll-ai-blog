---
audio: false
generated: true
image: false
lang: en
layout: post
title: Recovering from a Full Disk
translated: false
type: note
---

## How I got here

I was downloading **FineWeb-Edu** for a small-scale GPT-3 ablation — ~176 parquet shards, ~400 GB total target, via `scripts/download/plan_and_download_fineweb_gpt3.py`. The script is resumable: shard state lives in `progress.json`, and partial downloads use HTTP Range so a Ctrl-C resumes byte-accurately from `.part`.

At **shard 33** (`CC-MAIN-2014-10/train-00004`) the download started failing:

```
[34/176] data__CC-MAIN-2014-10__train-00005-of-00014.parquet
  attempt 1/3 failed: [Errno 28] No space left on device
  attempt 2/3 failed: [Errno 28] No space left on device
  attempt 3/3 failed: [Errno 28] No space left on device
RuntimeError: giving up on ...
```

The disk was **completely full**. Not "running low" — Claude Code itself couldn't start a bash subprocess because the harness needs to `mkdir` a session-env directory and there were literally zero bytes free.

## The diagnosis

Once I freed a sliver of space (deleting the dead `.part` file from the crashed shard — safe because `progress.json` still marks it `pending`, so no real progress was lost), I could finally run `df -h` and `lsblk`:

```
/dev/nvme0n1p2  916G  868G  1.7G 100% /      ← Samsung 980 boot drive, dying
sda             1.8T  empty, no partitions   ← WD Blue HDD, sitting unused
```

**The fix was sitting right there in the case.** The 2 TB WD Blue HDD was physically installed, kernel-visible as `/dev/sda`, but had no partition table — never been used.

The 868 GB on the NVMe broke down roughly:
- `~/projects/` — 518 GB (datasets, model weights, llama.cpp, imagenet, coco, …)
- `~/.cache/huggingface` — 69 GB
- `/var/lib/docker` — 43 GB
- `~/projects/blog-source/fineweb_test_dump` — 88 GB of stale experiment output
- The current FineWeb-Edu download — 72 GB so far

Way more than 400 GB of clearly-relocatable data.

## How I partitioned the HDD

GPT label, single ext4 partition spanning the whole disk — one scriptable line, no interactive `fdisk` prompts:

```bash
sudo parted /dev/sda --script mklabel gpt mkpart primary ext4 0% 100%
sudo partprobe /dev/sda
```

Why `parted` over `fdisk`: scriptable, GPT-by-default (matters for >2 TB and modern UEFI systems), no `n / p / 1 / Enter / Enter / w` dance.

`partprobe` tells the kernel to re-read the partition table without a reboot. Verified with `lsblk /dev/sda` — `sda1` showed up.

## How I formatted it

```bash
sudo mkfs.ext4 -L data /dev/sda1
```

Plain ext4, label `data` so I can reference it by `LABEL=data` if I ever want to. Took ~30 seconds because mke2fs uses `DISCARD` on the whole device first (which is a no-op on a spinning HDD but harmless).

## How I mounted it

```bash
sudo mkdir -p /mnt/data
sudo mount /dev/sda1 /mnt/data
sudo chown $USER:$USER /mnt/data
```

Mount point under `/mnt/data` — short path, system-level location (not buried in `/home`), and `chown` so I don't need `sudo` for every write.

## How I made it permanent

Without an fstab entry, the mount is gone on next reboot. By **UUID** (not by device name — `/dev/sda` can shift if you add disks later):

```bash
UUID=$(sudo blkid -s UUID -o value /dev/sda1)
echo "UUID=$UUID  /mnt/data  ext4  defaults,noatime  0  2" | sudo tee -a /etc/fstab
sudo mount -a   # validates the line; errors here would block boot
```

`noatime` skips per-read timestamp writes — tiny win for dataset reads where every parquet file gets touched repeatedly during training. `mount -a` is **not optional** — it catches a typo *now*, when you can fix it, instead of at boot when the machine drops to emergency mode.

End state: 1.8 TB filesystem, 1.7 TB free, persistent across reboots.

## How I moved the in-progress download

The user wanted a **clean move**, not a symlink. The download script writes to `--output-dir` relative paths in `progress.json`, so as long as the relative tree is preserved and the working directory matches, it resumes transparently:

```bash
cd ~   # don't move the directory you're standing in
mv ~/projects/zz /mnt/data/zz
cd /mnt/data/zz
```

72 GB, NVMe → SATA HDD, ~150 MB/s sustained write = ~8 minutes. Cross-filesystem `mv` is actually a `cp` + `rm` under the hood, so the source NVMe space only frees at the very end.

Verified afterwards: 33 parquet shards intact, `progress.json` came along, `git status` still works (`.git` moved with the tree). The downloader can be re-run from `/mnt/data/zz` and will pick up at shard 34.

## What I tripped over

**The Claude harness pins its working directory at session start.** When I `mv`'d `~/projects/zz` to `/mnt/data/zz`, my own cwd vanished out from under me and every subsequent `Bash` call returned `Path "/home/lzw/projects/zz" does not exist` — even simple ones like `df -h`. The fix is to relaunch Claude Code from the new directory (`cd /mnt/data/zz && claude`). It's not a bug, just a consequence of how the session bootstraps. Worth knowing if you ever move a project mid-session.

## What I'd do differently next time

1. **Check `lsblk` *before* starting a multi-hundred-GB download**, not after. A 30-second check would have routed the download to `/mnt/data` from the start.
2. **Add a disk-space precheck to the downloader.** Trivial: before each shard, `shutil.disk_usage(output_dir).free` vs. expected shard size + margin; bail with a clear message instead of letting `urllib` `Errno 28` halfway through.
3. **Set `HF_HOME` once, globally**, in `~/.bashrc` or `~/.profile`, pointing at `/mnt/data/hf_cache` — so every HuggingFace tool on this machine writes there by default. That alone would have prevented `~/.cache/huggingface` swelling to 69 GB.
4. **Mount big data disks at install time, not at panic time.** A `/data` mount is the kind of thing that belongs in the initial machine setup checklist alongside `git config` and SSH keys.

## The pattern, distilled

```
sudo parted /dev/sdX --script mklabel gpt mkpart primary ext4 0% 100%
sudo mkfs.ext4 -L <label> /dev/sdX1
sudo mkdir -p /mnt/<name> && sudo mount /dev/sdX1 /mnt/<name>
sudo chown $USER:$USER /mnt/<name>
echo "UUID=$(sudo blkid -s UUID -o value /dev/sdX1)  /mnt/<name>  ext4  defaults,noatime  0  2" \
  | sudo tee -a /etc/fstab
sudo mount -a
```

Six commands. Done in five minutes. The hard part wasn't the Linux — it was noticing the spare 2 TB drive that was sitting there the whole time.
