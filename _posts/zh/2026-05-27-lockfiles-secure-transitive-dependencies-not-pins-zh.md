---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 锁文件保护传递依赖，而非固定版本
translated: true
type: note
---

在 `pyproject.toml` 中固定（pin）**直接**依赖的版本，但不会固定**传递性**依赖。这就是差距所在。

示例：

```
# pyproject.toml
dependencies = ["requests==2.31.0"]
```

requests 会引入 `urllib3`、`idna`、`charset-normalizer`、`certifi`。你不固定这些依赖——解析器会自由选择版本。下个月，`urllib3` 发布 2.1.0 版本并带来破坏性变更，你的 CI 会出问题，而你的笔记本仍能正常工作（因为缓存了旧版本）。

**你也可以**在 pyproject.toml 中固定所有传递性依赖，但：

1. 你需要手动维护大约 20~50 行你从未明确要求的依赖
2. 每添加一个依赖，你都需要解析并固定它的所有子依赖
3. 你会失去完整性哈希（uv.lock 包含每个包的 SHA256 哈希）
4. 你会失去平台标识（某些传递性依赖在 Linux 和 macOS 上不同）

锁文件本质上就是“一次性解析所有依赖，提交结果，并在各处复现”的输出。这是标准模式——Cargo.lock、poetry.lock、package-lock.json、Gemfile.lock 都因相同原因而存在。

**核心要点：** 在 pyproject.toml 中固定直接依赖是良好实践（指定版本范围或最低版本）。但锁文件才是完整依赖图的可复现性保证。它们服务于不同的目的。两者都提交。