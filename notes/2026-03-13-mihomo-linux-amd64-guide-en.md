---
audio: false
generated: true
image: false
lang: en
layout: post
title: Choose Mihomo Linux AMD64 Binary Guide
translated: false
type: note
---

Question: Based on my `uname -a` output showing `x86_64 GNU/Linux` (Ubuntu 22.04), which mihomo alpha binary file should I download from the release assets?

Answer:

## Analysis of Your System

From your `uname -a` output:
```
Linux to 6.8.0-90-generic x86_64 x86_64 x86_64 GNU/Linux
```

Key facts:
- **OS**: Linux (Ubuntu 22.04)
- **Architecture**: `x86_64` (64-bit Intel/AMD)
- **NOT**: Android, macOS, or ARM

---

## ✅ Correct File to Download

**`mihomo-linux-amd64-v1-alpha-0317d9f.gz`**

> Note: This file is **not shown in your listed assets** above — you only see `android-*` and `darwin-*` variants in that partial list. You need to **scroll down** in the GitHub releases page to find the `linux-*` files.

---

## Understanding the `amd64` Variants

Once you see the Linux files, here's how to choose among the `amd64` sub-variants:

| Variant | CPU Requirement | Recommendation |
|---|---|---|
| `linux-amd64-v1` | Any x86_64 CPU (broadest compat) | ✅ **Safe default for most systems** |
| `linux-amd64-v2` | Requires SSE4.2 (2008+ CPUs) | Slightly faster if your CPU supports it |
| `linux-amd64-v3` | Requires AVX2 (2013+ CPUs) | Best performance on modern CPUs |

To check which level your CPU supports:
```bash
# Check for v2 support
grep -m1 -c 'sse4_2' /proc/cpuinfo

# Check for v3 support (AVX2)
grep -m1 -c 'avx2' /proc/cpuinfo
```
If the output is `1`, your CPU supports that level.

**For a safe and compatible choice**, stick with `mihomo-linux-amd64-v1-alpha-XXXXXXX.gz`.

---

## After Downloading

```bash
# Extract
gunzip mihomo-linux-amd64-v1-alpha-0317d9f.gz

# Make executable
chmod +x mihomo-linux-amd64-v1-alpha-0317d9f

# Run
./mihomo-linux-amd64-v1-alpha-0317d9f
```

References:

- [MetaCubeX/mihomo Releases - GitHub](https://github.com/MetaCubeX/mihomo/releases)
- [Mihomo Official Docs](https://wiki.metacubex.one/en/startup/)
