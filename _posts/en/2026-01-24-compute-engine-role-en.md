---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Compute Engine Instance Creation Role
translated: false
type: note
---

Question: What is the recommended way to grant a user the ability to create Compute Engine instances in a specific project without giving them broader permissions? A) roles/compute.instanceAdmin B) roles/compute.instanceAdmin.v1 C) roles/editor D) roles/owner

Answer:

The correct and **recommended** answer is **A) roles/compute.instanceAdmin**.

### Explanation

- **roles/compute.instanceAdmin**
  This is the standard, most commonly recommended predefined IAM role for managing Compute Engine instances. It includes permissions to:
  - Create, start, stop, delete, and update instances
  - Attach/detach disks
  - Set machine type, labels, metadata, etc.
  - Perform most day-to-day instance management tasks

  It is intentionally narrower than `roles/editor` or `roles/owner` and is the preferred choice when you want to allow instance creation and management **without** granting broad permissions across other Google Cloud services.

- **roles/compute.instanceAdmin.v1**
  This role exists mainly for **backward compatibility**.
  Google recommends using `roles/compute.instanceAdmin` (without .v1) for all new setups.
  The `.v1` suffix was used in earlier versions of the role, but the non-suffixed version is now the current, preferred role.

- **roles/editor**
  Grants very broad permissions — allows creating and managing almost all resources in the project (Cloud Storage, BigQuery, Cloud Functions, networking, etc.).
  This is **not** a least-privilege approach.

- **roles/owner**
  Full control over the project, including billing and IAM policy changes.
  This violates the principle of least privilege even more severely.

### Summary – Best Practice (2025/2026)

Use **roles/compute.instanceAdmin** when you want to let someone create and fully manage Compute Engine instances in a project while following least-privilege principles.

Correct answer: **A**

References:

- [https://cloud.google.com/compute/docs/access/iam](https://cloud.google.com/compute/docs/access/iam)
- [https://cloud.google.com/iam/docs/understanding-roles#compute-engine-roles](https://cloud.google.com/iam/docs/understanding-roles#compute-engine-roles)
