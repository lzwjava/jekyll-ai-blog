---
audio: false
date: 2025-09-07
generated: true
image: false
lang: zh
layout: post
title: 理解JaCoCo执行数据文件
translated: true
type: note
---

以下是一份实用且全面的指南。

# 什么是 `jacoco-it.exec`？

* 这是**集成测试**期间生成的 **JaCoCo 执行数据文件**。
* "`-it`" 只是一个**命名约定**（源自 `jacoco-maven-plugin` 的 *report-integration* 目标及 Failsafe 阶段）。单元测试通常输出到 `jacoco.exec`，而集成测试则输出到 `jacoco-it.exec`。
* 您可以拥有多个 `.exec` 文件（按模块、阶段或运行划分），并在后续**合并**它们以生成统一的覆盖率报告。

典型的 Maven 配置：

```xml
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.12</version>
  <executions>
    <!-- 单元测试配置 -->
    <execution>
      <id>prepare-agent</id>
      <goals><goal>prepare-agent</goal></goals>
    </execution>
    <!-- 集成测试配置 -->
    <execution>
      <id>prepare-agent-integration</id>
      <goals><goal>prepare-agent-integration</goal></goals>
    </execution>
    <execution>
      <id>report</id>
      <phase>verify</phase>
      <goals><goal>report</goal></goals>
    </execution>
    <execution>
      <id>report-it</id>
      <phase>verify</phase>
      <goals><goal>report-integration</goal></goals>
    </execution>
  </executions>
</plugin>
```

该配置通常会生成 `target/jacoco.exec`（单元测试）和 `target/jacoco-it.exec`（集成测试）。

# `.exec` 文件包含什么内容？

* 仅包含按类记录的**探针命中数据**。
* 具体来说：对于每个加载的类，JaCoCo 会计算一个**标识符**（基于字节码）并存储**探针的布尔数组**（记录哪些指令/分支被执行）。
* 同时还会存储**会话标识符**和时间戳。
* **不包含**类字节码、方法名称、行号或源代码。这些结构信息是在运行 `jacoco:report` 生成 HTML/XML 时，从您的**类文件**和**源代码**中获取的。

重要提示：

* 如果在生成 `.exec` 文件后修改了类文件，可能会导致文件不匹配（标识符无法对应）。生成报告时务必使用**与生成 exec 文件时完全相同的**类文件构建版本。

# 是否包含类结构信息？

* **不包含**。没有方法信息、行号或源代码。
* 这是每个类的紧凑二进制**命中图**。报告生成步骤会读取您的**编译类文件**（及可选的源代码），将这些命中映射到包、类、方法、行和分支。

# 通过 `-javaagent` 附加时会被更新吗？

简短回答：**会**，具体细节如下：

* 当使用该代理启动 JVM 时，它会**实时**插桩类并在**内存中**记录探针命中。
* 代理会**写入** `destfile`：

  * **在 JVM 退出时**（对于 `output=file`，这是默认设置），或
  * 当您显式**转储**时（通过 TCP/JMX/API），或
  * 当设置了 `append=true` 时，它会**追加/合并**到现有文件，而不是覆盖。

常用代理选项：

```bash
-javaagent:/path/to/org.jacoco.agent.jar=\
destfile=/path/to/jacoco-it.exec,\
append=true,\
output=file
```

其他有用模式：

* `output=tcpserver`（监听端口；可连接并触发转储）
* `output=tcpclient`（推送到服务器）
* `jmx=true`（暴露 JMX MBean 以进行转储/重置）
* 编程方式：`org.jacoco.agent.rt.RT.getAgent().dump(/*reset*/ true|false)`

关于“更新”的说明：

* 使用 `output=file` **且** `append=true` 时，**每次转储**都会将探针数组合并到现有文件中（命中数据的逻辑或运算）。
* 未设置 `append=true` 时，下一次写入会在转储/退出时**覆盖**文件。
* 如果有**多个 JVM**（微服务、分叉测试），请为每个 JVM 指定**不同的文件**，或使用 TCP/JMX 集中收集后再合并。

# 典型工作流

**集成测试阶段（Failsafe）：**

* Maven 将代理附加到集成测试的 JVM，并设置 `destfile=target/jacoco-it.exec`。
* 最后运行 `jacoco:report-integration`，该命令会读取：

  * `target/jacoco-it.exec`（命中数据）
  * `target/classes`（结构信息）
  * `src/main/java`（可选，用于源代码行映射）
* 输出：*仅集成测试*的 HTML/XML/CSV 覆盖率报告。

**合并多次运行结果：**

```bash
# 通过 Maven
mvn jacoco:merge -Djacoco.destFile=target/merged.exec \
  -Djacoco.dataFileList="target/jacoco.exec,target/jacoco-it.exec,other.exec"
# 然后
mvn jacoco:report -Djacoco.dataFile=target/merged.exec
```

# 常见问题与技巧

* **构建版本匹配**：生成报告时使用的**编译类文件**必须与生成 `.exec` 文件时使用的完全一致。
* **并行分叉**：当并行运行测试或多个 JVM 时，避免多个写入者同时操作同一文件，除非设置了 `append=true` 且您能接受并发追加（更安全的做法是每个 JVM 使用独立文件，后续再合并）。
* **长时间运行的服务**：启用 **TCP/JMX** 或调用运行时 API 以**定期转储**；不要等待进程退出。
* **类加载器隔离**：某些应用服务器会多次加载同一类；JaCoCo 会通过类标识符去重，但在复杂容器中需特别注意。
* **离线插桩**方案存在，但 **javaagent** 方法通常更简单可靠。

---

## 直接回答您的问题

* **“什么是 `jacoco-it.exec`？”**
  这是**集成测试**期间捕获的执行数据文件（探针命中数据）。它只是一个命名约定；功能上与 `jacoco.exec` 格式相同。

* **“是否包含类结构信息？”**
  **不包含。** 它仅存储每个类的**探针命中数组**和会话元数据。类/方法/行信息是在报告生成阶段从编译的类文件/源代码中获取的。

* **“通过 `-javaagent` 附加时会被更新吗？”**
  **会。** 使用 `output=file` 时，代理会在 **JVM 退出时** 或 **按需**（通过 TCP/JMX/API）写入。使用 `append=true` 时，它会与现有文件**合并**；未设置时则会**覆盖**。对于多 JVM 运行，请使用独立文件或远程转储，后续再**合并**。
