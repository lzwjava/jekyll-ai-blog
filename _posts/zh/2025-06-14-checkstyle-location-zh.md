---
audio: false
generated: true
lang: zh
layout: post
title: Checkstyle配置文件位置
translated: true
type: note
---

要解决运行 `mvn clean checkstyle:check` 时遇到的 `maven-checkstyle-plugin` 问题（即无法找到 `checks.xml` 文件以及初始化 `SuppressWithNearbyTextFilter` 模块失败），请按照以下步骤操作。这些问题源于文件位置和不兼容的 Checkstyle 版本。以下是完整的解决方案：

---

### 步骤 1：修复 `checks.xml` 文件位置
错误提示插件无法找到 `checks.xml`。由于该文件位于项目根目录（而非插件通常查找的 `src/main/resources` 目录），您需要明确告知插件其位置。

- **操作**：更新 `pom.xml` 中的 `<configLocation>`，使其指向项目根目录。

---

### 步骤 2：解决 `SuppressWithNearbyTextFilter` 错误
`SuppressWithNearbyTextFilter` 模块初始化失败是因为插件使用的 Checkstyle 版本过旧，不支持此过滤器。您需要升级插件并指定兼容的 Checkstyle 版本。

- **操作**：将 `maven-checkstyle-plugin` 升级至版本 `3.3.1`，并添加对 Checkstyle 版本 `10.17.0` 的依赖，该版本支持 `SuppressWithNearbyTextFilter`。

---

### 更新后的 `pom.xml` 配置
按如下方式修改 `pom.xml` 中的 `maven-checkstyle-plugin` 部分：

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-checkstyle-plugin</artifactId>
    <version>3.3.1</version> <!-- 升级至最新版本 -->
    <configuration>
        <configLocation>${project.basedir}/checks.xml</configLocation> <!-- 指向项目根目录的 checks.xml -->
    </configuration>
    <dependencies>
        <dependency>
            <groupId>com.puppycrawl.tools</groupId>
            <artifactId>checkstyle</artifactId>
            <version>10.17.0</version> <!-- 支持 SuppressWithNearbyTextFilter -->
        </dependency>
    </dependencies>
    <executions>
        <execution>
            <id>checkstyle-check</id>
            <phase>compile</phase>
            <goals>
                <goal>check</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```

#### 说明：
- **`<configLocation>${project.basedir}/checks.xml</configLocation>`**：指定 `checks.xml` 位于项目根目录（`${project.basedir}` 是 Maven 属性，表示根目录）。
- **`version 3.3.1`**：使用更新的插件版本以获得更好的兼容性。
- **Checkstyle `10.17.0` 依赖**：确保插件使用包含 `SuppressWithNearbyTextFilter` 的 Checkstyle 版本。

---

### 步骤 3：验证 `checks.xml` 配置
确保 `checks.xml` 中的 `SuppressWithNearbyTextFilter` 模块正确定义。示例配置可能如下：

```xml
<module name="SuppressWithNearbyTextFilter">
    <property name="nearbyTextPattern" value="@SuppressWarnings"/>
