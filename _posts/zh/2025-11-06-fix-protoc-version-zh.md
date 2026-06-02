---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 修复Substrait构建Protoc版本错误
translated: true
type: note
---

### 理解错误原因

这个构建失败发生在 `substrait` crate（v0.58.0）中，GreptimeDB 依赖它来实现跨语言查询规划。错误源于 protobuf 编译器（`protoc`）拒绝了 `substrait/algebra.proto` 文件，因为它在 proto3 语法中使用了"optional"字段——这个特性需要满足以下条件之一：

- Protoc 版本 ≥3.21（该版本中支持已稳定，无需特殊标志），或
- 较旧的 protoc（如 3.15–3.20）需要在编译时传递 `--experimental_allow_proto3_optional` 标志。

`substrait` 构建脚本中的 `prost-build` 工具没有传递此标志，因此它假定使用的是兼容的 protoc 版本。您系统的 `protobuf-compiler`（可能来自 Ubuntu 22.04 或更早版本的 `apt`，提供的是约 3.12.4 版本）太旧且缺少该标志，导致发生 panic。

GreptimeDB 的文档指定需要 protoc ≥3.15，但对于此依赖项，实际上需要 ≥3.21。

### 快速修复：升级 Protoc 到 ≥3.21

最简单且无需 root 权限的方法是下载并安装官方的二进制版本（无需编译）。方法如下：

1. **下载最新版 Protoc**：
   - 访问 [Protocol Buffers Releases](https://github.com/protocolbuffers/protobuf/releases)。
   - 获取最新的 `protoc-<version>-linux-x86_64.zip`（例如 `protoc-28.1-linux-x86_64.zip` 或任何当前最新版本——任何 ≥3.21 的版本均可）。
   - 示例直接链接（请调整版本号）：
     `wget https://github.com/protocolbuffers/protobuf/releases/download/v27.3/protoc-27.3-linux-x86_64.zip`

2. **安装**：

   ```
   unzip protoc-*.zip -d protoc-install
   sudo mv protoc-install/bin/protoc /usr/local/bin/
   sudo chmod +x /usr/local/bin/protoc
   rm -rf protoc-install protoc-*.zip  # 清理
   ```

3. **验证**：

   ```
   protoc --version
   ```

   应输出 `libprotoc 27.3`（或更高版本）。如果显示的仍是旧版本，请检查您的 PATH（`echo $PATH`）——`/usr/local/bin` 应位于 `/usr/bin` 之前。

4. **重新尝试构建**：

   ```
   make clean  # 清除过时的构建目标
   make
   ```

这会覆盖系统的 `protoc`，而不会与 `apt` 包冲突。如果您使用的是较新的发行版，如 Ubuntu 24.04+，`apt install protobuf-compiler` 可能已经提供 ≥3.21 的版本——请先仔细检查您的版本。

### 如果无法升级（罕见情况）

- 如果受限于旧系统，您需要修补 `substrait` 的 `build.rs` 以添加标志（通过 `Command::new(protoc).arg("--experimental_allow_proto3_optional")`），但这需要 fork 该 crate 并更新 GreptimeDB 的 `Cargo.toml`——过程繁琐，不推荐。
- 或者，一些 crate 提供了 `protobuf-src` 特性来捆绑一个较新的 protoc，但 `substrait` 默认未启用它。

### 额外提示

- 确保满足其他先决条件：`build-essential`（用于 GCC）、`libc6-dev`（glibc 头文件）。
- 如果构建通过但后续在 C++ 依赖项（例如 Arrow）上失败，请通过 conda 或 apt 安装 `libarrow-dev`。
- 对于 CI/CD 或 Docker：将此下载步骤添加到您的环境中。

这应该能解决问题——`substrait` 在现代设置上可以干净地编译。如果您遇到其他问题，请分享 `protoc --version` 的输出和您的发行版信息。

[GreptimeDB 构建文档](https://github.com/GreptimeTeam/greptimedb#build-from-source)
[Protobuf 发布页面](https://github.com/protocolbuffers/protobuf/releases)
[Proto3 可选字段文档](https://protobuf.dev/programming-guides/proto3/#optional)
