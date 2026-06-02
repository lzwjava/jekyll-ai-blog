---
audio: false
generated: true
lang: zh
layout: post
title: 在Checkstyle中禁用Javadoc检查
translated: true
type: note
---

要配置 Checkstyle 忽略所有 Javadoc 相关检查并将其视为非违规行为，你需要修改 Checkstyle 配置文件（通常是 `checkstyle.xml`），以禁用或抑制 Javadoc 相关模块。具体方法如下：

### 选项 1：禁用 Javadoc 相关检查

Checkstyle 包含多个 Javadoc 相关模块，例如 `JavadocMethod`、`JavadocType`、`JavadocVariable`、`JavadocStyle` 和 `JavadocPackage`。要禁用这些模块，请确保在配置文件中将其移除或注释掉。例如：

```xml
<module name="Checker">
    <!-- 其他模块 -->
    <!-- 注释或移除 Javadoc 相关检查 -->
    <!--
    <module name="JavadocMethod"/>
    <module name="JavadocType"/>
    <module name="JavadocVariable"/>
    <module name="JavadocStyle"/>
    <module name="JavadocPackage"/>
    -->
</module>
```

如果这些模块不在你的配置中，Checkstyle 将不会强制执行 Javadoc 检查。

### 选项 2：使用抑制过滤器全局屏蔽 Javadoc 检查

你可以使用 Checkstyle 的 `SuppressionFilter` 来全局抑制所有 Javadoc 相关检查。首先在单独的抑制文件中添加抑制规则（例如 `suppressions.xml`），然后在 Checkstyle 配置中引用该文件。

1. **创建抑制文件**（例如 `suppressions.xml`）：

   ```xml
   <!DOCTYPE suppressions PUBLIC
       "-//Checkstyle//DTD Suppression DTD 1.0//EN"
       "https://checkstyle.org/dtds/suppressions_1_0.dtd">
   <suppressions>
       <!-- 抑制所有 Javadoc 相关检查 -->
       <suppress checks="Javadoc.*" files=".*"/>
   </suppressions>
   ```

   其中 `checks="Javadoc.*"` 模式会匹配所有以 "Javadoc" 开头的检查（如 `JavadocMethod`、`JavadocType` 等），`files=".*"` 表示该抑制规则适用于所有文件。

2. **在 Checkstyle 配置中引用抑制文件**：

   ```xml
   <module name="Checker">
       <module name="SuppressionFilter">
           <property name="file" value="suppressions.xml"/>
       </module>
       <!-- 其他模块 -->
   </module>
   ```

### 选项 3：使用 `@SuppressWarnings` 注解

如果只需要针对特定类或方法抑制 Javadoc 检查，可以在 Java 代码中使用 `@SuppressWarnings("checkstyle:javadoc")` 注解。例如：

```java
@SuppressWarnings("checkstyle:javadoc")
public class MyClass {
    // 没有 Javadoc 的代码不会触发违规
}
```

这种方式适用于针对性抑制，但如需全局禁用 Javadoc 检查，则不适合在代码中添加大量注解。

### 注意事项

- **验证配置**：修改配置后，请运行 Checkstyle 以确保不再报告 Javadoc 相关违规。例如使用命令：

  ```bash
  java -jar checkstyle.jar -c checkstyle.xml YourSourceFiles
  ```

- **常见 Javadoc 模块**：确保处理所有相关模块，包括 `JavadocMethod`、`JavadocType`、`JavadocVariable`、`JavadocStyle`、`JavadocPackage`、`MissingJavadocMethod`、`MissingJavadocType` 和 `InvalidJavadocPosition`。
- **版本兼容性**：具体的模块名称和抑制语法可能因 Checkstyle 版本而异。以上示例兼容 Checkstyle 8.x 及更高版本。
- **全局抑制**：使用 `SuppressionFilter`（选项 2）通常是在不大量修改核心配置的情况下，禁用所有 Javadoc 检查的最简洁方法。

如果你在使用特定的构建工具（如 Maven 或 Gradle），请告知我，我可以提供关于集成更新后的 Checkstyle 配置的更多指导！
