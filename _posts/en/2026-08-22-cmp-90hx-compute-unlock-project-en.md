---
audio: false
generated: true
image: false
lang: en
layout: post
title: CMP 90HX Compute Unlock Project
translated: false
type: note
---

This is a **hardware-modding / firmware-unlock project** for the **NVIDIA CMP 90HX** GPU. (Note: "CMP90HX" doesn't appear to be an official NVIDIA part — it looks like a custom-marketed mining variant of the GA102 die used in RTX 3090, given the report compares it to RTX 3090/3080Ti.)

Here's what the project does at each level:

## What it is

A driver-level, **compute-unlock** (哈希/挖矿算力解锁) toolchain for the CMP 90HX on NVIDIA Open Kernel Modules `580.159.03`, Linux/systemd/root. It targets cards identified by PCI IDs `10de:220d / 10de:1555`.

## The core technique (the patch)

The GPU ships with crippled compute performance (compute-only "GSP-RM" firmware). The patch (`patches/0001-58015903-cmp90hx-direct-compute.patch`) modifies the NVIDIA kernel module's GSP (Graphics System Processor) bootstrap path to, at a precise window during boot:

1. **Open PLM** — writes a forged "signature" payload (`CMP90HX_FEAT_OVR_PLM @0x00823804`) and invokes V67 booter loads twice until the PLM (an access-gating fuse) reads back `0xffffffff` (open).
2. **Write compute speed selectors** — `SS0` (`FEAT_OVR_SM_SPD`) and `SS1` (`FEAT_OVR_SM_SPD_1`) with the known unlocked values, with readback verification.
3. **Restore the stock signature** immediately (so the module isn't left patched), then return an error to force the driver to stop — the actual PCIe **bus reset** that persists the change happens via systemd afterwards.

The bootstrap is temporary: it runs a custom-compiled `nvidia.ko.bootstrap` module, does its writes, then a systemd service does 2× PCIe `bus` resets and brings back the unmodified stock NVIDIA driver.

## The runtime system (systemd)

- `cmp90hx-persistent.service` runs at every boot, **before** GPU consumers and (critically) before HiveOS's `hive.service`/`os-core.service`.
- It pauses Hive services, processes cards **serially** (one at a time), does two PCIe resets, restores the stock driver, then resumes Hive.
- `cmp90hx-batch-bus-test.sh` and `cmp90hx-v67-one-test.sh` are the worker scripts (the `one.sh`/`batch.sh` are thin entry shims).

## The analysis report (`分析报告-90HX图形阉割定位.md`)

This is a separate investigative document (by a contributor) analyzing **why the card's gaming/graphics performance is terrible**, distinct from the compute unlock. Key finding: the cause is **not** a few registers but the whole PGRAPH (3D/graphics) engine's private space being gated (readback `0xBADFxxxx`) — because the GSP-RM firmware skips graphics init entirely (compute-only firmware variant). It's a firmware-init problem, not hardware fusing (unlike the 170HX fuse-throttle). It also documents real SKU-level silicon differences (fewer GPCs/LTCs ~15-20% slower than 3090) that can't be recovered.

## Project structure

| File | Purpose |
| --- | --- |
| `patches/0001-...patch` | The actual unlock code change |
| `install.sh` | Verifies environment, builds the bootstrap module, installs service |
| `verify.sh` / `check.sh` | Post-boot verification; `check.sh` reads 9 SM issue-rate fields read-only |
| `remove.sh` | Uninstalls, restores stock `nvidia.ko` |
| `cmp90hx-*.sh` / `defer-services.sh` | Runtime boot scripts |
| `UPSTREAM_GEN2.md` | Review of the upstream 170HX project (explicitly excludes the Gen2 PCIe path) |
| `patches/`, `work/`, `scripts/` | Patch, build trees, Python helpers |

**Risk note:** the README is emphatic that this is low-level kernel/driver/GPU-reset work, only for this exact hardware+firmware combo, requires Secure Boot off, and will need re-verification after any NVIDIA driver/kernel update. It never overwrites the vendor's runtime module in normal use — it backs it up and only edits selectors during the brief bootstrap window.
