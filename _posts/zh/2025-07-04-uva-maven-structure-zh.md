---
audio: false
generated: true
lang: zh
layout: post
title: UVA题目的Maven项目结构
translated: true
type: note
---

感谢您分享 `uva/106` 子目录的具体结构。看来您的项目采用了更细粒度的结构，每个 UVA 题目（如 `106`）都是独立的目录，包含自己的 `src` 文件夹（内含 `Main.java` 文件）和可能的输入文件（如 `1.in`）。这表明每个题目可能被视为独立的子项目或模块。要在 Maven 多模块配置中适应这种结构，我们可以：

1. 将每个题目目录（如 `uva/106`）作为独立的 Maven 子模块。
2. 将 `uva` 作为单个模块，并在其 `src/main/java` 目录内组织题目文件。

考虑到 UVA 题目数量（根据您之前列出的列表：`100`、`10000` 等），为每个题目创建独立的 Maven 模块会导致模块数量过多，可能变得繁琐。因此，我建议采用将 `uva` 作为单个模块的结构，每个题目的 `Main.java` 在 `uva/src/main/java` 下按包结构组织（例如题目 106 的包名为 `com.algorithm.solutions.uva.p106`）。这样可以在保持 Maven 优势的同时，确保项目的可管理性。

不过，如果您偏好更细粒度的方式，我也会提供将每个题目作为独立子模块的替代方案。下面，我将根据您的结构更新 `pom.xml` 文件，并提供重组文件的步骤。

---

### 选项 1：单个 `uva` 模块，按题目分包

#### 更新后的目录结构

```
algorithm-solutions/
├── pom.xml
├── nowcoder/
│   ├── pom.xml
│   └── src/
│       └── main/
│           └── java/
│               └── com/algorithm/solutions/nowcoder/
│                   ├── Main.java
│                   ├── nc140.java
│                   ├── nc45.java
│                   ├── nc78.java
│                   └── nc93.java
├── uva/
│   ├── pom.xml
│   ├── src/
│   │   └── main/
│   │       └── java/
│   │           └── com/algorithm/solutions/uva/
│   │               ├── p100/
│   │               │   └── Main.java
│   │               ├── p106/
│   │               │   └── Main.java
│   │               ├── p10000/
│   │               │   └── Main.java
│   │               └── (其他题目)
│   └── resources/
│       └── uva/
│           ├── p100/
│           │   └── 1.in
│           ├── p106/
│           │   └── 1.in
│           └── (其他题目)
└── README.md
```

#### 父级 `pom.xml`（根目录：`algorithm-solutions/pom.xml`）

此文件基本保持不变，将 `nowcoder` 和 `uva` 定义为模块。

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.algorithm.solutions</groupId>
    <artifactId>algorithm-solutions</artifactId>
    <version>1.0-SNAPSHOT</version>
    <packaging>pom</packaging>

    <name>Algorithm Solutions Parent</name>
    <description>Parent project for algorithm solutions</description>

    <modules>
        <module>nowcoder</module>
        <module>uva</module>
    </modules>

    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.13.0</version>
                <configuration>
                    <source>${maven.compiler.source}</source>
                    <target>${maven.compiler.target}</target>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

#### Nowcoder 子模块 `pom.xml`（`nowcoder/pom.xml`）

此文件与之前的回复相同，假设 `nowcoder` 文件已移至 `src/main/java/com/algorithm/solutions/nowcoder/`。

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>com.algorithm.solutions</groupId>
        <artifactId>algorithm-solutions</artifactId>
        <version>1.0-SNAPSHOT</version>
    </parent>

    <artifactId>nowcoder</artifactId>
    <name>Nowcoder Solutions</name>
    <description>Solutions for Nowcoder algorithm problems</description>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-jar-plugin</artifactId>
                <version>3.4.2</version>
                <configuration>
                    <archive>
                        <manifest>
                            <mainClass>com.algorithm.solutions.nowcoder.Main</mainClass>
                        </manifest>
                    </archive>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

#### UVA 子模块 `pom.xml`（`uva/pom.xml`）

