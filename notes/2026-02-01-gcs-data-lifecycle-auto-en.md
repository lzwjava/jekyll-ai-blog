---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Automate GCS Data with Lifecycle Rules
translated: false
type: note
---

Lifecycle management policies in Google Cloud help you automatically manage your data by transitioning objects between storage classes or deleting them based on conditions you define. This is primarily used with **Google Cloud Storage (GCS)** to optimize costs and maintain data hygiene.

## Key Concepts

**Object Lifecycle Management** allows you to set rules that automatically perform actions on objects when certain conditions are met. The two main actions are:

- **Delete** - Remove objects permanently
- **SetStorageClass** - Transition objects to different storage classes (like moving from Standard to Nearline, Coldline, or Archive)

## Common Use Cases

You might use lifecycle policies to:

- Delete old log files after 90 days
- Move infrequently accessed data to cheaper storage classes after 30 days
- Remove incomplete multipart uploads after 7 days
- Archive data older than 1 year to the Archive storage class

## How Conditions Work

Lifecycle rules are triggered based on conditions like:

- **Age** - Number of days since object creation
- **CreatedBefore** - Specific date
- **IsLive** - Whether it's the current version (for versioned buckets)
- **MatchesStorageClass** - Current storage class
- **NumberOfNewerVersions** - For version control
- **DaysSinceNoncurrentTime** - For non-current versions

## Basic Example

A simple lifecycle policy might look like this in JSON:

```json
{
  "lifecycle": {
    "rule": [
      {
        "action": {"type": "Delete"},
        "condition": {"age": 365}
      }
    ]
  }
}
```

This deletes objects older than 365 days.

Lifecycle policies are evaluated once per day, and changes typically take effect within 24 hours. They're a powerful way to automate storage management and reduce costs without manual intervention.

Would you like to know more about setting up specific policies or best practices for different scenarios?