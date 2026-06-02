---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Rust Crates 与私有注册表详解
translated: true
type: note
---

**问题：** Rust 的 crate 生态系统是如何运作的？Crates.io 是什么？企业如何托管和使用私有 crate 注册中心？

**答案：**

## Rust Crates — 从基本原理说起

### 什么是 Crate？

**crate** 是 Rust 的编译单元——`rustc` 编译的最小单位。分为两种：

- **二进制 crate** —— 包含 `main()`，生成可执行文件
- **库 crate** —— 不含 `main()`，生成 `.rlib`（或 `.so`/`.a`）供其他 crate 链接

**package** 是 Cargo 管理的单位——一个 `Cargo.toml` 文件，内部可以包含一个或多个 crate。

```
my-package/
├── Cargo.toml        # 包元数据 + 依赖清单
├── src/
│   ├── main.rs       # 二进制 crate 根
│   └── lib.rs        # 库 crate 根（可选）
└── tests/
    └── integration.rs
```

---

### Cargo 如何解析依赖

```toml
# Cargo.toml
[dependencies]
serde = { version = "1.0", features = ["derive"] }
tokio = { version = "1", features = ["full"] }
```

Cargo 执行**语义化版本感知的解析**：

1. 读取整个 workspace 中的 `Cargo.toml`
2. 构建**依赖图**（DAG）
3. 运行**SAT 求解器**（PubGrub 算法）寻找兼容版本
4. 将精确解写入 `Cargo.lock`
5. 从注册中心下载 `.crate` 压缩包
6. 按依赖顺序编译

`Cargo.lock` 锁定精确的 SHA——保证构建可重现。对于二进制项目请提交到版本控制，对于库项目请忽略。

---

### crates.io — 公共注册中心

`crates.io` 是官方的**稀疏注册中心**（自 Cargo 1.68+ 起）。协议如下：

```
# 旧版（基于 Git 的索引，速度慢）
https://github.com/rust-lang/crates.io-index

# 新版稀疏索引（HTTP，速度快）
https://index.crates.io/
```

当你执行 `cargo add serde` 时，Cargo：
1. 获取 `https://index.crates.io/se/rd/serde` —— 一个 JSON 文件，列出所有版本、yanked 状态和校验和
2. 根据语义化版本约束选取最佳版本
3. 下载 `https://static.crates.io/crates/serde/1.0.193/download`
4. 验证 SHA-256 校验和
5. 解压到 `~/.cargo/registry/src/`

---

### 发布到 crates.io

```bash
cargo login <你的API令牌>    # 从 crates.io 账号获取
cargo publish --dry-run         # 试运行
cargo publish                   # 上传压缩包并更新索引
```

一旦发布，crate 便是**不可变的**——你只能 `yank`（软删除，现有用户不受影响，新解析被阻止）。

---

## 企业级私有注册中心

这一部分在实际中非常重要。主要有三种选择：

### 1. Cloudsmith / Artifactory / Gemfury（SaaS）

托管的私有注册中心。企业中 JFrog Artifactory 最为常见：

```toml
# .cargo/config.toml
[registries]
my-company = { index = "sparse+https://artifactory.mycompany.com/artifactory/api/cargo/rust-local/index/" }

[net]
git-fetch-with-cli = true
```

```toml
# Cargo.toml
[dependencies]
internal-sdk = { version = "0.1", registry = "my-company" }
```

认证通过 `~/.cargo/credentials.toml`：
```toml
[registries.my-company]
token = "Bearer eyJ..."
```

### 2. Kellnr — 自托管开源方案

[Kellnr](https://kellnr.io) 是最流行的**自托管**选项。使用 Rust 编写，支持稀疏协议。

```bash
docker run -d \
  -p 8000:8000 \
  -v kellnr_data:/opt/kellnr/data \
  -e KELLNR_ORIGIN__HOSTNAME=registry.internal \
  ghcr.io/kellnr/kellnr:latest
```

然后在配置中：
```toml
[registries]
kellnr = { index = "sparse+http://registry.internal:8000/api/v1/crates/index/" }
```

### 3. Gitea / Forgejo（内置 Cargo 注册中心）

Gitea 1.21+ 支持**原生 Cargo 注册中心**——如果你已运行 Gitea 作为 Git 托管服务，无需额外服务：

```toml
[registries]
gitea = { index = "sparse+https://gitea.mycompany.com/api/packages/{owner}/cargo/index/" }
```

---

### 工作区 Monorepo 模式（企业标准）

大型企业使用 **Cargo workspace** 管理多个内部 crate：

```
company-platform/
├── Cargo.toml          # 工作区根
├── Cargo.lock          # 统一的锁定文件
├── crates/
│   ├── auth/           # 内部库
│   ├── db-client/      # 内部库
│   ├── api-server/     # 二进制
│   └── cli-tool/       # 二进制
```

```toml
# 工作区 Cargo.toml
[workspace]
members = ["crates/*"]
resolver = "2"

[workspace.dependencies]
# 在整个工作区中统一锁定版本
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }
```

每个成员的 `Cargo.toml` 继承：
```toml
[dependencies]
tokio = { workspace = true }
```

---

### Vendoring — 离线 / 合规环境

银行尤其需要——CI 期间没有互联网访问：

```bash
cargo vendor                    # 将全部依赖下载到 ./vendor/
```

生成 `vendor/` 目录及配置片段：
```toml
# .cargo/config.toml（自动生成）
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
```

将 `vendor/` 提交到 git。CI 构建时零网络访问，供应链完全可审计。

---

### 供应链安全（银行关键）

```bash
# 根据 RustSec 公告数据库审计依赖
cargo install cargo-audit
cargo audit

# 检查许可证
cargo install cargo-license
cargo license

# 禁止特定许可证或漏洞
# cargo-deny：功能最强大
cargo install cargo-deny
cargo deny check
```

`cargo-deny` 配置：
```toml
# deny.toml
[licenses]
allow = ["MIT", "Apache-2.0", "BSD-3-Clause"]

[advisories]
db-path = "~/.cargo/advisory-db"
db-urls = ["https://github.com/rustsec/advisory-db"]
deny = ["unmaintained", "unsound", "yanked"]
```

这是成熟企业 Rust 项目在 CI 中运行的内容——在依赖进入生产环境之前进行许可证合规与 CVE 门控。

---

## 总结

| 需求 | 工具 |
|---|---|
| 公共开源 | crates.io |
| 自托管私有注册中心 | Kellnr 或 Gitea |
| 企业级 SaaS 注册中心 | Artifactory / Cloudsmith |
| 离线 / 合规构建 | `cargo vendor` |
| Monorepo 管理 | Cargo workspace |
| 安全审计 | `cargo-audit` + `cargo-deny` |

考虑到你在银行工作，实际的技术栈是：**Artifactory 或 Kellnr** 作为注册中心 + **`cargo vendor`** 用于受监管的 CI 流水线 + **`cargo-deny`** 用于许可证 / CVE 门控。

**参考资源：**

- [The Cargo Book — Registries](https://doc.rust-lang.org/cargo/reference/registries.html)
- [Kellnr — 自托管 Crate 注册中心](https://kellnr.io)
- [cargo-deny](https://embarkstudios.github.io/cargo-deny/)
- [稀疏注册中心协议 RFC](https://rust-lang.github.io/rfcs/2789-sparse-index.html)
- [RustSec 公告数据库](https://rustsec.org)