此模块包含一个 `resources` 目录用于输入文件（如 `1.in`）。每个题目的 `Main.java` 文件按包组织。

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>com.algorithm.solutions</groupId>
        <artifactId>algorithm-solutions</artifactId>
        <version>1.0-SNAPSHOT</version>
    </parent>

    <artifactId>uva</artifactId>
    <name>UVA Solutions</name>
    <description>Solutions for UVA algorithm problems</description>

    <build>
        <resources>
            <resource>
                <directory>src/main/resources</directory>
                <includes>
                    <include>**/*.in</include>
                </includes>
            </resource>
        </resources>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-jar-plugin</artifactId>
                <version>3.4.2</version>
            </plugin>
        </plugins>
    </build>
</project>
```

#### 文件组织

- **移动 Java 文件**：
  - 对于每个题目（如 `uva/106/src/Main.java`），将 `Main.java` 移至 `uva/src/main/java/com/algorithm/solutions/uva/p106/Main.java`。
  - 更新 `Main.java` 文件以包含包声明：

    ```java
    package com.algorithm.solutions.uva.p106;
    public class Main {
        // ... 现有代码 ...
    }
    ```

  - 对所有题目（如 `p100`、`p10000` 等）执行此操作。

- **移动输入文件**：
  - 将输入文件（如 `uva/106/1.in`）移至 `uva/src/main/resources/uva/p106/1.in`。
  - 这允许 Maven 将这些文件包含在 JAR 中，可通过 `ClassLoader.getResource()` 或类似方法在 Java 代码中访问。

#### 运行程序

要运行特定的 UVA 题目（例如题目 106）：

```bash
mvn -pl uva exec:java -Dexec.mainClass="com.algorithm.solutions.uva.p106.Main"
```

---

### 选项 2：每个 UVA 题目作为独立子模块

如果您希望每个 UVA 题目（如 `106`、`100`）都是独立的 Maven 模块，以下是设置方法。这种方式更细粒度，但会增加 `pom.xml` 文件的数量。

#### 更新后的目录结构

```
algorithm-solutions/
├── pom.xml
├── nowcoder/
│   ├── pom.xml
│   └── src/
│       └── main/
│           └── java/
│               └── com/algorithm/solutions/nowcoder/
│                   ├── Main.java
│                   ├── nc140.java
│                   ├── nc45.java
│                   ├── nc78.java
│                   └── nc93.java
├── uva/
│   ├── 106/
│   │   ├── pom.xml
│   │   ├── src/
│   │   │   └── main/
│   │   │       └── java/
│   │   │           └── com/algorithm/solutions/uva/p106/
│   │   │               └── Main.java
│   │   └── resources/
│   │       └── 1.in
│   ├── 100/
│   │   ├── pom.xml
│   │   ├── src/
│   │   │   └── main/
│   │   │       └── java/
│   │   │           └── com/algorithm/solutions/uva/p100/
│   │   │               └── Main.java
│   │   └── resources/
│   │       └── (输入文件，如有)
│   └── (其他题目目录)
└── README.md
```

#### 父级 `pom.xml`（根目录：`algorithm-solutions/pom.xml`）

将每个题目添加为模块。

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.algorithm.solutions</groupId>
    <artifactId>algorithm-solutions</artifactId>
    <version>1.0-SNAPSHOT</version>
    <packaging>pom</packaging>

    <name>Algorithm Solutions Parent</name>
    <description>Parent project for algorithm solutions</description>

    <modules>
        <module>nowcoder</module>
        <module>uva/106</module>
        <module>uva/100</module>
        <module>uva/10000</module>
        <module>uva/10006</module>
        <module>uva/10008</module>
        <module>uva/10009</module>
        <module>uva/10012</module>
        <module>uva/10013</module>
        <module>uva/10018</module>
        <module>uva/10019</module>
        <module>uva/10026</module>
        <module>uva/10033</module>
        <module>uva/10034</module>
    </modules>

    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.13.0</version>
                <configuration>
                    <source>${maven.compiler.source}</source>
                    <target>${maven.compiler.target}</target>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

#### Nowcoder 子模块 `pom.xml`（`nowcoder/pom.xml`）

同上（未更改）。

#### UVA 题目 106 子模块 `pom.xml`（`uva/106/pom.xml`）

每个题目都有自己的 `pom.xml`。以下是 `uva/106` 的示例：

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>com.algorithm.solutions</groupId>
        <artifactId>algorithm-solutions</artifactId>
        <version>1.0-SNAPSHOT</version>
    </parent>

    <artifactId>uva-106</artifactId>
    <name>UVA Problem 106</name>
    <description>Solution for UVA problem 106</description>

    <build>
        <resources>
            <resource>
                <directory>resources</directory>
                <includes>
                    <include>**/*.in</include>
                </includes>
            </resource>
        </resources>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-jar-plugin</artifactId>
                <version>3.4.2</version>
                <configuration>
                    <archive>
                        <manifest>
                            <mainClass>com.algorithm.solutions.uva.p106.Main</mainClass>
                        </manifest>
                    </archive>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

