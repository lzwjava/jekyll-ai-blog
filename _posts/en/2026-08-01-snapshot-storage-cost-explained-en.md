---
audio: false
generated: true
image: false
lang: en
layout: post
title: Snapshot Storage Cost Explained
translated: false
type: note
---

Question: Why did AMD Developer Cloud / DigitalOcean charge $7.99 for a 133GB MI300X snapshot?

Answer:

This is **not GPU compute cost**. It is the cost of keeping a **Droplet Snapshot** stored.

Your bill:

```
Resource:
snapshots-gpu-mi300x1-192gb-devcloud-atl1-1780339218471

Size:
133.11 GB

Hours:
744 hours

Period:
07-01 00:00 → 08-01 00:00

Cost:
$7.99
```

The calculation:

DigitalOcean snapshot pricing is:

```
$0.06 / GB / month
```

([DigitalOcean][1])

So:

```
133.11 GB × $0.06 = $7.9866
```

≈

```
$7.99/month
```

Exactly matches your invoice.

The "744 hours" is just the billing period (~31 days × 24h). Snapshot storage is effectively monthly storage billing, not GPU runtime billing. ([DigitalOcean][1])

---

For your MI300X experiment:

You probably did something like:

```
AMD Developer Cloud MI300X VM
        |
        |
   create snapshot
        |
        |
   destroy GPU VM
        |
        |
   snapshot remains
```

The expensive GPU machine is gone, but the snapshot remains:

```
snapshot
 ├── Ubuntu image
 ├── ROCm
 ├── PyTorch
 ├── models
 ├── checkpoints
 └── your data

133GB
```

You are paying for this 133GB archive.

---

If you don't need it:

Go to:

```
DigitalOcean Console
 -> Images
 -> Snapshots
 -> snapshots-gpu-mi300x1-192gb-devcloud-atl1-1780339218471
 -> Destroy
```

Then future monthly charge becomes:

```
$0
```

---

For AI workloads, a better pattern:

### Keep only code + environment

Example:

```bash
# save environment
pip freeze > requirements.txt

# save docker
docker save my-rocm-env > rocm-env.tar

# upload model/checkpoints
rclone copy ./checkpoint s3://mybucket/checkpoint
```

Then delete snapshot.

For a MI300X experiment, 133GB snapshot is expensive because most of it is probably:

```
/home
 ├── huggingface cache
 │     ├── Qwen weights
 │     ├── datasets
 │
 ├── pytorch cache
 ├── docker layers
 └── checkpoints
```

Usually you only need:

```
git repo        < 1GB
configs         KB
checkpoint      depends
```

Store large models in:

* Hugging Face Hub
* S3 / R2
* cheap object storage

and recreate the machine.

For your kind of LLM infra experiments (ROCm, MI300X, vLLM, training), I would avoid long-lived snapshots. Keep a reproducible bootstrap script:

```bash
#!/bin/bash

apt install rocm
pip install torch vllm transformers

git clone your-repo

huggingface-cli download model-name
```

Then a fresh MI300X node can be rebuilt in ~10-30 minutes instead of paying $8/month forever.

References:

* DigitalOcean Snapshots Pricing ([DigitalOcean][1])
* DigitalOcean Droplet Pricing ([DigitalOcean][2])

[1]: https://docs.digitalocean.com/products/snapshots/details/?utm_source=chatgpt.com "Snapshots Details | DigitalOcean Documentation"
[2]: https://www.digitalocean.com/pricing/droplets?utm_source=chatgpt.com "Droplet Pricing | DigitalOcean"
