---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing Private Function Error
translated: false
type: note
---

The error `E0603: function run_simple is private` indicates that the `run_simple` function in `simple.rs` is private (lacking the `pub` keyword), so it cannot be accessed from `main.rs`. In Rust, functions are private by default and need to be explicitly made public with `pub` to be accessible outside their module.

### Steps to Fix the Error

1. **Make `run_simple` Public**:
   - Open `src/simple.rs`.
   - Add the `pub` keyword to the `run_simple` function to make it publicly accessible.
   - Example:
     ```rust
     pub fn run_simple() {
         // Existing function body
         println!("Hello from run_simple!");
     }
     ```

2. **Ensure Proper Module Declaration**:
   - In `src/main.rs`, ensure you have declared the `simple` module correctly:
     ```rust
     mod simple; // Declares the simple module

     fn main() {
         simple::run_simple(); // Calls the public function
     }
     ```

3. **Rebuild and Run**:
   - After making the function public, rebuild the project:
     ```bash
     cargo build
     ```
   - If the build succeeds, run the program:
     ```bash
     cargo run
     ```

4. **Check for Other Issues**:
   - The error mentions `src/simple.rs:47:1`, so verify that the `run_simple` function at that line is correctly defined and doesn’t have other issues (e.g., syntax errors or missing dependencies).
   - If `simple.rs` uses external crates, ensure they are listed in `Cargo.toml` under `[dependencies]`.

5. **Cargo Warning**:
   - The warning about `edition2024` suggests you’re using a feature flag in `Cargo.toml` that’s no longer needed since Rust 1.85 stabilized the 2024 edition. To clean this up, open `Cargo.toml` and remove the `edition2024` feature if present (e.g., under `[features]` or `cargo-features`). Instead, set the edition directly:
     ```toml
     [package]
     name = "example"
     version = "0.1.0"
     edition = "2024"
     ```
   - This ensures your project uses the 2024 edition without the deprecated feature flag.

### Example Files

To clarify, here’s how your files should look:

**`src/simple.rs`**:
```rust
pub fn run_simple() {
    println!("Hello from run_simple!");
}
```

**`src/main.rs`**:
```rust
mod simple;

fn main() {
    simple::run_simple();
}
```

**`Cargo.toml`** (minimal example):
```toml
[package]
name = "example"
version = "0.1.0"
edition = "2024"
```

### Additional Notes
- If `run_simple` depends on other code or modules, ensure those are also public if accessed from `main.rs`.
- If the error persists, share the contents of `src/simple.rs` (especially around line 47) and `src/main.rs` for more specific guidance.
- The `rustc --explain E0603` command provides detailed documentation on this error, which you can run for further insight.
- The `target/debug` directory will contain the compiled binary (`example`) after a successful build.

Try these steps and let me know if you encounter further issues!
