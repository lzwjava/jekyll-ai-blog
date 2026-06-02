---
audio: false
generated: true
lang: zh
layout: post
title: Maven算法解决方案整合
translated: true
type: note
---

为将所有算法题解（`nowcoder`、`uva`等）整合到由`algorithm-solutions`根目录下单个`pom.xml`文件管理的Maven模块中，我们将整个项目视为单一模块。来自`nowcoder`和`uva`（以及其他目录如`codeforces`、`hacker_rank`等）的Java文件将按对应包结构（如`com.algorithm.solutions.nowcoder`、`com.algorithm.solutions.uva`）组织在`src/main/java`目录下。输入文件（如`1.in`）将置于`src/main/resources`中。

### 前置条件

- 所有Java文件（如`nowcoder/Main.java`、`uva/106/src/Main.java`）将移至`src/main/java/com/algorithm/solutions/<平台>`（如`nowcoder`、`uva/p106`）。
- 输入文件（如`uva/106/1.in`）将移至`src/main/resources/<平台>`（如`uva/p106`）。
- 项目使用Java 17（可在`pom.xml`中调整）。
- `pom.xml`将置于`algorithm-solutions`根目录，不使用子模块。

### 目录结构

重组后（假设已运行先前针对`uva`的Python脚本及类似的`nowcoder`脚本），结构如下：

```
algorithm-solutions/
├── pom.xml
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/algorithm/solutions/
│   │   │       ├── nowcoder/
│   │   │       │   ├── Main.java
│   │   │       │   ├── nc140.java
│   │   │       │   ├── nc45.java
│   │   │       │   ├── nc78.java
│   │   │       │   └── nc93.java
│   │   │       ├── uva/
│   │   │       │   ├── p100/
│   │   │       │   │   └── Main.java
│   │   │       │   ├── p106/
│   │   │       │   │   └── Main.java
│   │   │       │   ├── p10000/
│   │   │       │   │   └── Main.java
│   │   │       │   └── (其他目录)
│   │   │       ├── codeforces/
│   │   │       └── hacker_rank/
│   │   └── resources/
│   │       ├── nowcoder/
│   │       │   └── (输入文件，如有)
│   │       ├── uva/
│   │       │   ├── p106/
│   │       │   │   └── 1.in
│   │       │   ├── p100/
│   │       │   └── (其他目录)
│   │       ├── codeforces/
│   │       └── hacker_rank/
└── README.md
```

### 父级 `pom.xml`

该`pom.xml`位于`algorithm-solutions`根目录。它将项目配置为单模块，包含输入文件的资源目录，并设置Maven编译器使用Java 17。

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.algorithm.solutions</groupId>
    <artifactId>algorithm-solutions</artifactId>
    <version>1.0-SNAPSHOT</version>
    <packaging>jar</packaging>

    <name>Algorithm Solutions</name>
    <description>整合多平台算法题解的统一项目</description>

    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

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
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.13.0</version>
                <configuration>
                    <source>${maven.compiler.source}</source>
                    <target>${maven.compiler.target}</target>
                </configuration>
            </plugin>
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

### 关于 `pom.xml` 的说明

- **打包方式**：设置为`jar`，因为这是单模块可执行项目。
- **资源文件**：包含`src/main/resources`中的`*.in`输入文件。
- **主类**：默认设置为`com.algorithm.solutions.nowcoder.Main`。由于每个题目可能有自己的`Main`类，通常需使用`mvn exec:java`运行特定类。
- **Java版本**：使用Java 17；如需调整可修改`<maven.compiler.source>`和`<maven.compiler.target>`。

### 设置步骤

1. **创建目录结构**：

   ```bash
   mkdir -p src/main/java/com/algorithm/solutions/{nowcoder,uva,codeforces,hacker_rank}
   mkdir -p src/main/resources/{nowcoder,uva,codeforces,hacker_rank}
   ```

