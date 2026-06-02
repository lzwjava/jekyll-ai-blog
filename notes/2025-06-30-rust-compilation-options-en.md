---
audio: false
generated: true
lang: en
layout: post
title: Rust Output Location Options
translated: false
type: note
---

You're asking a great question that touches on how Rust projects are typically structured and built\!

When you use `rustc` directly, you have two main options to specify the output location:

1. **`-o <output_filename>`**: This option specifies the *exact path and filename* for the compiled executable or library.

    ```bash
    rustc scripts/rust/example.rs -o test/example
    ```

    This will compile `example.rs` and place the executable named `example` directly into the `test/` directory. If `test/` doesn't exist, `rustc` will create it.

2. **`--out-dir <output_directory>`**: This option specifies a *directory* where `rustc` should place all generated output files (the executable/library, along with any intermediate files like `.d`, `.rmeta`, etc.).

    ```bash
    rustc scripts/rust/example.rs --out-dir test/
    ```

    In this case, `rustc` will compile `example.rs` and place the executable (which will be named `example` by default, derived from the source file name) inside the `test/` directory.

**Recommendation: Use Cargo for Projects**

While `rustc` directly gives you fine-grained control, for most Rust projects, you'll want to use **Cargo**. Cargo is Rust's build system and package manager, and it simplifies managing dependencies, building, testing, and running your code.

With Cargo, the output binaries are typically placed in a `target` directory within your project root. For example, if you have a project set up with Cargo:

```
my_project/
├── Cargo.toml
└── src/
    └── main.rs
```

When you run `cargo build` or `cargo run`, the compiled executable will be placed in `my_project/target/debug/my_project` (for debug builds) or `my_project/target/release/my_project` (for release builds).

If you want to control the `target` directory for Cargo, you can:

* **`CARGO_TARGET_DIR` environment variable**:

    ```bash
    CARGO_TARGET_DIR=./test cargo build
    ```

    This will place the entire `target` directory (containing `debug`, `release`, etc.) inside your `test/` directory. The executable would then be at `test/debug/my_project`.

* **`--target-dir` command-line option for Cargo**:

    ```bash
    cargo build --target-dir test/
    ```

    This does the same as the environment variable.

* **`.cargo/config.toml`**: You can set a default `target-dir` for all Cargo projects on your machine or for a specific workspace by adding it to a `.cargo/config.toml` file.

**Why use Cargo?**

* **Standardized Project Layout:** Cargo enforces a common project structure, making it easy for other Rust developers to understand your code.
* **Dependency Management:** Cargo handles downloading and compiling your project's dependencies automatically.
* **Testing and Benchmarking:** Cargo has built-in commands for running tests (`cargo test`) and benchmarks (`cargo bench`).
* **Release Management:** Cargo helps with creating release builds (`cargo build --release`) and publishing crates to crates.io.

Unless you have a very specific reason not to, it's highly recommended to organize your Rust code into a Cargo project.

**Given your `git status` output:**

Your `git status` shows `example` and `scripts/rust/` as untracked. This suggests you might be compiling `scripts/rust/example.rs` directly with `rustc` outside of a Cargo project.

If `example` is the compiled binary, then the previous `rustc scripts/rust/example.rs` command placed it in the current directory (`lzwjava.github.io`).

To achieve your goal of putting it in `test/example` (assuming `test` is a directory at the root of `lzwjava.github.io`), you would use:

```bash
rustc scripts/rust/example.rs -o test/example
```

This is the most direct way to get the specific output path you asked for using `rustc`.
