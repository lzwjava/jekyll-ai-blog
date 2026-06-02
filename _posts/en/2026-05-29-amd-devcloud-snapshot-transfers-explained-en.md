---
audio: false
generated: true
image: false
lang: en
layout: post
title: AMD DevCloud Snapshot Transfers Explained
translated: false
type: note
---

**Question:** What does "transfer snapshot" mean in AMD DevCloud, and what's the relationship to DigitalOcean?

**Answer:**

AMD Developer Cloud runs on DigitalOcean—devcloud.amd.com redirects to DigitalOcean, which hosts the GPU Droplets. So the snapshot interface you're seeing is powered by DigitalOcean's infrastructure.

**Transfer Snapshot** has two meanings in DigitalOcean (which powers AMD DevCloud):

1. **Transfer to another team/user**: Move a Droplet snapshot to a different DigitalOcean team, or transfer it to another user by email. When you transfer a snapshot, it is removed from its original team. Useful if you're sharing a configured environment or migrating ownership.

2. **Migrate to another region**: Transfer the snapshot into another region to subsequently create a new droplet in a different datacenter. This is how you move your MI300X droplet across DigitalOcean's geographic regions.

**What snapshots do for you:**

Snapshots let you restore the exact state of your droplet without re-running setup, though they incur a small storage cost. In your workflow: snapshot after you've got ROCm, PyTorch, and your models/datasets configured. Then you can destroy the droplet to stop paying, and later spin up a fresh droplet from that snapshot in ~2 minutes—all your setup is preserved.

**Practical workflow:**

```bash
# 1. Configure your MI300X droplet, train models, etc.
# 2. AMD DevCloud UI → Snapshots → Take Snapshot
# 3. Destroy droplet (stops hourly charges)
# 4. Later: Create new droplet from snapshot → instant resume
```

The snapshot transfer feature is mainly useful if you want to give someone else access to your configured environment, or migrate between regions—less common for individual development but important for team workflows.

---

References:

- [AMD Developer Cloud on DigitalOcean Architecture](https://www.phoronix.com/review/amd-developer-cloud)
- [DigitalOcean Transfer Snapshot Documentation](https://docs.digitalocean.com/products/snapshots/how-to/transfer/)
- [DigitalOcean Snapshot Migration Guide](https://docs.digitalocean.com/products/snapshots/how-to/migrate-droplets/)
