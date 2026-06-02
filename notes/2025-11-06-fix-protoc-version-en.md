---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Fix Substrait Build Protoc Version Error
translated: false
type: note
---

### Understanding the Error

This build failure is in the `substrait` crate (v0.58.0), which GreptimeDB depends on for cross-language query planning. The error stems from the protobuf compiler (`protoc`) rejecting the `substrait/algebra.proto` file because it uses "optional" fields in proto3 syntax—a feature that requires either:

- Protoc version ≥3.21 (where support is stable and no special flag is needed), or
- An older protoc (e.g., 3.15–3.20) with the `--experimental_allow_proto3_optional` flag passed during compilation.

The `prost-build` tool in `substrait`'s build script doesn't pass this flag, so it assumes a compatible protoc version. Your system's `protobuf-compiler` (likely from `apt` on Ubuntu 22.04 or earlier, giving ~3.12.4) is too old and lacks the flag, causing the panic.

GreptimeDB's docs specify protoc ≥3.15, but for this dependency, ≥3.21 is effectively required.

### Quick Fix: Upgrade Protoc to ≥3.21

The easiest, non-root way is to download and install the official binary release (no compilation needed). Here's how:

1. **Download the Latest Protoc**:
   - Go to [Protocol Buffers Releases](https://github.com/protocolbuffers/protobuf/releases).
   - Grab the latest `protoc-<version>-linux-x86_64.zip` (e.g., `protoc-28.1-linux-x86_64.zip` or whatever is current—anything ≥3.21 works).
   - Example direct link (adjust version):
     `wget https://github.com/protocolbuffers/protobuf/releases/download/v27.3/protoc-27.3-linux-x86_64.zip`

2. **Install It**:
   ```
   unzip protoc-*.zip -d protoc-install
   sudo mv protoc-install/bin/protoc /usr/local/bin/
   sudo chmod +x /usr/local/bin/protoc
   rm -rf protoc-install protoc-*.zip  # Cleanup
   ```

3. **Verify**:
   ```
   protoc --version
   ```
   Should output `libprotoc 27.3` (or higher). If it's still old, check your PATH (`echo $PATH`)—`/usr/local/bin` should come before `/usr/bin`.

4. **Retry the Build**:
   ```
   make clean  # Clears stale targets
   make
   ```

This overrides the system `protoc` without conflicting with `apt` packages. If you're on a newer distro like Ubuntu 24.04+, `apt install protobuf-compiler` might already give ≥3.21—double-check your version first.

### If You Can't Upgrade (Rare Cases)
- If stuck on an old system, you'd need to patch `substrait`'s `build.rs` to add the flag (via `Command::new(protoc).arg("--experimental_allow_proto3_optional")`), but this requires forking the crate and updating GreptimeDB's `Cargo.toml`—messy and not recommended.
- Alternatively, some crates offer a `protobuf-src` feature to bundle a recent protoc, but `substrait` doesn't enable it by default.

### Additional Tips
- Ensure other prereqs: `build-essential` (for GCC), `libc6-dev` (glibc headers).
- If the build passes but later fails on C++ deps (e.g., Arrow), install `libarrow-dev` via conda or apt.
- For CI/CD or Docker: Add the download step to your env.

This should resolve it—`substrait` compiles cleanly on modern setups. If you hit another snag, share `protoc --version` and your distro.

[GreptimeDB Build Docs](https://github.com/GreptimeTeam/greptimedb#build-from-source)
[Protobuf Releases](https://github.com/protocolbuffers/protobuf/releases)
[Proto3 Optional Fields](https://protobuf.dev/programming-guides/proto3/#optional)
