---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用Cargo编译示例
translated: true
type: note
---

要让你的示例代码成功编译，你需要：

1. **在 `Cargo.toml` 中声明**所使用的依赖包
2. **提供 `main` 函数**（如果使用异步请求，还需提供运行时）
3. **移除**现已不必要的 `edition2024` 特性标志

---

### 1. 更新 `Cargo.toml`

```toml
[package]
name = "example"
version = "0.1.0"
edition = "2024"        # 选择当前版本；无需特性标志

[dependencies]
# 用于 `#[tokio::main]` 的异步运行时
tokio = { version = "1.28", features = ["macros", "rt-multi-thread"] }

# 支持 JSON 功能的 HTTP 客户端
reqwest = { version = "0.11", features = ["json"] }

# 用于（反）序列化的 Serde
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
```

> **注意：** 移除任何包含 `edition2024` 的 `[features]` 部分——自 Cargo 1.85 起该功能已内置。

---

### 2. 提供异步 `main` 函数

如需使用 `reqwest::Client`（异步模式），请将代码包装在 Tokio 运行时中：

```rust
// src/main.rs
use reqwest::{Client, StatusCode};
use serde_json::{json, Value};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // 创建客户端实例
    let client = Client::new();

    // 示例 GET 请求
    let res = client
        .get("https://httpbin.org/status/200")
        .send()
        .await?;

    println!("状态码: {}", res.status());

    // 示例 JSON 响应体
    let body: Value = res.json().await?;
    println!("JSON 响应: {}", body);

    Ok(())
}
```

---

### 3. （替代方案）使用阻塞式 reqwest

如果不需要异步或 Tokio，可改用 `reqwest::blocking` 并移除 tokio 依赖：

```rust
// 在 Cargo.toml 中移除 tokio，将 reqwest 修改为：
reqwest = { version = "0.11", features = ["blocking", "json"] }

// src/main.rs:
use reqwest::blocking::Client;
use serde_json::Value;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = Client::new();
    let res = client.get("https://httpbin.org/status/200").send()?;
    println!("状态码: {}", res.status());
    let body: Value = res.json()?;
    println!("JSON 响应: {}", body);
    Ok(())
}
```

完成上述修改后，运行 `cargo build`（及后续的 `cargo run`）即可成功编译。
