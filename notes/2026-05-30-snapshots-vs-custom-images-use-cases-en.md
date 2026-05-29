---
audio: false
generated: true
image: false
lang: en
layout: post
title: Snapshots vs Custom Images Use Cases
translated: false
type: note
---

Question: Why do people use snapshots instead of custom images, or vice versa, in DigitalOcean or AMD Developer Cloud?

Answer:

The choice between **snapshots** and **custom images** depends on purpose, flexibility, cost, and workflow. Here's a breakdown:

### 1. **Snapshots**

* **Definition:** A snapshot is a point-in-time copy of an existing Droplet (VM) or volume.
* **Use Case:** Ideal for backups, quick rollback, or short-term cloning.
* **Pros:**

  * Fast to create directly from an existing Droplet.
  * Useful for disaster recovery or incremental updates.
  * Can capture the current running state, including data changes.
* **Cons:**

  * Usually tied to the specific cloud provider.
  * Less flexible for sharing or reusing across projects or accounts.
  * Cost accumulates if you keep many snapshots.

### 2. **Custom Images**

* **Definition:** A custom image is a reusable OS or application environment uploaded or created for repeated deployment.
* **Use Case:** Ideal for standardizing environments across multiple Droplets or teams.
* **Pros:**

  * Portable between projects or sometimes even between providers.
  * Great for scaling: deploy multiple Droplets with the exact same setup.
  * Can be created from snapshots, ISO, or other sources.
* **Cons:**

  * Slightly more setup overhead initially.
  * Does not automatically include incremental updates—you’d need to update the custom image manually.

### 3. **Decision Factors**

* **Temporary vs Permanent:** Snapshots are for quick backup or replication; custom images are for long-term, reusable templates.
* **Frequency of Deployment:** If deploying one Droplet once, snapshots are simpler. For repeated deployments, custom images are better.
* **Portability Needs:** Custom images can be exported/imported across regions or providers more easily than snapshots.
* **Cost Sensitivity:** Snapshots are billed based on storage size and frequency. Custom images may have similar costs but provide efficiency in large-scale deployment.

**Example Scenario:**

* You make changes on a Droplet and want to save the current state → take a **snapshot**.
* You develop a standard stack for multiple projects → save it as a **custom image** for repeated deployments.

In short: snapshots = **state capture**, custom images = **reusable templates**. Often, teams use snapshots **to create custom images**, combining both advantages.

References:

* [DigitalOcean Snapshots](https://www.digitalocean.com/docs/images/snapshots/)
* [DigitalOcean Custom Images](https://www.digitalocean.com/docs/images/custom-images/)
* [AMD Developer Cloud Images](https://developer.amd.com/devcloud/)