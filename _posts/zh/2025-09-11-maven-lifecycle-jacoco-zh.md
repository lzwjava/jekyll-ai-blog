---
audio: false
date: 2025-09-11
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5
title: 理解Maven生命周期与JaCoCo
translated: true
type: note
---

问得好——这涉及到 Maven 的*生命周期阶段*以及插件如何绑定到这些阶段。

### 生命周期基础

Maven 有三个标准生命周期：`clean`、`default`（有时称为*构建*）和 `site`。在 *default* 生命周期中，重要阶段按以下顺序执行：

* `validate`
* `compile`
* `test`
* `package`
* `verify`
* `install`
* `deploy`

每个阶段都包含之前的所有阶段（如果运行 `mvn verify`，Maven 会执行从 `validate` 到 `verify` 的所有阶段）。运行 `mvn package` 会在创建构件（JAR/WAR）后停止，不会执行 `verify` 阶段。

### 为什么 JaCoCo 会参与其中

JaCoCo Maven 插件通常根据配置将其 **`prepare-agent`** 目标绑定到 `initialize` 或 `verify` 阶段。

* 如果绑定到 `verify` 阶段（生成覆盖率报告的常见配置），那么 `mvn verify` 会触发它。
* `mvn package` 不会执行到生命周期中那么靠后的阶段，因此会跳过 `verify` 阶段（以及 JaCoCo 的步骤）。

这就是为什么运行 `mvn verify` 时能看到 JaCoCo 执行，而运行 `mvn package` 时却看不到。

### 实践要点

* 当你只需要构建构件时（快速，无额外检查），使用 **`mvn package`**。
* 当你需要运行*集成测试、检查、覆盖率报告或绑定到后期阶段的质量保证插件*时，使用 **`mvn verify`**。

👉 如果你希望即使运行 `mvn package` 时 JaCoCo 也能始终执行，可以在 `pom.xml` 中将 `prepare-agent` 目标重新绑定到更早的阶段，例如 `test` 或 `package`。

需要我展示一个具体的 `pom.xml` 代码片段，让 JaCoCo 的 `prepare-agent` 在 `test` 阶段而非 `verify` 阶段运行吗？
