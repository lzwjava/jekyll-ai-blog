---
audio: false
generated: true
image: false
lang: en
layout: post
title: Switch to Nouveau and Test
translated: false
type: note
---

Pushed as **`muda 0.8.0`** (`71e1f55`). The native backend is in place — now it needs your hands, because I have no non-interactive root.

## The one thing I need you to run

First stop anything using the M40 (ComfyUI, `llama-server`, etc.), then:

```sh
cd ~/projects/muda

# see current state (no root)
tools/muda-gpu-mode.sh status

# switch to nouveau (root)
sudo tools/muda-gpu-mode.sh nouveau
```

Then test the native path:

```sh
MUDA_DRIVER=nouveau ./build/mudainfo
MUDA_DRIVER=nouveau ./build/test_memory
```

**Paste the output back to me.** To undo at any time:

```sh
sudo tools/muda-gpu-mode.sh nvidia     # or just reboot
```

A reboot always restores `nvidia`, because `nouveau` stays blacklisted by the NVIDIA package — the switch is runtime-only.

## What I already built (compile-tested)

- **`src/driver_nouveau.c`** — talks straight to the nouveau kernel driver over `/dev/dri/renderD*` with a hand-written DRM ioctl ABI (no libdrm headers):
  - `DRM_IOCTL_VERSION` + `DRM_IOCTL_NOUVEAU_GETPARAM` → chipset, PCI id, framebuffer size
  - `DRM_IOCTL_NOUVEAU_GEM_NEW` + `mmap` → real GEM allocations for `mudaMalloc`
  - full stream/event surface; `launch` returns `mudaErrorNotSupported` for now
- **`tools/muda-gpu-mode.sh`** — `status` / `nouveau` / `nvidia`, reversible
- `MUDA_DRIVER=nouveau` wired into `mudaInit`

Current verified state is unchanged: **77 checks + 4 mudac programs**, all green on the OpenCL driver, and `MUDA_DRIVER=nouveau` cleanly reports "no nouveau DRM device found" while nvidia is bound.

## What happens after you paste the output

Once nouveau is bound and I can open its render node as a normal user, I can **actually develop and test** the native driver against real hardware (GEM allocation, `GETPARAM`, then the compute channel). If `GETPARAM`/GEM turn out to need different constants on your kernel, I'll see it in your output and fix it.

If you'd rather not switch right now, tell me and I'll pivot to `__constant__`/`cudaMemcpyToSymbol` support or a faster SGEMM instead.
