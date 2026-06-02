---
audio: false
date: 2025-09-08
generated: true
image: false
lang: zh
layout: post
title: 单JVM集成覆盖策略
translated: true
type: note
---

你无需运行两次 Jetty 或为每个模块创建单独的 JaCoCo `.exec` 文件。只需在部署 WAR 包的单个 JVM 上配置一个代理，即可将**该 JVM 加载的所有类**（包括 `PlaygroundUtils`）的覆盖率记录到**一个共享的 exec 文件中**。然后每个模块都可以通过指向同一 exec 文件生成各自的报告。对于大型反应堆项目（10+ 模块），这种方案能保持清晰的可扩展性。

以下是针对你代码库的具体实施方案和即用型修改。

---

## 实施策略

1. **在父级使用单一共享的 IT exec 文件**
   只需**启动一次**搭载 JaCoCo 的 Jetty，将其配置为写入 `../target/it-coverage/jacoco-it.exec`（父级作用域路径）。
2. **运行一次外部 Python 测试**
   测试会访问已部署的应用；代理会记录所有加载类（Web 模块及依赖库）的命中情况。
3. **生成各模块报告**，每个模块都指向共享的 `jacoco-it.exec` 文件
   即使 `PlaygroundUtils` 没有测试，也能生成报告——它会将共享 exec 文件映射到自身的 `target/classes`。
4. （可选）**在父级同时生成聚合 HTML 报告**，使用 `report-aggregate`，或仅保留各模块报告。

仅当存在**多个 JVM**（例如多个微服务）时，才需要多个 exec 文件和 `jacoco:merge` 步骤。对于当前单 JVM（Jetty）构建，保持单一 exec 文件即可。

---

## 具体修改

### 1) 父级 `pom.xml` (PlaygroundLib)

添加共享属性，以便所有模块都能引用同一 exec 文件：

```xml
<properties>
  <!-- ... 现有版本配置 ... -->
  <it.coverage.dir>${project.basedir}/target/it-coverage</it.coverage.dir>
  <jacoco.it.exec>${it.coverage.dir}/jacoco-it.exec</jacoco.it.exec>
  <!-- 控制各模块 IT 报告生成开关 -->
  <it.report.skip>false</it.report.skip>
</properties>
```

（可选）如需在父级生成**聚合** HTML 报告，添加以下执行配置：

```xml
<build>
  <pluginManagement>
    <!-- 保留现有配置块 -->
  </pluginManagement>

  <plugins>
    <plugin>
      <groupId>org.jacoco</groupId>
      <artifactId>jacoco-maven-plugin</artifactId>
      <executions>
        <execution>
          <id>it-aggregate-report</id>
          <phase>verify</phase>
          <goals>
            <goal>report-aggregate</goal>
          </goals>
          <configuration>
            <!-- 使用 Jetty 运行生成的共享 IT exec -->
            <dataFile>${jacoco.it.exec}</dataFile>
            <outputDirectory>${project.reporting.outputDirectory}/jacoco-it</outputDirectory>
          </configuration>
        </execution>
      </executions>
    </plugin>
  </plugins>
</build>
```

> 如果你的 JaCoCo 版本在 `report-aggregate` 中不支持 `<dataFile>`，可跳过此可选配置块，依赖下述各模块报告。后续随时可添加小型“覆盖率”聚合模块来执行 `merge` + `report`。

---

### 2) `PlaygroundWeb/pom.xml`

将 Jetty 代理指向**父级** exec 路径并启用追加模式：

```xml
<plugin>
  <groupId>org.eclipse.jetty</groupId>
  <artifactId>jetty-maven-plugin</artifactId>
  <executions>
    <execution>
      <id>start-jetty</id>
      <phase>pre-integration-test</phase>
      <goals><goal>start</goal></goals>
      <configuration>
        <daemon>true</daemon>
        <jvmArgs>
          -javaagent:${settings.localRepository}/org/jacoco/org.jacoco.agent/${jacoco.version}/org.jacoco.agent-${jacoco.version}-runtime.jar=destfile=${project.parent.basedir}/target/it-coverage/jacoco-it.exec,append=true,includes=org.lzw.*
        </jvmArgs>
        <httpConnector>
          <port>8080</port>
          <host>127.0.0.1</host>
        </httpConnector>
        <webApp><contextPath>/</contextPath></webApp>
        <stopHost>127.0.0.1</stopHost>
        <stopPort>8081</stopPort>
        <stopKey>stop</stopKey>
      </configuration>
    </execution>

    <execution>
      <id>stop-jetty</id>
      <phase>post-integration-test</phase>
      <goals><goal>stop</goal></goals>
      <configuration>
        <stopHost>127.0.0.1</stopHost>
        <stopPort>8081</stopPort>
        <stopKey>stop</stopKey>
        <stopWait>15</stopWait>
      </configuration>
    </execution>
  </executions>
</plugin>
```

