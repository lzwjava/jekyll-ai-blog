---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Git项目结构与架构
translated: true
type: note
---

这是 Git 项目的全面总结：

---

## Git — 分布式版本控制系统

**版本**: 2.54.0.265.g56a4f3c3（最新开发版）
**语言**: C（部分 Perl、Tcl/Tk 和 shell）
**许可证**: GPLv2

---

### 源码统计

- **629 个 C 源文件**，342 个头文件
- **~385,000 行** C 代码
- **130 个内置命令**（add、commit、push、pull、merge、rebase 等）
- **1,094 个测试脚本**位于 `t/`
- **252 个文档文件**（AsciiDoc）

---

### 目录结构与子系统

| 目录 | 用途 |
| ----------- | --------- |
| `builtin/` | 130 个命令实现（add.c、commit.c、merge.c、rebase.c...） |
| `refs/` | 引用存储后端：files、packed、reftable |
| `reftable/` | 新的二进制引用存储格式（比 packed-refs 更快、更紧凑） |
| `odb/` | 对象数据库层（松散对象、包文件、流式处理） |
| `xdiff/` | 差异/合并算法：patience diff、histogram diff、三方合并 |
| `negotiator/` | 获取协商策略：default、skipping、noop |
| `sha256/`、`sha1/`、`sha1dc/` | 哈希实现（带碰撞检测的 SHA-1、SHA-256） |
| `block-sha1/` | 优化的块 SHA-1 |
| `trace2/` | 结构化跟踪/遥测（JSON、性能、正常目标） |
| `compat/` | 平台兼容性垫片 |
| `contrib/` | 社区工具：subtree、diff-highlight、credential helpers、libgit-rs |
| `t/` | 测试套件（基于 shell，通过 `make test` 运行） |
| `Documentation/` | AsciiDoc man 页面和指南 |
| `perl/`、`git-gui/`、`gitk-git/` | Perl 绑定、GUI 工具 |

---

### 关键源文件（顶层目录）

| 文件 | 功能 |
| ------ | -------------- |
| `commit.c` | 提交对象的创建和解析 |
| `merge.c`、`merge-ort.c` | 合并引擎（ORT = Ostensibly Recursive's Twin，现代三方合并） |
| `diff.c`、`diffcore-*.c` | 差异管道：拆分、重命名检测、pickaxe、排序 |
| `sequencer.c` | rebase/cherry-pick 状态机 |
| `rerere.c` | 重用已记录的解决方案（记住合并冲突解决） |
| `pack-objects.c`、`packfile.c` | 包文件的创建、读取、位图 |
| `commit-graph.c`、`midx.c` | 性能加速器：提交图、多包索引 |
| `transport.c`、`connect.c` | Git 协议 v2 传输层 |
| `fetch-pack.c`、`send-pack.c` | 客户端 fetch/push |
| `remote-curl.c` | HTTP(S) 智能传输 |
| `config.c` | 配置文件解析（gitconfig） |
| `hash-ll.c` | 哈希抽象（SHA-1 ↔ SHA-256） |
| `worktree.c` | 链接工作树管理 |
| `credential.c` | 凭据助手框架 |

---

### 架构亮点

1. **对象模型**：一切都是对象（blob、tree、commit、tag），通过 SHA-1 或 SHA-256 哈希寻址。对象以松散形式或包文件存储。

2. **差异管道**：模块化管道，阶段包括：`diffcore-break` → `diffcore-rename` → `diffcore-pickaxe` → `diffcore-order`。xdiff 库执行实际的行级比较。

3. **合并引擎（ORT）**：2021 年取代了旧的递归合并。单次传递处理重命名、目录检测和冲突解决。

4. **引用后端**：可插拔——`files-backend.c`（传统）、`packed-backend.c` 以及新的 `reftable-backend.c`（Google 贡献的二进制格式）。

5. **协商**：在 fetch 期间，客户端和服务器协商需要哪些对象。三种策略：default（连续）、skipping（跳过祖先）、noop。

6. **协议 v2**：`serve.c` 实现了现代线缆协议，支持能力、引用过滤和 ls-refs。

7. **构建系统**：GNU Make，可选 autoconf。支持 `make prefix=/usr/local`、`NO_*` 标志禁用特性，以及 `DEVELOPER=1` 启用严格警告。

---

### 测试

```
make test              # 运行完整套件（约 1094 个脚本）
make test T=t1234.sh   # 运行单个测试
GIT_TEST_OPTS=-v make test  # 详细输出
```

---

### Contrib/值得注意

- `contrib/subtree/` — git subtree 合并策略
- `contrib/diff-highlight/` — 单词级别差异高亮
- `contrib/credential/` — 凭据助手（store、cache、netrc）
- `contrib/libgit-rs/`、`contrib/libgit-sys/` — Rust 绑定（新）

---

这是现存最经考验的 C 代码库之一——经过约 20 年的开发，几乎被地球上每个软件团队使用。
