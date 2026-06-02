---
audio: false
date: 2025-09-11
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5
title: 理解JaCoCo与Maven集成
translated: true
type: note
---

明白了——以下是您**当前POM文件**中JaCoCo各组件协同工作的步骤及原理说明。

---

# 该POM文件创建的两类覆盖率数据流

1. **单元测试覆盖率（Surefire路径）**

* 您未配置特殊参数就绑定了JaCoCo的**`prepare-agent`**：

  ```xml
  <execution>
    <id>prepare-agent</id>
    <goals><goal>prepare-agent</goal></goals>
  </execution>
  ```

  这会通过`argLine`参数将`-javaagent:...org.jacoco.agent-<ver>-runtime.jar`注入**Surefire**测试JVM。
  • 默认**destfile**为`${project.build.directory}/jacoco.exec`。
  • 默认**append**为`true`（当文件已存在时，JaCoCo代理会追加数据）。
  • 效果：在`test`阶段运行单元测试（如有）时，覆盖率数据会写入`target/jacoco.exec`。

2. **集成测试覆盖率（Jetty路径）**

* 您为集成测试覆盖率定义了**独立文件**：

  ```xml
  <properties>
    <jacoco.it.exec>${project.build.directory}/jacoco-it.exec</jacoco.it.exec>
  </properties>
  ```
* 您启动Jetty时**使用独立的JaCoCo代理**指向该文件：

  ```xml
  <plugin>
    <artifactId>jetty-maven-plugin</artifactId>
    ...
    <execution>
      <id>start-jetty</id>
      <phase>pre-integration-test</phase>
      <goals><goal>start</goal></goals>
      <configuration>
        <daemon>true</daemon>
        <jvmArgs>
          -javaagent:${settings.localRepository}/org/jacoco/org.jacoco.agent/${jacoco.version}/org.jacoco.agent-${jacoco.version}-runtime.jar=destfile=${jacoco.it.exec}
        </jvmArgs>
        ...
      </configuration>
    </execution>
  </plugin>
  ```

  • Jetty在**独立JVM**中运行；其代理将数据写入`target/jacoco-it.exec`。
  • 由于未指定`append`参数，JaCoCo默认`append=true`生效——因此除非执行清理或设置`append=false`，多次启动Jetty会向同一文件追加数据。

---

# 生命周期流程（执行`mvn verify`时的过程）

1. **compile**

   * Spotless格式化（`spotless-maven-plugin`）和Checkstyle检查（`maven-checkstyle-plugin`）。
   * 准备WAR包（`maven-war-plugin`）。

2. **test (Surefire)**

   * 如有单元测试，它们会在**`prepare-agent`**注入的argLine参数下运行 → 覆盖率数据写入`target/jacoco.exec`。

3. **pre-integration-test**

   * Jetty以**守护模式**启动：

     ```xml
     <daemon>true</daemon>
     ```

     Maven立即恢复控制权；Jetty持续运行并附带JaCoCo代理，将数据写入`jacoco-it.exec`。

4. **integration-test**

   * 您的Python测试访问运行中的应用程序：

     ```xml
     <plugin>
       <artifactId>exec-maven-plugin</artifactId>
       <execution>
         <id>python-integration-tests</id>
         <phase>integration-test</phase>
         <goals><goal>exec</goal></goals>
         <configuration>
           <executable>python3</executable>
           <workingDirectory>${project.parent.basedir}</workingDirectory>
           <arguments>
             <argument>-m</argument><argument>unittest</argument>
             <argument>discover</argument><argument>tests/</argument>
             <argument>-v</argument>
           </arguments>
         </configuration>
       </execution>
     </plugin>
     ```

     这些测试会调用Jetty，因此覆盖率通过Jetty JVM的代理累积到**`target/jacoco-it.exec`**。

5. **post-integration-test**

   * 干净地停止Jetty：

     ```xml
     <execution>
       <id>stop-jetty</id>
       <phase>post-integration-test</phase>
       <goals><goal>stop</goal></goals>
       ...
     </execution>
     ```

6. **verify**

   * 您使用IT数据文件和自定义输出目录生成**独立的IT报告**：

     ```xml
     <execution>
       <id>report-it</id>
       <phase>verify</phase>
       <goals><goal>report</goal></goals>
       <configuration>
         <dataFile>${jacoco.it.exec}</dataFile>
         <outputDirectory>${project.reporting.outputDirectory}/jacoco-it
         </outputDirectory>
       </configuration>
     </execution>
     ```
   * 结果：HTML报告生成于`target/site/jacoco-it/index.html`，仅汇总**集成**测试覆盖率（来自Jetty）。

