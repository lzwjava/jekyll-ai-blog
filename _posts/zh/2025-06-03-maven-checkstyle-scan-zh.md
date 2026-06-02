---
audio: false
generated: true
lang: zh
layout: post
title: Maven Checkstyle：持续扫描
translated: true
type: note
---

要让 `mvn checkstyle:check` 在发现代码规范违规时不立即终止，而是继续扫描所有模块，您需要配置 Checkstyle Maven 插件来禁用 `failOnViolation` 选项。默认情况下，`failOnViolation` 设置为 `true`，这会在检测到违规时立即停止构建。将其设置为 `false` 可让扫描在所有模块中完成，报告所有违规而不会中断构建。

### 解决方案
按如下方式更新您的 `pom.xml` 来配置 Checkstyle 插件：

```xml
<build>
  <plugins>
    <plugin>
      <groupId>org.apache.maven.plugins</groupId>
      <artifactId>maven-checkstyle-plugin</artifactId>
      <version>3.3.1</version> <!-- 使用最新版本 -->
      <configuration>
        <failOnViolation>false</failOnViolation>
        <logViolationsToConsole>true</logViolationsToConsole> <!-- 可选：将违规记录到控制台 -->
      </configuration>
      <executions>
        <execution>
          <id>checkstyle</id>
          <phase>validate</phase> <!-- 或您偏好的阶段 -->
          <goals>
            <goal>check</goal>
          </goals>
        </execution>
      </executions>
    </plugin>
  </plugins>
</build>
```

### 说明
- **`<failOnViolation>false</failOnViolation>`**：此设置可在检测到 Checkstyle 违规时防止构建失败，从而允许扫描在所有模块中继续。
- **`<logViolationsToConsole>true</logViolationsToConsole>`**：（可选）确保即使构建未失败，违规信息也会打印到控制台以便查看。
- **执行阶段**：`<phase>validate</phase>` 将 Checkstyle 检查绑定到 Maven 生命周期的 `validate` 阶段。如果您希望它在不同阶段（例如 `compile`、`verify`）运行，请调整此阶段。

### 运行命令
再次运行命令：
```bash
mvn checkstyle:check
```
将 `failOnViolation` 设置为 `false` 后，Maven 将扫描所有模块，报告所有违规，并在不提前停止的情况下完成构建。

### 注意事项
- 确保您使用的是最新版本的 `maven-checkstyle-plugin`（例如所示的 3.3.1）。如果需要，请在 Maven Central 上查看最新版本。
- 如果您在多模块项目中工作，此配置将应用于所有模块，除非在子 `pom.xml` 中被覆盖。
- 要生成违规报告，请考虑改为运行 `mvn checkstyle:checkstyle`，该命令默认情况下会生成 HTML 报告而不会使构建失败。

如果您有特定要求（例如自定义 Checkstyle 规则或不同的设置），请告诉我，我可以进一步调整解决方案！
