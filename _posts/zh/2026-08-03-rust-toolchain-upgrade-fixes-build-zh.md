---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Rust工具链升级修复构建问题
translated: true
type: note
---

好的，以下是翻译后的内容：

## 摘要

**1. Git pull** — 已处于最新提交。`origin/main` 已更新至 `d48ab2d`（"修复 BCG 循环导入问题，在服务器启动期间"）。

**2. 初始构建失败** — 新拉取的代码包含一个新的 Rust crate，`sglang-server`（在 PR #33103 中新增，标题为 "feat: rust sglang server openai apis"），该 crate 引入了 `rustpython-ruff_python_ast@0.15.8` 及其依赖项，这些依赖项需要 **rustc ≥ 1.92**。您安装的工具链是 rustc 1.91.0，因此 `cargo` 拒绝编译。

**3. 修复了工具链** — 升级了 rustup stable 工具链：
```
stable 已更新 - rustc 1.97.1（来自 rustc 1.91.0）
```

**4. 重新构建** — `pip install -e . --no-deps` 重新编译了所有 Rust/PyO3 扩展：
- `sglang/srt/grpc/_core` → 6.5 MB
- `sglang/srt/multimodal/_core` → 1.1 MB
- `sglang/srt/server/_core` → 13.4 MB（新 crate）

**5. 已验证** — 全新安装的 `sglang-0.0.0.dev63+gd48ab2d38` 能够干净地导入，所有 Rust 扩展均已加载。

注意：旧版本的工具链 1.91.0 仍通过 rustup 安装在系统中（如有需要，可使用 `rustup override` 切换回去），并且此次升级是用户级别的 —— 系统范围内没有任何修改。