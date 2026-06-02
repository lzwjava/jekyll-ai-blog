---
audio: false
generated: true
lang: zh
layout: post
title: Maven Java程序中的输入重定向
translated: true
type: note
---

为 `exec:java` 程序重定向输入可能有些棘手，因为 `exec:java` 在与 Maven *相同的 JVM* 中运行 Java 进程。这意味着您不能像对独立进程那样使用标准 shell 重定向操作符（`<`、`>`）。

不过，您仍有几种方法可以向 `exec:java` 程序提供输入：

## 1. 编程式输入（标准 `System.in`）

最直接的方法是设计您的 Java 程序像往常一样从 `System.in` 读取。当您运行 `mvn exec:java` 时，您在控制台中输入的任何内容都将定向到 Java 程序的 `System.in`。

**Java 程序示例（`MyInputProgram.java`）：**

```java
package com.example.app;

import java.util.Scanner;

public class MyInputProgram {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("请输入您的姓名：");
        String name = scanner.nextLine();
        System.out.println("你好，" + name + "！");

        System.out.print("请输入您的年龄：");
        int age = scanner.nextInt();
        System.out.println("您 " + age + " 岁了。");

        scanner.close();
    }
}
```

**从命令行运行：**

```bash
mvn compile exec:java -Dexec.mainClass="com.example.app.MyInputProgram"
```

运行此命令时，Maven 将启动，然后您的程序会提示您输入。您可以直接在控制台中输入。

## 2. 使用 `exec.args` 属性进行输入（适用于简单情况）

如果您的程序期望非常简单、非交互式的输入，您*或许可以*将其作为参数传递，然后您的程序读取该参数而不是 `System.in`。这不是真正的标准输入重定向，但对于简单数据可以达到类似目的。

**Java 程序示例（`MyArgProgram.java`）：**

```java
package com.example.app;

public class MyArgProgram {
    public static void main(String[] args) {
        if (args.length > 0) {
            String inputData = args[0];
            System.out.println("从参数接收到输入：" + inputData);
        } else {
            System.out.println("未提供输入参数。");
        }
    }
}
```

**从命令行运行：**

```bash
mvn compile exec:java -Dexec.mainClass="com.example.app.MyArgProgram" -Dexec.args="MyCustomInputString"
```

或者包含空格时：

```bash
mvn compile exec:java -Dexec.mainClass="com.example.app.MyArgProgram" -Dexec.args="\"包含空格的输入\""
```

此方法仅适用于您的程序可以修改为接受其"输入"作为命令行参数的情况。

## 3. 使用 Shell 重定向输入（配合 `exec:exec`）

如果您绝对需要从文件或管道重定向输入，您**必须**使用 `exec:exec` 目标而不是 `exec:java`。`exec:exec` 目标会生成一个独立的进程，这允许 shell 处理标准输入/输出重定向。

**`pom.xml` 中 `exec:exec` 的配置：**

```xml
<project>
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.yourcompany</groupId>
    <artifactId>my-maven-app</artifactId>
    <version>1.0-SNAPSHOT</version>

    <build>
        <plugins>
            <plugin>
                <groupId>org.codehaus.mojo</groupId>
                <artifactId>exec-maven-plugin</artifactId>
                <version>3.2.0</version> <executions>
                    <execution>
                        <id>run-my-java-app</id>
                        <phase>package</phase> <goals>
                            <goal>exec</goal>
                        </goals>
                        <configuration>
                            <executable>java</executable>
                            <arguments>
                                <argument>-classpath</argument>
                                <classpath/> <argument>com.example.app.MyInputProgram</argument>
                                </arguments>
                            <workingDirectory>${project.build.directory}/classes</workingDirectory>
                            </configuration>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>

    <properties>
        <maven.compiler.source>11</maven.compiler.source>
        <maven.compiler.target>11</maven.compiler.target>
    </properties>

</project>
```

**Java 程序示例（与上面相同的 `MyInputProgram.java`）：**

```java
package com.example.app;

import java.util.Scanner;

public class MyInputProgram {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("请输入您的姓名：");
        String name = scanner.nextLine();
        System.out.println("你好，" + name + "！");

        // 假设在输入姓名后还想读取另一行作为年龄
        System.out.print("请输入您的年龄：");
        int age = scanner.nextInt();
        System.out.println("您 " + age + " 岁了。");

        scanner.close();
    }
}
```

**输入文件（`input.txt`）：**

```
Alice
30
```

**使用 `exec:exec` 和输入重定向运行：**

首先，编译您的项目：

```bash
mvn compile
```

然后，运行 `exec:exec` 目标并使用您的 shell 重定向输入：

```bash
mvn exec:exec@run-my-java-app < input.txt
```

**解释：**

  * `mvn exec:exec@run-my-java-app`：使用 ID "run-my-java-app" 执行 `exec-maven-plugin` 的 `exec` 目标。
  * `< input.txt`：这是一个标准的 shell 重定向操作符。它告诉您的 shell 获取 `input.txt` 的内容并将其作为标准输入提供给正在执行的命令（`java com.example.app.MyInputProgram`）。

**`exec:exec` 的重要注意事项：**

  * **`executable`：** 您需要明确指定 `java` 为可执行文件。
  * **`arguments`：** 您需要手动构建 `java` 命令的参数，包括 `-classpath` 和 `mainClass`。`<classpath/>` 标签是一个特殊值，`exec-maven-plugin` 会将其替换为项目实际计算出的类路径。
  * **`workingDirectory`：** 将 `workingDirectory` 设置为 `${project.build.directory}/classes` 通常很有帮助，这样 Java 可以找到您编译的 `.class` 文件。
  * **`outputFile`（可选）：** `exec-maven-plugin` 的 `exec:exec` 目标还提供了一个 `<outputFile>` 配置选项，用于将程序的标准输出和错误重定向到文件，这直接在插件配置中完成，而不是依赖 shell 重定向。这对于日志记录很有用。

**总结：**

  * 对于用户直接输入的交互式输入，`exec:java` 和 `System.in` 可以正常工作。
  * 对于从文件或管道提供输入的情况，您需要切换到 `exec:exec` 并利用 shell 的输入重定向功能（`<`）。
