---
audio: false
generated: true
image: false
lang: en
layout: post
title: Running Rust Program from Directory
translated: false
type: note
---

To run a simple Rust program from the directory structure you provided, it looks like you're working in a Rust project (`lzwjava.github.io/rust`) with a `src` folder containing `main.rs` and `simple.rs`. Here's how you can run a simple Rust program, assuming you want to execute the code in `main.rs` or `simple.rs`.

### Steps to Run a Rust Program

1. **Check the Project Structure**:
   - Your project has a `Cargo.toml` file, indicating it's a Rust project managed by Cargo, Rust's build tool.
   - The `src/main.rs` file is the default entry point for a Rust binary application.
   - The `simple.rs` file is likely a module or another source file, but it won't run directly unless it's referenced in `main.rs` or configured as a binary in `Cargo.toml`.

2. **Run the Program Using Cargo**:
   - If you want to run the code in `src/main.rs`, use the following command from the project root (`~/projects/lzwjava.github.io/rust`):
     ```bash
     cargo run
     ```
     This command:
     - Compiles the project (resolving dependencies and building the code).
     - Executes the binary generated from `src/main.rs`.
     - The output will appear in the terminal.

3. **If You Want to Run `simple.rs`**:
   - By default, Cargo expects the main entry point to be `src/main.rs`. If `simple.rs` is a module, you need to reference it in `main.rs`. For example, in `src/main.rs`:
     ```rust
     mod simple; // Declares the simple module

     fn main() {
         simple::some_function(); // Call a function from simple.rs
     }
     ```
     Then run `cargo run` as above.
   - If `simple.rs` is meant to be a standalone binary, you need to configure it in `Cargo.toml`. Add the following to `Cargo.toml`:
     ```toml
     [[bin]]
     name = "simple"
     path = "src/simple.rs"
     ```
     Then run:
     ```bash
     cargo run --bin simple
     ```

4. **Alternative: Run Without Cargo**:
   - If you want to compile and run a single file (e.g., `simple.rs`) without Cargo, ensure it has a `main` function and use the `rustc` compiler:
     ```bash
     rustc src/simple.rs
     ./simple
     ```
     This generates an executable named `simple` in the current directory and runs it. Note: This approach doesn't handle dependencies, so it's only suitable for simple, self-contained programs.

5. **Check for Errors**:
   - If you encounter errors, ensure:
     - Rust and Cargo are installed (`rustc --version` and `cargo --version` to verify).
     - `Cargo.toml` is correctly configured with necessary dependencies.
     - The code in `main.rs` or `simple.rs` has a valid `fn main()` function.
   - Run `cargo check` to verify the code without building the binary:
     ```bash
     cargo check
     ```

6. **Example `simple.rs`**:
   If `simple.rs` contains something like:
   ```rust
   fn main() {
       println!("Hello from simple!");
   }
   ```
   And you’ve added it as a binary in `Cargo.toml`, running `cargo run --bin simple` will print `Hello from simple!`.

### Notes
- The `target/debug` directory contains compiled artifacts. You can run the binary directly with `./target/debug/<project_name>` (replace `<project_name>` with the name in `Cargo.toml`), but `cargo run` is preferred as it handles compilation and execution.
- If `simple.rs` is a module, ensure it’s correctly integrated into `main.rs` with `mod simple;`.
- For more complex setups or specific code in `simple.rs`, share the contents of `simple.rs` or `Cargo.toml` for tailored guidance.

If you meant something specific by "run simple here" (e.g., a specific function or configuration), please provide more details, and I’ll refine the answer!
