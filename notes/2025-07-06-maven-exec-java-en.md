---
audio: false
generated: true
lang: en
layout: post
title: Run Java Classes with Maven Exec
translated: false
type: note
---

The `exec:java` goal of the Maven Exec Plugin is a powerful way to run a Java class with a `main` method directly from your Maven build. It executes the specified Java class **within the same JVM** as your Maven build, using the project's dependencies as the classpath.

Here's how to use it, with common scenarios and examples:

## 1\. Basic Usage from the Command Line

The simplest way to use `exec:java` is directly from the command line, especially for quick tests or running a specific utility class.

**Command:**

```bash
mvn exec:java -Dexec.mainClass="com.yourcompany.YourMainClass"
```

**Explanation:**

* `mvn exec:java`: Invokes the `java` goal of the `exec-maven-plugin`.
* `-Dexec.mainClass="com.yourcompany.YourMainClass"`: This system property specifies the fully qualified name of the Java class that contains the `public static void main(String[] args)` method you want to execute.

**Example:**

Let's say you have a class `com.example.myapp.HelloWorld` with a `main` method:

```java
package com.example.myapp;

public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello from Maven exec:java!");
    }
}
```

You would run it using:

```bash
mvn compile exec:java -Dexec.mainClass="com.example.myapp.HelloWorld"
```

**Note:** It's good practice to run `mvn compile` first to ensure your classes are compiled before `exec:java` attempts to run them.

## 2\. Passing Arguments to Your Java Program

You can pass arguments to your Java program's `main` method using the `exec.args` system property:

**Command:**

```bash
mvn exec:java -Dexec.mainClass="com.yourcompany.YourMainClass" -Dexec.args="arg1 arg2 \"arg with spaces\""
```

**Example:**

If your `HelloWorld` class was:

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

You would run it like:

```bash
mvn compile exec:java -Dexec.mainClass="com.example.myapp.HelloWorld" -Dexec.args="FirstArgument SecondArgument"
```

For arguments with spaces, enclose them in quotes:

```bash
mvn compile exec:java -Dexec.mainClass="com.example.myapp.HelloWorld" -Dexec.args="\"Hello World\" AnotherArg"
```

## 3\. Configuring `exec:java` in `pom.xml`

For more permanent or default configurations, you can add the `exec-maven-plugin` to your `pom.xml`. This allows you to define a default `mainClass` and other parameters, so you don't have to specify them on the command line every time.

**`pom.xml` configuration:**

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

**Explanation of configuration options:**

* `<groupId>org.codehaus.mojo</groupId>` and `<artifactId>exec-maven-plugin</artifactId>`: Standard coordinates for the plugin.
* `<version>3.2.0</version>`: Always specify a recent version of the plugin.
* `<goals><goal>java</goal></goals>`: This binds the `java` goal. If you don't bind it to a specific phase, it will be executed when you explicitly call `mvn exec:java`.
* `<mainClass>com.example.myapp.HelloWorld</mainClass>`: Sets the default main class to execute. If you run `mvn exec:java` without `-Dexec.mainClass` on the command line, this class will be used.
* `<arguments>`: A list of arguments to pass to the `main` method. These are default arguments that can be overridden by `exec.args` on the command line.
* `<systemProperties>`: Allows you to define system properties (`-Dkey=value`) that will be available to your Java application when `exec:java` runs.

**Running with `pom.xml` configuration:**

Once configured in `pom.xml`:

* To run with the default main class and arguments:

    ```bash
    mvn compile exec:java
    ```

* To override the main class from the command line:

    ```bash
    mvn compile exec:java -Dexec.mainClass="com.example.myapp.AnotherMainClass"
    ```

* To override/add arguments from the command line:

    ```bash
    mvn compile exec:java -Dexec.args="commandLineArg1 commandLineArg2"
    ```

    (Note: `exec.args` will typically *replace* `arguments` defined in `pom.xml` if provided on the command line.)

## 4\. Key Differences from `exec:exec`

It's important to understand the distinction between `exec:java` and `exec:exec`:

* **`exec:java`**: Runs the Java program **in the same JVM** as Maven. This is generally faster as it avoids spawning a new process. It automatically sets up the project's dependencies on the classpath.
* **`exec:exec`**: Runs an arbitrary external program (including `java` itself) **in a separate process**. This is useful when you need to specify a different Java executable, pass JVM arguments (like `-Xmx`), or run non-Java executables. If you use `exec:exec` to run a Java program, you typically have to manually construct the classpath using `%classpath` in the arguments.

For most standard Java application execution within a Maven build, `exec:java` is the more convenient choice.

## 5\. Important Considerations

* **Classpath:** `exec:java` automatically includes your project's compiled classes and its dependencies in the classpath.
* **JVM Arguments:** Because `exec:java` runs in the *same* JVM as Maven, you cannot pass JVM arguments (like `-Xmx`, `-XX:MaxPermSize`) directly to `exec:java` through its configuration or `exec.args`. These arguments need to be passed to the Maven JVM itself, typically via the `MAVEN_OPTS` environment variable:

    ```bash
    export MAVEN_OPTS="-Xmx1024m -Dsome.jvm.property=value"
    mvn exec:java ...
    ```

* **System.exit()**: If your Java program calls `System.exit()`, it will terminate the entire Maven build process, not just your program. Be mindful of this when using `exec:java`. The plugin has an option `blockSystemExit` (since version 3.2.0) that tries to prevent this, but it's best to design your main method to complete gracefully without calling `System.exit()`.
* **Dependencies:** `exec:java` relies on the project's dependencies. If you need to run a class from a dependency that is not part of your project's build, you might need to adjust the plugin's configuration or consider using `exec:exec` with explicit classpath definition.
* **Plugin Version:** Always use a recent version of the `exec-maven-plugin` for the latest features and bug fixes. Check the MojoHaus website for the most up-to-date information.
