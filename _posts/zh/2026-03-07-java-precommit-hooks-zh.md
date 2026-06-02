---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Java 预提交钩子指南
translated: true
type: note
---

**问题：** 如何在 Java 项目中使用 pre-commit hooks —— 使用 Spotless 或 Checkstyle —— Java 是否支持此类 pre-commit 工具？

---

**回答：**

## 是的，Java 完全支持 Pre-Commit Hooks

Java 项目支持 pre-commit hooks，但方法与 Python/Node 项目不同。由于 Java 使用 **Maven 或 Gradle** 作为构建工具，pre-commit hooks 通常调用 Maven/Gradle goals，而不是运行独立的二进制文件。主要有两种策略：

- **策略 A** —— 使用 `pre-commit` Python 框架与调用 Maven/Gradle 的 shell-script hooks
- **策略 B** —— 使用 Maven 插件直接安装 git hooks（无需 `pre-commit` 框架）

---

## 工具比较：Spotless 与 Checkstyle

| | Spotless | Checkstyle |
|---|---|---|
| **用途** | **Formatter** — 自动修复代码风格 | **Linter** — 检查规则，报告违规 |
| **自动修复** | 是 (`spotless:apply`) | 否（仅检查） |
| **范围** | Java、XML、YAML、JSON、SQL 等 | 仅 Java |
| **风格选项** | Google Java Format、Eclipse formatter | Google、Sun、自定义 XML 规则 |
| **最适合** | 强制一致的格式化 | 强制命名、复杂度、Javadoc 规则 |

两者互补——Spotless 处理格式化，而 Checkstyle 强制执行编码指南，如命名规范、大括号风格和 Javadoc 要求。将两者结合使用可实现完整的自动化风格强制执行。

---

## 方法 1：使用 `.pre-commit-config.yaml`（推荐用于跨语言团队）

您可以使用标准的 `pre-commit` 框架与自定义 shell hooks，这些 hooks 调用 Maven goals 来处理 Spotless 和 Checkstyle：

### 步骤 1 —— 创建 hook shell 脚本

```bash
# hooks/spotless-hook.sh
#!/bin/bash
echo "Running Spotless format check..."
mvn spotless:check
if [ $? -ne 0 ]; then
  echo "Formatting issues found. Run: mvn spotless:apply"
  exit 1
fi
```

```bash
# hooks/checkstyle-hook.sh
#!/bin/bash
echo "Running Checkstyle..."
mvn checkstyle:check
if [ $? -ne 0 ]; then
  echo "Checkstyle violations found. Commit aborted."
  exit 1
fi
```

使它们可执行：

```bash
chmod +x hooks/spotless-hook.sh hooks/checkstyle-hook.sh
```

### 步骤 2 —— `.pre-commit-config.yaml`

```yaml
repos:
  - repo: local
    hooks:
      - id: spotless-format-check
        name: Spotless Format Check
        entry: hooks/spotless-hook.sh
        language: script
        files: \.java$               # only trigger on .java files

      - id: checkstyle
        name: Checkstyle
        entry: hooks/checkstyle-hook.sh
        language: script
        files: \.java$
```

### 步骤 3 —— 安装并运行

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files        # test manually
```

---

## 方法 2：通过 Docker Hook 使用 Checkstyle（无需 Maven 包装器）

有一个基于 Docker 的 pre-commit hook 用于 Checkstyle，它会自动下载 Checkstyle JAR：

```yaml
repos:
  - repo: https://github.com/HotSprings-GmbH/pre-commit-checkstyle
    rev: ""   # pin a commit hash
    hooks:
      - id: checkstyle
        args:
          - "10.12.5"          # checkstyle version
          - "-c=checkstyle.xml" # your rules file
        stages: [commit]
