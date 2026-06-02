---
audio: false
generated: true
lang: en
layout: post
title: Rust One-Liner with Shell Chaining
translated: false
type: note
---

You're hitting on a common desire for experienced developers coming from languages like Python, Ruby, or JavaScript, where you often have a single command to execute a script directly. Rust, being a compiled language, has a slightly different workflow by default.

However, you can definitely achieve a "one-liner" feel, especially for simple scripts or exercises, by chaining commands in your shell.

### The Direct "One-Liner" (Shell Chaining)

You already have the components: `rustc` for compilation and `./` for execution. You can combine them using shell operators:

```bash
rustc scripts/rust/example.rs -o test/example && ./test/example
```

**Explanation:**

* `rustc scripts/rust/example.rs -o test/example`: This compiles your Rust file and places the executable at `test/example`.
* `&&`: This is a **conditional command separator** in bash (and most Unix-like shells). The command *after* `&&` will only execute if the command *before* `&&` successfully completes (i.e., returns an exit code of 0).
  * If `rustc` compiles without errors, it will return 0, and then `./test/example` will run.
  * If `rustc` encounters a compilation error, it will return a non-zero exit code, and `./test/example` will *not* be executed. This is good behavior\!

### For a More "Script-like" Experience (Cargo)

While the above `&&` approach works well for quick tests, for anything beyond trivial single-file scripts, Rust's `cargo` tool is the recommended way to go, and it *does* provide a Python-like one-liner for running code within a project:

1. **Initialize a Cargo Project (if you haven't already):**
    If your `scripts/rust/example.rs` is just a standalone file, you'd typically start by creating a Cargo project in its parent directory (or a new dedicated directory).

    ```bash
    # Go to the directory where you want your project (e.g., scripts/rust)
    cd scripts/rust

    # Initialize a new Cargo binary project
    cargo init --bin .
    ```

    This will create `Cargo.toml` and move your `example.rs` (if it was `main.rs`) or adjust the `Cargo.toml` to point to it (if you rename `example.rs` to `main.rs` within `src/`).

2. **Run with Cargo:**
    Once you have a Cargo project set up, you can compile and run with a single command:

    ```bash
    # From your project root (e.g., scripts/rust if you ran cargo init there)
    cargo run
    ```

    `cargo run` will:

      * Compile your code (if it hasn't been compiled or if changes have been made).
      * Then, execute the resulting binary.
      * By default, the binary is placed in `target/debug/` within your project, but you don't have to worry about its specific path.

**Why Cargo is preferred:**

* **Dependency Management:** If your code ever needs external libraries (crates), Cargo handles fetching, compiling, and linking them automatically. You specify them in `Cargo.toml`.
* **Standard Project Structure:** It encourages a consistent layout (`src/main.rs`, `Cargo.toml`), which makes your code easier for others (and future you) to understand.
* **Testing:** `cargo test` runs your unit and integration tests.
* **Release Builds:** `cargo run --release` (or `cargo build --release`) compiles with optimizations for production.
* **No Manual Cleanup:** You don't have to manually delete compiled binaries. `cargo clean` takes care of it.

### What about a true "Scripting" approach like Python's `python script.py`?

Rust isn't designed as an interpreted scripting language. It's a compiled systems language. So, you won't get a direct `rust script.rs` command that compiles and runs without an explicit compilation step.

However, there are community tools that try to bridge this gap for quick, single-file Rust "scripts" (though they are still compiling under the hood):

* **`cargo-script`**: A Cargo subcommand that allows you to run single `.rs` files, handling dependencies if specified via comments. You'd typically install it with `cargo install cargo-script`. Then you could potentially run `cargo script scripts/rust/example.rs`.
* **`rust-script`**: Another popular tool for running Rust files directly like scripts. Install it via `cargo install rust-script`. Then, you can often just make your `.rs` file executable (`chmod +x example.rs`) and run it: `./example.rs`. It handles the compilation and execution in the background.

For your use case of quickly testing `example.rs`, the `rustc ... && ./...` one-liner is perfectly fine and directly answers your question about chaining the two commands. For any non-trivial development, embracing Cargo will be a more productive and idiomatic Rust experience.
