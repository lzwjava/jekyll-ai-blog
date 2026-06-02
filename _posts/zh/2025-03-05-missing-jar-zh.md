---
audio: false
generated: true
lang: zh
layout: post
title: WebSphere Liberty 中缺失的 JAR 文件
translated: true
type: note
---

在 WebSphere Liberty 中，您可能会在 `console.log` 文件中看到类似这样的警告：*"清单类路径中的 grpc-protobuf.jar 在 ..ear/war 或其父级 jar 文件中找不到"*。这些警告表明服务器无法找到 `grpc-protobuf.jar` 文件，该文件在应用程序的 EAR 或 WAR 文件的清单类路径中被引用。下面，我将回答您的问题：这些警告是否重要，是否会影响应用程序的运行，以及如何消除它们。

---

### 这些警告重要吗？

这取决于缺失的 JAR 是否是应用程序所必需的：

- **如果 JAR 是必需的：**
  如果 `grpc-protobuf.jar` 包含应用程序在运行时需要的类或资源，那么这个警告是重要的。没有这个 JAR，您的应用程序可能会遇到运行时错误，例如 `ClassNotFoundException`，这可能导致部分功能失败或行为异常。

- **如果 JAR 不需要：**
  如果该 JAR 实际上并不需要——可能是旧配置的残留引用或可选依赖项——那么警告是无害的，不会影响应用程序的功能。但它仍然会干扰日志记录。

简而言之，如果缺失的 JAR 对您的应用程序至关重要，那么这些警告就很重要。您需要进一步调查以确定其重要性。

---

### 是否会影响应用程序的运行？

对应用程序运行时的影响取决于缺失 JAR 的作用：

- **如果 JAR 是必需的：**
  如果您的应用程序尝试使用 `grpc-protobuf.jar` 中的类或资源，而该 JAR 缺失，您很可能会看到运行时错误。这可能导致应用程序无法正常工作或完全失败。

- **如果 JAR 不需要：**
  如果该 JAR 不是必需的，您的应用程序将正常运行，尽管有警告。该消息将仅作为干扰存在于日志中。

为了确认，请检查应用程序的行为和日志，查看是否有超出警告本身的其他错误。如果一切正常，该 JAR 可能不是必需的。

---

### 如何消除警告？

要消除警告，您需要确保 JAR 正确包含在应用程序中，或者删除对它的不必要引用。以下是逐步解决方法：

1. **验证 JAR 是否必需：**
   - 查看应用程序的文档、源代码或依赖项列表（例如，如果使用 Maven，请查看 `pom.xml`），以确定是否需要 `grpc-protobuf.jar`。
   - 如果不需要，请转到步骤 3 以删除引用。如果需要，请继续步骤 2。

2. **修正打包（如果 JAR 是必需的）：**
   - 确保 `grpc-protobuf.jar` 包含在应用程序包的正确位置中：
     - **对于 WAR 文件：** 将其放在 `WEB-INF/lib` 目录中。
     - **对于 EAR 文件：** 将其放在 EAR 的根目录或指定的库目录中（例如 `lib/`）。
   - 重新构建并重新部署应用程序，确认 WebSphere Liberty 现在可以找到该 JAR。
   - 检查 `console.log` 文件，查看警告是否消失。

3. **更新清单（如果 JAR 不需要）：**
   - 打开 EAR 或 WAR 中的 `MANIFEST.MF` 文件，该文件位于 `META-INF/` 目录中。
   - 查找 `Class-Path` 属性，它可能如下所示：

     ```
     Class-Path: grpc-protobuf.jar some-other-lib.jar
     ```

   - 删除对 `grpc-protobuf.jar` 的引用，使其不再出现在列表中。
   - 保存文件，重新构建应用程序并重新部署。警告应不再出现。

4. **检查类路径配置：**
   - 如果您的应用程序在 WebSphere Liberty 中使用共享库或自定义类加载器，请验证服务器的配置（例如 `server.xml`）是否包含必要的 JAR，或者没有错误地引用 `grpc-protobuf.jar`。
   - 如果需要，调整配置并重新启动服务器。

---

### 一般建议

- **调查警告：** 即使应用程序似乎运行正常，了解警告的原因以避免以后出现意外情况是一个好习惯。
- **更改后测试：** 在添加 JAR 或更新清单后，彻底测试您的应用程序，确保其行为符合预期。
- **保持日志清洁：** 解决不必要的警告可以使日志保持清晰，便于将来发现真正的问题。

通过遵循这些步骤，您可以确定 `grpc-protobuf.jar` 警告是否关键，解决任何潜在的运行时影响，并从 WebSphere Liberty 的 `console.log` 中消除警告。

---

当您运行 `mvn package` 构建 EAR 文件并遇到清单类路径中缺失 JAR（如 `grpc-protobuf.jar`）的警告时，问题不太可能源于缺少命令行参数。`mvn package` 命令本身足以触发 Maven 构建生命周期直至 `package` 阶段，该阶段包括编译、测试和打包您的 EAR。然而，该警告表明您的 Maven 项目存在配置问题，而不是命令或其参数的问题。让我们逐步探讨这个问题。

---

### 警告的含义是什么？

