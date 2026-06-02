---
audio: false
generated: true
lang: zh
layout: post
title: Rust输出路径选项
translated: true
type: note
---

你提出了一个很好的问题，这涉及到 Rust 项目的典型结构和构建方式！

当你直接使用 `rustc` 时，有两个主要选项可以指定输出位置：

1.  **`-o <输出文件名>`**：此选项指定编译后的可执行文件或库的*确切路径和文件名*。

    ```bash
    rustc scripts/rust/example.rs -o test/example
    ```

    这将编译 `example.rs` 并将名为 `example` 的可执行文件直接放入 `test/` 目录。如果 `test/` 目录不存在，`rustc` 会创建它。

2.  **`--out-dir <输出目录>`**：此选项指定一个*目录*，`rustc` 应将所有生成的输出文件（可执行文件/库，以及任何中间文件，如 `.d`、`.rmeta` 等）放入该目录。

    ```bash
    rustc scripts/rust/example.rs --out-dir test/
    ```

    在这种情况下，`rustc` 将编译 `example.rs` 并将可执行文件（默认情况下命名为 `example`，源自源文件名）放入 `test/` 目录中。

**推荐：对项目使用 Cargo**

虽然直接使用 `rustc` 可以让你进行细粒度控制，但对于大多数 Rust 项目，你可能会希望使用 **Cargo**。Cargo 是 Rust 的构建系统和包管理器，它简化了依赖项管理、构建、测试和运行代码的过程。

使用 Cargo 时，输出的二进制文件通常放置在项目根目录下的 `target` 目录中。例如，如果你有一个使用 Cargo 设置的项目：

```
my_project/
├── Cargo.toml
└── src/
    └── main.rs
```

当你运行 `cargo build` 或 `cargo run` 时，编译后的可执行文件将放置在 `my_project/target/debug/my_project`（用于调试构建）或 `my_project/target/release/my_project`（用于发布构建）中。

如果你想控制 Cargo 的 `target` 目录，可以：

  * **使用 `CARGO_TARGET_DIR` 环境变量**：

    ```bash
    CARGO_TARGET_DIR=./test cargo build
    ```

    这会将整个 `target` 目录（包含 `debug`、`release` 等）放入你的 `test/` 目录中。可执行文件将位于 `test/debug/my_project`。

  * **使用 Cargo 的 `--target-dir` 命令行选项**：

    ```bash
    cargo build --target-dir test/
    ```

    这与使用环境变量的效果相同。

  * **使用 `.cargo/config.toml`**：你可以通过将其添加到 `.cargo/config.toml` 文件中，为机器上的所有 Cargo 项目或特定的工作区设置默认的 `target-dir`。

**为什么使用 Cargo？**

  * **标准化的项目布局：** Cargo 强制执行通用的项目结构，使其他 Rust 开发人员易于理解你的代码。
  * **依赖项管理：** Cargo 自动处理项目依赖项的下载和编译。
  * **测试和基准测试：** Cargo 内置了用于运行测试（`cargo test`）和基准测试（`cargo bench`）的命令。
  * **发布管理：** Cargo 有助于创建发布构建（`cargo build --release`）并将 crate 发布到 crates.io。

除非你有非常特殊的理由，否则强烈建议将你的 Rust 代码组织到 Cargo 项目中。

**根据你的 `git status` 输出：**

你的 `git status` 显示 `example` 和 `scripts/rust/` 未被跟踪。这表明你可能是在 Cargo 项目之外直接使用 `rustc` 编译 `scripts/rust/example.rs`。

如果 `example` 是编译后的二进制文件，那么之前的 `rustc scripts/rust/example.rs` 命令将其放置在了当前目录（`lzwjava.github.io`）中。

要实现将其放入 `test/example` 的目标（假设 `test` 是 `lzwjava.github.io` 根目录下的一个目录），你可以使用：

```bash
rustc scripts/rust/example.rs -o test/example
```

这是使用 `rustc` 获得你所要求的具体输出路径的最直接方法。
