---
audio: false
generated: true
lang: zh
layout: post
title: 使用Shell链式操作的Rust单行代码
translated: true
type: note
---

你提到的正是许多从 Python、Ruby 或 JavaScript 等语言转来的资深开发者的共同诉求——在这些语言中，通常只需一条命令就能直接执行脚本。而 Rust 作为编译型语言，其默认工作流程略有不同。

不过，你完全可以通过在 shell 中串联命令的方式实现“一行式”操作，特别适合简单脚本或练习场景。

### 直接“一行式”方案（Shell 串联）

你已掌握核心要素：用 `rustc` 编译，用 `./` 执行。通过 shell 操作符将它们组合起来：

```bash
rustc scripts/rust/example.rs -o test/example && ./test/example
```

**说明：**

* `rustc scripts/rust/example.rs -o test/example`：编译 Rust 文件并将可执行文件输出至 `test/example`
* `&&`：这是 bash（及大多数类 Unix shell）中的**条件命令分隔符**。只有当 `&&` 前的命令成功执行（即返回退出码 0）时，后续命令才会执行。
  * 若 `rustc` 编译无误（返回 0），则自动执行 `./test/example`
  * 若 `rustc` 编译出错（返回非零退出码），则不会执行 `./test/example`。这是符合预期的行为！

### 更接近“脚本化”体验的方案（Cargo）

虽然 `&&` 串联的方式适合快速测试，但对于超越单文件脚本的简单场景，更推荐使用 Rust 的 `cargo` 工具——它确实能为项目内的代码运行提供类似 Python 的一行式操作：

1. **初始化 Cargo 项目（若尚未创建）：**
    如果你的 `scripts/rust/example.rs` 是独立文件，通常需要在其父目录（或新建专用目录）中创建 Cargo 项目。

    ```bash
    # 进入项目目录（例如 scripts/rust）
    cd scripts/rust

    # 初始化新的 Cargo 二进制项目
    cargo init --bin .
    ```

    这将创建 `Cargo.toml` 文件，并根据需要自动调整文件结构（比如将 `example.rs` 重命名为 `src/main.rs` 或修改 `Cargo.toml` 配置）。

2. **通过 Cargo 运行：**
    完成 Cargo 项目初始化后，即可用单条命令完成编译和运行：

    ```bash
    # 在项目根目录执行（例如在 scripts/rust 目录执行 cargo init 后）
    cargo run
    ```

    `cargo run` 会：
      * 编译代码（如果未编译或检测到变更）
      * 自动执行生成的可执行文件
      * 编译产物默认存放在项目的 `target/debug/` 目录，你无需关心具体路径

**推荐 Cargo 的理由：**

* **依赖管理**：当代码需要外部库（crate）时，Cargo 会自动处理下载、编译和链接，只需在 `Cargo.toml` 中声明即可
* **标准化项目结构**：倡导一致的项目布局（`src/main.rs` + `Cargo.toml`），提升代码可维护性
* **测试集成**：`cargo test` 可运行单元测试与集成测试
* **发布构建**：`cargo run --release`（或 `cargo build --release`）会启用生产级优化编译
* **自动清理**：无需手动删除编译产物，`cargo clean` 一键清理

### 能否像 Python 的 `python script.py` 实现真正“脚本化”？

Rust 并非设计成交互式脚本语言，而是编译型系统语言。因此不存在直接执行 `rust script.rs` 这种跳过显式编译环节的命令。

不过社区提供了某些工具来弥补这一缺口，实现快速单文件 Rust “脚本”执行（底层仍进行编译）：

* **`cargo-script`**：支持通过注释声明依赖，直接运行单个 `.rs` 文件的 Cargo 子命令。可通过 `cargo install cargo-script` 安装，然后使用 `cargo script scripts/rust/example.rs` 执行
* **`rust-script`**：另一款热门工具，支持直接运行 Rust 文件。通过 `cargo install rust-script` 安装后，甚至只需为 `.rs` 文件添加可执行权限（`chmod +x example.rs`）即可直接运行：`./example.rs`。该工具会在后台处理编译和执行流程

对于快速测试 `example.rs` 的需求，`rustc ... && ./...` 的串联方案完全可行，直接解决了你关于命令串联的疑问。而对于任何非简单的开发场景，采用 Cargo 工作流将是更高效且符合 Rust 惯例的选择。
