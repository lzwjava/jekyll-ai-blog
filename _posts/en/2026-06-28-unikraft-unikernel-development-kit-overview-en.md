---
audio: false
generated: true
image: false
lang: en
layout: post
title: Unikraft Unikernel Development Kit Overview
translated: false
type: note
---

**Question:** What is Unikraft (github.com/unikraft/unikraft)?

**Answer:**

Unikraft is an open-source **unikernel development kit** — a framework for building specialized, single-purpose VMs where your application and a minimal kernel are compiled into one bootable image. Instead of `app → libc → Linux kernel → hardware`, you get `app + only-the-kernel-bits-you-need → hypervisor`. ~80% C, BSD-3-Clause, Linux Foundation / Xen Project incubator, ~3.7k stars, latest release v0.21.0 (May 2026).

**The core idea (first principles)**

A normal Linux VM ships a full general-purpose kernel: process isolation, multiple address spaces, syscall boundary, scheduler for thousands of processes, drivers for hardware you'll never touch. A unikernel throws almost all of that away because a VM running *one* app doesn't need it:

- **Single address space, no user/kernel split.** App and kernel run in the same ring. A "syscall" becomes a plain function call — no `syscall` instruction, no context switch, no TLB flush. That's where the latency wins come from.
- **Library OS model.** The OS is a menu of libraries (`lib/`, `plat/`, `arch/` in the repo). You link only what you use — no networking? No TCP/IP stack in your image. This is the `Config.uk` / `Makefile.uk` Kconfig-style build system, very kernel-dev-flavored.
- **Compile-time specialization.** Because the whole thing is one binary, the compiler can inline across the app/kernel boundary and dead-code-eliminate unused OS paths.

**Why people care**

- **Millisecond cold boots** vs. seconds for Linux VMs — the headline feature, and why it's interesting for serverless/scale-to-zero. No init, no driver probing, no userspace bring-up.
- **Tiny image / attack surface.** No shell, no extra syscalls, fewer CVEs reachable. If `system()` isn't linked, a code-exec bug can't spawn a shell.
- **High server saturation.** Footprints in the single-digit MB range → far more instances per host.

**How you'd actually use it**

The companion CLI is `kraft` (separate repo, kraftkit):

```bash
curl -sSfL https://get.kraftkit.sh | sh
kraft run unikraft.org/helloworld:latest   # boots a unikernel VM
```

The slick part for your workflow: it can consume an existing **Dockerfile** as the rootfs via a `Kraftfile`, so you don't hand-write kernel config:

```yaml
spec: v0.6
runtime: base:latest
rootfs: ./Dockerfile
cmd: ["/path/to/my-server-app"]
```

The creators commercialized it as **KraftCloud / kraft.cloud** — a serverless platform betting on those millisecond boots for scale-to-zero economics.

**Where it sits in the landscape**

Spiritual successor to earlier unikernel projects (MirageOS, OSv, IncludeOS) but with a stronger bet on **POSIX compatibility + container-compatible tooling**, which was the historical killer of unikernels — nobody wanted to rewrite their app against a bespoke library OS. Unikraft tries to let you run mostly-unmodified Go/Python/Node/Rust binaries.

**Relevance to your trajectory:** the genuinely interesting angle for an AI-infra person is *inference cold-start*. The dream is sub-second scale-to-zero for model-serving endpoints, where today you eat container + CUDA-runtime + weights-load latency. Unikraft solves the first slice (VM/OS bring-up), not the GPU/weights slice — but it's the kind of substrate that LLM-serving cost optimization will eventually push on. Worth a `kraft run` on your workstation just to feel a millisecond boot.

**References:**

- [unikraft/unikraft (GitHub)](https://github.com/unikraft/unikraft)
- [Unikraft docs — what is a unikernel?](https://unikraft.org/docs/concepts/)
- [kraftkit CLI](https://github.com/unikraft/kraftkit)
