---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在 Cargo 中使用 GitHub Crates
translated: true
type: note
---

**问题：** 如何在 `Cargo.toml` 中配置从 GitHub 而非 crates.io 拉取 crate，以便在企业环境中编译（注册表被屏蔽）？

**答案：**

## 1. 在 `Cargo.toml` 中直接使用 GitHub 依赖

```toml
[dependencies]
# 按分支
serde = { git = "https://github.com/serde-rs/serde", branch = "master" }

# 按标签
serde = { git = "https://github.com/serde-rs/serde", tag = "v1.0.197" }

# 按精确提交（最可重现——企业环境推荐）
serde = { git = "https://github.com/serde-rs/serde", rev = "9b868ef831b32de" }
```

## 2. 如果 GitHub 也被屏蔽——在本地 vendor 依赖

```bash
# 在有网络的机器上：
cargo vendor

# 这会创建一个 `vendor/` 目录，包含所有源代码
# 然后提交该目录，或复制到企业机器上
```

然后在 `.cargo/config.toml`（项目级别或 `~/.cargo/config.toml`）中添加：

```toml
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
```

现在 `cargo build` 会从 `vendor/` 读取——零网络请求。

## 3. 如果可以访问内部镜像（Artifactory / Cloudsmith 等）

```toml
# .cargo/config.toml
[source.crates-io]
replace-with = "internal-mirror"

[source."internal-mirror"]
registry = "https://artifactory.corp.example.com/cargo"
```

## 4. 混合方式：部分来自 GitHub，部分来自 vendor

你可以组合使用。Cargo 按优先级顺序解析。要修补特定的 crate（例如，覆盖传递依赖而无需修改每个消费者）：

```toml
# Cargo.toml
[patch.crates-io]
ring = { git = "https://github.com/briansmith/ring", rev = "fabd88f" }
```

`[patch]` 是覆盖传递依赖最干净的方式——你不需要修改每个 crate 自身的 `Cargo.toml`，只需要修改工作区根目录。

## 5. 工作区级别的补丁（monorepo / 多 crate 设置）

```toml
# 工作区根目录 Cargo.toml
[patch.crates-io]
tokio = { git = "https://github.com/tokio-rs/tokio", branch = "master" }
```

工作区中的所有 crate 会自动继承此补丁。

## 快速决策树

```
能否访问 GitHub？
├── 能 → 在 [dependencies] 或 [patch.crates-io] 中使用 git = "https://github.com/..."
└── 不能
    ├── 能否访问内部注册表？→ 在 config.toml 中使用 [source] replace-with
    └── 完全离线 → cargo vendor + 提交 vendor/
```

## 注意事项：`Cargo.lock` 很重要

在企业环境中始终提交 `Cargo.lock`。没有它，没有 `rev` 的 git 依赖可能会静默地引入新提交。使用 `rev = "..."` 加上已提交的锁文件，你可以获得完全可重现的构建。