---
audio: false
generated: true
lang: zh
layout: post
title: Spring Boot 属性文件选择方案
translated: true
type: note
---

在 Spring Boot Maven 项目中，若存在两个属性文件 `appProperties.properties` 和 `appProperties-hk.properties`，且位于 `src/main/resources` 目录下。要控制使用哪个属性文件，特别是指定使用带 `-hk` 后缀的属性文件，可以利用 Spring Boot 的配置机制。具体操作如下：

### 解决方案

1. **创建 `application.properties` 文件**
   - 默认情况下，Spring Boot 会在 `src/main/resources` 目录下查找 `application.properties` 或 `application.yml` 来加载配置设置。
   - 要使用自定义属性文件（`appProperties.properties` 和 `appProperties-hk.properties`），需要告知 Spring Boot 查找基础名称为 `appProperties` 的文件，而非默认的 `application`。
   - 在 `src/main/resources` 目录下新建 `application.properties` 文件，并添加以下行：

     ```properties
     spring.config.name=appProperties
     ```

   - 此设置会指示 Spring Boot 将 `appProperties.properties` 作为基础配置文件加载，并在激活特定配置文件时自动查找对应的变体文件，例如 `appProperties-{profile}.properties`。

2. **使用 Spring 配置文件指定 `-hk` 属性**
   - Spring Boot 支持配置文件功能，允许根据激活的配置文件加载附加或覆盖的属性文件。
   - 由于文件命名为 `appProperties-hk.properties`，符合 `appProperties-{profile}.properties` 的命名模式。此处可将 "hk" 视为配置文件名。
   - 要使用 `appProperties-hk.properties`，只需在运行应用时激活 "hk" 配置文件。Spring Boot 便会同时加载 `appProperties.properties` 和 `appProperties-hk.properties`，且后者中的属性会覆盖前者中的同名属性。

3. **激活 "hk" 配置文件的方法**
   - **通过命令行**：运行 Spring Boot 应用时，使用 `--spring.profiles.active` 参数指定激活的配置文件。例如：
     ```bash
     java -jar target/myapp.jar --spring.profiles.active=hk
     ```
     请将 `myapp.jar` 替换为 Maven 生成的实际应用 JAR 文件名。

   - **通过 Maven**：如果使用 `spring-boot:run` 目标运行应用，可在 `pom.xml` 中配置配置文件：
     ```xml
     <plugin>
         <groupId>org.springframework.boot</groupId>
         <artifactId>spring-boot-maven-plugin</artifactId>
         <configuration>
             <profiles>
                 <profile>hk</profile>
             </profiles>
         </configuration>
     </plugin>
     ```
     随后运行：
     ```bash
     mvn spring-boot:run
     ```

   - **通过系统属性**：将配置文件设置为 JVM 参数：
     ```bash
     java -Dspring.profiles.active=hk -jar target/myapp.jar
     ```

   - **通过环境变量**：在环境中导出配置文件（例如在类 Unix 系统中）：
     ```bash
     export SPRING_PROFILES_ACTIVE=hk
     java -jar target/myapp.jar
     ```

### 工作原理
- 在 `application.properties` 中设置 `spring.config.name=appProperties` 后，Spring Boot 会使用 `appProperties` 作为配置文件的基础名称。
- 当未激活任何配置文件时，仅加载 `appProperties.properties`。
- 当激活 "hk" 配置文件时（例如通过 `--spring.profiles.active=hk`），Spring Boot 会同时加载 `appProperties.properties` 和 `appProperties-hk.properties`。若存在重复属性，`appProperties-hk.properties` 中定义的属性将优先于 `appProperties.properties` 中的属性。

### 最终步骤
- 确保 `appProperties.properties` 和 `appProperties-hk.properties` 均位于 `src/main/resources` 目录中。
- 在 `src/main/resources` 目录下添加包含 `spring.config.name=appProperties` 的 `application.properties` 文件。
- 通过激活 "hk" 配置文件运行应用，以使用带 `-hk` 后缀的属性文件。

这种方法遵循 Spring Boot 的约定，成为在项目中控制属性文件使用的典型且直接的方式。要特别使用带 `-hk` 后缀的属性文件，只需按上述方法激活 "hk" 配置文件即可。