> 注意：如需**单元测试**报告，可添加另一个指向默认`target/jacoco.exec`并输出至`target/site/jacoco`的`jacoco:report`执行配置——保持单元测试与集成测试报告分离。

---

# 关于`.exec`文件的“新建或替换？”问题

* **JaCoCo代理默认`append=true`**。

  * 对于**单元测试**，文件是`target/jacoco.exec`。当重复执行`mvn verify`且**不执行`clean`**时，数据可能在不同运行间追加。
  * 对于**Jetty集成测试**，您的`jvmArgs`未覆盖`append`设置，因此`target/jacoco-it.exec`也默认**追加**数据。

**最佳实践**（避免混合旧数据）：

* 运行`mvn clean verify`，**或**在Jetty代理配置中添加`append=false`：

  ```xml
  -javaagent:...org.jacoco.agent-...-runtime.jar=destfile=${jacoco.it.exec},append=false
  ```
* 如需有意合并多个`.exec`文件，可在`jacoco:report`前使用`jacoco:merge`。

---

# 原始XML中各相关模块的功能说明（按引用关系）

* **集成测试文件位置**

  ```xml
  <properties>
    <jacoco.it.exec>${project.build.directory}/jacoco-it.exec</jacoco.it.exec>
    <it.report.skip>false</it.report.skip>
  </properties>
  ```

  定义集成测试覆盖率数据的存储位置。`it.report.skip`已声明但尚未接入报告执行配置（参见下文提示）。

* **单元测试代理（Surefire路径）**

  ```xml
  <plugin>
    <artifactId>jacoco-maven-plugin</artifactId>
    <executions>
      <execution>
        <id>prepare-agent</id>
        <goals><goal>prepare-agent</goal></goals>
      </execution>
      ...
    </executions>
  </plugin>
  ```

* **带JaCoCo的Jetty集成测试**

  ```xml
  <plugin>
    <artifactId>jetty-maven-plugin</artifactId>
    ...
    <jvmArgs>
      -javaagent:${settings.localRepository}/org/jacoco/org.jacoco.agent/${jacoco.version}/org.jacoco.agent-${jacoco.version}-runtime.jar=destfile=${jacoco.it.exec}
    </jvmArgs>
    ...
  </plugin>
  ```

* **Jetty运行时执行Python集成测试**

  ```xml
  <plugin>
    <artifactId>exec-maven-plugin</artifactId>
    <execution>
      <id>python-integration-tests</id>
      <phase>integration-test</phase>
      <goals><goal>exec</goal></goals>
      ...
    </execution>
  </plugin>
  ```

* **在verify阶段生成集成测试覆盖率报告**

  ```xml
  <execution>
    <id>report-it</id>
    <phase>verify</phase>
    <goals><goal>report</goal></goals>
    <configuration>
      <dataFile>${jacoco.it.exec}</dataFile>
      <outputDirectory>${project.reporting.outputDirectory}/jacoco-it</outputDirectory>
    </configuration>
  </execution>
  ```

---

# 实用技巧 / 小幅改进

* **避免陈旧的集成测试数据**
  在Jetty代理配置中添加`append=false`（如上所示），或始终运行`mvn clean verify`。

* **接入`it.report.skip`开关**
  如需通过属性控制是否跳过IT报告生成：

  ```xml
  <execution>
    <id>report-it</id>
    <phase>verify</phase>
    <goals><goal>report</goal></goals>
    <configuration>
      <skip>${it.report.skip}</skip>
      <dataFile>${jacoco.it.exec}</dataFile>
      <outputDirectory>${project.reporting.outputDirectory}/jacoco-it</outputDirectory>
    </configuration>
  </execution>
  ```

* **保持单元测试与集成测试报告分离**
  您已成功将IT报告分离至`site/jacoco-it`。如需单元测试报告，可添加另一个不覆盖`dataFile`的`jacoco:report`配置，输出至`site/jacoco`。

* **多模块注意事项**
  当前模块级配置仅报告**PlaygroundWeb**的覆盖率。如需**合并**视图，可在父POM（`packaging=pom`）中使用`jacoco:merge`（合并`.exec`文件）和/或`report-aggregate`（JaCoCo 0.8.8+）。

---

# 总结

* **单元测试** → `prepare-agent`将JaCoCo注入Surefire JVM → `target/jacoco.exec`。
* **集成测试** → Jetty启动时附带独立JaCoCo代理 → `target/jacoco-it.exec`。
* **报告生成** → 在`verify`阶段，`jacoco:report`仅将**集成测试**覆盖率渲染至`target/site/jacoco-it`。
* **文件行为** → JaCoCo**默认追加数据**；建议使用`mvn clean verify`或设置`append=false`避免不同运行批次的数据混合。
