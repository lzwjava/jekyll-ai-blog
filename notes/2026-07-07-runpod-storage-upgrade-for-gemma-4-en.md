---
audio: false
generated: true
image: false
lang: en
layout: post
title: RunPod Storage Upgrade for Gemma 4
translated: false
type: note
---

Question: How to upgrade RunPod storage quota so Gemma 4 26B A4B AWQ can fit?

Answer:

Your `/workspace` is likely a **RunPod Network Volume** with a small size (around 10GB). You need to increase the **Network Volume size**, not the pod GPU/container disk. RunPod supports increasing a network volume size later, but **you cannot decrease it afterward**. ([Runpod Documentation][1])

## Option A — RunPod Web UI (recommended)

1. Open RunPod dashboard:

   * Go to **Storage**
   * Find your Network Volume

2. Edit the volume:

   * Increase size from:

     ```
     10 GB
     ```

     to something like:

     ```
     50 GB
     ```

3. Restart/reconnect your Pod.

RunPod's docs say network volume size can be increased later, but not reduced. ([Runpod Documentation][1])

For your case I would choose:

```
Gemma 4 26B A4B AWQ
~20 GB model

+ tokenizer
+ SGLang cache
+ LibreChat
+ logs

minimum:
40 GB

comfortable:
50 GB
```

---

## Option B — API

RunPod exposes an update endpoint:

```bash
curl --request POST \
  --url https://rest.runpod.io/v1/networkvolumes/<NETWORK_VOLUME_ID>/update \
  --header "Authorization: Bearer <RUNPOD_API_KEY>" \
  --header "Content-Type: application/json" \
  --data '
{
  "size": 50
}
'
```

The new size must be larger than the current size. ([Runpod Documentation][2])

---

## Check current volume

Inside pod:

```bash
df -h /workspace
```

You probably see something like:

```
Filesystem      Size Used Avail
moosefs         10G  10G     0
```

After resize:

```
Filesystem      Size Used Avail
moosefs          50G  10G    40G
```

---

## Important: don't confuse these three storages

RunPod has:

```
Container Disk
    |
    | temporary
    | deleted when pod removed


Volume Disk
    |
    | pod-local


Network Volume (/workspace)
    |
    | persistent
    | model storage
```

For LLM serving, you want Network Volume. ([Runpod Documentation][1])

---

## My recommendation for your setup

Since you are building:

```
SGLang
   |
   |
LibreChat
   |
   |
local LLM API
```

I would upgrade once:

```
10GB  ❌
50GB  ✅
100GB ⭐
```

50GB is enough for:

```
Gemma4-26B-A4B-AWQ     20GB
Qwen2.5-14B-AWQ         8GB
embeddings              1-2GB
LibreChat               2GB
cache                   5GB
```

Then you can swap models without fighting storage every time. ([Runpod Documentation][1])

References:

* RunPod Network Volumes documentation ([Runpod Documentation][1])
* RunPod Network Volume update API ([Runpod Documentation][2])

[1]: https://docs.runpod.io/storage/network-volumes?utm_source=chatgpt.com "Network volumes - Runpod Documentation"
[2]: https://docs.runpod.io/api-reference/network-volumes/POST/networkvolumes/networkVolumeId/update?utm_source=chatgpt.com "Update a network volume - Runpod Documentation"
