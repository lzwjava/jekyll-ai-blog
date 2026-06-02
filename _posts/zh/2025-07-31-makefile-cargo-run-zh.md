---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Cargo Run 冗余机制
translated: true
type: note
---

你说得完全正确！在你的 `Makefile` 示例中：

```makefile
run:
	cargo build
	cargo run
```

在 `cargo run` 之前包含 `cargo build` 是多余的，因为 `cargo run` 已经包含了构建步骤。当你执行 `cargo run` 时，Cargo 会自动检查项目是否需要重新构建（例如，如果源文件发生了更改），并在必要时在运行生成的二进制文件之前编译项目。这使得显式的 `cargo build` 步骤在此上下文中变得不必要。

### 说明
- **`cargo run`**：
  - 结合了 `cargo build`（将项目编译为 `target/debug/<项目名称>`）然后运行二进制文件。
  - 仅当源代码或依赖项发生更改时才会重新构建。
- **`cargo build`**：
  - 仅编译项目而不运行二进制文件。
  - 适用于希望验证编译而不执行程序的情况。

### 修复 `Makefile`
为了简化你的 `Makefile`，可以移除多余的 `cargo build`：

```makefile
run:
	cargo run
```

这实现了相同的结果：项目被构建（如果需要）然后执行。

### 何时单独使用 `cargo build`
你可能希望将 `cargo build` 作为 `Makefile` 中的独立目标，用于以下情况：
- 仅检查编译错误。
- 准备用于部署或测试的二进制文件而不执行。

例如：

```makefile
build:
	cargo build

run:
	cargo run

clean:
	cargo clean
```

- 运行 `make build` 仅进行编译。
- 运行 `make run` 进行构建（如果需要）并运行。
- 运行 `make clean` 清除构建产物。

### 解决你之前的上下文
由于你正在处理一个 Rust 项目，其中 `main.rs` 调用了 `simple.rs` 中的 `run_simple`，请确保通过将 `run_simple` 在 `src/simple.rs` 中设为公开来解决隐私错误（`E0603`）：

```rust
pub fn run_simple() {
    println!("Hello from run_simple!");
}
```

在 `src/main.rs` 中：

```rust
mod simple;

fn main() {
    simple::run_simple();
}
```

同时，按照之前讨论的，更新 `Cargo.toml` 以移除 `edition2024` 警告：

```toml
[package]
name = "example"
version = "0.1.0"
edition = "2024"
```

### 测试设置
1. 按照上述方式更新 `Makefile`。
2. 运行：
   ```bash
   make run
   ```
   这将执行 `cargo run`，构建（如果需要）并运行程序，打印 `Hello from run_simple!`（或 `run_simple` 产生的任何输出）。
3. 如果你想单独验证编译：
   ```bash
   make build
   ```

### 补充说明
- 如果你使用 `cargo run --bin simple`（用于 `simple.rs` 中的独立二进制文件），请确保 `Cargo.toml` 包含：

  ```toml
  [[bin]]
  name = "simple"
  path = "src/simple.rs"
  ```

  并且 `simple.rs` 有一个 `main` 函数：

  ```rust
  pub fn run_simple() {
      println!("Hello from run_simple!");
  }

  fn main() {
      run_simple();
  }
  ```

- 如果遇到问题，请分享 `make run` 或 `cargo run` 的输出以便进一步调试。

### 最终 `Makefile` 建议

```makefile
build:
	cargo build

run:
	cargo run

clean:
	cargo clean
```

这种设置避免了冗余，支持构建和运行，并保持工作流程清晰。如果你有更多问题或需要特定错误的帮助，请告诉我！
