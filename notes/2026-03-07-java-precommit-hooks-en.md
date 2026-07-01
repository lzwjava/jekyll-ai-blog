---
audio: false
generated: true
image: false
lang: en
layout: post
title: Java Pre-Commit Hooks Guide
translated: false
type: note
---

**Question:** How do you use pre-commit hooks for Java projects — using Spotless or Checkstyle — and does Java support such pre-commit tooling?

---

**Answer:**

## Yes, Java Fully Supports Pre-Commit Hooks

Java projects do support pre-commit hooks, but the approach is different from Python/Node projects. Since Java uses **Maven or Gradle** as build tools, pre-commit hooks typically invoke Maven/Gradle goals rather than running standalone binaries. There are two main strategies:

- **Strategy A** — Use the `pre-commit` Python framework with shell-script hooks that call Maven/Gradle
- **Strategy B** — Use Maven plugins to install git hooks directly (no `pre-commit` framework needed)

---

## Tool Comparison: Spotless vs Checkstyle

| | Spotless | Checkstyle |
| --- | --- | --- |
| **Purpose** | **Formatter** — auto-fixes code style | **Linter** — checks rules, reports violations |
| **Auto-fix** | Yes (`spotless:apply`) | No (check only) |
| **Scope** | Java, XML, YAML, JSON, SQL, etc. | Java only |
| **Style options** | Google Java Format, Eclipse formatter | Google, Sun, custom XML rules |
| **Best for** | Enforcing consistent formatting | Enforcing naming, complexity, Javadoc rules |

Both are complementary — Spotless handles formatting while Checkstyle enforces coding guidelines like naming conventions, brace styles, and Javadoc requirements. Using both together gives you full automated style enforcement.

---

## Approach 1: Using `.pre-commit-config.yaml` (Recommended for Cross-Language Teams)

You can use the standard `pre-commit` framework with custom shell hooks that invoke Maven goals for both Spotless and Checkstyle:

### Step 1 — Create hook shell scripts

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

Make them executable:

```bash
chmod +x hooks/spotless-hook.sh hooks/checkstyle-hook.sh
```

### Step 2 — `.pre-commit-config.yaml`

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

### Step 3 — Install and run

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files        # test manually
```

---

## Approach 2: Checkstyle via Docker Hook (No Maven wrapper needed)

There is a Docker-based pre-commit hook for Checkstyle that downloads the Checkstyle JAR automatically:

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

> Add `.pre-commit/` to your `.gitignore` since the hook caches the Checkstyle JAR in a `.pre-commit` folder in your working directory.

---

## Approach 3: Pure Maven (No `pre-commit` framework)

Using the `git-build-hook-maven-plugin`, you can configure the hook entirely inside `pom.xml` — no external tooling needed:

### `pom.xml` configuration

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

When any developer runs `mvn install`, the git-build-hook plugin automatically installs the pre-commit hook into their `.git/hooks` directory — no manual step required.

---

## Checkstyle `checkstyle.xml` Example

A minimal `checkstyle.xml` enforcing common Java conventions:

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

## Enforce on GitHub (Server-Side)

Since hooks are local, add a GitHub Actions workflow as the safety net:

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

## Summary: Which Approach to Use?

| Scenario | Recommended Approach |
| --- | --- |
| Maven-only team | Approach 3 (git-build-hook in pom.xml) |
| Mixed language repo (Java + Python/JS) | Approach 1 (`.pre-commit-config.yaml`) |
| Want Checkstyle without Maven wrapper | Approach 2 (Docker-based hook) |
| Always enforce on GitHub | Add GitHub Actions workflow regardless |

---

**References:**

- [Spring Boot with Spotless and Git Pre-commit Hooks (DEV.to)](https://dev.to/gridou/spring-boot-with-spotless-and-git-pre-commit-hooks-1h4f)
- [pre-commit-hooks-for-java (GitHub)](https://github.com/PramodKumarYadav/pre-commit-hooks-for-java)
- [pre-commit-checkstyle Docker hook (GitHub)](https://github.com/HotSprings-GmbH/pre-commit-checkstyle)
- [Enforcing Code Quality with Checkstyle and Git Pre-Commit Hooks (Medium)](https://medium.com/@sahuamit076/enforcing-code-quality-with-checkstyle-and-git-pre-commit-hooks-17e5f548c9d2)
- [Apply Spotless formatting with Git pre-commit hook (Medium)](https://medium.com/@mmessell/apply-spotless-formatting-with-git-pre-commit-hook-1c484ea68c34)
