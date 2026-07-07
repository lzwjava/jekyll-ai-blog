---
audio: false
generated: true
image: false
lang: en
layout: post
title: RunPod Network Volume S3 Access
translated: false
type: note
---

Question: Is RunPod network volume storage using S3?

Answer: **Yes, but with an important distinction.** RunPod Network Volumes are **not literally AWS S3 buckets**, but RunPod provides an **S3-compatible API layer** to access them.

Your volume:

```
Name: pleasant_apricot_swift
Size: 30 GB
Data center: EU-RO-1
S3 API access: Enabled
```

means:

* The actual storage is a **RunPod Network Volume**.
* You can mount it normally inside pods (for example `/workspace`).
* You can also access it externally through an **S3-compatible endpoint** using tools like:

  * `aws s3`
  * `s3cmd`
  * `rclone`
  * Python SDKs (`boto3`)

The model is roughly:

```
                 +----------------+
                 | RunPod Pod     |
                 |                |
                 | /workspace     |
                 +-------+--------+
                         |
                         |
                 RunPod Network Volume
                         |
                         |
              +----------+----------+
              |                     |
        POSIX mount             S3 API
        (filesystem)            (object API)
              |                     |
        Linux commands        aws/rclone/boto3
        cp/rsync             upload/download
```

Example inside a pod:

```bash
ls /workspace
cp model.gguf /workspace/models/
```

Example through S3 API:

```bash
aws configure
```

Set:

```
AWS_ACCESS_KEY_ID=<RUNPOD_ACCESS_KEY>
AWS_SECRET_ACCESS_KEY=<RUNPOD_SECRET>
```

Then:

```bash
aws s3 ls \
  --endpoint-url https://<runpod-s3-endpoint>
```

or:

```bash
aws s3 cp model.gguf \
  s3://<volume-name>/models/
```

The S3 interface is useful for:

* uploading large models before starting pods
* moving datasets between machines
* backups
* automation pipelines

For AI workloads, the common pattern is:

```
Network Volume
      |
      +-- models/
      |     llama/
      |     qwen/
      |     gemma/
      |
      +-- datasets/
      |
      +-- checkpoints/
      |
      +-- cache/
            huggingface/
            torch/
```

Then every new GPU pod in the same RunPod region can attach this volume and immediately reuse the data.

One important limitation: **Network Volumes are region-specific.** Your volume is:

```
EU-RO-1
```

so you generally attach it to pods in the same data center/region. It is not like global S3 storage replicated worldwide.

For LLM serving (SGLang/vLLM), this is actually the preferred setup: keep models on the network volume, spin up GPU pods, mount the volume, start the server.
