---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing OpenSSL Build Failure
translated: false
type: note
---

You’re running into the classic “openssl-sys” build failure because you don’t have the system’s pkg-config tool or the OpenSSL development headers installed. On Ubuntu/Debian, the simplest fix is:

1. **Install pkg-config and OpenSSL dev-headers**

   ```bash
   sudo apt update
   sudo apt install pkg-config libssl-dev
   ```

   * `pkg-config` lets the Rust build script detect where OpenSSL is.
   * `libssl-dev` provides the headers & libs (the “–dev” package).

2. **Re-run your build**

   ```bash
   cargo clean
   cargo run
   ```

---

### Alternative: use the “vendored” feature

If you don’t want to rely on system OpenSSL (or you lack root access), you can ask the crate to build a bundled copy of OpenSSL from source:

1. In your **Cargo.toml**, change your dependency to:

   ```toml
   [dependencies]
   openssl = { version = "0.10", features = ["vendored"] }
   ```
2. Then build again:

   ```bash
   cargo clean
   cargo run
   ```

This will compile OpenSSL itself and link against that, avoiding the need for a system install.

---

### (Optional) Custom OpenSSL install

If you have OpenSSL installed in a non-standard location, you can point the build to it:

```bash
export OPENSSL_DIR=/path/to/your/openssl
export OPENSSL_LIB_DIR=$OPENSSL_DIR/lib
export OPENSSL_INCLUDE_DIR=$OPENSSL_DIR/include
```

Then re-run `cargo run`. This tells openssl-sys exactly where to find headers and libraries.

---

> **Note:** The warning about `edition2024` being stabilized is harmless—you can remove that feature from your `Cargo.toml`, but it won’t block your build.
