---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Google Cloud Hierarchy Root Node
translated: false
type: note
---

Question: Which Google Cloud resource hierarchy level is the root node where billing is attached and Organization Policies are typically enforced? A) Folder B) Project C) Organization D) Resource

Answer:

**The correct answer is C) Organization.**

In Google Cloud Platform (GCP), the resource hierarchy is structured as follows (from top to bottom):

- **Organization** → the root node (only exists if you have a Google Workspace or Cloud Identity account linked)
- **Folders** → optional grouping layer under the organization
- **Projects** → the main level where most resources live
- **Resources** → individual services (VMs, buckets, databases, etc.)

Key characteristics of the **Organization** level:

- It is the **root node** of the hierarchy.
- **Billing** is attached at the Organization level (via a Billing Account linked to the Organization).
- **Organization Policies** (Org Policies) are most commonly and effectively enforced at the Organization level, as this applies the constraints to all folders, projects, and resources underneath it (unless overridden lower down).
- Most central governance, security, and compliance controls are applied here.

Why the other options are incorrect:

- **A) Folder**: Optional grouping layer; can have policies, but it is not the root and billing is not attached here.
- **B) Project**: Contains actual resources and can have its own billing (in older setups), but in modern organizations, billing is centralized at the Organization level. Projects are not the root.
- **D) Resource**: Lowest level (individual services); neither billing nor organization policies are attached here.

So the root node where billing is attached and where Organization Policies are typically enforced is the **Organization**.

References:

- [Google Cloud Resource Hierarchy Documentation](https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy)
- [Organization Policy Overview](https://cloud.google.com/resource-manager/docs/organization-policy/overview)