更新 `PlaygroundWeb` 中的 `jacoco:report`，使其读取**同一**共享 exec：

```xml
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <executions>
    <execution>
      <id>report-it</id>
      <phase>verify</phase>
      <goals><goal>report</goal></goals>
      <configuration>
        <dataFile>${project.parent.basedir}/target/it-coverage/jacoco-it.exec</dataFile>
        <outputDirectory>${project.reporting.outputDirectory}/jacoco-it</outputDirectory>
      </configuration>
    </execution>
  </executions>
</plugin>
```

现有执行 `python -m unittest discover tests -v` 的 Exec Maven Plugin 配置完美——保持原样即可。

---

### 3) `PlaygroundUtils/pom.xml`

添加**仅生成报告**的执行配置，使其能将共享 exec 映射到自身类文件：

```xml
<build>
  <plugins>
    <!-- 保留现有插件 -->

    <plugin>
      <groupId>org.jacoco</groupId>
      <artifactId>jacoco-maven-plugin</artifactId>
      <executions>
        <execution>
          <id>report-it</id>
          <phase>verify</phase>
          <goals><goal>report</goal></goals>
          <configuration>
            <dataFile>${project.parent.basedir}/target/it-coverage/jacoco-it.exec</dataFile>
            <outputDirectory>${project.reporting.outputDirectory}/jacoco-it</outputDirectory>
            <skip>${it.report.skip}</skip>
          </configuration>
        </execution>
      </executions>
    </plugin>
  </plugins>
</build>
```

此模块从不启动 Jetty 或运行 Python；它仅消费共享 exec 和自身的 `target/classes`。如果测试期间 Web 应用使用了任何 `PlaygroundUtils` 类，它们将显示覆盖率。如果未被调用，则显示 0%——这是正确的信号。

---

## 操作流程

在代码库根目录执行：

```bash
mvn -pl PlaygroundWeb -am clean verify
```

构建顺序会编译两个模块，启动一次带代理的 Jetty，运行 Python 测试，停止 Jetty，随后生成：

* `PlaygroundWeb/target/site/jacoco-it/index.html`
* `PlaygroundUtils/target/site/jacoco-it/index.html`
* （可选）如果启用了 `report-aggregate`，还会在父级生成聚合报告。

---

## 扩展至 10 模块场景

* 如果所有 10 个模块最终都部署在**同一 WAR/JVM** 中，保持**单一共享 exec** 模式。每个模块添加指向共享 exec 的 `report` 执行配置。仍只需启动一次 Jetty 并运行一次 Python。

* 如果存在**多个 JVM**（例如独立服务），为每个 JVM 指定独立的 `destfile`（例如 `it-coverage/serviceA.exec`、`serviceB.exec`），然后在父级运行：

  ```xml
  <plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <executions>
      <execution>
        <id>merge-it</id>
        <phase>post-integration-test</phase>
        <goals><goal>merge</goal></goals>
        <configuration>
          <destFile>${project.basedir}/target/it-coverage/jacoco-merged.exec</destFile>
          <files>
            <file>${project.basedir}/target/it-coverage/serviceA.exec</file>
            <file>${project.basedir}/target/it-coverage/serviceB.exec</file>
            <!-- 按需添加更多文件 -->
          </files>
        </configuration>
      </execution>

      <execution>
        <id>aggregate-report</id>
        <phase>verify</phase>
        <goals><goal>report-aggregate</goal></goals>
        <configuration>
          <dataFile>${project.basedir}/target/it-coverage/jacoco-merged.exec</dataFile>
          <outputDirectory>${project.reporting.outputDirectory}/jacoco-it</outputDirectory>
        </configuration>
      </execution>
    </executions>
  </plugin>
  ```

* 如需减少干扰，可在代理行设置 `includes=org.lzw.*`（已展示）或添加 `excludes` 来过滤第三方库。

---

## 当前问题的根源

* 你之前创建了**各模块独立的 exec 文件**，导致不得不为填充每个文件而用不同代理重新运行 Jetty。这是不必要的。代理并不关心类属于哪个模块——它会记录所有加载的类。将 exec 文件集中管理，并让每个模块的 `report` 指向该共享文件。

---

## 快速检查清单

* 在父级设置一个**共享**的 `${jacoco.it.exec}`。
* **启动一次** Jetty，配置 `append=true` 和 `includes=org.lzw.*`。
* **运行一次** Python 测试。
* 每个模块配置读取共享 exec 的 `jacoco:report`。
* （可选）配置父级 `report-aggregate` 以生成统一顶层 HTML 报告。

这套方案将使你的配置更简洁且具备可扩展性。如果需要，我可以根据这些修改为你当前的 POM 文件生成具体的差异对比。
