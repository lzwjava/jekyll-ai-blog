---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Google Cloud Storage IAM Roles
translated: false
type: note
---

Question: What roles can we configure in Google Cloud Storage? For example, Storage Object Viewer IAM role, etc.

Answer:

Google Cloud Storage uses **Identity and Access Management (IAM)** to control access to buckets and objects. You can assign both **predefined roles** (Google-managed) and **custom roles** at the project level, bucket level, or (for fine-grained access) object level.

Here are the main **predefined IAM roles** specific to Cloud Storage:

- **Storage Object Viewer** (`roles/storage.objectViewer`)
  Grants read-only access to objects and their metadata (excluding ACLs).
  Allows listing objects in a bucket (`storage.objects.list`) and reading object data/metadata (`storage.objects.get`).
  Does **not** allow viewing or listing buckets themselves.

- **Storage Object Creator** (`roles/storage.objectCreator`)
  Allows creating objects (`storage.objects.create`), but not reading, deleting, or overwriting existing objects.

- **Storage Object Admin** (`roles/storage.objectAdmin`)
  Full control over objects: create, list, get, delete, and update objects and their metadata (but not bucket-level configuration).

- **Storage Legacy Bucket Reader** (`roles/storage.legacyBucketReader`)
  Read-only access to bucket metadata and the ability to list objects.

- **Storage Legacy Bucket Writer** (`roles/storage.legacyBucketWriter`)
  Grants read + create/delete objects (legacy equivalent to object admin + some bucket permissions).

- **Storage Legacy Bucket Owner** (`roles/storage.legacyBucketOwner`)
  Full control over a bucket and its objects (legacy owner role).

- **Storage Admin** (`roles/storage.admin`)
  Full control over buckets and objects: create/delete buckets, manage IAM policies, configure lifecycle/rules, etc.

- **Storage Object Viewer** (already listed above — most commonly used for read-only object access)

Other commonly used broader roles that grant Cloud Storage permissions:

- **Viewer** (`roles/viewer`) — read-only access to most resources, including listing buckets/objects.
- **Editor** (`roles/editor`) — read/write access to most resources (includes most Storage permissions).
- **Owner** (`roles/owner`) — full control over the project, including all Storage resources.

**Key notes**:

- For most modern use cases, prefer the granular **object-level roles** (`objectViewer`, `objectCreator`, `objectAdmin`) rather than the legacy bucket roles.
- You can also create **custom roles** if the predefined ones don't fit your needs exactly (e.g., allow get + list but not metadata updates).
- Permissions can be granted at:
  - Project level (affects all buckets)
  - Bucket level (most common)
  - Individual object level (fine-grained access control)

For the most up-to-date and complete list (including exact permissions each role includes), refer to the official Google Cloud documentation.

References:

- [IAM roles for Cloud Storage](https://docs.cloud.google.com/storage/docs/access-control/iam-roles)
- [Cloud Storage roles and permissions](https://docs.cloud.google.com/iam/docs/roles-permissions/storage)
- [Identity and Access Management for Cloud Storage](https://docs.cloud.google.com/storage/docs/access-control/iam)
