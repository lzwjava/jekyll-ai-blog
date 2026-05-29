---
audio: false
generated: true
image: false
lang: en
layout: post
title: Droplets vs Custom Images Explained
translated: false
type: note
---

Question: Why do people use Droplets instead of Custom Images, or vice versa, in DigitalOcean or AMD Developer Cloud?

Answer:

In platforms like [DigitalOcean](https://www.digitalocean.com?utm_source=chatgpt.com) or AMD Developer Cloud, **Droplets** and **Custom Images** solve different problems. They work together rather than replacing each other.

## What is a Droplet?

A **Droplet** is basically a running virtual machine (VM).

Think of it as:

* CPU
* RAM
* Disk
* Network
* Operating system
* Running processes/services

It is the actual compute instance you SSH into and run workloads on.

Examples:

* LLM inference server
* Kubernetes node
* Jupyter notebook
* Database server
* Web backend
* GPU training machine

In DigitalOcean terminology:

* Droplet = VM instance
* Snapshot/Custom Image = reusable VM template

---

## What is a Custom Image?

A **Custom Image** is like a saved template or frozen state of a machine.

It usually contains:

* OS
* Installed packages
* CUDA/ROCm
* Python environments
* Docker images
* SSH configs
* Model weights
* Your project setup

You use it to create new Droplets quickly.

Instead of:

```bash
apt install ...
pip install ...
git clone ...
docker pull ...
```

you boot from a prepared image and everything is already there.

---

# Why people use Droplets directly

Most people only need:

* 1 machine
* temporary testing
* experimentation
* simple workloads

So they just:

1. Create a Droplet
2. Configure it manually
3. Use it
4. Destroy it later

This is simpler and cheaper initially.

Especially for:

* hobby users
* students
* researchers
* short GPU sessions

On AMD Developer Cloud, many users:

* spin up MI300X
* test ROCm
* benchmark
* then terminate

No need for reusable images.

---

# Why people use Custom Images

Custom Images become useful when setup is expensive or repeated.

## Common reasons

### 1. Fast scaling

Suppose you spent:

* 2 days configuring ROCm
* optimized PyTorch
* inference stack
* monitoring
* datasets

You don't want to redo this every time.

So you create a custom image and instantly clone new machines.

This is common in:

* AI startups
* MLOps
* distributed inference
* Kubernetes worker pools

---

### 2. Consistency

Without images:

* one server has CUDA 12.1
* another has CUDA 12.4
* different Python libs
* different bugs

Custom images ensure:

* identical environment
* reproducible deployments
* fewer "works on my machine" problems

Very important in enterprises and banks like [HSBC](https://www.hsbc.com?utm_source=chatgpt.com).

---

### 3. Disaster recovery

If a server dies:

* recreate from image in minutes

Instead of rebuilding manually.

This matters for:

* production services
* GPU clusters
* CI/CD infrastructure

---

### 4. Cost optimization for time

Images cost storage money:

* $0.06/GiB/month in DigitalOcean

But engineers are expensive.

Example:

* 100 GB image = ~$6/month
* rebuilding environment manually may take 4–8 hours

So companies gladly pay storage cost.

---

# Why people avoid Custom Images

## 1. Storage costs

Large AI images become huge.

Typical ML image:

* Ubuntu
* ROCm/CUDA
* Docker
* Models
* Conda caches

Can easily become:

* 50 GB
* 100 GB
* 300 GB+

That becomes expensive across many snapshots.

---

## 2. Images become stale

You save an image today:

* packages outdated next month
* security patches missing
* old drivers
* incompatible libraries

Then maintaining images becomes operational work.

---

## 3. Infrastructure-as-Code became popular

Modern DevOps often prefers:

* Docker
* Terraform
* Ansible
* Kubernetes
* cloud-init

Instead of huge VM snapshots.

Reason:

* text configs are version-controlled
* easier to audit
* easier to reproduce

So many advanced teams now use:

* small base image
* automated provisioning scripts

instead of giant custom images.

---

# In AI/GPU workloads

Custom images are especially valuable because setup is painful.

Example on AMD MI300X:

* ROCm version compatibility
* PyTorch build
* kernel modules
* Flash Attention
* vLLM
* model cache

can take hours.

So AI engineers often:

1. Configure one perfect GPU VM
2. Snapshot it
3. Reuse everywhere

This is extremely common.

---

# Simple analogy

| Concept      | Real-world analogy             |
| ------------ | ------------------------------ |
| Droplet      | Running computer               |
| Custom Image | Backup disk / machine template |
| Snapshot     | Saved restore point            |
| Docker Image | App-level template             |
| Kubernetes   | Large-scale orchestration      |

---

# Your observation about AMD Developer Cloud quota is related

You noticed AMD limits users to small GPU quotas.

That changes behavior:

* users often treat GPU instances as temporary
* less need for persistent infrastructure
* more "ephemeral experimentation"

So users:

* create Droplet
* test
* destroy

rather than building large image pipelines.

But startups or advanced users often still create reusable images because GPU environment setup is expensive and fragile.

References:

* [https://www.digitalocean.com/products/droplets](https://www.digitalocean.com/products/droplets)
* [https://docs.digitalocean.com/products/images/custom-images/](https://docs.digitalocean.com/products/images/custom-images/)
* [https://www.amd.com/en/developer/resources/cloud-access.html](https://www.amd.com/en/developer/resources/cloud-access.html)