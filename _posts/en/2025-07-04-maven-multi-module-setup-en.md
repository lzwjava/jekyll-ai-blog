---
audio: false
generated: true
lang: en
layout: post
title: Convert Repository to Maven Multi-Module
translated: false
type: note
---

To convert your `algorithm-solutions` repository into a multi-module Java project managed by Maven, you'll need a parent `pom.xml` in the root directory and individual `pom.xml` files for each submodule (`nowcoder` and `uva`). The parent `pom.xml` will define common configurations and manage the submodules, while each submodule's `pom.xml` will handle its specific settings.

Below, I'll provide the `pom.xml` files for the parent project and the two submodules. I'll assume:
- The project uses Java 17 (a common version for modern projects; adjust if needed).
- The `nowcoder` and `uva` directories contain Java source files in a standard Maven structure (`src/main/java`).
- No external dependencies are required for now, but the structure allows for easy addition.
- Each submodule will be packaged as a JAR (since these are likely standalone algorithm solutions).

### Directory Structure
After setting up, your directory structure should look like this:

```
algorithm-solutions/
├── pom.xml
├── nowcoder/
│   ├── pom.xml
│   └── src/
│       └── main/
│           └── java/
│               └── (your Java files, e.g., Main.java, nc140, etc.)
├── uva/
│   ├── pom.xml
│   └── src/
│       └── main/
│           └── java/
│               └── (your Java files, e.g., 100.java, 10000.java, etc.)
└── README.md
```

### Parent `pom.xml`
This file goes in the root directory (`algorithm-solutions/pom.xml`). It defines the parent project, lists the submodules, and sets common configurations like Java version and compiler settings.

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

### Nowcoder Submodule `pom.xml`
This file goes in the `nowcoder` directory (`nowcoder/pom.xml`). It inherits from the parent and specifies its own artifact details.

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

### UVA Submodule `pom.xml`
This file goes in the `uva` directory (`uva/pom.xml`). It also inherits from the parent and specifies its own artifact details. Since UVA solutions typically don't have a single `Main` class (each problem might be a standalone program), I won't specify a main class here, but you can add one if needed.

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

### Steps to Set Up
1. **Create Maven Directory Structure**:
   - Move your Java files in `nowcoder` to `nowcoder/src/main/java/`.
   - Move your Java files in `uva` to `uva/src/main/java/`.
   - For example, `nowcoder/Main.java` should be in `nowcoder/src/main/java/Main.java`.

2. **Place the `pom.xml` Files**:
   - Put the parent `pom.xml` in the `algorithm-solutions` root directory.
   - Put the `nowcoder/pom.xml` in the `nowcoder` directory.
   - Put the `uva/pom.xml` in the `uva` directory.

3. **Build the Project**:
   - Navigate to the `algorithm-solutions` root directory in a terminal.
   - Run `mvn clean install` to build both submodules.

4. **Run a Specific Program**:
   - For `nowcoder`, if `Main.java` is the entry point, you can run it with:
     ```bash
     mvn -pl nowcoder exec:java -Dexec.mainClass="Main"
     ```
   - For UVA solutions, since each file might be a standalone program, you can run a specific class (e.g., `100.java`) with:
     ```bash
     mvn -pl uva exec:java -Dexec.mainClass="100"
     ```

### Notes
- **Java Version**: I used Java 17. If you need a different version, update the `<maven.compiler.source>` and `<maven.compiler.target>` properties in the parent `pom.xml`.
- **Dependencies**: If your solutions require libraries (e.g., for input/output utilities), add them to the submodule's `pom.xml` under a `<dependencies>` section.
- **File Naming**: Ensure your Java files match the class names (e.g., `100.java` should contain `public class 100`).
- **Other Directories**: Your repo includes `codeforces`, `hacker_rank`, etc. If you want to include these as submodules, add `<module>codeforces</module>` (etc.) to the parent `pom.xml` and create corresponding `pom.xml` files in those directories, similar to `nowcoder` and `uva`.

Let me know if you need additional submodules or specific configurations!
