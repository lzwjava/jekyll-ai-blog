---
audio: false
generated: true
lang: en
layout: post
title: Consolidate Algorithm Solutions in Maven
translated: false
type: note
---

To consolidate all your algorithm solutions (`nowcoder`, `uva`, etc.) into a single Maven module managed by one `pom.xml` file in the `algorithm-solutions` root directory, we’ll treat the entire project as one module. The Java files from `nowcoder` and `uva` (and other directories like `codeforces`, `hacker_rank`, etc.) will be organized under `src/main/java` with appropriate package structures (e.g., `com.algorithm.solutions.nowcoder`, `com.algorithm.solutions.uva`). Input files (e.g., `1.in`) will go into `src/main/resources`.

### Assumptions

- All Java files (e.g., `nowcoder/Main.java`, `uva/106/src/Main.java`) will be moved to `src/main/java/com/algorithm/solutions/<platform>` (e.g., `nowcoder`, `uva/p106`).
- Input files (e.g., `uva/106/1.in`) will be moved to `src/main/resources/<platform>` (e.g., `uva/p106`).
- The project uses Java 17 (adjustable in the `pom.xml`).
- The `pom.xml` will be in the `algorithm-solutions` root directory, and no submodules will be used.

### Directory Structure

After reorganization (assuming you run the Python script from the previous response for `uva` and a similar one for `nowcoder`), the structure will be:

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
│   │   │       │   └── (etc.)
│   │   │       ├── codeforces/
│   │   │       └── hacker_rank/
│   │   └── resources/
│   │       ├── nowcoder/
│   │       │   └── (input files, if any)
│   │       ├── uva/
│   │       │   ├── p106/
│   │       │   │   └── 1.in
│   │       │   ├── p100/
│   │       │   └── (etc.)
│   │       ├── codeforces/
│   │       └── hacker_rank/
└── README.md
```

### Parent `pom.xml`

This `pom.xml` goes in the `algorithm-solutions` root directory. It configures the project as a single module, includes resources for input files, and sets up the Maven compiler for Java 17.

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
    <description>Consolidated project for algorithm solutions from multiple platforms</description>

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

### Notes on the `pom.xml`

- **Packaging**: Set to `jar` since this is a single executable module.
- **Resources**: Includes `*.in` files from `src/main/resources` for input files.
- **Main Class**: Set to `com.algorithm.solutions.nowcoder.Main` as a default. Since each problem may have its own `Main` class, you’ll typically run specific classes using `mvn exec:java`.
- **Java Version**: Uses Java 17; adjust `<maven.compiler.source>` and `<maven.compiler.target>` if needed.

### Steps to Set Up

1. **Create Directory Structure**:

   ```bash
   mkdir -p src/main/java/com/algorithm/solutions/{nowcoder,uva,codeforces,hacker_rank}
   mkdir -p src/main/resources/{nowcoder,uva,codeforces,hacker_rank}
   ```

2. **Move Files**:
   - For `nowcoder`:

     ```bash
     mkdir -p src/main/java/com/algorithm/solutions/nowcoder
     mv nowcoder/*.java src/main/java/com/algorithm/solutions/nowcoder/
     ```

     Add package declaration to each Java file (e.g., `Main.java`):

     ```java
     package com.algorithm.solutions.nowcoder;
     // ... rest of the code ...
     ```

   - For `uva`, use the Python script from the previous response, or manually:

     ```bash
     mkdir -p src/main/java/com/algorithm/solutions/uva/p106
     mv uva/106/src/Main.java src/main/java/com/algorithm/solutions/uva/p106/Main.java
     mkdir -p src/main/resources/uva/p106
     mv uva/106/1.in src/main/resources/uva/p106/1.in
     ```

     Add package declaration to `Main.java`:

     ```java
     package com.algorithm.solutions.uva.p106;
     // ... rest of the code ...
     ```

     Repeat for other UVA problems (`100`, `10000`, etc.).

3. **Place the `pom.xml`**:
   - Save the above `pom.xml` in the `algorithm-solutions` root directory.

4. **Build the Project**:

   ```bash
   mvn clean install
   ```

5. **Run a Specific Program**:
   - For a `nowcoder` problem:

     ```bash
     mvn exec:java -Dexec.mainClass="com.algorithm.solutions.nowcoder.Main"
     ```

   - For a UVA problem (e.g., problem 106):

     ```bash
     mvn exec:java -Dexec.mainClass="com.algorithm.solutions.uva.p106.Main"
     ```

### Python Script for `nowcoder`

To complement the previous `uva` script, here’s a Python script to move `nowcoder` files to `src/main/java/com/algorithm/solutions/nowcoder/` and add package declarations. Run this from the `algorithm-solutions` root directory.

```python
import os
from pathlib import Path

def add_package_declaration(java_file, package):
    """Add package declaration to the top of a Java file if not already present."""
    with open(java_file, 'r', encoding='utf-8') as f:
        content = f.read()

    if not content.strip().startswith('package '):
        new_content = f'package {package};\n\n{content}'
        with open(java_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Added package declaration to {java_file}')

def reorganize_nowcoder():
    # Define paths
    nowcoder_root = Path('nowcoder')
    target_dir = Path('src/main/java/com/algorithm/solutions/nowcoder')

    # Create target directory
    target_dir.mkdir(parents=True, exist_ok=True)

    if not nowcoder_root.exists():
        print('Error: nowcoder directory not found.')
        return

    # Move Java files
    for java_file in nowcoder_root.glob('*.java'):
        target_file = target_dir / java_file.name
        shutil.move(str(java_file), str(target_file))
        print(f'Moved {java_file} to {target_file}')

        # Add package declaration
        add_package_declaration(target_file, 'com.algorithm.solutions.nowcoder')

    # Remove empty nowcoder directory
    if not any(nowcoder_root.iterdir()):
        nowcoder_root.rmdir()
        print(f'Removed empty directory {nowcoder_root}')

if __name__ == '__main__':
    reorganize_nowcoder()
    print('Nowcoder reorganization complete.')
```

### Notes

- **Running Scripts**: Run the `reorganize_uva.py` (from the previous response) and `reorganize_nowcoder.py` scripts to move files:

  ```bash
  python reorganize_uva.py
  python reorganize_nowcoder.py
  ```

- **Input Files**: If `nowcoder` has input files, modify the script to move `*.in` files to `src/main/resources/nowcoder/`.
- **Other Directories**: For `codeforces`, `hacker_rank`, etc., you can adapt the `nowcoder` script by changing the source directory and package name.
- **Resource Access**: Update your Java code to read input files from `src/main/resources` (e.g., `getClass().getResource("/uva/p106/1.in")`).
- **Ignoring Files**: Add `*.iml` to a `.gitignore` file to exclude IntelliJ project files.

Let me know if you need scripts for other directories or further tweaks to the `pom.xml`!