该警告表明您的 EAR 中的 `MANIFEST.MF` 文件在其 `Class-Path` 属性中引用了 `grpc-protobuf.jar`，但在 EAR 的预期位置（例如 `lib/` 目录）中找不到该 JAR。`Class-Path` 属性列出了应用程序在运行时需要的 JAR，缺失的 JAR 可能导致运行时错误，例如 `ClassNotFoundException`。

---

### 是否与缺少参数有关？

不，您不需要为 `mvn package` 添加额外的参数来解决此问题。Maven 依赖于您的项目的 `pom.xml` 文件和插件配置（例如 `maven-ear-plugin`）来确定 EAR 中包含的内容以及如何生成清单。添加诸如 `-DskipTests` 或 `-U` 之类的参数可能会调整构建过程，但它们不会直接解决此警告。根本原因在于您的项目设置，而不是命令本身。

---

### 警告的常见原因

以下是导致警告的可能原因：

1. **缺少依赖声明**
   如果 `grpc-protobuf.jar` 是您的应用程序所必需的，它可能未在您的 EAR 模块的 `pom.xml` 或其子模块（例如 WAR 或 JAR 模块）中声明为依赖项。

2. **依赖作用域错误**
   如果 `grpc-protobuf.jar` 被声明为 `provided` 等作用域，Maven 会假设它由运行时环境（例如 WebSphere Liberty）提供，因此不会将其打包到 EAR 中。

3. **不需要的清单条目**
   `maven-ear-plugin` 可能被配置为将 `grpc-protobuf.jar` 添加到清单的 `Class-Path` 中，即使它未包含在 EAR 中。

4. **传递依赖问题**
   该 JAR 可能是一个传递依赖项（另一个依赖项的依赖项），但被排除或未正确包含在 EAR 中。

---

### 如何调查

要定位问题，请尝试以下步骤：

1. **检查清单文件**
   运行 `mvn package` 后，解压缩生成的 EAR 并查看 `META-INF/MANIFEST.MF`。检查 `grpc-protobuf.jar` 是否在 `Class-Path` 中列出。这可以确认警告是否与清单内容匹配。

2. **查看 EAR 的 `pom.xml`**
   检查 `maven-ear-plugin` 配置。例如：

   ```xml
   <plugin>
       <groupId>org.apache.maven.plugins</groupId>
       <artifactId>maven-ear-plugin</artifactId>
       <version>3.2.0</version>
       <configuration>
           <version>7</version> <!-- 匹配您的 Java EE 版本 -->
           <defaultLibBundleDir>lib</defaultLibBundleDir>
       </configuration>
   </plugin>
   ```

   确保它设置为将依赖项包含在 `lib/` 目录中（或您的 JAR 应放置的位置）。

3. **检查依赖项**
   在您的 EAR 模块上运行 `mvn dependency:tree`，查看 `grpc-protobuf.jar` 是否出现。如果缺失，则表示它在您的依赖项树中未声明。

4. **查看子模块**
   如果您的 EAR 包含 WAR 或 JAR，请检查它们的 `pom.xml` 文件是否依赖 `grpc-protobuf.jar`。

---

### 如何修复

根据您的发现，应用以下解决方案之一：

1. **如果 JAR 是必需的**
   在您的 EAR 的 `pom.xml` 中添加 `grpc-protobuf.jar` 作为依赖项：

   ```xml
   <dependency>
       <groupId>io.grpc</groupId>
       <artifactId>grpc-protobuf</artifactId>
       <version>1.39.0</version> <!-- 使用正确的版本 -->
   </dependency>
   ```

   确保 `maven-ear-plugin` 将其包含在 EAR 中（例如在 `lib/` 目录中）。

2. **如果作用域错误**
   如果它被声明为 `<scope>provided</scope>` 但需要打包，请将其更改为 `<scope>compile</scope>`（默认作用域）。

3. **如果 JAR 不需要**
   如果 `grpc-protobuf.jar` 不应出现在清单中，请检查 `maven-ear-plugin` 中的自定义清单配置：

   ```xml
   <configuration>
       <manifestFile>META-INF/MANIFEST.MF</manifestFile>
   </configuration>
   ```

   删除任何手动添加的 `grpc-protobuf.jar` 条目，或让 Maven 自动生成清单。

4. **处理传递依赖**
   如果它是您不需要的传递依赖项，请排除它：

   ```xml
   <dependency>
       <groupId>some.group</groupId>
       <artifactId>some-artifact</artifactId>
       <exclusions>
           <exclusion>
               <groupId>io.grpc</groupId>
               <artifactId>grpc-protobuf</artifactId>
           </exclusion>
       </exclusions>
   </dependency>
   ```

5. **重新构建并验证**
   运行 `mvn clean package` 重新构建 EAR，然后检查输出的 EAR 文件，确保警告消失且结构正确。

---

### 结论

`mvn package` 命令本身不需要额外的参数来解决此警告。相反，问题很可能源于您的 `pom.xml` 或 `maven-ear-plugin` 的配置错误。通过确保 `grpc-protobuf.jar` 被正确包含（如果需要）或从清单中删除（如果不需要），您可以消除警告。首先检查您的清单和依赖项，然后相应地调整配置。这应该可以在不更改构建命令的情况下解决问题。