</module>
```

- **操作**：检查 `checks.xml` 是否存在拼写错误或不正确的属性。详情请参考 [Checkstyle 文档](https://checkstyle.org/filters/suppresswithnearbytextfilter.html)。
- **故障排除提示**：如果错误仍然存在，请暂时从 `checks.xml` 中移除 `SuppressWithNearbyTextFilter` 模块，然后运行 `mvn checkstyle:check`，以确定问题是否特定于此过滤器。

---

### 步骤 4：测试修复
- 运行以下命令进行测试：
  ```bash
  mvn clean checkstyle:check
  ```
- 如果修复成功，插件应能找到 `checks.xml` 并处理所有模块而无错误。
- 要确保 Checkstyle 在编译期间运行，请使用：
  ```bash
  mvn compile
  ```

---

### 可选：替代文件位置
如果您倾向于更标准的 Maven 设置：
- 将 `checks.xml` 移至 `src/main/resources/checks.xml`。
- 将 `<configLocation>` 更新为：
  ```xml
  <configLocation>classpath:checks.xml</configLocation>
  ```
- 这符合 Maven 将资源放置在 `src/main/resources` 的约定。

---

### 补充说明
- **无关警告**：如果您在 `/usr/share/maven/conf/settings.xml` 中看到有关 `<blocked>` 标签的警告，这与当前问题无关，但表明您的 Maven 设置文件存在问题。如有需要，请单独检查。
- **问题仍未解决？** 请提供以下信息以获取进一步帮助：
  - `checks.xml` 的内容（或片段）。
  - `mvn clean checkstyle:check -X` 的完整输出（调试模式）。

---

通过应用这些更改，`maven-checkstyle-plugin` 应能正确定位 `checks.xml` 并支持 `SuppressWithNearbyTextFilter`，从而解决您的错误。

---

您之前遇到的错误表明 `maven-checkstyle-plugin` 无法在类路径中找到 `checks.xml`，随后因 `SuppressWithNearbyTextFilter` 模块的问题而失败。从您更新的项目结构来看，`checks.xml` 位于项目根目录（`~/Projects/blog-server/checks.xml`），而非之前假设的 `src/main/resources`。这解释了为什么插件在配置为 `<configLocation>classpath:checks.xml</configLocation>` 或 `<configLocation>checks.xml</configLocation>` 时无法找到该文件，因为这些设置期望文件位于类路径中（通常是 `src/main/resources`）。

要解决此问题并确保 `maven-checkstyle-plugin` 在运行 `mvn compile` 时使用您位于项目根目录的自定义 `checks.xml`，您需要更新 `<configLocation>` 以指向文件的绝对路径或项目相对路径。此外，您需要通过确保与 Checkstyle 版本的兼容性来解决 `SuppressWithNearbyTextFilter` 问题。以下是逐步解决方案。

### 更新后的 `pom.xml` 配置
修改 `pom.xml` 中的 `maven-checkstyle-plugin`，以引用项目根目录的 `checks.xml`，并使用兼容的 Checkstyle 版本来支持 `SuppressWithNearbyTextFilter`。

```xml
<build>
    <resources>
        <resource>
            <directory>src/main/resources</directory>
            <includes>
                <include>**/*.xml</include>
                <include>**/*.yaml</include>
            </includes>
        </resource>
    </resources>
    <plugins>
        <plugin>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-maven-plugin</artifactId>
            <version>3.4.2</version>
            <executions>
                <execution>
                    <goals>
                        <goal>repackage</goal>
                    </goals>
                </execution>
            </executions>
        </plugin>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-surefire-plugin</artifactId>
            <version>3.0.0-M8</version>
        </plugin>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-checkstyle-plugin</artifactId>
            <version>3.3.1</version> <!-- 最新版本以获得更好兼容性 -->
            <configuration>
                <configLocation>${project.basedir}/checks.xml</configLocation> <!-- 指向项目根目录的 checks.xml -->
            </configuration>
            <dependencies>
                <dependency>
                    <groupId>com.puppycrawl.tools</groupId>
                    <artifactId>checkstyle</artifactId>
                    <version>10.17.0</version> <!-- 支持 SuppressWithNearbyTextFilter -->
                </dependency>
            </dependencies>
            <executions>
                <execution>
                    <id>checkstyle-check</id>
                    <phase>compile</phase>
                    <goals>
                        <goal>check</goal>
                    </goals>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

### 更改说明
1. **更新 `<configLocation>`**：
   - 更改为 `${project.basedir}/checks.xml`，以指向项目根目录的 `checks.xml`（`~/Projects/blog-server/checks.xml`）。
   - `${project.basedir}` 解析为包含 `pom.xml` 的目录，确保插件无论类路径如何都能找到文件。

2. **升级插件版本**：
   - 将 `maven-checkstyle-plugin` 更新至 `3.3.1`（截至 2025 年 6 月的最新版本），以获得更好的兼容性和错误修复。

3. **添加 Checkstyle 依赖**：
   - 添加了 Checkstyle `10.17.0` 的 `<dependency>`，该版本支持 `SuppressWithNearbyTextFilter`。`maven-checkstyle-plugin:3.1.1` 中的默认 Checkstyle 版本（`8.29`）不支持此过滤器，导致之前的错误。

4. **保留 `<phase>compile</phase>`**：
   - 确保 `checkstyle:check` 在 `mvn compile` 期间运行，如您所要求。

5. **资源部分**：
   - 保留了 `<resources>` 部分以确保处理 `src/main/resources` 文件（如 `application.yaml`），尽管这与 `checks.xml` 无直接关系，因为它现在位于项目根目录。

### 验证 `checks.xml` 内容
关于 `SuppressWithNearbyTextFilter` 的错误表明您的 `checks.xml` 引用了此过滤器。请确保其正确配置。有效示例如下：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE module PUBLIC
    "-//Checkstyle//DTD Checkstyle Configuration 1.3//EN"
    "https://checkstyle.org/dtds/configuration_1_3.dtd">
