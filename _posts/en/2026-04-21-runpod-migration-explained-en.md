---
audio: false
generated: true
image: false
lang: en
layout: post
title: RunPod Pod Migration Process Explained
translated: false
type: note
---

**Question:** What does it mean when RunPod says "Migration for notable_gray_pike is queued, and being compressed" — and what should I do when the original GPU (RTX 2000 Ada) is no longer available for my pod?

**Answer:**

## What Is Happening?

This is RunPod's **Pod Migration** feature in action. Here's what's going on under the hood:

When you start a pod, it's assigned to a specific physical machine. As long as your pod is running, that GPU is exclusively reserved for you. However, when you **stop** a pod, you release that specific GPU — allowing other users to rent it. If another user rents the GPU while your pod is stopped, the GPU will be occupied when you try to restart. Because your pod is still tied to that original machine, you'll see a message asking you to migrate.

So the message you're seeing — **"Migration queued and being compressed"** — means RunPod has automatically detected that your original RTX 2000 Ada GPU is no longer free on the physical machine your pod was tied to, and it is now **transferring your pod's data to a new machine** that has an available RTX 2000 Ada.

---

## What "Queued and Being Compressed" Means

The migration process goes through stages:
1. **Queued** — RunPod is finding a new machine with your requested GPU type (RTX 2000 Ada).
2. **Being Compressed** — Your pod's container/disk data is being compressed in preparation for transfer to the new machine.
3. After this, it will be **transferred and provisioned** on the new host.

The migration process finds a new machine with your requested GPU type, provisions the instance, and transfers your network volume data from the old pod to the new one. When the migration completes, you will receive a **new Pod ID and a new IP address**.

---

## Your Options

When prompted to migrate your pod, you have three options:

- **Do nothing:** Wait and try again later. The GPU will become available once another user stops their pod on that machine.
- **Start Pod with CPUs only:** Access your data with limited CPU resources, not suitable for compute-intensive tasks.
- **Automatically migrate Pod data:** This spins up a new pod with the same specifications and automatically migrates your data to a machine with available GPUs.

Since you're already seeing "queued and being compressed," it looks like **automatic migration is already in progress** — just wait for it to complete.

---

## After Migration Completes

- Your pod will have a **new Pod ID and new IP address** — update any SSH configs or scripts accordingly.
- All your `/workspace` data should be intact on the new machine.
- The GPU type (RTX 2000 Ada) will remain the same.

---

## How to Avoid This in the Future

The most effective way to avoid pod migrations is to use **Network Volumes**. Network volumes decouple your data from specific physical machines, storing your `/workspace` data on a separate, persistent volume that can be attached to any pod. If you need to terminate a pod, you can deploy a new one and attach the same network volume, giving you immediate access to your data on any machine with an available GPU.

---

**Summary:** Your situation is normal and expected — RunPod is migrating your pod to a new physical machine because someone else took your original RTX 2000 Ada GPU slot. Just wait for the migration to finish, then reconnect using the new IP/ID.

**References:**

- [RunPod Pod Migration Documentation](https://docs.runpod.io/references/troubleshooting/pod-migration)
