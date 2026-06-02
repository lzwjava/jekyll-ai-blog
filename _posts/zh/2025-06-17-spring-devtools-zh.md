---
audio: false
generated: true
lang: zh
layout: post
title: Spring Boot DevTools 自动重启功能
translated: true
type: note
---

当使用 `mvn spring-boot:run` 运行 Spring Boot 应用时，默认情况下不会启用文件监视和自动重启或热重载功能。但您可以通过在项目中添加 `spring-boot-devtools` 依赖来启用这些功能。该模块提供了自动重启和 LiveReload 等功能，以加速开发过程。

### 详细说明

1. **未使用 DevTools 时的默认行为**：
   - 在没有 `spring-boot-devtools` 的情况下运行 `mvn spring-boot:run` 不会包含文件监视或自动重启功能。您需要手动停止并重启应用才能应用对 Java 类、静态资源或模板的更改。
   - 静态资源（例如 HTML、CSS、JS）可能需要完整重新构建或重启，除非另行配置。

2. **使用 `spring-boot-devtools` 时**：
   - **文件监视**：DevTools 会监视类路径上对 Java 文件、属性文件以及某些资源（例如 `/resources`、`/static`、`/templates`）的更改。
   - **自动重启**：当类路径上的文件发生更改时（例如 Java 类或属性文件），DevTools 会触发应用的自动重启。这比冷启动更快，因为它使用了两个类加载器：一个用于未更改的第三方库（基础类加载器），另一个用于您的应用代码（重启类加载器）。
   - **LiveReload**：对静态资源（例如 `/static`、`/public` 或 `/templates` 中的 HTML、CSS、JS）或模板（例如 Thymeleaf）的更改会触发浏览器刷新，而不是完全重启，前提是您已安装了 LiveReload 浏览器扩展（支持 Chrome、Firefox、Safari）。
   - **排除项**：默认情况下，`/META-INF/maven`、`/META-INF/resources`、`/resources`、`/static`、`/public` 和 `/templates` 中的资源不会触发重启，但会触发 LiveReload。您可以使用 `spring.devtools.restart.exclude` 自定义此行为。

3. **DevTools 的设置**：
   在 `pom.xml` 中添加以下依赖：

   ```xml
   <dependency>
       <groupId>org.springframework.boot</groupId>
       <artifactId>spring-boot-devtools</artifactId>
       <scope>runtime</scope>
       <optional>true</optional>
   </dependency>
   ```

   - `<optional>true</optional>` 确保 DevTools 不会包含在生产构建中。
   - 使用 `mvn spring-boot:run` 运行应用。DevTools 将自动启用文件监视和自动重启。

4. **在 IDE 中的行为**：
   - **Eclipse**：保存更改（Ctrl+S）会自动触发构建，DevTools 会检测到并重启应用。
   - **IntelliJ IDEA**：您需要手动触发构建（Ctrl+F9 或“Make Project”）才能使 DevTools 检测到更改，除非您配置了自动构建。或者，在 IntelliJ 设置中启用“Build project automatically”以实现无缝重启。
   - 对于 LiveReload，请从 <http://livereload.com/extensions/> 安装浏览器扩展并启用它。

5. **替代方案：Spring Loaded**：
   - 除了 DevTools，您还可以使用 Spring Loaded 进行更高级的热交换（例如方法签名更改）。将其添加到 `spring-boot-maven-plugin`：

     ```xml
     <plugin>
         <groupId>org.springframework.boot</groupId>
         <artifactId>spring-boot-maven-plugin</artifactId>
         <dependencies>
             <dependency>
                 <groupId>org.springframework</groupId>
                 <artifactId>springloaded</artifactId>
                 <version>1.2.8.RELEASE</version>
             </dependency>
         </dependencies>
     </plugin>
     ```

   - 与 DevTools 相比，Spring Loaded 不太推荐，因为它维护不积极，且可能不支持所有框架。

6. **静态资源的热重载**：
   - 在没有 DevTools 的情况下，您可以通过设置 `spring-boot-maven-plugin` 的 `addResources` 属性来启用静态资源的热重载：

     ```xml
     <plugin>
         <groupId>org.springframework.boot</groupId>
         <artifactId>spring-boot-maven-plugin</artifactId>
         <configuration>
             <addResources>true</addResources>
         </configuration>
     </plugin>
     ```

   - 这会将 `src/main/resources` 添加到类路径中，允许对静态文件进行原地编辑，但不如 DevTools 全面。

7. **注意事项**：
   - DevTools 在多模块项目中可能会引起类加载问题。如果发生这种情况，请尝试使用 `spring.devtools.restart.enabled=false` 禁用重启，或使用 JRebel 进行高级重载。
   - 对于非类路径文件，请使用 `spring.devtools.restart.additional-paths` 来监视其他目录。
   - LiveReload 需要浏览器扩展，并且可能不适用于所有前端设置（例如使用 Webpack 的 React）。
   - 如果重启速度较慢，请调整 `spring.devtools.restart.poll-interval` 和 `spring.devtools.restart.quiet-period` 以优化文件监视。

### 简单应用的步骤

