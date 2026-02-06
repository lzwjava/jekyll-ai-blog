---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Maven Exec Plugin Environment Variables Guide
translated: false
type: note
---

You can use environment variables in the maven-exec-plugin in several ways:

## 1. **Using existing system environment variables**

The plugin automatically inherits environment variables from your system. You can reference them in your command:

```xml
<plugin>
    <groupId>org.codehaus.mojo</groupId>
    <artifactId>exec-maven-plugin</artifactId>
    <version>3.1.0</version>
    <executions>
        <execution>
            <goals>
                <goal>exec</goal>
            </goals>
        </execution>
    </executions>
    <configuration>
        <executable>echo</executable>
        <arguments>
            <argument>${env.MY_VARIABLE}</argument>
        </arguments>
    </configuration>
</plugin>
```

## 2. **Setting custom environment variables**

You can define environment variables directly in the plugin configuration:

```xml
<configuration>
    <executable>java</executable>
    <arguments>
        <argument>-classpath</argument>
        <argument>target/classes</argument>
        <argument>com.example.MainClass</argument>
    </arguments>
    <environmentVariables>
        <MY_VAR>some_value</MY_VAR>
        <DATABASE_URL>jdbc:postgresql://localhost/mydb</DATABASE_URL>
        <API_KEY>${api.key}</API_KEY>
    </environmentVariables>
</configuration>
```

## 3. **For Java execution (exec:java goal)**

When running Java code directly:

```xml
<configuration>
    <mainClass>com.example.MainClass</mainClass>
    <systemProperties>
        <systemProperty>
            <key>myProperty</key>
            <value>${env.MY_ENV_VAR}</value>
        </systemProperty>
    </systemProperties>
</configuration>
```

## 4. **Combining with Maven properties**

You can reference environment variables in your pom.xml properties and use them in the plugin:

```xml
<properties>
    <app.environment>${env.APP_ENV}</app.environment>
</properties>

<build>
    <plugins>
        <plugin>
            <groupId>org.codehaus.mojo</groupId>
            <artifactId>exec-maven-plugin</artifactId>
            <configuration>
                <environmentVariables>
                    <ENV>${app.environment}</ENV>
                </environmentVariables>
            </configuration>
        </plugin>
    </plugins>
</build>
```

The key syntax is `${env.VARIABLE_NAME}` to reference existing environment variables, and the `<environmentVariables>` section to set new ones for the executed process.