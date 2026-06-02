---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cost-Efficient GPU Data Workflow
translated: false
type: note
---

Yes, exactly. That's a smart workflow separation.

## The Pattern

```
CPU Droplet (cheap, ~$0.015/hr)          GPU Droplet (expensive, ~$2/hr)
─────────────────────────────            ────────────────────────────────
Download raw text data
Tokenize (CPU-bound anyway)
Write train.bin, val.bin          ──►    Attach volume
Detach volume                            Mount /mnt/data
Destroy CPU droplet                      Train GPT
                                         Detach volume
                                         Destroy GPU droplet
```

## Why This Makes Perfect Sense

Tokenization with tiktoken is **pure CPU work** — no GPU needed at all:

```python
# This runs fine on a $0.015/hr CPU droplet
enc = tiktoken.get_encoding('gpt2')
ids = enc.encode_ordinary(text)  # CPU only
```

So instead of burning $2/hr GPU time on:

- `wget` downloading 80GB of text
- `prepare.py` tokenizing 30B tokens (takes hours)
- Waiting for data upload

You do all that on a cheap CPU droplet, then hand off the volume.

## Concrete Cost Saving

```
Data prep: ~6 hours work
On GPU droplet:  6hr × $2.00 = $12.00
On CPU droplet:  6hr × $0.015 = $0.09

Saving: ~$11.91 just for data prep
```

## Workflow Script

```bash
# Phase 1: CPU droplet — data prep
doctl compute droplet create data-prep \
  --image ubuntu-24-04-x64 \
  --size s-4vcpu-8gb \        # cheap, enough CPU/RAM
  --region atl1 \
  --ssh-keys <your-key-id>

# attach your volume
doctl compute volume-action attach <volume-id> <cpu-droplet-id> --wait

# SSH in, mount, prepare data
ssh root@<cpu-ip>
mount /dev/sda /mnt/data
cd /mnt/data
pip install tiktoken datasets
python prepare.py   # download + tokenize → writes train.bin, val.bin

# done — detach
umount /mnt/data
doctl compute volume-action detach <volume-id> <cpu-droplet-id> --wait
doctl compute droplet delete <cpu-droplet-id> --force

# Phase 2: GPU droplet — training
doctl compute droplet create amd-gpu \
  --image <your-gpu-snapshot-id> \
  --size <gpu-slug> \
  --region atl1 \
  --ssh-keys <your-key-id>

doctl compute volume-action attach <volume-id> <gpu-droplet-id> --wait

ssh root@<gpu-ip>
mount /dev/sda /mnt/data
ls /mnt/data   # train.bin, val.bin already there ✅
python train.py config/train_gpt3_1b.py
```

## One Important Constraint

**Volume and droplets must be in the same region.** Your volume is `ATL1` — so both CPU and GPU droplets must also be `ATL1`. You already have that since it's the AMD Dev Cloud region.

## Bottom Line

```
Your volume-atl1-1780280110689 (100GB) is already created ✅
Next: spin up cheap CPU droplet in ATL1
      attach volume
      download + tokenize data
      detach
      spin up GPU droplet in ATL1
      attach same volume
      train
```

You're thinking about this exactly right — CPU for data, GPU for compute, volume as the handoff mechanism.
