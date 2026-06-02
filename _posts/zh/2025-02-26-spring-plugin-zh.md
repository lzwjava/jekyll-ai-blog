---
audio: false
generated: true
lang: zh
layout: post
title: Spring Boot Maven 插件
translated: true
type: note
---

要在基于 Maven 的 Spring Boot 项目中使用 `spring-boot-maven-plugin`，请按照以下步骤配置和使用该插件来构建、运行和管理应用程序。以下是完整指南：

---

### **1. 确保项目是 Spring Boot 项目**

在使用 `spring-boot-maven-plugin` 之前，请确认您的项目已设置为 Spring Boot 项目。这通常包括：

- **继承 `spring-boot-starter-parent`（推荐）**：
  - 在 `pom.xml` 中将 `spring-boot-starter-parent` 设置为父项目，以管理 Spring Boot 依赖项和插件版本。
  - 示例：

    ```xml
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.5.4</version> <!-- 替换为您的 Spring Boot 版本 -->
        <relativePath/> <!-- 从仓库查找父项目 -->
    </parent>
    ```

- **或者，使用 `spring-boot-dependencies` BOM（物料清单）**：
  - 如果无法使用 `spring-boot-starter-parent`，请在 `dependencyManagement` 部分导入 `spring-boot-dependencies` BOM。
  - 示例：

    ```xml
    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-dependencies</artifactId>
                <version>2.5.4</version> <!-- 替换为您的 Spring Boot 版本 -->
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>
    ```

推荐使用 `spring-boot-starter-parent`，因为它会自动管理插件版本，操作更简单。

---

### **2. 将 `spring-boot-maven-plugin` 添加到 `pom.xml`**

要使用该插件，需要在 `pom.xml` 的 `<build><plugins>` 部分声明它。

- **如果使用 `spring-boot-starter-parent`**：
  - 添加插件时无需指定版本，因为父项目已管理版本。
  - 示例：

    ```xml
    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
    ```

- **如果不使用 `spring-boot-starter-parent`**：
  - 明确指定版本，确保与使用的 Spring Boot 版本匹配。
  - 示例：

    ```xml
    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <version>2.5.4</version> <!-- 替换为您的 Spring Boot 版本 -->
            </plugin>
        </plugins>
    </build>
    ```

---

### **3. 使用插件目标**

`spring-boot-maven-plugin` 提供了多个目标，帮助构建、运行和管理 Spring Boot 应用程序。以下是最常用的目标：

- **`spring-boot:run`**
  - 使用嵌入式 Web 服务器（例如 Tomcat）直接从 Maven 运行 Spring Boot 应用程序。
  - 适用于开发和测试。
  - 命令：

    ```
    mvn spring-boot:run
    ```

- **`spring-boot:repackage`**
  - 将 `mvn package` 生成的 JAR 或 WAR 文件重新打包为包含所有依赖项的可执行“fat JAR”或 WAR。
  - 如果配置了该插件，此目标会在 `package` 阶段自动执行。
  - 命令：

    ```
    mvn package
    ```

  - 运行后，可以使用以下命令启动应用程序：

    ```
    java -jar target/myapp.jar
    ```

- **`spring-boot:start` 和 `spring-boot:stop`**
  - 用于集成测试，分别在 `pre-integration-test` 和 `post-integration-test` 阶段启动和停止应用程序。
  - 示例：

    ```
    mvn spring-boot:start
    mvn spring-boot:stop
    ```

- **`spring-boot:build-info`**
  - 生成包含构建信息（例如构建时间、版本）的 `build-info.properties` 文件。
  - 该信息可以通过 Spring Boot 的 `BuildProperties` Bean 或 `@Value` 注解在应用程序中访问。
  - 命令：

    ```
    mvn spring-boot:build-info
    ```

---

### **4. 自定义插件配置（可选）**

您可以通过在 `pom.xml` 中添加配置选项来自定义 `spring-boot-maven-plugin` 的行为。以下是一些常见的自定义配置：

- **指定主类**：
  - 如果插件无法自动检测到主类，请手动指定。
  - 示例：

    ```xml
    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <configuration>
                    <mainClass>com.example.MyApplication</mainClass>
                </configuration>
            </plugin>
        </plugins>
    </build>
    ```

- **从 Fat JAR 中排除依赖项**：
  - 排除由运行时环境（例如外部 servlet 容器）提供的依赖项。
  - 示例：

    ```xml
    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <configuration>
                    <excludes>
                        <exclude>
                            <groupId>com.example</groupId>
                            <artifactId>some-dependency</artifactId>
                        </exclude>
                    </excludes>
                </configuration>
            </plugin>
        </plugins>
    </build>
    ```

- **设置应用程序参数**：
  - 配置在运行 `spring-boot:run` 时传递给应用程序的参数。
  - 在 `pom.xml` 中的示例：

    ```xml
    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <configuration>
                    <arguments>
                        <argument>--server.port=8081</argument>
                    </arguments>
                </configuration>
            </plugin>
        </plugins>
    </build>
    ```

  - 或者，通过命令行传递参数：

    ```
    mvn spring-boot:run -Dspring-boot.run.arguments=--server.port=8081
    ```

- **构建 WAR 文件**：
  - 如果要构建 WAR 文件以部署到外部 servlet 容器，请确保在 `pom.xml` 中将项目打包方式设置为 `war`：

    ```xml
    <packaging>war</packaging>
    ```

  - 如果环境提供了嵌入式 servlet 容器（例如 Tomcat），可能需要排除它们。将以下依赖项添加为 `provided`：

    ```xml
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-tomcat</artifactId>
            <scope>provided</scope>
        </dependency>
    </dependencies>
    ```

---

### **5. 关键注意事项**

- **默认行为**：
  - 当运行 `mvn package` 时，插件会在 `package` 阶段自动重新打包 JAR/WAR，使其可执行。
  - 重新打包后的工件是主要工件，原始 JAR/WAR 会附加分类器（例如 `original`）。

- **开发工作流**：
  - 使用 `mvn spring-boot:run` 进行快速开发和测试。
  - 使用 `mvn package` 构建可部署的可执行 JAR 或 WAR。

- **集成测试**：
  - 使用 `spring-boot:start` 和 `spring-boot:stop` 在集成测试期间管理应用程序生命周期。

---

### **总结**

要使用 `spring-boot-maven-plugin`：

1. 确保您的项目是 Spring Boot 项目，通常通过继承 `spring-boot-starter-parent` 或使用 `spring-boot-dependencies` BOM 实现。
2. 将插件添加到 `pom.xml` 的 `<build><plugins>` 部分。
3. 使用 Maven 命令，例如：
   - `mvn spring-boot:run` 运行应用程序。
   - `mvn package` 构建可执行 JAR/WAR。
   - 根据需要使用的其他目标，如 `spring-boot:start`、`spring-boot:stop` 和 `spring-boot:build-info`。
4. 可选地，在 `pom.xml` 中自定义插件配置以满足高级用例。

此设置使您能够使用 Maven 高效地构建、运行和管理 Spring Boot 应用程序。