1. 创建一个基本的 Spring Boot 应用（例如使用 Spring Initializr 并选择 `spring-boot-starter-web`）。
2. 将 `spring-boot-devtools` 依赖添加到 `pom.xml`。
3. 运行 `mvn spring-boot:run`。
4. 修改 Java 文件、属性文件或静态资源（例如 `src/main/resources/static` 中的 HTML）。
5. 观察自动重启（针对 Java/属性文件）或浏览器刷新（针对启用了 LiveReload 的静态资源）。

### 示例

对于一个带有 REST 控制器的简单应用：

```java
@RestController
public class HelloController {
    @GetMapping("/hello")
    public String hello() {
        return "Hello, World!";
    }
}
```

- 添加 DevTools，运行 `mvn spring-boot:run`，并更改 `hello()` 方法的返回值。应用将自动重启。
- 在 `src/main/resources/static` 中添加 `index.html`，安装 LiveReload 扩展，并修改 HTML。浏览器将刷新而无需重启。

### 结论

对于简单的 Spring Boot 应用，添加 `spring-boot-devtools` 是启用文件监视、自动重启和热重载的最简单方法。使用带有 DevTools 的 `mvn spring-boot:run` 可以获得无缝的开发体验。如果您需要更高级的热交换功能，请考虑使用 Spring Loaded 或 JRebel，但 DevTools 在大多数情况下已经足够。

---

以下是一个示例，展示如何使用 `application.yml` 文件为您的 Spring Boot 应用配置 `spring-boot-devtools` 以实现文件监视、自动重启和热重载。此配置根据您提供的日志（显示 DevTools 处于活动状态并监视 `target/classes`）为您的 `blog-server` 项目量身定制。

### `application.yml` 配置

```yaml
spring:
  devtools:
    restart:
      # 启用自动重启（默认：true）
      enabled: true
      # 监视其他目录以触发重启（例如自定义配置文件夹）
      additional-paths:
        - /home/lzw/Projects/blog-server/config
      # 排除触发重启的文件/目录（保留默认排除项）
      exclude: static/**,public/**,templates/**,logs/**,generated/**
      # 文件更改的轮询间隔（毫秒，默认：1000）
      poll-interval: 1000
      # 文件更改后重启前的静默期（毫秒，默认：400）
      quiet-period: 400
      # 可选：用于手动触发重启的文件
      trigger-file: .restart
    livereload:
      # 启用 LiveReload 以在静态资源更改时刷新浏览器（默认：true）
      enabled: true
```

### 设置说明

- **`spring.devtools.restart.enabled`**：当类路径文件更改时（例如 `target/classes`，如您的日志所示：`file:/home/lzw/Projects/blog-server/target/classes/`）启用自动重启。
- **`spring.devtools.restart.additional-paths`**：监视额外目录（例如 `/home/lzw/Projects/blog-server/config`）的更改以触发重启。
- **`spring.devtools.restart.exclude`**：防止对 `static/`、`public/`、`templates/`、`logs/` 或 `generated/` 目录中的更改触发重启，同时允许对静态资源（例如 HTML、CSS、JS）使用 LiveReload。
- **`spring.devtools.restart.poll-interval`**：设置 DevTools 检查文件更改的频率（1000ms = 1 秒）。
- **`spring.devtools.restart.quiet-period`**：在检测到更改后等待 400ms，以确保没有进一步的更改待处理，然后再重启。
- **`spring.devtools.restart.trigger-file`**：通过更新 `.restart` 允许手动重启（例如 `touch /home/lzw/Projects/blog-server/.restart`）。
- **`spring.devtools.livereload.enabled`**：启用 LiveReload 服务器，该服务器会触发浏览器刷新以响应 `static/` 或 `templates/` 中的更改（需要 LiveReload 浏览器扩展）。

### 应用步骤

1. 使用上述配置创建或更新 `src/main/resources/application.yml`。
2. 确保 `spring-boot-devtools` 在您的 `pom.xml` 中：

   ```xml
   <dependency>
       <groupId>org.springframework.boot</groupId>
       <artifactId>spring-boot-devtools</artifactId>
       <scope>runtime</scope>
       <optional>true</optional>
   </dependency>
   ```

3. 运行 `mvn spring-boot:run`。DevTools 将监视 `target/classes` 和 `/home/lzw/Projects/blog-server/config`（如果已添加），在 Java 或属性文件更改时重启应用，并在静态资源更改时刷新浏览器。
4. 对于 LiveReload，请安装浏览器扩展（例如从 <http://livereload.com/extensions/）或在前端集成> LiveReload 客户端。

### 注意事项

- 您的日志显示启动速度很快（0.8 秒），因此默认的 `poll-interval` 和 `quiet-period` 应该没问题。如果在较大的项目中重启感觉迟缓，请调整它们（例如 `poll-interval: 500`）。
- 如果不需要 LiveReload（例如使用单独的前端开发服务器），请设置 `livereload.enabled: false`。
- 对于手动重启，请在项目根目录中创建 `.restart` 并在需要时更新它。

此 YAML 配置应与您的设置无缝协作，增强您已经看到的文件监视和自动重启功能。
