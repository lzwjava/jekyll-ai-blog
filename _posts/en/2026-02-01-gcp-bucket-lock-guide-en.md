---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Google Cloud Bucket Lock Explained
translated: false
type: note
---

I'll search for the most current information about the Bucket Lock feature in Google Cloud.# Google Cloud Bucket Lock: A Comprehensive Introduction

Google Cloud's Bucket Lock is a powerful feature for Cloud Storage that allows you to enforce data retention policies and ensure regulatory compliance. Here's what you need to know:

## What is Bucket Lock?

Bucket Lock lets you configure a retention policy that governs how long objects in a bucket must be retained, and allows you to lock this policy to permanently prevent it from being reduced or removed. This creates immutable storage on Google Cloud Storage, which is particularly valuable for meeting regulatory requirements.

## Key Concepts

**Retention Policy**: When you set a retention policy on a bucket, objects in the bucket can only be deleted or replaced once their age is greater than the retention period. The policy applies retroactively to all existing objects and automatically covers any new objects added to the bucket.

**Locking the Policy**: This is where Bucket Lock gets serious. When you lock a retention policy, the action is **irreversible**. Once locked, you cannot remove the policy or reduce the retention period. You can only increase the retention period if needed.

## How It Works

Every object in a bucket with a retention policy has a retention expiration date in its metadata. The bucket's retention policy also includes an effective time, after which all objects are guaranteed to comply with the retention period.

Before locking, you can freely modify or remove the retention policy. After locking, your only option to "remove" the policy is to wait until every object has fulfilled its retention period, then delete the entire bucket. You cannot delete a bucket with a locked policy if it contains any objects that haven't met their retention requirements.

## Regulatory Compliance

In conjunction with Detailed audit logging mode, Bucket Lock can help with regulatory and compliance requirements such as those associated with FINRA, SEC, and CFTC, and can help address certain health care industry retention regulations.

## Additional Protection Features

Beyond basic retention policies, Google Cloud Storage offers complementary features:

- **Temporary holds**: You can place a temporary hold on individual objects to prevent deletion until the hold is released
- **Event-based holds**: These delay the retention policy countdown until a specific event occurs (like when a loan is paid off), at which point the retention period begins

## Important Considerations

When you lock a retention policy, Cloud Storage automatically applies a lien to the projects.delete permission for the project containing the bucket, preventing the project from being deleted while the lien is in place.

Object metadata remains editable even when the object itself is protected by a retention policy. The policy also works with Object Versioning, protecting all versions of objects in the bucket.

## Bucket Lock vs Object Retention Lock

It's worth noting that Google Cloud also offers Object Retention Lock, which lets you define data retention requirements on a per-object basis, whereas Bucket Lock applies uniformly to all objects in a bucket.

Bucket Lock is ideal when you need consistent retention requirements across all data in a bucket, making it particularly well-suited for log buckets, financial records, or any scenario where uniform compliance requirements apply to an entire data set.
