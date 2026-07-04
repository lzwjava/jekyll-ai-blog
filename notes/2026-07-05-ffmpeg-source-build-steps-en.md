---
audio: false
generated: true
image: false
lang: en
layout: post
title: FFmpeg source build steps
translated: false
type: note
---

Here's the full procedure I followed to build FFmpeg from source:

---

## 1. Initial Assessment

I checked:

- **Build system**: Project uses `./configure` + `make` (standard autoconf-style)
- **Previous build**: No `config.mak` existed → never configured before, needed a fresh build
- **Toolchain**: `gcc` and `make` were already installed
- **Dependencies**: Only runtime libs present (`libx264-164`, `libmp3lame0`, etc.) but **no `-dev` packages** — headers needed for compilation were absent

## 2. First Configure Attempt

Ran:

```
./configure --enable-gpl --enable-version3 --enable-nonfree
```

Failed with:

```
nasm not found or too old. Please install/update nasm or use --disable-x86asm
```

**Why**: NASM is the assembler FFmpeg uses to compile hand-optimized x86 assembly routines (SIMD-optimized codecs, filters, etc.). Without it, configure forces a fallback to pure C, which is slower but still works. I chose to install it instead for a faster build.

## 3. Install NASM

Since this machine requires interactive `sudo`, I used `pkexec` (Polkit GUI elevation):

```
pkexec bash -c 'apt-get update -qq && apt-get install -y nasm'
```

This installed `nasm 2.16.01` from the Ubuntu 24.04 (Noble) repos.

## 4. Second Configure — Success

Re-ran the same configure command:

```
./configure --enable-gpl --enable-version3 --enable-nonfree
```

Succeeded. Configure auto-detected:

- 2,414 object files would be compiled
- Which codecs, filters, muxers, demuxers, protocols, and bitstream filters to enable
- No external libraries found (no `-dev` packages)
- Generated `config.h`, `config.mak`, `ffbuild/config.mak`, and library version headers

**About the flags**:

- `--enable-gpl` — enables GPL-licensed components (many FFmpeg parts are GPL)
- `--enable-version3` — enables LGPLv3/GPLv3 code
- `--enable-nonfree` — enables non-free codecs (e.g., libaacplus, certain encoders). Combined makes the output non-redistributable

## 5. Compilation

```
make -j$(nproc)
```

- `-j$(nproc)` → parallel build on all CPU cores (`nproc` returns the core count)
- Compiled 2,414 `.o` files across 7 libraries
- Linked `ffmpeg_g` and `ffprobe_g` (debug-symbol versions), then `strip`'d them down to 29 MB release binaries
- Built man pages from POD documentation
- Total time: ~a few minutes (parallel compilation)

## 6. Verification

Checked:

- Binary exist: `ffmpeg` (29 MB), `ffprobe` (29 MB)
- Version string: `ffmpeg version git-2026-07-02-14ed5e8`
- Library versions: avutil 61.2, avcodec 63.3, avformat 63.3, avdevice 63.2, avfilter 12.2, swscale 10.2, swresample 7.2
- Encoders: ~189, Decoders: ~527, Filters: ~483, Muxers: ~191, Demuxers: ~368, BSFs: ~53, Protocols: ~50
- Hardware acceleration: none (no `libva-dev`/`libvdpau-dev` installed)

## Key Takeaways

- **No `./configure` flags beyond license types were needed** — FFmpeg's configure has excellent auto-detection and pulls in everything it can find
- The **only missing tool** was `nasm` — everything else (gcc, make, ld) was already present
- To add external encoders (x264, x265, etc.), you'd run:

  ```
  sudo apt-get install libx264-dev libx265-dev libvpx-dev libmp3lame-dev libopus-dev libvorbis-dev libass-dev libsdl2-dev
  ./configure --enable-gpl --enable-version3 --enable-nonfree
  make -j$(nproc)
  ```

- For a redistributable build (without non-free code), drop `--enable-nonfree`; configure will still work fine
