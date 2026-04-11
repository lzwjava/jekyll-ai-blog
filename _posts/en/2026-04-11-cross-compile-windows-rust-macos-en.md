---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cross-Compiling Windows Rust on macOS
translated: false
type: note
---

Here's the blog post:

---

## Cross-Compiling a Windows-Only Rust Project on macOS: Lessons from WeFriends

Recently I came across [WeFriends](https://github.com/StrayMeteor3337/WeFriends), an open-source WeChat friend detection tool written in Rust. It uses `egui` for the GUI and hooks into the Windows WeChat desktop client via DLL injection to detect which friends have deleted or blocked you. Cool project — but it's built exclusively for Windows. I wanted to see if I could get it to at least compile on macOS.

### The First Build Attempt

Running `cargo build` immediately hit a wall:

```
error[E0433]: failed to resolve: could not find `windows` in `os`
 --> src/wechat_manager.rs:1:14
  |
1 | use std::os::windows::process::CommandExt;
  |              ^^^^^^^ could not find `windows` in `os`
```

This makes sense — `std::os::windows` simply doesn't exist on macOS. The module is conditionally compiled by `rustc` and only available when targeting Windows.

### The Root Problem

The codebase had Windows-specific code scattered across several layers:

1. **Unconditional Windows imports** — `std::os::windows::process::CommandExt`, `std::process::Command` (used only in Windows blocks), `libloading` types for DLL loading
2. **Build script** — `build.rs` used `extern crate winres` unconditionally, which fails to resolve on non-Windows
3. **Cargo.toml** — `winres` and `winapi` were listed as plain `[build-dependencies]`, downloaded and compiled on all platforms

Interestingly, the original author *did* use `#[cfg(target_os = "windows")]` inside function bodies (e.g., `kill_wechat`, `start_wechat`), but forgot to gate the **imports** and **type aliases** at the top of the file.

### The Fixes

**1. Gate Windows-only imports with `#[cfg]`**

```rust
// Before
use std::os::windows::process::CommandExt;
use std::process::{Command, Stdio};
use libloading::{Library, Symbol};
use rand::Rng;

// After
#[cfg(target_os = "windows")]
use std::os::windows::process::CommandExt;
#[cfg(target_os = "windows")]
use std::process::{Command, Stdio};
#[cfg(target_os = "windows")]
use libloading::{Library, Symbol};
#[cfg(target_os = "windows")]
use rand::Rng;
```

The key insight: imports that are only used inside `#[cfg(target_os = "windows")]` blocks must themselves be gated. Rust's unused-import warnings would normally catch this, but since the code was never compiled on non-Windows, nobody noticed.

Some imports like `std::time::Duration` and `tokio::time` were used in cross-platform code (`install_wechat` uses `tokio::time::sleep`), so those stayed ungated.

**2. Add non-Windows stubs for public functions**

Functions like `login_wechat` and `unhook_wechat` are called from `main.rs` unconditionally. Rather than wrapping every call site in `#[cfg]`, I added stub implementations:

```rust
#[cfg(not(target_os = "windows"))]
pub async fn login_wechat() -> Result<u16> {
    Err(anyhow::anyhow!("Only supported on Windows"))
}

#[cfg(target_os = "windows")]
pub async fn login_wechat() -> Result<u16> {
    // ... actual implementation
}
```

This keeps the same public API on all platforms. The GUI compiles and runs everywhere; it just returns errors when you try to do Windows-specific things.

**3. Make build-dependencies platform-specific**

```toml
# Before
[build-dependencies]
winres = "0.1"
winapi = { version = "0.3", features = ["winnt"] }

# After
[target.'cfg(target_os = "windows")'.build-dependencies]
winres = "0.1"
winapi = { version = "0.3", features = ["winnt"] }
```

And in `build.rs`, wrap the entire body:

```rust
fn main() {
    #[cfg(target_os = "windows")]
    {
        let mut res = winres::WindowsResource::new();
        res.set_manifest_file("app.manifest");
        // ...
        res.compile().unwrap();
    }
}
```

### Result

After these changes, `cargo build` succeeds on macOS with only warnings (deprecated `rand` methods, unused variables in commented-out code blocks).

### Will It Actually Run on macOS?

**No** — not in any meaningful way. The GUI will launch, but every core feature depends on:

- **DLL injection** (`wxdriver64.dll`) — Windows-only mechanism
- **Process commands** (`taskkill`, `tasklist`) — Windows CLI tools
- **File paths** (`%LocalAppData%\Tencent\WeChat`) — Windows directory structure
- **Process creation flags** (`.creation_flags()`) — Windows API

The app is fundamentally a Windows tool. Making it compile cross-platform is useful for development (IDE support, CI checks, library compatibility testing), but the runtime behavior is Windows-only by design.

### Takeaways

1. **Gate your imports, not just your function bodies.** If code inside a function is behind `#[cfg]`, the types it uses probably need the same gate at the import level.

2. **Use platform-specific dependency tables in Cargo.toml.** `[target.'cfg(target_os = "windows")'.dependencies]` prevents pulling in and compiling Windows-only crates on other platforms.

3. **Provide stubs for public APIs.** If your library exposes functions that only work on one platform, a stub that returns `Err("unsupported")` is better than a missing symbol. It lets downstream code compile everywhere while failing gracefully at runtime.

4. **`#[cfg]` is contagious.** Once one thing is gated, everything that depends on it needs gating too — or you need an alternative path. Plan your cfg boundaries at module level rather than sprinkling them line by line.

---