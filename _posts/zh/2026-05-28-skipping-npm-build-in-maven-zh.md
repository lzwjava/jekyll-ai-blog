---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在Maven中跳过npm构建
translated: true
type: note
---

**问题：** 在 Java + Angular 全栈应用的 Maven exec 插件配置中，能否使用 `exec.skip` 跳过 npm 构建？

**回答：**

可以——但具体属性名称取决于运行 npm 构建的是哪个 Maven 插件。

## 常见配置

### 1. `frontend-maven-plugin`（Angular 项目中最常用）

这是 `com.github.eirslett:frontend-maven-plugin`。它不使用 `exec.skip`，而是有自己的跳过属性：

```xml
<plugin>
  <groupId>com.github.eirslett</groupId>
  <artifactId>frontend-maven-plugin</artifactId>
  <configuration>
    <skip>${skipFrontend}</skip>
  </configuration>
</plugin>
```

然后在构建时跳过：

```bash
mvn install -DskipFrontend=true
```

或在 profile 中硬编码：

```xml
<profiles>
  <profile>
    <id>skip-ui</id>
    <properties>
      <skipFrontend>true</skipFrontend>
    </properties>
  </profile>
</profiles>
```

```bash
mvn install -P skip-ui
```

### 2. `maven-exec-plugin`（通过 `exec:exec` 或 `exec:java` 调用 npm 时）

此时 `exec.skip` **确实有效**：

```bash
mvn install -Dexec.skip=true
```

这会跳过所有 `exec-maven-plugin` 的执行。检查你的 `pom.xml` ——如果看到：

```xml
<groupId>org.codehaus.mojo</groupId>
<artifactId>exec-maven-plugin</artifactId>
```

……那么 `-Dexec.skip=true` 就是正确的标志。

### 3. 通过 `<skip>` + 自定义属性实现按执行粒度跳过

如果你希望更精细地控制（只跳过 npm 而不跳过其他 exec 目标）：

```xml
<execution>
  <id>npm-build</id>
  <goals><goal>exec</goal></goals>
  <configuration>
    <executable>npm</executable>
    <arguments><argument>run build</argument></arguments>
    <skip>${skipNpmBuild}</skip>
  </configuration>
</execution>
```

```bash
mvn install -DskipNpmBuild=true
```

## 快速诊断

```bash
grep -r "exec-maven-plugin\|frontend-maven-plugin" pom.xml */pom.xml
```

这能告诉你应该针对哪个插件。然后：

| 插件 | 跳过标志 |
|---|---|
| `frontend-maven-plugin` | `-DskipFrontend=true`（或与 `<skip>${...}</skip>` 绑定的任何属性） |
| `exec-maven-plugin` | `-Dexec.skip=true` |
| 自定义属性 | `-DskipNpmBuild=true` |

`exec.skip` 标志是真实存在且有效的，但仅当 npm 步骤通过 `exec-maven-plugin` 实现时——而不是 `frontend-maven-plugin`。