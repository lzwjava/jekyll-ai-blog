---
audio: false
generated: true
image: false
lang: en
layout: post
title: Warp on Windows and Building from Source
translated: false
type: note
---

**Question:** Does Warp terminal work on Windows? And since it's written in Rust, can you compile it from source with Rust + Visual Studio Build Tools?

**Answer:**

## Yes, Warp works on Windows — and yes, you can now build from source

### Windows Support

Warp launched on Windows in February 2025, supporting PowerShell, WSL, and Git Bash, on both x64 and ARM64 architectures. The core experience is nearly identical across platforms — written entirely in Rust and rendered directly on the GPU.

So just download and run it, no special setup needed.

---

### Building from Source

This is the more interesting part. Warp open-sourced its client on April 30, 2026, releasing the source code on GitHub under the AGPL license. So you can now actually build it yourself.

The Warp UI framework crates use the MIT license, while the rest of the code uses AGPL v3.

The repo is at: **https://github.com/warpdotdev/warp**

---

### Can you compile it with Rust + Visual Studio Build Tools?

**Yes, in principle** — this is exactly the standard Windows Rust toolchain setup.

On Windows, Rust uses MSVC as its default linker backend. The standard setup is:

```powershell
# Install Rust (uses MSVC toolchain by default on Windows)
winget install Rustlang.Rustup

# Rustup will prompt you to install VS Build Tools if missing
# Or install manually: https://visualstudio.microsoft.com/visual-cpp-build-tools/
# Select "Desktop development with C++" workload

# Verify toolchain
rustup show
# Should show: stable-x86_64-pc-windows-msvc

# Clone and build
git clone https://github.com/warpdotdev/warp
cd warp
cargo build --release
```

**But** — Warp is a GPU-rendered terminal (using their own rendering stack via `wgpu`/similar). On Windows, it integrates with DirectX/graphics drivers directly. Warp does all its own graphics calls and has to integrate with graphics drivers on Windows and handle event handling. So the build will likely have additional dependencies beyond just Rust + MSVC — expect things like Windows SDK headers, possibly `cmake`, and graphics API bindings.

**Practical advice before trying:**

1. Check the repo's `CONTRIBUTING.md` and `WARP.md` — Warp has a lightweight contribution workflow documented in their CONTRIBUTING.md guide.
2. Look at `.cargo/config.toml` in the repo for any platform-specific linker flags or target overrides.
3. Check `Cargo.toml` for dependencies that might need native libs (e.g., `wgpu`, `winit`, `windows-rs`).

The `windows-rs` crate (Microsoft's official Rust bindings for Windows APIs) compiles fine with MSVC toolchain. `wgpu` on Windows uses DirectX 12 by default and also compiles cleanly with VS Build Tools. So the stack is compatible — the question is just what exact dev dependencies Warp documents.

---

### TL;DR

| Question | Answer |
|---|---|
| Does Warp work on Windows? | Yes, since Feb 2025 |
| Is source code available? | Yes, open-sourced Apr 2026 (AGPL) |
| Can you build with Rust + VS Build Tools? | Yes, that's the correct Windows toolchain |
| Any gotchas? | GPU rendering deps — check CONTRIBUTING.md first |

**References:**

- [Warp launches on Windows (Feb 2025)](https://www.warp.dev/blog/launching-warp-on-windows)
- [Warp is now open-source (Apr 2026)](https://www.warp.dev/blog/warp-is-now-open-source)
- [warpdotdev/warp on GitHub](https://github.com/warpdotdev/warp)
