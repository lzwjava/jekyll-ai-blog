---
audio: false
generated: true
image: false
lang: en
layout: post
title: Compile Example with Cargo
translated: false
type: note
---

To get your example compiling, you need to:

1. **Declare the crates** you’re using in `Cargo.toml`
2. **Provide a `main` function** (and a runtime, if you’re using async requests)
3. **Remove** the now‐unnecessary `edition2024` feature flag

---

### 1. Update `Cargo.toml`

```toml
[package]
name = "example"
version = "0.1.0"
edition = "2024"        # pick the current edition; no need for a feature flag

[dependencies]
# Async runtime for `#[tokio::main]`
tokio = { version = "1.28", features = ["macros", "rt-multi-thread"] }

# HTTP client with JSON support
reqwest = { version = "0.11", features = ["json"] }

# Serde for (de)serialization
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
```

> **Note:** Remove any `[features]` section that lists `edition2024` — it’s built in as of Cargo 1.85.

---

### 2. Provide an async `main`

If you want to use `reqwest::Client` (async), wrap your code in Tokio’s runtime:

```rust
// src/main.rs
use reqwest::{Client, StatusCode};
use serde_json::{json, Value};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Build a client
    let client = Client::new();

    // Example GET
    let res = client
        .get("https://httpbin.org/status/200")
        .send()
        .await?;

    println!("Status: {}", res.status());

    // Example JSON body
    let body: Value = res.json().await?;
    println!("JSON response: {}", body);

    Ok(())
}
```

---

### 3. (Alternative) Use blocking reqwest

If you don’t want async or Tokio, switch to `reqwest::blocking` and drop the `tokio` dependency:

```rust
// In Cargo.toml, remove tokio and change reqwest to:
reqwest = { version = "0.11", features = ["blocking", "json"] }

// src/main.rs:
use reqwest::blocking::Client;
use serde_json::Value;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = Client::new();
    let res = client.get("https://httpbin.org/status/200").send()?;
    println!("Status: {}", res.status());
    let body: Value = res.json()?;
    println!("JSON response: {}", body);
    Ok(())
}
```

With those changes, running `cargo build` (and then `cargo run`) should succeed.
