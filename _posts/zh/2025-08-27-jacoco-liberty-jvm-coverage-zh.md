---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Liberty JVM覆盖率检测的JaCoCo指南
translated: true
type: note
---

你可以做到——将 JaCoCo 附加到运行你 EAR 的 **Liberty JVM** 上。关键在于：JaCoCo 必须与 Liberty 位于同一个 JVM 内，而不是在你的 Python 运行器中。

以下是可靠的设置方案（任选其一）。

---

## 1) 简单且稳健：在 JVM 退出时写入文件

**适用场景：** 测试完成后可以停止 Liberty 服务器。

1. **确保代理 jar 可用**（在构建中一次性配置）

```xml
<!-- 将 jacoco 代理复制到 target/jacoco/jacocoagent.jar -->
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-dependency-plugin</artifactId>
  <version>3.6.1</version>
  <executions>
    <execution>
      <id>copy-jacoco-agent</id>
      <phase>prepare-package</phase>
      <goals><goal>copy</goal></goals>
      <configuration>
        <artifactItems>
          <artifactItem>
            <groupId>org.jacoco</groupId>
            <artifactId>org.jacoco.agent</artifactId>
            <version>0.8.12</version>
            <classifier>runtime</classifier>
            <destFileName>jacocoagent.jar</destFileName>
          </artifactItem>
        </artifactItems>
        <outputDirectory>${project.build.directory}/jacoco</outputDirectory>
      </configuration>
    </execution>
  </executions>
</plugin>
```

2. **添加 Liberty JVM 选项**（文件：`wlp/usr/servers/<serverName>/jvm.options`）

```text
-javaagent:${server.config.dir}/jacoco/jacocoagent.jar=output=file,append=false,includes=com.myco.*,excludes=org.slf4j.*,destfile=${server.output.dir}/jacoco/jacoco-it.exec
```

* 将 `jacocoagent.jar` 放入 `wlp/usr/servers/<serverName>/jacoco/`（或任何可读路径）。
* 根据你的包结构调整 `includes`/`excludes`。

3. **运行流程**

* 启动 Liberty（`server start <serverName>`），部署 EAR。
* 运行你的 Python `unittest`（它们会访问端点）。
* 停止 Liberty（`server stop <serverName>`）。
  → 代理将写入 `${server.output.dir}/jacoco/jacoco-it.exec`。

4. **生成报告**

* 如果你的项目是多模块的（EAR + EJB + WAR），使用聚合 pom 和 `report-aggregate`：

```xml
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.12</version>
  <executions>
    <execution>
      <id>report-it</id>
      <phase>verify</phase>
      <goals><goal>report-aggregate</goal></goals>
      <configuration>
        <dataFile>${env.SERVER_OUTPUT_DIR}/jacoco/jacoco-it.exec</dataFile>
        <includes>
          <include>com/myco/**</include>
        </includes>
      </configuration>
    </execution>
  </executions>
</plugin>
```

（或使用 `jacococli`：）

```bash
java -jar jacococli.jar report /path/to/jacoco-it.exec \
  --classfiles module1/target/classes --classfiles module2/target/classes \
  --sourcefiles module1/src/main/java --sourcefiles module2/src/main/java \
  --html target/jacoco-it-report
```

---

## 2) 无需停止 Liberty 的实时转储（TCP 服务器模式）

**适用场景：** 希望保持 Liberty 运行并按需获取覆盖率。

1. `jvm.options`：

```text
-javaagent:${server.config.dir}/jacoco/jacocoagent.jar=output=tcpserver,address=*,port=6300,append=false,includes=com.myco.*
```

2. 运行 Liberty，执行 Python 测试，然后**转储**：

```bash
# 通过 TCP 获取覆盖率并在本地写入 .exec 文件
java -jar jacococli.jar dump --address 127.0.0.1 --port 6300 --destfile jacoco-it.exec --reset
```

然后按照上述方法生成报告。
提示：`--reset` 会重置计数器，以便在长时间运行中多次获取快照。

---

## 3) 容器 / CI（环境变量方式）

* 如果在 Docker/K8s 中运行 Liberty，挂载代理并设置：

  * 如上所述的 `jvm.options`，**或**
  * 包含相同 `-javaagent=...` 的 `WLP_JAVA_OPTIONS` / `JAVA_TOOL_OPTIONS` 环境变量。
* 对于具有多个 Liberty JVM 的集群，为每个 JVM 分配不同的 TCP 端口或文件路径，然后**合并**：

```bash
java -jar jacococli.jar merge node1.exec node2.exec --destfile merged.exec
```

---

## 注意事项与常见问题

* **EAR 布局对 JaCoCo 无关紧要**；它会在内存中检测字节码。报告只需要你模块中的**原始类文件**（`target/classes`）及其源代码以生成美观的 HTML。
* 使用**最新的 JaCoCo（0.8.12+）** 以确保 Java 17/21 兼容性（Liberty 通常在 OpenJ9/HotSpot 上运行——两者均可）。
* 注意 `includes/excludes` 以避免统计第三方库。
* 如果 `.exec` 文件为空，可能是由于：

  * 忘记附加代理，
  * 过滤掉了你的包，
  * 或在流量命中代码之前进行了转储。

---

如果你分享 EAR 的模块布局（EJB/WAR 模块和包根目录），我可以提供一个精确的 `report-aggregate` 配置和一个小脚本，以便：启动 Liberty → 运行 Python 测试 → 获取转储 → 一键生成 HTML 报告。
