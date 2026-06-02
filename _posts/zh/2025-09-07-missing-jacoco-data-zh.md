---
audio: false
date: 2025-09-07
generated: true
image: false
lang: zh
layout: post
title: 解决JaCoCo执行数据文件缺失问题
translated: true
type: note
---

要生成 JaCoCo 执行数据文件（通常称为 **'.exec' 文件**），您需要在附加 JaCoCo 代理的情况下运行测试。日志信息"由于缺少执行数据文件而跳过 JaCoCo 执行"表明，在执行 `report` 目标时，未能先成功运行 `prepare-agent` 目标。

-----

### 步骤 1：配置 JaCoCo Maven 插件

首先，请确保您的 `pom.xml` 文件已正确配置 JaCoCo Maven 插件。配置应类似如下：

```xml
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <version>0.8.12</version>
    <executions>
        <execution>
            <goals>
                <goal>prepare-agent</goal>
            </goals>
        </execution>
        <execution>
            <id>report</id>
            <phase>test</phase>
            <goals>
                <goal>report</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```

**`prepare-agent`** 目标至关重要，它会设置 JaCoCo 运行时代理。该代理在测试运行期间对代码进行检测以收集覆盖率数据。

-----

### 步骤 2：运行测试

配置插件后，运行您的 Maven 构建。运行测试并生成报告的典型命令是：

`mvn clean install`

运行此命令时，Maven 会首先执行 `prepare-agent` 目标，将 JaCoCo 代理附加到 JVM。随后，当执行 `test` 阶段时，代理会记录代码覆盖率数据并将其保存到文件中，通常位于 **`target/jacoco.exec`**。接着执行 `report` 目标，该目标读取此 `.exec` 文件并生成最终的 HTML 或 XML 报告。

如果您仍然遇到问题，请检查以下事项：

  * **项目结构**：确保您的测试位于标准的 Maven 目录 `src/test/java` 中。
  * **测试失败**：如果测试失败，构建可能会在生成 `.exec` 文件之前停止。请先解决所有测试失败问题。
  * **版本不匹配**：确保 JaCoCo 插件版本与您的 Maven 和 Java 版本兼容。
