---
audio: false
generated: true
lang: zh
layout: post
title: 使用Maven Exec运行Java类
translated: true
type: note
---

Maven Exec 插件的 `exec:java` 目标是一种直接从 Maven 构建运行具有 `main` 方法的 Java 类的强大方式。它在**与 Maven 构建相同的 JVM 内**执行指定的 Java 类，并使用项目的依赖项作为类路径。

以下是使用方法，包含常见场景和示例：

## 1. 从命令行基本使用

使用 `exec:java` 最简单的方式是直接从命令行，特别适用于快速测试或运行特定的工具类。

**命令：**

```bash
mvn exec:java -Dexec.mainClass="com.yourcompany.YourMainClass"
```

**解释：**

* `mvn exec:java`：调用 `exec-maven-plugin` 的 `java` 目标。
* `-Dexec.mainClass="com.yourcompany.YourMainClass"`：此系统属性指定包含要执行的 `public static void main(String[] args)` 方法的 Java 类的完全限定名。

**示例：**

假设您有一个包含 `main` 方法的类 `com.example.myapp.HelloWorld`：

```java
package com.example.myapp;

public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello from Maven exec:java!");
    }
}
```

您将使用以下命令运行它：

```bash
mvn compile exec:java -Dexec.mainClass="com.example.myapp.HelloWorld"
```

**注意：** 最好先运行 `mvn compile`，以确保在 `exec:java` 尝试运行您的类之前它们已被编译。

## 2. 向 Java 程序传递参数

您可以使用 `exec.args` 系统属性向 Java 程序的 `main` 方法传递参数：

**命令：**

```bash
mvn exec:java -Dexec.mainClass="com.yourcompany.YourMainClass" -Dexec.args="arg1 arg2 \"arg with spaces\""
```

**示例：**

如果您的 `HelloWorld` 类是：

```java
package com.example.myapp;

public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello from Maven exec:java!");
        if (args.length > 0) {
            System.out.println("Arguments received: ");
            for (String arg : args) {
                System.out.println("- " + arg);
            }
        }
    }
}
```

您将这样运行它：

```bash
mvn compile exec:java -Dexec.mainClass="com.example.myapp.HelloWorld" -Dexec.args="FirstArgument SecondArgument"
```

对于包含空格的参数，请用引号括起来：

```bash
mvn compile exec:java -Dexec.mainClass="com.example.myapp.HelloWorld" -Dexec.args="\"Hello World\" AnotherArg"
```

## 3. 在 `pom.xml` 中配置 `exec:java`

对于更持久或默认的配置，您可以将 `exec-maven-plugin` 添加到您的 `pom.xml` 中。这允许您定义默认的 `mainClass` 和其他参数，因此您不必每次都在命令行中指定它们。

**`pom.xml` 配置：**

```xml
<project>
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.yourcompany</groupId>
    <artifactId>my-maven-app</artifactId>
    <version>1.0-SNAPSHOT</modelVersion>

    <build>
        <plugins>
            <plugin>
                <groupId>org.codehaus.mojo</groupId>
                <artifactId>exec-maven-plugin</artifactId>
                <version>3.2.0</version> <executions>
                    <execution>
                        <goals>
                            <goal>java</goal>
                        </goals>
                    </execution>
                </executions>
                <configuration>
                    <mainClass>com.example.myapp.HelloWorld</mainClass>
                    <arguments>
                        <argument>defaultArg1</argument>
                        <argument>defaultArg2</argument>
                    </arguments>
                    <systemProperties>
                        <systemProperty>
                            <key>my.custom.property</key>
                            <value>someValue</value>
                        </systemProperty>
                    </systemProperties>
                </configuration>
            </plugin>
        </plugins>
    </build>

    <properties>
        <maven.compiler.source>11</maven.compiler.source>
        <maven.compiler.target>11</maven.compiler.target>
    </properties>

</project>
```

**配置选项解释：**

* `<groupId>org.codehaus.mojo</groupId>` 和 `<artifactId>exec-maven-plugin</artifactId>`：插件的标准坐标。
* `<version>3.2.0</version>`：始终指定插件的最新版本。
* `<goals><goal>java</goal></goals>`：这将绑定 `java` 目标。如果您不将其绑定到特定阶段，则当您显式调用 `mvn exec:java` 时它将被执行。
* `<mainClass>com.example.myapp.HelloWorld</mainClass>`：设置要执行的默认主类。如果您在命令行上运行 `mvn exec:java` 而没有使用 `-Dexec.mainClass`，则将使用此类。
* `<arguments>`：传递给 `main` 方法的参数列表。这些是默认参数，可以通过命令行上的 `exec.args` 覆盖。
* `<systemProperties>`：允许您定义系统属性（`-Dkey=value`），这些属性在 `exec:java` 运行时将可用于您的 Java 应用程序。

**使用 `pom.xml` 配置运行：**

一旦在 `pom.xml` 中配置：

* 要使用默认主类和参数运行：

    ```bash
    mvn compile exec:java
    ```

* 要从命令行覆盖主类：

    ```bash
    mvn compile exec:java -Dexec.mainClass="com.example.myapp.AnotherMainClass"
    ```

* 要从命令行覆盖/添加参数：

    ```bash
    mvn compile exec:java -Dexec.args="commandLineArg1 commandLineArg2"
    ```

    （注意：如果在命令行上提供了 `exec.args`，它通常会*替换*在 `pom.xml` 中定义的 `arguments`。）

## 4. 与 `exec:exec` 的主要区别

理解 `exec:java` 和 `exec:exec` 之间的区别很重要：

* **`exec:java`**：在与 Maven **相同的 JVM** 中运行 Java 程序。这通常更快，因为它避免了生成新进程。它会自动将项目的依赖项设置到类路径上。
* **`exec:exec`**：在**单独的进程**中运行任意外部程序（包括 `java` 本身）。当您需要指定不同的 Java 可执行文件、传递 JVM 参数（如 `-Xmx`）或运行非 Java 可执行文件时，这很有用。如果您使用 `exec:exec` 运行 Java 程序，通常必须使用参数中的 `%classpath` 手动构造类路径。

对于在 Maven 构建中执行大多数标准 Java 应用程序，`exec:java` 是更方便的选择。

## 5. 重要注意事项

* **类路径：** `exec:java` 自动将您项目的已编译类及其依赖项包含在类路径中。
* **JVM 参数：** 因为 `exec:java` 在与 Maven *相同* 的 JVM 中运行，所以您不能通过其配置或 `exec.args` 直接将 JVM 参数（如 `-Xmx`、`-XX:MaxPermSize`）传递给 `exec:java`。这些参数需要传递给 Maven JVM 本身，通常通过 `MAVEN_OPTS` 环境变量：

    ```bash
    export MAVEN_OPTS="-Xmx1024m -Dsome.jvm.property=value"
    mvn exec:java ...
    ```

* **System.exit()**：如果您的 Java 程序调用 `System.exit()`，它将终止整个 Maven 构建过程，而不仅仅是您的程序。在使用 `exec:java` 时请注意这一点。该插件有一个选项 `blockSystemExit`（自 3.2.0 版起）试图防止这种情况，但最好设计您的 main 方法在不调用 `System.exit()` 的情况下正常完成。
* **依赖项：** `exec:java` 依赖于项目的依赖项。如果您需要运行不属于项目构建的依赖项中的类，您可能需要调整插件的配置或考虑使用具有显式类路径定义的 `exec:exec`。
* **插件版本：** 始终使用最新版本的 `exec-maven-plugin` 以获取最新功能和错误修复。请查看 MojoHaus 网站以获取最新信息。