```

> 将 `.pre-commit/` 添加到您的 `.gitignore`，因为 hook 会将 Checkstyle JAR 缓存在工作目录中的 `.pre-commit` 文件夹。

---

## 方法 3：纯 Maven（无需 `pre-commit` 框架）

使用 `git-build-hook-maven-plugin`，您可以在 `pom.xml` 中完全配置 hook —— 无需外部工具：

### `pom.xml` 配置

```xml
<build>
  <plugins>

    <!-- Spotless: formatter -->
    <plugin>
      <groupId>com.diffplug.spotless</groupId>
      <artifactId>spotless-maven-plugin</artifactId>
      <version>2.40.0</version>
      <configuration>
        <java>
          <includes>
            <include>src/main/java/**/*.java</include>
            <include>src/test/java/**/*.java</include>
          </includes>
          <googleJavaFormat>
            <version>1.16.0</version>
            <style>GOOGLE</style>
          </googleJavaFormat>
          <removeUnusedImports/>
        </java>
      </configuration>
    </plugin>

    <!-- git-build-hook: installs the pre-commit hook automatically -->
    <plugin>
      <groupId>com.rudikershaw.gitbuildhook</groupId>
      <artifactId>git-build-hook-maven-plugin</artifactId>
      <version>3.4.1</version>
      <configuration>
        <preCommit>mvn spotless:apply checkstyle:check</preCommit>
      </configuration>
      <executions>
        <execution>
          <goals><goal>install</goal></goals>
          <phase>initialize</phase>
        </execution>
      </executions>
    </plugin>

  </plugins>
</build>
```

当任何开发者运行 `mvn install` 时，git-build-hook 插件会自动将 pre-commit hook 安装到他们的 `.git/hooks` 目录 —— 无需手动步骤。

---

## Checkstyle `checkstyle.xml` 示例

一个最小化的 `checkstyle.xml`，强制执行常见的 Java 规范：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE module PUBLIC
  "-//Puppy Crawl//DTD Check Configuration 1.3//EN"
  "http://www.puppycrawl.com/dtds/configuration_1_3.dtd">
<module name="Checker">
  <module name="FileTabCharacter"/>
  <module name="TreeWalker">
    <module name="UnusedImports"/>
    <module name="TypeName"/>       <!-- Classes must be PascalCase -->
    <module name="MethodName"/>     <!-- Methods must be camelCase -->
    <module name="PackageName"/>
  </module>
</module>
```

---

## 在 GitHub 上强制执行（服务器端）

由于 hooks 是本地的，请添加 GitHub Actions workflow 作为安全网：

```yaml
# .github/workflows/code-quality.yml
name: Code Quality

on: [pull_request, push]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-java@v3
        with:
          java-version: '17'
          distribution: 'temurin'
      - name: Run Spotless Check
        run: mvn spotless:check
      - name: Run Checkstyle
        run: mvn checkstyle:check
```

---

## 总结：使用哪种方法？

| 场景 | 推荐方法 |
|---|---|
| 仅 Maven 团队 | 方法 3（pom.xml 中的 git-build-hook） |
| 混合语言仓库（Java + Python/JS） | 方法 1（`.pre-commit-config.yaml`） |
| 希望无需 Maven 包装器使用 Checkstyle | 方法 2（基于 Docker 的 hook） |
| 始终在 GitHub 上强制执行 | 无论如何添加 GitHub Actions workflow |

---

**参考资料：**

- [Spring Boot with Spotless and Git Pre-commit Hooks (DEV.to)](https://dev.to/gridou/spring-boot-with-spotless-and-git-pre-commit-hooks-1h4f)
- [pre-commit-hooks-for-java (GitHub)](https://github.com/PramodKumarYadav/pre-commit-hooks-for-java)
- [pre-commit-checkstyle Docker hook (GitHub)](https://github.com/HotSprings-GmbH/pre-commit-checkstyle)
- [Enforcing Code Quality with Checkstyle and Git Pre-Commit Hooks (Medium)](https://medium.com/@sahuamit076/enforcing-code-quality-with-checkstyle-and-git-pre-commit-hooks-17e5f548c9d2)
- [Apply Spotless formatting with Git pre-commit hook (Medium)](https://medium.com/@mmessell/apply-spotless-formatting-with-git-pre-commit-hook-1c484ea68c34)
