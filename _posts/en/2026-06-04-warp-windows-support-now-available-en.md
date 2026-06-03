---
audio: false
generated: true
image: false
lang: en
layout: post
title: Warp Windows Support Now Available
translated: false
type: note
---

Question: Why doesn't Warp work on Windows?

**Answer:**

Short answer: **It does now.** Warp officially launched Windows support in February 2025, with support for PowerShell, WSL, and Git Bash on both x64 and ARM64 architectures.

But the historical "why it took so long" is worth understanding:

## Technical Reasons for the Delay

**Graphics rendering:** Warp is a totally native app written in Rust with direct GPU rendering, not an Electron or VS Code-based wrapper. This means the team had to implement platform-specific graphics calls for three separate graphics APIs:

- macOS: Metal
- Linux: Vulkan
- Windows: Direct3D 12

Each has different event handling, driver integration, and performance characteristics. Building one unified terminal that scales across all three without compromising performance is nontrivial.

**Shell complexity:** Windows support required "a bunch of time" to seamlessly interface with PowerShell, Git Bash, and WSL in a way similar to Windows Terminal, allowing users to start sessions in different shell environments. This isn't just spawning processes—it's managing ConPTY (Pseudo Console), handling Windows-specific shell quirks, and integrating with the Windows Package Manager (WinGet).

**User demand vs. engineering effort:** macOS + Linux covered the core developer audience (Unix/Linux preference bias in terminal tooling). Windows has fragmented shell landscapes (PowerShell, WSL, Git Bash) that each require slightly different handling. The team probably made a calculated decision: maximize value for 80% of users first, then tackle Windows when the architecture was solid enough.

## Why This Matters to You

If you're on Windows or considering it, Warp is now a viable terminal choice. The Rust-based approach gives you:

- Zero-overhead GPU acceleration (no Electron bloat)
- Same AI-native features across all platforms
- Native integration with WSL (useful if you need Linux for dev work while staying on Windows)

Still on macOS + Ubuntu? You're in the sweet spot—Warp has been battle-tested there for years and has the deepest feature parity.

---

References:

- [Warp Launches on Windows](https://www.warp.dev/blog/launching-warp-on-windows) (Feb 26, 2025)
- [The New Stack: Warp AI Terminal Windows Launch](https://thenewstack.io/warp-launches-ai-first-native-terminal-app-for-windows/) (Feb 26, 2025)
- [Warp 2025 in Review](https://www.warp.dev/blog/2025-in-review) (Dec 30, 2025)
