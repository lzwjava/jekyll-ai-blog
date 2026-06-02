---
audio: false
generated: true
lang: zh
layout: post
title: 在 macOS 上使用 rustup 安装 Rust
translated: true
type: note
---

## 使用 rustup 安装 Rust

1. **打开终端**
    您可以在**应用程序 > 实用工具**中找到终端，或使用 Spotlight 搜索。

2. **安装 rustup 和 Rust**
    运行以下命令下载并执行 rustup 安装脚本：

    ```sh
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
    ```

    脚本将提示您继续操作。按 `1` 选择默认安装。

3. **配置 Shell 环境**
    安装完成后，您可能需要将 Rust 添加到系统 `PATH` 中。安装程序会提供类似以下的命令：

    ```sh
    source $HOME/.cargo/env
    ```

    将此行添加到您的 Shell 配置文件（例如 `.zshrc`、`.bashrc` 或 `.bash_profile`）中，以便在后续会话中使用 Rust。

4. **验证安装**
    检查 Rust 是否安装正确：

    ```sh
    rustc --version
    ```

    如果安装成功，您将看到 Rust 编译器版本信息。

---

## 使用 Homebrew 安装 Rust

您也可以使用 [Homebrew](https://brew.sh/) 安装 Rust，但通常推荐使用 `rustup` 以便更轻松地更新和管理版本。

1. **安装 Homebrew**（如果尚未安装）：

    ```sh
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```

2. **通过 Homebrew 安装 Rust**：

    ```sh
    brew install rust
    ```

3. **验证安装**：

    ```sh
    rustc --version
    ```

---

## 编译 Rust 代码

1. **编写 Rust 程序**
    创建一个名为 `main.rs` 的文件，内容如下：

    ```rust
    fn main() {
         println!("Hello, World!");
    }
    ```

2. **编译程序**
    在终端中，导航到包含该文件的目录并运行：

    ```sh
    rustc main.rs
    ```

3. **运行编译后的程序**：

    ```sh
    ./main
    ```

---

以上设置将帮助您在 macOS 上开始 Rust 开发。如果遇到任何问题，欢迎随时提问！
