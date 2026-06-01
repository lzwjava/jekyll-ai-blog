---
audio: false
generated: true
image: false
lang: en
layout: post
title: DigitalOcean Open Source Tools Workflow
translated: false
type: note
---

Yes, DigitalOcean has everything open source. The main ones relevant to you:Yes, fully open source. Here's everything relevant:

## The Main Repo

**`digitalocean/doctl`** — the official CLI for the DigitalOcean API, written in Go.

```
https://github.com/digitalocean/doctl
```

Find the source code or report issues at the `digitalocean/doctl` repository on GitHub. There's also a specific tutorial: "How To Work with DigitalOcean Block Storage Using doctl."

## Volume-Specific Source Code

The volume commands live at `doctl/commands/volumes.go` on GitHub — you can see exactly how `volume create`, `volume delete`, attach/detach are implemented. Block storage volumes range from 1GiB to 16TiB and can be moved between droplets in the same region.

## Install on Your MacBook

```bash
# macOS
brew install doctl

# authenticate
doctl auth init
# paste your DO API token
```

## Key Volume Commands for Your Workflow

```bash
# list your volumes
doctl compute volume list

# create 200GB volume
doctl compute volume create ml-data \
  --region sfo3 \
  --size 200GiB \
  --fs-type ext4

# attach to droplet
doctl compute volume-action attach <volume-id> <droplet-id>

# detach before destroying
doctl compute volume-action detach <volume-id> <droplet-id>

# destroy droplet (volume persists)
doctl compute droplet delete <droplet-id> --force

# list snapshots
doctl compute snapshot list
```

## Also Useful — DigitalOcean's Other OSS Repos

```
github.com/digitalocean/godo        # Go SDK (what doctl uses internally)
github.com/digitalocean/terraform-provider-digitalocean  # Terraform provider
```

**`godo`** is useful if you want to build your own automation scripts in Go — same API surface as doctl but as a library.

## For Your Workflow — Script the Whole Session

Since you build CLI tools (`ww`, `zz`, `iclaw`), you could wrap this into a shell script:

```bash
#!/bin/bash
# ml-session.sh

VOLUME_ID="your-volume-id"
SNAPSHOT_ID="your-os-snapshot-id"
REGION="sfo3"
SIZE="g-8vcpu-32gb-nvidia-l40s-1"  # or your MI300X slug

case $1 in
  start)
    # create droplet from snapshot
    DROPLET_ID=$(doctl compute droplet create amd-gpu \
      --image $SNAPSHOT_ID \
      --size $SIZE \
      --region $REGION \
      --ssh-keys $(doctl compute ssh-key list --no-header --format ID) \
      --wait \
      --format ID --no-header)
    
    # attach volume
    doctl compute volume-action attach $VOLUME_ID $DROPLET_ID --wait
    
    # get IP
    IP=$(doctl compute droplet get $DROPLET_ID --format PublicIPv4 --no-header)
    echo "Ready: ssh root@$IP"
    ;;

  stop)
    DROPLET_ID=$(doctl compute droplet list --format ID,Name --no-header | grep amd-gpu | awk '{print $1}')
    doctl compute volume-action detach $VOLUME_ID $DROPLET_ID --wait
    doctl compute droplet delete $DROPLET_ID --force
    echo "Droplet destroyed, volume persists."
    ;;
esac
```

```bash
./ml-session.sh start   # spin up, attach volume, print IP
./ml-session.sh stop    # detach volume, destroy droplet
```

One command to start your training session, one to end it cleanly. Fits perfectly into your terminal-first workflow.