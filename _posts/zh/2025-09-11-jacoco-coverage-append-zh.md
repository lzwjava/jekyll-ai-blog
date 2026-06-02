---
audio: false
date: 2025-09-11
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5
title: JaCoCo覆盖率文件与追加模式
translated: true
type: note
---

这是 JaCoCo 工作原理中一个微妙但重要的细节。

### `jacoco:prepare-agent` 的行为

* 当 Maven 执行 **`prepare-agent`** 目标时，并不会立即生成覆盖率文件。
* 而是**配置 JVM**（通常通过 `-javaagent:jacocoagent.jar` 参数），以便在测试或应用运行时收集覆盖率数据。
* `.exec` 文件的位置由属性 `jacoco.destFile` 控制（默认为 `target/jacoco.exec`，但经常被自定义，例如 `target/jacoco-it.exec`）。

### 如果文件已存在会发生什么？

* 默认情况下，**JaCoCo 会在带有代理的 JVM 启动时覆盖该文件**。
* 这意味着每次执行 `prepare-agent` → 测试运行都会生成一个*全新*的 `.exec` 文件。
* 它不会自动追加数据——除非另行配置，否则旧数据会丢失。

### 如何启用追加模式

如果希望多次运行的数据累积到同一个 exec 文件中，必须显式启用追加模式：

```xml
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.12</version>
  <configuration>
    <destFile>${project.build.directory}/jacoco-it.exec</destFile>
    <append>true</append>   <!-- ✅ 追加覆盖率数据 -->
  </configuration>
</plugin>
```

设置 `<append>true>` 后，如果文件已存在，新的覆盖率数据将被合并到该文件中。

### 简要总结

* **默认行为：** 每次运行都会替换旧的 `.exec` 文件。
* **启用 `append=true` 时：** 多次 JVM 运行（或多个模块/测试）的覆盖率数据会合并到同一个文件中。

---

需要我进一步说明这在**多模块 Maven 构建**中的交互情况吗？每个模块可能尝试写入自己的 JaCoCo exec 文件，这通常是人们遇到覆盖与追加问题的主要原因。
