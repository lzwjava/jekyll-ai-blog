---
audio: false
generated: true
image: false
lang: en
layout: post
title: AMD Dev Cloud Storage UI Limitations
translated: false
type: note
---

**Question:** Why can't we see Block Storage / Volume options in the AMD Dev Cloud portal UI? Do we need to use the API instead?

**Answer:**

AMD Dev Cloud is powered by DigitalOcean infrastructure (you can see "Powered by DigitalOcean" at the bottom of their portal). However, AMD has a **customized/restricted portal** — they only expose a subset of DigitalOcean's features in their UI. Block Storage Volumes is one of the features not surfaced in the AMD Dev Cloud portal UI.

Your options:

## Option 1: Use the DigitalOcean API directly

AMD Dev Cloud gives you API access. Go to **Settings → API → Tokens** and generate a token. Then use the standard DigitalOcean API:

```bash
# Create a volume
curl -X POST https://api.digitalocean.com/v2/volumes \
  -H "Authorization: Bearer $AMD_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "size_gigabytes": 500,
    "name": "ml-data-vol",
    "region": "atl1",
    "filesystem_type": "ext4"
  }'

# List volumes
curl -X GET https://api.digitalocean.com/v2/volumes \
  -H "Authorization: Bearer $AMD_API_TOKEN"

# Attach volume to a droplet
curl -X POST https://api.digitalocean.com/v2/volumes/actions \
  -H "Authorization: Bearer $AMD_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "attach",
    "droplet_id": YOUR_DROPLET_ID,
    "region": "atl1"
  }'
```

## Option 2: Use `doctl` CLI

```bash
# Install
brew install doctl  # or snap install doctl on Ubuntu

# Auth with your AMD token
doctl auth init --access-token $AMD_API_TOKEN

# Create volume in atl1
doctl compute volume create ml-data-vol \
  --size 500GiB \
  --region atl1 \
  --fs-type ext4

# Attach to droplet
doctl compute volume-action attach VOLUME_ID --droplet-id DROPLET_ID

# After attach, on the droplet:
# lsblk  → find the new disk (e.g. /dev/sda)
# mkfs.ext4 /dev/sda  (if new)
# mount /dev/sda /mnt/data
```

## Likely limitation

Not all DigitalOcean regions support block storage, and **ATL1 may have limited feature parity** since it's AMD's dedicated datacenter. Check via API first:

```bash
curl -X GET "https://api.digitalocean.com/v2/regions" \
  -H "Authorization: Bearer $AMD_API_TOKEN" \
  | python3 -c "
import json, sys
regions = json.load(sys.stdin)['regions']
atl = [r for r in regions if 'atl' in r['slug']]
print(json.dumps(atl, indent=2))
"
```

Look at `features` in the ATL1 region response — if `private_networking` is there but `storage` is not, block storage isn't available in ATL1 at all.

## Practical alternative for ML workloads

If block storage isn't available in ATL1, your best bet for large dataset storage is:

```bash
# Use Spaces (S3-compatible object storage) — always available via API
# Upload datasets
aws s3 cp ./dataset s3://your-space/ \
  --endpoint-url https://atl1.digitaloceanspaces.com

# Or rsync from your local machine to the droplet directly
rsync -avz --progress ./data/ root@<droplet-ip>:/mnt/data/
```

Check the AMD Dev Cloud support page or open a support ticket — they may enable volumes on request for MI300X droplets given the storage-heavy nature of ML workloads.