- **为其他题目重复此操作**：为 `uva/100`、`uva/10000` 等创建类似的 `pom.xml` 文件，调整 `artifactId`（如 `uva-100`）、`name` 和 `mainClass`（如 `com.algorithm.solutions.uva.p100.Main`）。

#### 文件组织

- **移动 Java 文件**：
  - 对于 `uva/106/src/Main.java`，移至 `uva/106/src/main/java/com/algorithm/solutions/uva/p106/Main.java`。
  - 添加包声明：

    ```java
    package com.algorithm.solutions.uva.p106;
    public class Main {
        // ... 现有代码 ...
    }
    ```

- **移动输入文件**：
  - 将 `uva/106/1.in` 移至 `uva/106/resources/1.in`。

#### 运行程序

要运行题目 106：

```bash
mvn -pl uva/106 exec:java -Dexec.mainClass="com.algorithm.solutions.uva.p106.Main"
```

---

### 推荐

- **选项 1（单个 `uva` 模块）** 更简单且更具可扩展性，特别是当您有大量 UVA 题目时。它避免了创建大量 `pom.xml` 文件，并保持了项目结构的整洁。使用包来逻辑组织题目。
- **选项 2（每题独立模块）** 如果您希望每个题目完全独立（例如用于独立部署或测试）则更合适。但由于模块数量多，需要更多维护工作。

### 实施选项 1 的步骤

1. **创建目录结构**：
   - 在 `algorithm-solutions` 根目录下运行以下命令：

     ```bash
     mkdir -p uva/src/main/java/com/algorithm/solutions/uva
     mkdir -p uva/src/main/resources/uva
     mkdir -p nowcoder/src/main/java/com/algorithm/solutions/nowcoder
     ```

2. **移动文件**：
   - 对于每个 UVA 题目（例如 `106`）：

     ```bash
     mkdir -p uva/src/main/java/com/algorithm/solutions/uva/p106
     mv uva/106/src/Main.java uva/src/main/java/com/algorithm/solutions/uva/p106/Main.java
     mkdir -p uva/src/main/resources/uva/p106
     mv uva/106/1.in uva/src/main/resources/uva/p106/1.in
     ```

   - 对于 `nowcoder`：

     ```bash
     mv nowcoder/*.java nowcoder/src/main/java/com/algorithm/solutions/nowcoder/
     ```

3. **更新 Java 文件**：
   - 添加适当的包声明（例如，对于 `uva/106/Main.java`，添加 `package com.algorithm.solutions.uva.p106;`）。
4. **添加 `pom.xml` 文件**：
   - 将父级 `pom.xml` 放在 `algorithm-solutions/` 目录下。
   - 按所示内容放置 `nowcoder/pom.xml` 和 `uva/pom.xml`。
5. **构建**：

   ```bash
   mvn clean install
   ```

### 注意事项

- **输入文件**：如果您的 `Main.java` 读取输入文件（如 `1.in`），请更新代码以通过 `getClass().getResource("/uva/p106/1.in")` 或类似方式访问它们，因为它们现在位于 `src/main/resources` 中。
- **忽略 `.iml` 文件**：在 `.gitignore` 文件中添加 `*.iml`，以从版本控制中排除 IntelliJ 项目文件。
- **其他目录**：对于 `codeforces`、`hacker_rank` 等，您可以在准备就绪时创建类似的模块。如果您需要这些模块的 `pom.xml` 文件，请告知我。
- **Java 版本**：如果您使用不同的 Java 版本，请调整 `<maven.compiler.source>` 和 `<maven.compiler.target>`。

如果您偏好选项 2 或需要特定问题的帮助（例如调整 `Main.java` 以进行资源加载），请告知我！
