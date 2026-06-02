---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: Maven 调试日志：实现类似 npm Silly 的效果
translated: true
type: note
---

是的，Maven 确实有类似于 npm 的 silly 日志级别的详细日志（verbose logging），尽管它使用了不同的术语。

在 Maven 中，你可以通过以下标志（flags）来控制日志的详细程度：

**`-X` 或 `--debug`** - 这是 Maven 中对应 npm 的 silly/verbose 日志。它会显示详细的 debug 输出，包括：

- 完整的错误堆栈追踪（stack traces）
- 详细的 plugin 执行信息
- Dependency 解析详情
- Maven 的内部处理过程

**`-e` 或 `--errors`** - 显示错误堆栈追踪（比 debug 模式输出少）

**`-q` 或 `--quiet`** - 最简输出，仅显示错误

用法示例：

```bash
mvn clean install -X
```

使用 `-X` 产生的 debug 输出可能非常庞大，它几乎会显示 Maven 在后台执行的所有操作 —— 这与 npm 的 `--loglevel silly` 产生海量信息的方式非常相似。

如果你需要对日志进行更精细的控制，由于 Maven 底层使用 SLF4J，你也可以在 `simplelogger.properties` 文件中配置 logging levels。但通常情况下，当你需要进行 troubleshooting 时，使用 `-X` 标志就足够了，就像你在调试 npm 问题时使用 `npm --loglevel silly` 一样。
