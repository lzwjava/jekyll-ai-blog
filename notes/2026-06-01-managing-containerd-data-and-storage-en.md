---
audio: false
generated: true
image: false
lang: en
layout: post
title: Managing containerd data and storage
translated: false
type: note
---

**Question:** What is containerd data, and do we actually need to move it from the root disk to the volume?

**Answer:**

## What is containerd data?

`/var/lib/containerd/` stores everything the container runtime manages:

- **Snapshots** — layered filesystem snapshots for container images (the bulk of the 59G)
- **Content store** — raw OCI blobs (image layers, manifests, configs) downloaded from registries
- **Metadata** — BoltDB databases tracking image/container state
- **Runtime state** — running container state, shim processes

On a GPU dev machine like your AMD Dev Cloud node, this is almost entirely **Docker/container image layers** — think PyTorch images, ROCm images, Ollama containers, etc. These can be enormous (ROCm PyTorch alone is often 20–30G per image).

## Do you need to move it?

**Probably not, or at least not urgently.** Here's the reasoning:

| Factor | Assessment |
|--------|-----------|
| Reproducible? | Yes — images can be re-pulled from registry |
| Risk of moving | High — containerd uses hardlinks and overlay mounts; `rsync` can break this |
| Benefit | Frees 59G on root disk |
| Alternative | Just `docker system prune` or `crictl rmi` to delete unused images |

## Safer alternative — just prune

```bash
# See what's actually in there
du -sh /var/lib/containerd/io.containerd.snapshotter.v1.overlayfs/snapshots/*

# If using Docker on top of containerd:
docker system df
docker system prune -af --volumes  # nuke unused images, containers, volumes

# If using containerd directly (nerdctl/crictl):
nerdctl system prune -af
```

This will likely recover most of the 59G without any symlink gymnastics or risk of breaking the runtime.

## If you DO want to move it properly

`rsync` is the wrong tool — containerd uses **hardlinks** in its snapshot store that rsync breaks. The correct approach:

```bash
systemctl stop containerd
cp -a --reflink=auto /var/lib/containerd /mnt/volume/containerd-data
# NOT rsync — cp -a preserves hardlinks better, or use tar pipe:
# tar -C /var/lib/containerd -cf - . | tar -C /mnt/volume/containerd-data -xf -

# Then bind-mount, not symlink:
mount --bind /mnt/volume/containerd-data /var/lib/containerd
echo '/mnt/volume/containerd-data /var/lib/containerd none bind 0 0' >> /etc/fstab
systemctl start containerd
```

## My recommendation

**Stop the move. Just prune first:**

```bash
# Quick audit
ssh root@<your-node> "du -sh /var/lib/containerd/*/snapshots 2>/dev/null; docker system df 2>/dev/null || nerdctl system df 2>/dev/null"
```

If you have Ollama/llama.cpp pulling GGUF models AND Docker pulling GPU images, you're likely carrying stale layers you don't need. Pruning is safer, faster, and zero-risk compared to relocating a live runtime data directory.