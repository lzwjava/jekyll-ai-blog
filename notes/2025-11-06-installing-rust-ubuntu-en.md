---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Installing Rust on Ubuntu
translated: false
type: note
---

### Installing Rust on Ubuntu 22.04 LTS

Rust is best installed using `rustup`, the official toolchain installer. This method is straightforward, supports easy updates, and works on your 64-bit Ubuntu 22.04 system. No additional dependencies are typically needed beyond a basic Ubuntu setup.

#### Step-by-Step Instructions

1. **Update your package list** (optional but recommended):

   ```
   sudo apt update
   ```

2. **Install Rust using rustup**:
   Run the following command to download and execute the installer script:

   ```
   curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
   ```

   - This will download the script securely via HTTPS.
   - When prompted, choose the default installation option (press `1` and Enter).
   - The installer will add Rust binaries to `~/.cargo/bin` and update your shell profile (e.g., `~/.bashrc` or `~/.profile`).

3. **Reload your shell configuration**:
   To make the changes take effect immediately without restarting your terminal:

   ```
   source ~/.cargo/env
   ```

   Alternatively, close and reopen your terminal.

4. **Verify the installation**:
   Check that Rust is installed correctly:

   ```
   rustc --version
   cargo --version
   ```

   You should see output like `rustc 1.82.0` (or the latest stable version) and similar for Cargo.

#### Additional Notes

- **Uninstalling**: If needed, run `rustup self uninstall`.
- **Updating Rust**: Use `rustup update` to get the latest version.
- **IDE/Support**: For development, consider installing `rust-analyzer` via your editor (e.g., VS Code extension) for better code completion.
- This installs the stable channel by default. For nightly or beta, use `rustup install nightly` after setup.

If you encounter any errors (e.g., curl not found), install it with `sudo apt install curl`.

[Official Rust Installation Guide](https://www.rust-lang.org/tools/install)
