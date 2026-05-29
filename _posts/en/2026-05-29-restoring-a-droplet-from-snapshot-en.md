---
audio: false
generated: true
image: false
lang: en
layout: post
title: Restoring a Droplet from Snapshot
translated: false
type: note
---

**Question:** What does "restore droplet" mean?

**Answer:**

"Restore droplet" means restoring a Droplet to an older point in time using a snapshot, which can be useful for restoring files that were accidentally deleted or to revert to a known-good Droplet to recover from accidental configuration changes.

**Key differences:**

| Operation | What happens | When to use |
|-----------|-------------|-----------|
| **Restore Droplet** | Replace the running Droplet entirely with its previous state from a backup/snapshot. The Droplet turns off during restoration and turns back on automatically. | You made a mistake and want to undo everything since the snapshot |
| **Create Droplet** | Spin up a *new* separate Droplet from a snapshot | You want a copy of an old state without losing current state |

**⚠️ Critical caveat:**

You currently cannot undo restoring a Droplet from a backup. Once you restore, everything after that snapshot is gone. So if you restore to a snapshot from yesterday, any work you did today is permanently lost.

**For your AMD DevCloud workflow:**

You'd use restore only if:
- You accidentally broke ROCm/PyTorch setup and want to go back
- You want to revert a bad config change

Normally you'd just destroy the droplet (stop paying) and create a fresh one from your snapshot later. That's cleaner because you keep your current state intact.

---

References:

- [DigitalOcean Create/Restore from Snapshots](https://docs.digitalocean.com/products/snapshots/how-to/create-and-restore-droplets/)
- [DigitalOcean Restore from Backup](https://docs.digitalocean.com/products/backups/how-to/create-and-restore/)