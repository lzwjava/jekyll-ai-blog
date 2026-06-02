---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: Maven Exec 插件环境变量指南
translated: true
type: note
---

你可以通过几种方式在 maven-exec-plugin 中使用 environment variables：

## 1. **使用现有的系统 environment variables**

该 plugin 会自动继承系统的 environment variables。你可以在命令中引用它们：

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

## 2. **设置自定义 environment variables**

你可以在 plugin 配置中直接定义 environment variables：

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

## 3. **用于 Java 执行 (exec:java goal)**

当直接运行 Java 代码时：

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

## 4. **结合 Maven properties**

你可以在 pom.xml 的 properties 中引用 environment variables，并在 plugin 中使用它们：

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

核心语法是使用 `${env.VARIABLE_NAME}` 来引用现有的 environment variables，并使用 `<environmentVariables>` 部分为执行的进程设置新的变量。