2. **移动文件**：
   - 对于`nowcoder`：

     ```bash
     mkdir -p src/main/java/com/algorithm/solutions/nowcoder
     mv nowcoder/*.java src/main/java/com/algorithm/solutions/nowcoder/
     ```

     为每个Java文件添加包声明（如`Main.java`）：

     ```java
     package com.algorithm.solutions.nowcoder;
     // ... 其余代码 ...
     ```

   - 对于`uva`，使用先前提供的Python脚本或手动操作：

     ```bash
     mkdir -p src/main/java/com/algorithm/solutions/uva/p106
     mv uva/106/src/Main.java src/main/java/com/algorithm/solutions/uva/p106/Main.java
     mkdir -p src/main/resources/uva/p106
     mv uva/106/1.in src/main/resources/uva/p106/1.in
     ```

     为`Main.java`添加包声明：

     ```java
     package com.algorithm.solutions.uva.p106;
     // ... 其余代码 ...
     ```

     对其他UVA题目（`100`、`10000`等）重复此操作。

3. **放置`pom.xml`**：
   - 将上述`pom.xml`保存至`algorithm-solutions`根目录。

4. **构建项目**：

   ```bash
   mvn clean install
   ```

5. **运行特定程序**：
   - 运行`nowcoder`题目：

     ```bash
     mvn exec:java -Dexec.mainClass="com.algorithm.solutions.nowcoder.Main"
     ```

   - 运行UVA题目（如106题）：

     ```bash
     mvn exec:java -Dexec.mainClass="com.algorithm.solutions.uva.p106.Main"
     ```

### 用于 `nowcoder` 的Python脚本

作为之前`uva`脚本的补充，以下Python脚本可将`nowcoder`文件移至`src/main/java/com/algorithm/solutions/nowcoder/`并添加包声明。请在`algorithm-solutions`根目录运行。

```python
import os
from pathlib import Path

def add_package_declaration(java_file, package):
    """如果不存在包声明，则将其添加到Java文件顶部"""
    with open(java_file, 'r', encoding='utf-8') as f:
        content = f.read()

    if not content.strip().startswith('package '):
        new_content = f'package {package};\n\n{content}'
        with open(java_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'已为 {java_file} 添加包声明')

def reorganize_nowcoder():
    # 定义路径
    nowcoder_root = Path('nowcoder')
    target_dir = Path('src/main/java/com/algorithm/solutions/nowcoder')

    # 创建目标目录
    target_dir.mkdir(parents=True, exist_ok=True)

    if not nowcoder_root.exists():
        print('错误：未找到nowcoder目录')
        return

    # 移动Java文件
    for java_file in nowcoder_root.glob('*.java'):
        target_file = target_dir / java_file.name
        shutil.move(str(java_file), str(target_file))
        print(f'已移动 {java_file} 至 {target_file}')

        # 添加包声明
        add_package_declaration(target_file, 'com.algorithm.solutions.nowcoder')

    # 移除空nowcoder目录
    if not any(nowcoder_root.iterdir()):
        nowcoder_root.rmdir()
        print(f'已移除空目录 {nowcoder_root}')

if __name__ == '__main__':
    reorganize_nowcoder()
    print('Nowcoder重组完成。')
```

### 注意事项

- **运行脚本**：通过以下命令移动文件：

  ```bash
  python reorganize_uva.py
  python reorganize_nowcoder.py
  ```

- **输入文件**：如果`nowcoder`有输入文件，需修改脚本将`*.in`文件移至`src/main/resources/nowcoder/`。
- **其他目录**：对于`codeforces`、`hacker_rank`等目录，可通过修改源目录和包名来适配`nowcoder`脚本。
- **资源访问**：需更新Java代码以从`src/main/resources`读取输入文件（例如`getClass().getResource("/uva/p106/1.in")`）。
- **文件忽略**：在`.gitignore`文件中添加`*.iml`以排除IntelliJ项目文件。

如需其他目录的脚本或对`pom.xml`的进一步调整，请随时告知！
