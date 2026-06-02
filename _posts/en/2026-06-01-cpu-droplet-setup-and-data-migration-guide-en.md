---
audio: false
generated: true
image: false
lang: en
layout: post
title: CPU Droplet Setup and Data Migration Guide
translated: false
type: note
---

No — the snapshot requires 720 GB minimum disk, but the biggest CPU droplet only has 240 GB disk. The portal won't allow it.

    Look for a "Create Droplet" option that doesn't require a snapshot — a fresh Ubuntu image. In the AMD Dev Cloud portal, there should be an option to create a basic/standard droplet (not from snapshot) in atl1. Something like:

    - Image: Ubuntu 24.04 (not from snapshot)
    - Plan: Basic / Regular CPU
    - Region: atl1

    If the portal only offers GPU droplet options in atl1, then this partner account truly can't create CPU droplets in atl1 at all. In that case:

    1. Create CPU droplet in nyc1 ($6/mo)
    2. Create a new volume in nyc1 ($10/mo)
    3. Do data prep there
    4. When ready: move data to a new atl1 volume, recreate GPU droplet in atl1

    Want me to set up the nyc1 path instead?
