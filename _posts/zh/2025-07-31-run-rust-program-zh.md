---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 从目录运行Rust程序
translated: true
type: note
---

要从您提供的目录结构中运行一个简单的 Rust 程序，看起来您正在处理一个 Rust 项目（`lzwjava.github.io/rust`），其中包含 `src` 文件夹，内有 `main.rs` 和 `simple.rs` 文件。以下是运行简单 Rust 程序的方法，假设您要执行 `main.rs` 或 `simple.rs` 中的代码。

### 运行 Rust 程序的步骤

1. **检查项目结构**：
   - 您的项目包含 `Cargo.toml` 文件，表明这是一个由 Cargo（Rust 的构建工具）管理的 Rust 项目。
   - `src/main.rs` 文件是 Rust 二进制应用程序的默认入口点。
   - `simple.rs` 文件可能是一个模块或其他源文件，但除非在 `main.rs` 中引用或在 `Cargo.toml` 中配置为二进制文件，否则无法直接运行。

2. **使用 Cargo 运行程序**：
   - 如果要运行 `src/main.rs` 中的代码，请在项目根目录（`~/projects/lzwjava.github.io/rust`）中使用以下命令：
     ```bash
     cargo run
     ```
     此命令：
     - 编译项目（解析依赖项并构建代码）。
     - 执行从 `src/main.rs` 生成的二进制文件。
     - 输出将显示在终端中。

3. **如果要运行 `simple.rs`**：
   - 默认情况下，Cargo 期望主入口点为 `src/main.rs`。如果 `simple.rs` 是一个模块，您需要在 `main.rs` 中引用它。例如，在 `src/main.rs` 中：
     ```rust
     mod simple; // 声明 simple 模块

     fn main() {
         simple::some_function(); // 调用 simple.rs 中的函数
     }
     ```
     然后如上所述运行 `cargo run`。
   - 如果 `simple.rs` 是独立的二进制文件，您需要在 `Cargo.toml` 中配置它。在 `Cargo.toml` 中添加以下内容：
     ```toml
     [[bin]]
     name = "simple"
     path = "src/simple.rs"
     ```
     然后运行：
     ```bash
     cargo run --bin simple
     ```

4. **替代方法：不使用 Cargo 运行**：
   - 如果要编译并运行单个文件（例如 `simple.rs`）而不使用 Cargo，请确保该文件包含 `main` 函数，并使用 `rustc` 编译器：
     ```bash
     rustc src/simple.rs
     ./simple
     ```
     这将在当前目录中生成名为 `simple` 的可执行文件并运行它。注意：此方法不处理依赖项，因此仅适用于简单、自包含的程序。

5. **检查错误**：
   - 如果遇到错误，请确保：
     - 已安装 Rust 和 Cargo（使用 `rustc --version` 和 `cargo --version` 验证）。
     - `Cargo.toml` 正确配置了必要的依赖项。
     - `main.rs` 或 `simple.rs` 中的代码包含有效的 `fn main()` 函数。
   - 运行 `cargo check` 以在不构建二进制文件的情况下验证代码：
     ```bash
     cargo check
     ```

6. **示例 `simple.rs`**：
   如果 `simple.rs` 包含类似以下内容：
   ```rust
   fn main() {
       println!("Hello from simple!");
   }
   ```
   并且您已在 `Cargo.toml` 中将其添加为二进制文件，运行 `cargo run --bin simple` 将打印 `Hello from simple!`。

### 注意事项
- `target/debug` 目录包含编译后的产物。您可以直接使用 `./target/debug/<项目名称>` 运行二进制文件（将 `<项目名称>` 替换为 `Cargo.toml` 中的名称），但推荐使用 `cargo run`，因为它处理编译和执行。
- 如果 `simple.rs` 是一个模块，请确保通过 `mod simple;` 正确集成到 `main.rs` 中。
- 对于更复杂的设置或 `simple.rs` 中的特定代码，请分享 `simple.rs` 或 `Cargo.toml` 的内容以获得针对性指导。

如果您对“在此处运行 simple”有特定含义（例如特定函数或配置），请提供更多详细信息，我将进一步完善答案！
