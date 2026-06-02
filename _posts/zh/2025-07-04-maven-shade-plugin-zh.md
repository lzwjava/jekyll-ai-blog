---
audio: false
generated: true
lang: zh
layout: post
title: Maven Shade 插件：创建 Uber-JAR 包
translated: true
type: note
---

`maven-shade-plugin` 是一款用于创建「超级JAR包」（即包含项目编译代码及其依赖项的独立JAR文件）的 Maven 插件。该插件在 Java 项目中广泛使用，通过将应用程序及其所有依赖库打包成单一可执行 JAR 文件，从而简化分发和部署流程。

### 核心特性：
- **Group ID**：`org.apache.maven.plugins`（表明这是 Apache 官方维护的 Maven 插件）
- **Artifact ID**：`maven-shade-plugin`（插件具体名称）
- **核心功能**：
  - **依赖遮蔽**：通过重定位依赖包路径避免类冲突（例如当多个库使用相同类的不同版本时）
  - **打包聚合**：将依赖项嵌入最终生成的 JAR 文件，形成自包含部署单元
  - **资源转换**：支持修改资源文件（例如合并 `MANIFEST.MF` 等配置文件）
- **典型应用场景**：
  - 为命令行应用创建可执行 JAR
  - 解决多依赖项目的类路径冲突
  - 简化 Spark 或 Hadoop 作业等应用的部署流程
- **运作机制**：
  - 在 `pom.xml` 文件的 `<plugins>` 节点中配置
  - 在构建过程中（通常在 `package` 阶段）合并类文件与资源，可选执行包重定位，最终生成目标 JAR
- **配置示例**：
  ```xml
  <plugin>
      <groupId>org.apache.maven.plugins</groupId>
      <artifactId>maven-shade-plugin</artifactId>
      <version>3.5.0</version> <!-- 建议使用最新版本 -->
      <executions>
          <execution>
              <phase>package</phase>
              <goals>
                  <goal>shade</goal>
              </goals>
              <configuration>
                  <transformers>
                      <transformer implementation="org.apache.maven.plugins.shade.resource.ManifestResourceTransformer">
                          <mainClass>com.example.Main</mainClass>
                      </transformer>
                  </transformers>
              </configuration>
          </execution>
      </executions>
  </plugin>
  ```
  此示例通过配置主类生成可执行 JAR，并在 `package` 阶段触发插件执行

- **核心能力**：
  - **依赖内嵌**：将依赖库嵌入目标 JAR
  - **包重定位**：通过重命名包路径避免冲突（例如将 `com.google.common` 改为 `shaded.com.google.common`）
  - **资源处理**：合并或转换资源文件
  - **可执行化**：添加清单配置使 JAR 支持 `java -jar` 直接运行

### 适用时机：
- 需要单一 JAR 文件简化分发流程时
- 遇到依赖冲突（例如相同库的不同版本）时
- 向外部依赖管理困难的环境部署应用时

若需了解具体配置细节或应用场景，欢迎随时提问！
