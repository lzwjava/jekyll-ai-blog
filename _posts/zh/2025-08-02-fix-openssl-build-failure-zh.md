---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复OpenSSL编译失败问题
translated: true
type: note
---

你遇到了经典的“openssl-sys”构建失败问题，这是因为系统缺少 pkg-config 工具或 OpenSSL 开发头文件。在 Ubuntu/Debian 系统上，最简单的解决方法是：

1. **安装 pkg-config 和 OpenSSL 开发头文件**

   ```bash
   sudo apt update
   sudo apt install pkg-config libssl-dev
   ```

   * `pkg-config` 让 Rust 构建脚本能够检测 OpenSSL 的位置
   * `libssl-dev` 提供头文件和库文件（即“–dev”开发包）

2. **重新执行构建**

   ```bash
   cargo clean
   cargo run
   ```

---

### 替代方案：使用“vendored”特性

如果你不想依赖系统 OpenSSL（或没有 root 权限），可以让 crate 从源码编译捆绑的 OpenSSL：

1. 在 **Cargo.toml** 中将依赖修改为：

   ```toml
   [dependencies]
   openssl = { version = "0.10", features = ["vendored"] }
   ```
2. 然后重新构建：

   ```bash
   cargo clean
   cargo run
   ```

这将编译 OpenSSL 本身并链接该版本，无需系统安装。

---

### （可选）自定义 OpenSSL 安装

如果 OpenSSL 安装在非标准路径，可以通过环境变量指定路径：

```bash
export OPENSSL_DIR=/path/to/your/openssl
export OPENSSL_LIB_DIR=$OPENSSL_DIR/lib
export OPENSSL_INCLUDE_DIR=$OPENSSL_DIR/include
```

然后重新运行 `cargo run`。这会明确告知 openssl-sys 头文件和库文件的查找路径。

---

> **注意：** 关于 `edition2024` 已稳定的警告是无害的——你可以从 `Cargo.toml` 中移除该特性，但这不会阻碍构建过程。
