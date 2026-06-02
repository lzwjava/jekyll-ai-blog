---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cargo Run Redundancy
translated: false
type: note
---

You’re absolutely correct! In your `Makefile` example:

```makefile
run:
 cargo build
 cargo run
```

Including `cargo build` before `cargo run` is redundant because `cargo run` already includes the build step. When you execute `cargo run`, Cargo automatically checks if the project needs to be rebuilt (e.g., if source files have changed) and, if necessary, compiles the project before running the resulting binary. This makes the explicit `cargo build` step unnecessary in this context.

### Clarification

- **`cargo run`**:
  - Combines `cargo build` (compiles the project into `target/debug/<project_name>`) and then runs the binary.
  - Only rebuilds if there are changes in the source code or dependencies.
- **`cargo build`**:
  - Only compiles the project without running the binary.
  - Useful if you want to verify compilation without executing the program.

### Fixing the `Makefile`

To streamline your `Makefile`, you can remove the redundant `cargo build`:

```makefile
run:
 cargo run
```

This achieves the same result: the project is built (if needed) and then executed.

### When to Use `cargo build` Separately

You might want to keep `cargo build` as a separate target in the `Makefile` for cases where you only want to compile without running, such as:

- Checking for compilation errors.
- Preparing binaries for deployment or testing without execution.

For example:

```makefile
build:
 cargo build

run:
 cargo run

clean:
 cargo clean
```

- Run `make build` to compile only.
- Run `make run` to build (if needed) and run.
- Run `make clean` to clear build artifacts.

### Addressing Your Previous Context

Since you’re working with a Rust project where `main.rs` calls `run_simple` from `simple.rs`, ensure the privacy error (`E0603`) is resolved by making `run_simple` public in `src/simple.rs`:

```rust
pub fn run_simple() {
    println!("Hello from run_simple!");
}
```

And in `src/main.rs`:

```rust
mod simple;

fn main() {
    simple::run_simple();
}
```

Also, update `Cargo.toml` to remove the `edition2024` warning, as discussed earlier:

```toml
[package]
name = "example"
version = "0.1.0"
edition = "2024"
```

### Testing the Setup

1. Update the `Makefile` as shown above.
2. Run:

   ```bash
   make run
   ```

   This will execute `cargo run`, which builds (if needed) and runs the program, printing `Hello from run_simple!` (or whatever output `run_simple` produces).
3. If you want to verify compilation separately:

   ```bash
   make build
   ```

### Additional Notes

- If you’re using `cargo run --bin simple` (for a separate binary in `simple.rs`), ensure `Cargo.toml` includes:

  ```toml
  [[bin]]
  name = "simple"
  path = "src/simple.rs"
  ```

  And `simple.rs` has a `main` function:

  ```rust
  pub fn run_simple() {
      println!("Hello from run_simple!");
  }

  fn main() {
      run_simple();
  }
  ```

- If you encounter issues, share the output of `make run` or `cargo run` for further debugging.

### Final `Makefile` Recommendation

```makefile
build:
 cargo build

run:
 cargo run

clean:
 cargo clean
```

This setup avoids redundancy, supports both building and running, and keeps your workflow clean. Let me know if you have more questions or need help with specific errors!
