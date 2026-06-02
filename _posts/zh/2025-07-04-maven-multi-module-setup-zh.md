---
audio: false
generated: true
lang: zh
layout: post
title: 将仓库转换为Maven多模块项目
translated: true
type: note
---

要将你的 `algorithm-solutions` 代码库转换为由 Maven 管理的多模块 Java 项目，你需要在根目录中放置一个父级 `pom.xml`，并为每个子模块（`nowcoder` 和 `uva`）分别创建独立的 `pom.xml` 文件。父级 `pom.xml` 将定义通用配置并管理子模块，而每个子模块的 `pom.xml` 将处理其特定设置。

下面，我将提供父项目和两个子模块的 `pom.xml` 文件。我假设：
- 项目使用 Java 17（现代项目的常用版本；如有需要可调整）。
- `nowcoder` 和 `uva` 目录包含标准 Maven 结构（`src/main/java`）中的 Java 源文件。
- 目前不需要外部依赖，但该结构允许轻松添加。
- 每个子模块将打包为 JAR（因为这些很可能是独立的算法解决方案）。

### 目录结构
设置完成后，你的目录结构应如下所示：

```
algorithm-solutions/
├── pom.xml
├── nowcoder/
│   ├── pom.xml
│   └── src/
│       └── main/
│           └── java/
│               └── （你的 Java 文件，例如 Main.java、nc140 等）
├── uva/
│   ├── pom.xml
│   └── src/
│       └── main/
│           └── java/
│               └── （你的 Java 文件，例如 100.java、10000.java 等）
└── README.md
```

### 父级 `pom.xml`
该文件位于根目录（`algorithm-solutions/pom.xml`）。它定义了父项目，列出了子模块，并设置了通用配置，如 Java 版本和编译器设置。

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

### Nowcoder 子模块 `pom.xml`
该文件位于 `nowcoder` 目录（`nowcoder/pom.xml`）。它继承自父级，并指定其自身的构件详情。

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
                            <mainClass>Main</mainClass>
                        </manifest>
                    </archive>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

### UVA 子模块 `pom.xml`
该文件位于 `uva` 目录（`uva/pom.xml`）。它也继承自父级，并指定其自身的构件详情。由于 UVA 解决方案通常没有单一的 `Main` 类（每个问题可能是一个独立的程序），我在此不指定主类，但如有需要，你可以添加一个。

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

### 设置步骤
1. **创建 Maven 目录结构**：
   - 将 `nowcoder` 中的 Java 文件移动到 `nowcoder/src/main/java/`。
   - 将 `uva` 中的 Java 文件移动到 `uva/src/main/java/`。
   - 例如，`nowcoder/Main.java` 应位于 `nowcoder/src/main/java/Main.java`。

2. **放置 `pom.xml` 文件**：
   - 将父级 `pom.xml` 放在 `algorithm-solutions` 根目录中。
   - 将 `nowcoder/pom.xml` 放在 `nowcoder` 目录中。
   - 将 `uva/pom.xml` 放在 `uva` 目录中。

3. **构建项目**：
   - 在终端中导航到 `algorithm-solutions` 根目录。
   - 运行 `mvn clean install` 以构建两个子模块。

4. **运行特定程序**：
   - 对于 `nowcoder`，如果 `Main.java` 是入口点，你可以使用以下命令运行：
     ```bash
     mvn -pl nowcoder exec:java -Dexec.mainClass="Main"
     ```
   - 对于 UVA 解决方案，由于每个文件可能是一个独立的程序，你可以使用以下命令运行特定类（例如 `100.java`）：
     ```bash
     mvn -pl uva exec:java -Dexec.mainClass="100"
     ```

### 注意事项
- **Java 版本**：我使用了 Java 17。如果你需要不同的版本，请在父级 `pom.xml` 中更新 `<maven.compiler.source>` 和 `<maven.compiler.target>` 属性。
- **依赖项**：如果你的解决方案需要库（例如用于输入/输出工具），请在子模块的 `pom.xml` 中的 `<dependencies>` 部分添加它们。
- **文件命名**：确保你的 Java 文件与类名匹配（例如，`100.java` 应包含 `public class 100`）。
- **其他目录**：你的代码库包含 `codeforces`、`hacker_rank` 等。如果你想将这些作为子模块包含，请在父级 `pom.xml` 中添加 `<module>codeforces</module>`（等），并在这些目录中创建相应的 `pom.xml` 文件，类似于 `nowcoder` 和 `uva`。

如果你需要额外的子模块或特定配置，请告诉我！
