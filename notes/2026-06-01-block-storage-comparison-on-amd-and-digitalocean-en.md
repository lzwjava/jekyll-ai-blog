---
audio: false
generated: true
image: false
lang: en
layout: post
title: Block Storage Comparison on AMD and DigitalOcean
translated: false
type: note
---

**Question:** How does block storage / volumes work on AMD Dev Cloud and DigitalOcean — what's the mechanism, and how do you use it?

**Answer:**

## Block Storage: How It Actually Works

At the infrastructure level, **network block storage** (NVMe-oF or iSCSI over the datacenter fabric) exposes a remote disk as if it were a local block device. The hypervisor/driver maps the remote volume to a `/dev/sdX` or `/dev/vdX` device node inside your VM. From the OS perspective, it's indistinguishable from a local disk — you partition it, format it, mount it, use it.

```
Your Droplet/Instance
  ↕ virtio-blk / NVMe-oF driver
Storage Node (separate physical hardware)
  ↕ high-bandwidth datacenter fabric
  Raw block device exposed as /dev/sda, /dev/vda, etc.
```

The "detach and re-attach" property works because the storage node holds the data independently — your compute instance is stateless relative to the volume.

---

## DigitalOcean Volumes

### Concepts

- NVMe SSDs, network-attached
- Up to 16 TB per volume, up to 10 volumes per Droplet
- Billed by GB/month, persists independently of Droplet lifecycle
- Can be moved between Droplets **in the same region**

### CLI workflow (doctl)

```bash
# Install doctl
brew install doctl
doctl auth init

# Create a volume
doctl compute volume create my-data \
  --region sfo3 \
  --size 100GiB \
  --fs-type ext4

# Attach to a running Droplet
doctl compute volume-action attach <volume-id> <droplet-id>

# Inside the Droplet — find the device
lsblk
# Usually shows up as /dev/sda or /dev/disk/by-id/scsi-...

# Mount it
sudo mkdir -p /mnt/data
sudo mount -o discard,defaults /dev/sda /mnt/data

# Persist across reboots
echo '/dev/sda /mnt/data ext4 discard,defaults 0 0' | sudo tee -a /etc/fstab
```

### Move volume between Droplets

```bash
# Detach from old Droplet
doctl compute volume-action detach <volume-id> <droplet-id-old>

# Attach to new Droplet (GPU droplet, etc.)
doctl compute volume-action attach <volume-id> <droplet-id-new>
```

This is the key use case — your dataset or model weights live on the volume, you spin up a cheap CPU Droplet for prep work, then re-attach to a GPU Droplet for training. Pay for compute only when you need it.

---

## AMD Dev Cloud (devcloud.amd.com)

AMD Dev Cloud uses a slightly different model — it's more of a **managed cloud with project-scoped storage** rather than a raw IaaS block device marketplace. Here's what's actually going on:

### Storage tiers on AMD Dev Cloud

| Type | Where | Use case |
|------|--------|----------|
| Instance local storage | NVMe on the MI300X node | Fast scratch, ephemeral |
| Persistent project storage | Network-attached, per-account | Datasets, checkpoints |
| Object storage (if enabled) | S3-compatible endpoint | Large dataset staging |

The "Volumes" concept in their UI maps to **persistent block devices** that survive instance termination — similar to DO Volumes but scoped to your AMD Dev Cloud project.

### Practical workflow

```bash
# SSH into your AMD Dev Cloud instance
ssh user@<amd-instance-ip>

# Check what block devices are attached
lsblk -o NAME,SIZE,TYPE,MOUNTPOINT,FSTYPE

# If volume is attached but not mounted
sudo mkfs.ext4 /dev/sdb          # only first time!
sudo mkdir -p /mnt/volume
sudo mount /dev/sdb /mnt/volume

# Persist
echo '/dev/sdb /mnt/volume ext4 defaults 0 0' | sudo tee -a /etc/fstab
```

For AMD Dev Cloud specifically — since you're on the MI300X ($2/hr), the key pattern is:

```bash
# Before stopping instance — unmount cleanly
sudo umount /mnt/volume

# Detach via UI or CLI, then re-attach to new instance
# On new instance:
sudo mount /dev/sdb /mnt/volume
# Your data is there
```

---

## Key Pattern for Your ML Workflow

Since you're doing model training on AMD Dev Cloud:

```
[Volume: 500GB]
  ├── /datasets/         ← HuggingFace datasets, prepped
  ├── /checkpoints/      ← model.pt saves every N steps
  └── /runs/             ← wandb local logs, metrics

Workflow:
1. Spin up MI300X instance ($2/hr)
2. Attach volume → mount at /mnt/vol
3. Train → checkpoint to /mnt/vol/checkpoints/
4. Stop instance (billing stops)
5. Volume persists → re-attach next session
```

This saves you from re-downloading datasets or losing checkpoints when an instance terminates or you switch between machines.

---

## Gotchas

- **Region-locked**: volumes can only attach to instances in the same region — check before creating
- **One attachment at a time**: a volume can only be attached to one instance simultaneously (it's a block device, not shared filesystem — for shared use, you'd need NFS over it or object storage)
- **`discard` mount flag**: use it for NVMe volumes — enables TRIM which keeps performance from degrading
- **XFS vs ext4**: XFS handles large files (model checkpoints, dataset shards) better; ext4 is fine for general use
- **Don't `mkfs` twice**: formatting destroys data — only format on first use