<module name="Checker">
    <module name="SuppressWithNearbyTextFilter">
        <!-- 示例属性，根据需要调整 -->
        <property name="nearbyTextPattern" value="@SuppressWarnings"/>
    </module>
    <module name="TreeWalker">
        <!-- 其他检查 -->
        <module name="ConstantName"/>
    </module>
</module>
```

- **检查**：打开 `~/Projects/blog-server/checks.xml` 处的 `checks.xml`，并验证 `SuppressWithNearbyTextFilter` 是否拼写正确且包含任何必需属性（参见 [Checkstyle 文档](https://checkstyle.org/filters/suppresswithnearbytextfilter.html)）。
- **操作**：如果不确定，请暂时移除 `<module name="SuppressWithNearbyTextFilter"/>` 部分并进行测试以隔离问题。

### 测试配置
1. **清理项目**：
   ```bash
   mvn clean
   ```
   这将移除 `target` 目录，包括 `checkstyle-checker.xml` 和 `checkstyle-result.xml`，确保没有陈旧的构件干扰。

2. **运行 Checkstyle**：
   ```bash
   mvn checkstyle:check
   ```
   这将独立测试 Checkstyle 配置。

3. **运行编译**：
   ```bash
   mvn compile
   ```
   由于绑定了 `compile` 阶段，这应运行 Checkstyle，然后如果没有违规导致构建失败，则进行编译。

### 如果问题持续存在，请进行调试
如果遇到错误：
1. **检查文件路径**：
   - 确认 `checks.xml` 存在于 `~/Projects/blog-server/checks.xml`。
   - 验证文件名确为 `checks.xml`（区分大小写，无隐藏扩展名）。

2. **使用调试日志运行**：
   ```bash
   mvn clean checkstyle:check -X
   ```
   查找有关 `checks.xml` 加载或 `SuppressWithNearbyTextFilter` 初始化的消息。如果错误持续存在，请分享相关输出。

3. **使用最小化 `checks.xml` 进行测试**：
   临时将 `checks.xml` 替换为最小化配置，以排除文件内容的问题：
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE module PUBLIC
       "-//Checkstyle//DTD Checkstyle Configuration 1.3//EN"
       "https://checkstyle.org/dtds/configuration_1_3.dtd">
   <module name="Checker">
       <module name="TreeWalker">
           <module name="ConstantName"/>
       </module>
   </module>
   ```
   然后运行 `mvn checkstyle:check`。如果此配置工作正常，则问题出在原始 `checks.xml` 中的 `SuppressWithNearbyTextFilter` 或其他模块。

### 补充说明
- **Settings.xml 警告**：您的输出显示 `/usr/share/maven/conf/settings.xml` 中存在关于无法识别的 `<blocked>` 标签的警告。这与 Checkstyle 问题无关，但表明您的 Maven 配置可能存在潜在问题。请检查 `/usr/share/maven/conf/settings.xml` 的第 164 行，并移除或更正 `<blocked>` 标签，因为它不是标准的 Maven 设置元素。
- **替代文件位置**：如果您愿意，可以将 `checks.xml` 移至 `src/main/resources/checks.xml`，并将 `<configLocation>` 恢复为 `classpath:checks.xml`。这对于 Maven 项目更为常规，因为资源会自动包含在类路径中。
- **违规时失败**：如果 Checkstyle 违规导致构建失败，而您希望允许编译继续进行，请在插件的 `<configuration>` 中添加 `<failOnViolation>false</failOnViolation>`：
  ```xml
  <configuration>
      <configLocation>${project.basedir}/checks.xml</configLocation>
      <failOnViolation>false</failOnViolation>
  </configuration>
  ```

### 验证
应用更改后：
1. 运行 `mvn clean compile` 并确认：
   - Checkstyle 使用项目根目录的 `checks.xml` 运行。
   - 没有出现与 `checks.xml` 或 `SuppressWithNearbyTextFilter` 相关的错误。
   - 如果 Checkstyle 通过或配置为不使构建失败，则编译继续进行。
2. 检查 `target/checkstyle-result.xml` 以查看 Checkstyle 结果。

如果错误仍然存在，请分享：
- `checks.xml` 的内容（或相关片段）。
- `mvn clean checkstyle:check -X` 的调试输出。
- 您尝试使用 `SuppressWithNearbyTextFilter` 强制执行的任何特定 Checkstyle 规则。
