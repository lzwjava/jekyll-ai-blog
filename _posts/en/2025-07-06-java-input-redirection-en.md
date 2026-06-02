---
audio: false
generated: true
lang: en
layout: post
title: Redirecting Input in Maven Java Programs
translated: false
type: note
---

Redirecting input for `exec:java` programs can be a bit tricky because `exec:java` runs the Java process within the *same JVM* as Maven. This means you can't use standard shell redirection operators (`<`, `>`) in the same way you would for a separate process.

However, you still have a few options to provide input to your `exec:java` program:

## 1\. Programmatic Input (Standard `System.in`)

The most straightforward way is to design your Java program to read from `System.in` as usual. When you run `mvn exec:java`, whatever you type in your console will be directed to `System.in` of your Java program.

**Example Java Program (`MyInputProgram.java`):**

```java
package com.example.app;

import java.util.Scanner;

public class MyInputProgram {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter your name: ");
        String name = scanner.nextLine();
        System.out.println("Hello, " + name + "!");

        System.out.print("Enter your age: ");
        int age = scanner.nextInt();
        System.out.println("You are " + age + " years old.");

        scanner.close();
    }
}
```

**Running from the command line:**

```bash
mvn compile exec:java -Dexec.mainClass="com.example.app.MyInputProgram"
```

When you run this, Maven will start, and then your program will prompt you for input. You type directly into the console.

## 2\. Using the `exec.args` Property for Input (for simple cases)

If your program expects very simple, non-interactive input, you *might* be able to pass it as an argument, and your program then reads that argument instead of `System.in`. This isn't true standard input redirection, but it serves a similar purpose for simple data.

**Example Java Program (`MyArgProgram.java`):**

```java
package com.example.app;

public class MyArgProgram {
    public static void main(String[] args) {
        if (args.length > 0) {
            String inputData = args[0];
            System.out.println("Received input from argument: " + inputData);
        } else {
            System.out.println("No input argument provided.");
        }
    }
}
```

**Running from the command line:**

```bash
mvn compile exec:java -Dexec.mainClass="com.example.app.MyArgProgram" -Dexec.args="MyCustomInputString"
```

Or with spaces:

```bash
mvn compile exec:java -Dexec.mainClass="com.example.app.MyArgProgram" -Dexec.args="\"Input with spaces\""
```

This approach is only suitable if your program can be modified to accept its "input" as command-line arguments.

## 3\. Redirecting Input using Shell Redirection (with `exec:exec`)

If you absolutely need to redirect input from a file or pipe, you **must** use the `exec:exec` goal instead of `exec:java`. The `exec:exec` goal spawns a separate process, which allows the shell to handle standard input/output redirection.

**`pom.xml` configuration for `exec:exec`:**

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

**Example Java Program (same `MyInputProgram.java` as above):**

```java
package com.example.app;

import java.util.Scanner;

public class MyInputProgram {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter your name: ");
        String name = scanner.nextLine();
        System.out.println("Hello, " + name + "!");

        // Assuming you want to read another line for age after name
        System.out.print("Enter your age: ");
        int age = scanner.nextInt();
        System.out.println("You are " + age + " years old.");

        scanner.close();
    }
}
```

**Input File (`input.txt`):**

```
Alice
30
```

**Running with `exec:exec` and input redirection:**

First, compile your project:

```bash
mvn compile
```

Then, run the `exec:exec` goal and redirect input using your shell:

```bash
mvn exec:exec@run-my-java-app < input.txt
```

**Explanation:**

  * `mvn exec:exec@run-my-java-app`: Executes the `exec` goal of the `exec-maven-plugin` with the `id` "run-my-java-app".
  * `< input.txt`: This is a standard shell redirection operator. It tells your shell to take the content of `input.txt` and feed it as standard input to the command being executed (`java com.example.app.MyInputProgram`).

**Important Notes for `exec:exec`:**

  * **`executable`:** You explicitly specify `java` as the executable.
  * **`arguments`:** You need to construct the `java` command's arguments manually, including `-classpath` and the `mainClass`. The `<classpath/>` tag is a special value that the `exec-maven-plugin` replaces with the actual computed classpath of your project.
  * **`workingDirectory`:** It's often helpful to set the `workingDirectory` to `${project.build.directory}/classes` so that Java can find your compiled `.class` files.
  * **`outputFile` (Optional):** The `exec-maven-plugin` for `exec:exec` also provides an `<outputFile>` configuration option to redirect the program's standard output and error to a file directly within the plugin's configuration, rather than relying on shell redirection. This can be useful for logging.

**In summary:**

  * For interactive input where a user types directly, `exec:java` and `System.in` work fine.
  * For providing input from a file or a pipe, you'll need to switch to `exec:exec` and leverage your shell's input redirection capabilities (`<`).
