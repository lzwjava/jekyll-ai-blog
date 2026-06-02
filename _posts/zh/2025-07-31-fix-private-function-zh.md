---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复私有函数错误
translated: true
type: note
---

错误 `E0603: function run_simple is private` 表明 `simple.rs` 中的 `run_simple` 函数是私有的（缺少 `pub` 关键字），因此无法从 `main.rs` 访问。在 Rust 中，函数默认是私有的，需要使用 `pub` 显式声明为公开才能在其模块外部访问。

### 解决错误的步骤

1. **将 `run_simple` 设为公开**：
   - 打开 `src/simple.rs`。
   - 在 `run_simple` 函数前添加 `pub` 关键字，使其可公开访问。
   - 示例：

     ```rust
     pub fn run_simple() {
         // 现有函数体
         println!("Hello from run_simple!");
     }
     ```

2. **确保正确声明模块**：
   - 在 `src/main.rs` 中，确保正确声明了 `simple` 模块：

     ```rust
     mod simple; // 声明 simple 模块

     fn main() {
         simple::run_simple(); // 调用公开函数
     }
     ```

3. **重新构建并运行**：
   - 将函数设为公开后，重新构建项目：

     ```bash
     cargo build
     ```

   - 如果构建成功，运行程序：

     ```bash
     cargo run
     ```

4. **检查其他问题**：
   - 错误信息提到 `src/simple.rs:47:1`，请确认该行的 `run_simple` 函数正确定义且没有其他问题（例如语法错误或缺少依赖）。
   - 如果 `simple.rs` 使用了外部 crate，请确保它们在 `Cargo.toml` 的 `[dependencies]` 中列出。

5. **Cargo 警告处理**：
   - 关于 `edition2024` 的警告表明你在 `Cargo.toml` 中使用了一个不再需要的功能标志，因为 Rust 1.85 已稳定支持 2024 edition。要清理此问题，请打开 `Cargo.toml` 并移除 `edition2024` 功能（如果存在于 `[features]` 或 `cargo-features` 中）。改为直接设置 edition：

     ```toml
     [package]
     name = "example"
     version = "0.1.0"
     edition = "2024"
     ```

   - 这确保你的项目使用 2024 edition 而无需已弃用的功能标志。

### 文件示例

为明确起见，以下是文件应有的内容：

**`src/simple.rs`**：

```rust
pub fn run_simple() {
    println!("Hello from run_simple!");
}
```

**`src/main.rs`**：

```rust
mod simple;

fn main() {
    simple::run_simple();
}
```

**`Cargo.toml`**（最小示例）：

```toml
[package]
name = "example"
version = "0.1.0"
edition = "2024"
```

### 补充说明

- 如果 `run_simple` 依赖其他代码或模块，请确保这些依赖项在从 `main.rs` 访问时也是公开的。
- 如果错误仍然存在，请分享 `src/simple.rs`（特别是第 47 行附近）和 `src/main.rs` 的内容以获取更具体的指导。
- `rustc --explain E0603` 命令提供了此错误的详细文档，你可以运行该命令以获取更多信息。
- 成功构建后，`target/debug` 目录将包含编译后的二进制文件（`example`）。

尝试这些步骤，如果遇到其他问题请告知！
