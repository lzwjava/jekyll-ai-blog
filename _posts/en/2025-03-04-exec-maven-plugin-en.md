---
audio: false
generated: true
lang: en
layout: post
title: Exec Maven Plugin
translated: false
type: note
---

To use the `org.codehaus.mojo` Exec Maven Plugin in your Maven project, you need to configure it in your `pom.xml` file and decide how you want to execute programs—either external commands or Java programs—during your build process. The plugin provides two main goals: `exec:exec` for running external programs and `exec:java` for executing Java classes. Below, I’ll guide you through the steps to set it up and use it effectively.

### Step 1: Add the Plugin to Your `pom.xml`
First, include the Exec Maven Plugin in the `<build><plugins>` section of your `pom.xml`. Specify the `groupId`, `artifactId`, and a version (the latest as of now is `3.1.0`):

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.codehaus.mojo</groupId>
            <artifactId>exec-maven-plugin</artifactId>
            <version>3.1.0</version>
        </plugin>
    </plugins>
</build>
```

This adds the plugin to your project, but it won’t do anything yet until you configure it or run its goals manually.

### Step 2: Choose Your Goal
The plugin offers two primary goals:
- **`exec:exec`**: Executes any external program (e.g., shell scripts, binaries, or even the `java` command).
- **`exec:java`**: Runs a Java class with a `main` method from your project in the same JVM as Maven.

You can use these goals either by running them manually from the command line (e.g., `mvn exec:exec`) or by binding them to a specific phase in the Maven build lifecycle.

### Option 1: Running a Java Program with `exec:java`
If you want to execute a Java class from your project, use the `exec:java` goal. This is ideal for running a `main` method in a class that’s part of your project, leveraging the project’s runtime classpath (including dependencies) automatically.

#### Manual Execution
Add a configuration to specify the main class:

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.codehaus.mojo</groupId>
            <artifactId>exec-maven-plugin</artifactId>
            <version>3.1.0</version>
            <configuration>
                <mainClass>com.example.Main</mainClass>
            </configuration>
        </plugin>
    </plugins>
</build>
```

Then, run it from the command line:

```bash
mvn exec:java
```

This executes `com.example.Main` in the same JVM as Maven, inheriting Maven’s JVM settings.

#### Automatic Execution During Build
To run it automatically during a build phase (e.g., `test`), use the `<executions>` section:

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.codehaus.mojo</groupId>
            <artifactId>exec-maven-plugin</artifactId>
            <version>3.1.0</version>
            <executions>
                <execution>
                    <id>run-my-java</id>
                    <phase>test</phase>
                    <goals>
                        <goal>java</goal>
                    </goals>
                    <configuration>
                        <mainClass>com.example.Main</mainClass>
                    </configuration>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

Now, when you run `mvn test`, the `com.example.Main` class will execute during the `test` phase.

#### Passing Arguments or System Properties
You can pass arguments to the `main` method or set system properties:

```xml
<configuration>
    <mainClass>com.example.Main</mainClass>
    <arguments>
        <argument>arg1</argument>
        <argument>arg2</argument>
    </arguments>
    <systemProperties>
        <systemProperty>
            <key>propertyName</key>
            <value>propertyValue</value>
        </systemProperty>
    </systemProperties>
</configuration>
```

Note that `exec:java` runs in the same JVM as Maven, so JVM options (e.g., `-Xmx`) are inherited from how Maven is invoked (e.g., `mvn -Xmx512m exec:java`).

### Option 2: Running an External Program with `exec:exec`
For executing external programs like shell scripts or commands, use the `exec:exec` goal.

#### Manual Execution
Configure the plugin to run a script:

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.codehaus.mojo</groupId>
            <artifactId>exec-maven-plugin</artifactId>
            <version>3.1.0</version>
            <configuration>
                <executable>myScript.sh</executable>
                <workingDirectory>/path/to/dir</workingDirectory>
                <arguments>
                    <argument>param1</argument>
                    <argument>param2</argument>
                </arguments>
            </configuration>
        </plugin>
    </plugins>
</build>
```

Run it with:

```bash
mvn exec:exec
```

This executes `myScript.sh` with the specified arguments in the given working directory.

#### Automatic Execution During Build
Bind it to a phase, such as starting and stopping a server for integration tests:

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.codehaus.mojo</groupId>
            <artifactId>exec-maven-plugin</artifactId>
            <version>3.1.0</version>
            <executions>
                <execution>
                    <id>start-server</id>
                    <phase>pre-integration-test</phase>
                    <goals>
                        <goal>exec</goal>
                    </goals>
                    <configuration>
                        <executable>startServer.sh</executable>
                    </configuration>
                </execution>
                <execution>
                    <id>stop-server</id>
                    <phase>post-integration-test</phase>
                    <goals>
                        <goal>exec</goal>
                    </goals>
                    <configuration>
                        <executable>stopServer.sh</executable>
                    </configuration>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

Running `mvn integration-test` will start the server before tests and stop it afterward.

#### Running Java with Custom JVM Options
If you need a separate JVM with specific options (unlike `exec:java`), use `exec:exec` with the `java` executable. You’ll need to manage the classpath manually. Here’s an example:

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.codehaus.mojo</groupId>
            <artifactId>exec-maven-plugin</artifactId>
            <version>3.1.0</version>
            <configuration>
                <executable>java</executable>
                <arguments>
                    <argument>-Xmx512m</argument>
                    <argument>-classpath</argument>
                    <argument>${project.build.outputDirectory}</argument>
                    <argument>com.example.Main</argument>
                </arguments>
            </configuration>
        </plugin>
    </plugins>
</build>
```

To include dependencies in the classpath, you can use the `maven-dependency-plugin` to generate it:

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-dependency-plugin</artifactId>
            <version>3.2.0</version>
            <executions>
                <execution>
                    <id>build-classpath</id>
                    <phase>generate-resources</phase>
                    <goals>
                        <goal>build-classpath</goal>
                    </goals>
                    <configuration>
                        <outputProperty>project.classpath</outputProperty>
                    </configuration>
                </execution>
            </executions>
        </plugin>
        <plugin>
            <groupId>org.codehaus.mojo</groupId>
            <artifactId>exec-maven-plugin</artifactId>
            <version>3.1.0</version>
            <executions>
                <execution>
                    <id>run-java</id>
                    <phase>test</phase>
                    <goals>
                        <goal>exec</goal>
                    </goals>
                    <configuration>
                        <executable>java</executable>
                        <arguments>
                            <argument>-Xmx512m</argument>
                            <argument>-classpath</argument>
                            <argument>${project.classpath}:${project.build.outputDirectory}</argument>
                            <argument>com.example.Main</argument>
                        </arguments>
                    </configuration>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

Adjust the classpath separator (`:` for Unix, `;` for Windows) as needed.

### Additional Configuration Options
- **Environment Variables** (for `exec:exec`):
  ```xml
  <configuration>
      <executable>myScript.sh</executable>
      <environmentVariables>
          <MY_VAR>value</MY_VAR>
      </environmentVariables>
  </configuration>
  ```
- **Working Directory**: Use `<workingDirectory>` to set where the command runs.

### Summary
The Exec Maven Plugin is versatile:
- Use `exec:java` to run Java classes from your project easily, leveraging the project’s classpath, but it runs in Maven’s JVM.
- Use `exec:exec` for external programs or Java with custom JVM options, requiring manual classpath management if needed.
- Configure it in `pom.xml` and either run it manually (`mvn exec:java` or `mvn exec:exec`) or bind it to build phases with `<executions>`.

This setup allows you to integrate custom executions seamlessly into your Maven build process!
