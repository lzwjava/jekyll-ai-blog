---
audio: false
date: 2025-09-11
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5
title: JaCoCo运行时执行文件行为
translated: true
type: note
---

当您在 **WebSphere Liberty Profile** 中配合 **JaCoCo 代理** 以 `exec` 模式运行时，JaCoCo 代理在运行期间**不会修改**原始的 `.exec` 文件。具体情况如下：

---

### JaCoCo 在 `exec` 模式下的工作原理
- **目的**：JaCoCo 代理在应用程序运行时收集**代码覆盖率数据**。
- **输出**：它将覆盖率数据写入 `.exec` 文件（例如 `jacoco.exec`）。
- **文件行为**：
  - 如果文件**不存在**，JaCoCo 会创建该文件。
  - 如果文件**已存在**，JaCoCo 会将新的覆盖率数据**追加**到文件中（不会覆盖或修改现有数据，除非您显式重置或合并文件）。
  - 原始的 `.exec` 文件**不会被破坏或改变结构**——只会随着新数据的加入而增长。

---

### `.exec` 文件是否会被修改？
- **会，但仅通过追加数据**：每次使用 JaCoCo 代理运行应用程序时，文件都会更新新的覆盖率信息。
- **无结构变化**：`.exec` 文件的格式保持不变；它是一个包含覆盖率数据的二进制文件。

---

### 最佳实践
- **合并或重置**：如需重新开始，请在再次运行应用程序前删除或重命名 `.exec` 文件。
- **合并多次运行**：如需合并多个 `.exec` 文件，可使用 Maven 的 `jacoco:merge` 目标或 `org.jacoco.agent.rt.RT` 类。

---

### Liberty 配置示例
在 Liberty 的 `server.env` 或 `jvm.options` 中可能会看到：
```bash
-javaagent:/path/to/jacocoagent.jar=destfile=/path/to/jacoco.exec,append=true
```
- `append=true` 确保新数据会追加到现有文件中。

---
