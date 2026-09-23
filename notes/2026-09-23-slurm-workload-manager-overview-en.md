---
audio: false
generated: true
image: false
lang: en
layout: post
title: Slurm Workload Manager Overview
translated: false
type: note
---

This project is **Slurm Workload Manager** — the open-source cluster resource management and job scheduling system used in HPC (high-performance computing) environments.

## What it does

As a cluster resource manager, Slurm provides three key functions:

1. **Resource allocation** — allocates exclusive/non-exclusive access to compute nodes for users over a specified duration.
2. **Job execution framework** — starts, executes, and monitors work (typically parallel jobs) on the allocated nodes.
3. **Job scheduling/arbitration** — manages a queue of pending work and resolves conflicting resource requests.

## Key characteristics

- Open-source, GPL-licensed
- Designed to be simple, scalable, portable, fault-tolerant, and interconnect-agnostic
- Runs on Linux

## Repository structure

- `src/` — core Slurm source code (organized into subdirectories like `src/api`, `src/slurmctld`)
- `doc/` — documentation, guides, and man pages
- `etc/` — sample config files and scripts
- `slurm/` — installed public headers (`slurm.h`, `slurm_errno.h`, `slurmdb.h`, `pmi.h`, `spank.h`) for compiling against the Slurm API
- `testsuite/` — tests written for Check, Expect, and Pytest
- `auxdir/` — autotools build scripts
- `contribs/` — helpful tools outside of core Slurm
- `CHANGELOG/` — version changelogs (this checkout includes release notes up through 26.05)

This looks like a full Slurm source distribution checkout (with autotools `configure`, `Makefile.in`, etc.), not just a partial mirror.