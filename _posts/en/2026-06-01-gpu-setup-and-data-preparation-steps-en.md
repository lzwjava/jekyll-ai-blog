---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPU Setup and Data Preparation Steps
translated: false
type: note
---

Done. Status:

```
GPU Droplet:  OFF    (574422820 — billing paused)
Volume:       DETACHED  (100 GiB, 37G used by llama-models)
```

**Next steps when you're ready to prepare data:**

```bash
# 1. Create cheap CPU droplet in atl1 (~$4-6/mo)
doctl compute droplet create data-prep \
  --size s-2vcpu-4gb \
  --region atl1 \
  --image ubuntu-24-04-x64 \
  --ssh-keys <your-key-fingerprint>

# 2. Attach volume to it
doctl compute volume-action attach 52743aec-... <new-droplet-id>

# 3. SSH in, mount, download dataset, tokenize, dedup
# 4. When done: detach volume, destroy CPU droplet
# 5. Power on GPU droplet, attach volume, train
```

Want me to create the CPU droplet now, or do you want to decide on the dataset first?
