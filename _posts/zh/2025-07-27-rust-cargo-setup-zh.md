---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复Rust项目配置
translated: true
type: note
---

看起来你正在尝试基于提供的 `Cargo.toml` 代码片段和文件结构（包含 `example.rs` 的 `rust` 子目录）来设置并运行一个简单的 Rust 项目。但存在几个问题导致无法直接运行：

- 目录 `/Users/lzwjava/projects/lzwjava.github.io`（你的 GitHub Pages 根目录）似乎尚未配置为有效的 Rust 工作空间，这就是之前 rust-analyzer 失败的原因。
- `Cargo.toml` 中的 `edition = "2025"` 无效——Rust 目前的版本有 2015、2018、2021 和 2024（2025 年初发布）。没有 2025 版本可用。
- 由 Cargo 管理的 Rust 项目需要标准结构：根目录下的 `Cargo.toml`，源文件放在 `src/` 子目录中（例如，二进制可执行文件为 `src/main.rs`）。你的 `example.rs` 在 `rust/` 子目录中，默认情况下无法识别。
- 假设 `example.rs` 包含一个简单的可执行程序（例如带有 `fn main()` 的 "Hello, World!"），你有两个主要选择：将其作为单文件脚本运行（无需 Cargo）或设置为适当的 Cargo 项目。

我将逐步引导你完成这两种方法。在你的项目根目录（`lzwjava.github.io`）中使用终端。

### 选项 1：作为单文件脚本运行（最快，无需 Cargo）
这种方法直接使用 Rust 编译器（`rustc`）编译并运行 `example.rs`。如果你不需要依赖项或完整的项目设置，这很理想。

1. 导航到包含文件的目录：
   ```
   cd rust
   ```

2. 编译文件：
   ```
   rustc example.rs
   ```
   - 这会生成一个名为 `example`（在 macOS/Linux 上）或 `example.exe`（在 Windows 上）的可执行文件。
   - 如果编译失败（例如，由于 `example.rs` 中的语法错误），请修复代码并重试。

3. 运行可执行文件：
   ```
   ./example
   ```
   - 输出将取决于 `example.rs` 中的内容（例如，"Hello, World!"）。

如果 `example.rs` 是一个库（没有 `fn main()`），此方法将无效——请改用项目设置中的 `cargo test`。

### 选项 2：设置为 Cargo 项目并运行（推荐用于 rust-analyzer 和可扩展性）
这种方法通过创建有效的工作空间来解决 rust-analyzer 错误。它还允许使用 `cargo run` 来更轻松地构建/运行。

1. 创建或移动到专用的项目目录（以避免弄乱你的 GitHub Pages 根目录）：
   ```
   mkdir rust_project
   cd rust_project
   ```
   - 如果你坚持使用现有的 `rust` 目录，请改为 `cd rust` 并继续。

2. 使用你提供的内容创建 `Cargo.toml`，但修正版本：
   ```
   [package]
   name = "example"
   version = "0.1.0"
   edition = "2024"  # 从无效的 "2025" 更改而来
   authors = ["lzwjava@gmail.com"]
   description = "一个简单的 Rust 示例项目"

   [dependencies]
   ```
   - 将此文件保存为当前目录中的 `Cargo.toml`。

3. 设置源目录并移动你的文件：
   ```
   mkdir src
   mv ../rust/example.rs src/main.rs  # 如果需要，调整路径；将其重命名为 main.rs 以用于二进制执行
   ```
   - 如果 `example.rs` 不是主要的入口点，请将其重命名为 `lib.rs`，并在 `Cargo.toml` 中添加 `[lib]` 以用于库 crate。

4. 构建项目：
   ```
   cargo build
   ```
   - 这会下载任何需要的 crate（此处没有）并进行编译。如果失败，请检查 `src/main.rs` 中的错误。

5. 运行项目：
   ```
   cargo run
   ```
   - 这会在需要时构建并执行 `src/main.rs`。

6. 解决 VS Code（或类似编辑器）中的 rust-analyzer 错误：
   - 将 `rust_project` 文件夹作为你的工作空间根目录打开（**文件 > 打开文件夹**）。
   - 重新加载窗口（**Cmd+Shift+P** > **开发者: 重新加载窗口**）。
   - rust-analyzer 现在应该通过 `Cargo.toml` 检测到项目。

### 故障排除提示
- **如果未安装 `cargo`**：运行 `rustup update`（假设你通过 rustup 安装了 Rust）。如果没有，请从 https://rustup.rs/ 安装 Rust。
- **版本错误**：如果你保留 "2025"，Cargo 会报错："error: invalid edition: '2025'"。请坚持使用 "2024"。
- **`example.rs` 中没有 `fn main()`**：添加一个，例如：
  ```
  fn main() {
      println!("Hello, World!");
  }
  ```
- **需要依赖项？**：在 `Cargo.toml` 的 `[dependencies]` 下添加它们，例如 `rand = "0.8"`，然后运行 `cargo build`。
- **rust-analyzer 仍然失败？**：确保你的编辑器 Rust 扩展已更新，并且如果项目在子目录中，请将 `"rust-analyzer.linkedProjects": ["./Cargo.toml"]` 添加到你的工作空间 `settings.json` 中。
- 对于更复杂的设置（例如，多个 crate），使用 `cargo new --bin example` 生成模板。

如果这与你的设置不匹配（例如，提供 `example.rs` 的内容或更多细节），请告诉我以获取更精确的步骤。

[宣布 Rust 1.88.0](https://blog.rust-lang.org/2025/06/26/Rust-1.88.0/)
[Rust | endoflife.date](https://endoflife.date/rust)
