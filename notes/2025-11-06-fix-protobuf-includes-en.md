---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Fix Missing Protobuf Include Files
translated: false
type: note
---

### Understanding the Error

This failure in `greptime-proto` (pinned to commit `14b9dc40` from the GreptimeTeam repo) occurs during protobuf compilation. Specifically, `protoc` can't locate the standard Google well-known type `google/protobuf/duration.proto` (and likely others like `timestamp.proto`). This cascades into import errors in GreptimeDB's own protos (e.g., `ddl.proto` imports Duration, causing undefined type errors in `database.proto`).

The root cause: Your `protoc` installation (from the manual upgrade) only includes the binary (`/usr/local/bin/protoc`), but not the include files containing Google's core protos. `prost-build` in the crate's `build.rs` runs `protoc` without explicitly setting `--proto_path` to Google's includes, so it fails on relative imports like `"google/protobuf/duration.proto"`.

This is common with binary-only protobuf installs; the full SDK provides `/usr/include/google/protobuf/` (or equivalent).

### Quick Fix: Install Protobuf Includes

Since you already have a recent `protoc` binary, add the missing includes without downgrading:

1. **Download the Full Protobuf Release** (matching your protoc version, e.g., 27.3 or latest):

   ```
   wget https://github.com/protocolbuffers/protobuf/releases/download/v27.3/protoc-27.3-linux-x86_64.zip
   unzip protoc-27.3-linux-x86_64.zip -d protoc-full
   ```

2. **Install the Include Files**:

   ```
   sudo mkdir -p /usr/local/include/google/protobuf
   sudo cp -r protoc-full/include/google /usr/local/include/
   sudo chmod -R a+r /usr/local/include/google/protobuf  # Ensure readability
   rm -rf protoc-full protoc-*.zip  # Cleanup
   ```

3. **Verify**:
   - Check protoc: `protoc --version` (should be ≥3.21).
   - Test includes: `ls /usr/local/include/google/protobuf/duration.proto` (should exist).
   - Quick smoke test: `protoc --proto_path=/usr/local/include proto/greptime/v1/ddl.proto --decode_raw=stdin < /dev/null` (from your project dir; ignore output, just check for no "File not found").

4. **Retry the Build**:

   ```
   make clean  # Clears partial builds
   make
   ```

If you're on a distro with `apt` (e.g., Ubuntu), an alternative is `sudo apt install libprotobuf-dev`—but this might install an older version (e.g., 3.12), conflicting with your manual protoc. If so, stick to the manual include copy and set `PROTOC=/usr/local/bin/protoc` explicitly.

### Additional Tips

- If errors persist (e.g., other missing protos like `wrappers.proto`), the full `include/google/` copy should cover them.
- For containerized builds (Docker), add these steps to your Dockerfile.
- Post-build, test with `cargo run --bin greptime -- standalone start` to ensure protos integrate correctly.
- This revision of greptime-proto is recent (Oct 2024-ish); if issues linger, check for upstream fixes in the repo.

[GreptimeDB Build Docs](https://github.com/GreptimeTeam/greptimedb#build-from-source)
[Protobuf Well-Known Types](https://protobuf.dev/reference/protobuf/google.protobuf/)
