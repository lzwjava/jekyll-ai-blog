---
audio: false
generated: true
image: false
lang: en
layout: post
title: Compiling Linux Kernel from Source
translated: false
type: note
---

Question: How do I compile the Linux kernel from source?

Answer:

```bash
# 1. Get the source (mainline or a stable tag)
git clone --depth 1 --branch v6.12 \
  https://github.com/torvalds/linux.git
cd linux

# 2. Install build deps (Ubuntu)
sudo apt install -y build-essential libncurses-dev bison flex \
  libssl-dev libelf-dev bc dwarves zstd

# 3. Start from your running kernel's config (fast path)
cp /boot/config-$(uname -r) .config
make olddefconfig          # fill new symbols with defaults
# or: make menuconfig       # TUI to tweak options
# or: make defconfig        # arch default config from scratch

# 4. Build (use all cores)
make -j$(nproc)            # builds vmlinux + modules

# 5a. Just the kernel image
make -j$(nproc) bzImage    # -> arch/x86/boot/bzImage

# 5b. Install (modules + image + initramfs + grub)
sudo make modules_install   # -> /lib/modules/<ver>/
sudo make install           # -> /boot, updates initramfs & grub
```

Key knobs:

- `make -j$(nproc)` — parallel build; full kernel ~5–30 min depending on config/cores. On your 192GB MI300X box it'll fly; on the M2 Air a `tinyconfig` build is saner.
- `localmodconfig` — only build modules currently loaded (`lsmod`), drastically cuts build time:

  ```bash
  make localmodconfig
  ```

- `O=` — out-of-tree build dir to keep the source clean:

  ```bash
  make O=../build defconfig
  make O=../build -j$(nproc)
  ```

- `CC=clang LLVM=1` — build with Clang/LLVM instead of GCC.
- `make clean` (keep config) / `make mrproper` (nuke config too).

Minimal config for fast iteration (e.g. learning, QEMU boots):

```bash
make tinyconfig
make -j$(nproc)
# boot it without touching your real system:
qemu-system-x86_64 -kernel arch/x86/boot/bzImage \
  -append "console=ttyS0" -nographic
```

If you just want a single module or subsystem, build that subtree:

```bash
make -j$(nproc) drivers/net/        # trailing slash = build dir
make M=drivers/mydriver modules     # external/standalone module
```

What's the goal — booting a custom kernel, building one driver, or studying internals? The config strategy differs a lot (full distro config vs. `tinyconfig` + QEMU).
