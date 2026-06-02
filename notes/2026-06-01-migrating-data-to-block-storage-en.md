---
audio: false
generated: true
image: false
lang: en
layout: post
title: Migrating Data to Block Storage
translated: false
type: note
---

**Question:** How do I set up a DigitalOcean block storage volume and move my 130GB of model/data files onto it from my current GPU droplet?

**Answer:**

## Step 1: Create the Volume

In the DigitalOcean UI when creating your droplet, select **"Create new"** under Add a Volume:

- Size: **150GB** (give yourself headroom)
- It will be attached at creation time

Or via `doctl` if droplet already exists:

```bash
doctl compute volume create my-ml-data \
  --region sfo3 \
  --size 150 \
  --fs-type ext4
```

## Step 2: Format and Mount (First Time Only)

SSH into your droplet:

```bash
# Check what the volume is named (usually /dev/sda or /dev/disk/by-id/...)
lsblk

# Format it (ONLY do this once, first time ever)
mkfs.ext4 /dev/sda

# Create mount point
mkdir -p /mnt/data

# Mount it
mount /dev/sda /mnt/data

# Verify
df -h /mnt/data
```

## Step 3: Move Your 130GB Data onto It

```bash
# If data is on root disk currently
rsync -avh --progress /root/data/ /mnt/data/
# or
cp -r /your/model/weights /mnt/data/

# After confirming copy is good, remove from root disk
rm -rf /root/data/
```

If data is on your **local machine or workstation** (192.168.1.36), push directly to the volume:

```bash
# From your workstation
rsync -avh --progress --compress \
  /local/path/to/data/ \
  root@<droplet-ip>:/mnt/data/
```

## Step 4: Make Mount Persistent (Within Same Droplet Session)

For auto-mount on reboot within same droplet:

```bash
# Get UUID
blkid /dev/sda

# Add to fstab
echo "UUID=<your-uuid>  /mnt/data  ext4  defaults,nofail  0  2" >> /etc/fstab
```

## Step 5: End of Session — Detach, Don't Snapshot

```bash
# Unmount before detaching
umount /mnt/data

# Detach via doctl
doctl compute volume-action detach <volume-id> <droplet-id>

# Now safely destroy droplet
doctl compute droplet delete <droplet-id> --force
```

## Step 6: Next Session — Attach and Mount

```bash
# Create fresh droplet (from your thin OS snapshot)
doctl compute droplet create ...

# Attach volume
doctl compute volume-action attach <volume-id> <new-droplet-id>

# SSH in, mount
mount /dev/sda /mnt/data

# Your 130GB is right there, no hydration wait
ls /mnt/data
```

## Your New Workflow Summary

```
Old:  create snapshot (20min) → restore (fast but hydrates lazily)
New:  volume persists → attach (instant) → mount (2 sec) → work
```

The 130GB never moves. It just stays on the volume, detached, costing ~$15/month at rest, ready to attach to any new GPU droplet in seconds.
