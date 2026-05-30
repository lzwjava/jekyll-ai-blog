---
audio: false
generated: true
image: false
lang: en
layout: post
title: AMD Developer Cloud Is White-Labeled DigitalOcean
translated: false
type: note
---

**Question:** How does AMD Developer Cloud work with DigitalOcean? Looking at this snapshot deletion script that uses `api.digitalocean.com`, it seems like only the web portal (UI) is different but the API endpoints and backend/database are the same — is that correct?

**Answer:**

Yes, your inference is correct. **AMD Developer Cloud is a white-labeled / OEM'd DigitalOcean deployment.** Here's the breakdown:

## What's Actually Happening

AMD Developer Cloud is built **on top of DigitalOcean's infrastructure platform**, with AMD-specific GPU hardware (MI300X etc.) added to DO's datacenter fleet. The relationship:

```
AMD Developer Cloud Portal (amd.com/en/developer/...)
        ↓  (just a themed frontend)
DigitalOcean Control Plane API  ← api.digitalocean.com
        ↓
DigitalOcean backend / database (same droplet/snapshot/volume infra)
        ↓
AMD GPU hardware nodes in DO's Atlanta datacenter
```

## Evidence From Your Script

Your script hits `https://api.digitalocean.com/v2` with `AMD_DEV_CLOUD_API_KEY` — a DigitalOcean Personal Access Token issued through the AMD portal. The fact that this works confirms:

- The **API is 100% standard DigitalOcean v2 API** — no AMD-specific endpoints
- The token is a real DO PAT scoped to an AMD-provisioned DO account/project
- Snapshots, droplets, volumes all live in **DigitalOcean's backend database** — AMD just provisions a DO account for you

## What AMD Adds

| Layer | Who owns it |
|---|---|
| Web portal UI | AMD (themed, different from cloud.digitalocean.com) |
| GPU droplet SKUs (MI300X) | AMD (hardware + BIOS/driver config) |
| API endpoint | DigitalOcean (unchanged) |
| Account/billing | AMD (they resell DO capacity) |
| Snapshot/volume/networking DB | DigitalOcean |
| Support tier | AMD for GPU issues, DO infra underneath |

## Practical Implication

Since the API is identical, **any DigitalOcean SDK or tool works against AMD Dev Cloud** with zero modification — just swap the token:

```python
import digitalocean  # pydo or python-digitalocean

manager = digitalocean.Manager(token=os.environ["AMD_DEV_CLOUD_API_KEY"])
snapshots = manager.get_all_snapshots()
droplets = manager.get_all_droplets()  # lists your MI300X droplets
```

Same for `doctl`:
```bash
doctl auth init --access-token $AMD_DEV_CLOUD_API_KEY
doctl compute droplet list
doctl compute snapshot list
```

Your snapshot deletion script is a clean, correct implementation — the only "AMD-specific" thing is the token source. Everything else is vanilla DO API.