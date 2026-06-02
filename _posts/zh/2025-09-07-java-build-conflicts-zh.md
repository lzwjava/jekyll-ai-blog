---
audio: false
date: 2025-09-07
generated: true
image: false
lang: zh
layout: post
title: 解决Java构建版本冲突
translated: true
type: note
---

您当前使用 **Java 8**（类文件版本 52.0）进行构建，但 POM 文件中的某些构建插件/库是针对更高版本 Java 编译的。首先报错的是 **Spotless**（类文件版本 55.0 = Java 11）。即使移除 Spotless，您还有一些其他 Java 11+ 的依赖项会引发问题（Checkstyle 10.x、Logback 1.5，以及 Jakarta Servlet 5 与 Spring 5 的 javax 命名空间冲突）。

以下是两种清晰的解决方案。选择其一即可解决问题。

---

## 方案 A — 停留在 Java 8（兼容 Spring 5.2.x 和 Jetty 9.4）

* 移除/回退 Java 11+ 的插件和库。
* 使用 **javax.servlet-api 4.0.1**（Spring 5 使用 `javax.*`，而非 `jakarta.*`）。
* 保持使用 Jetty 9.4（Servlet 3.1/4 时代）。

粘贴此 POM（仅列出与您配置不同的部分）：

```xml
<project>
  ...
  <properties>
    <maven.compiler.source>8</maven.compiler.source>
    <maven.compiler.target>8</maven.compiler.target>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
  </properties>

  <dependencies>
    <!-- Spring 5.x 没问题 -->
    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-context</artifactId>
      <version>5.2.2.RELEASE</version>
    </dependency>
    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-web</artifactId>
      <version>5.2.2.RELEASE</version>
    </dependency>
    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-webmvc</artifactId>
      <version>5.2.2.RELEASE</version>
    </dependency>
    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-core</artifactId>
      <version>5.2.2.RELEASE</version>
    </dependency>

    <!-- 测试依赖保持不变 -->
    <dependency>
      <groupId>org.junit.jupiter</groupId>
      <artifactId>junit-jupiter-api</artifactId>
      <version>5.13.1</version>
      <scope>test</scope>
    </dependency>
    <dependency>
      <groupId>org.junit.jupiter</groupId>
      <artifactId>junit-jupiter-engine</artifactId>
      <version>5.13.1</version>
      <scope>test</scope>
    </dependency>
    <dependency>
      <groupId>org.mockito</groupId>
      <artifactId>mockito-core</artifactId>
      <version>5.18.0</version>
      <scope>test</scope>
    </dependency>
    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-test</artifactId>
      <version>5.2.2.RELEASE</version>
      <scope>test</scope>
    </dependency>

    <!-- AOP 没问题 -->
    <dependency>
      <groupId>org.aspectj</groupId>
      <artifactId>aspectjrt</artifactId>
      <version>1.9.24</version>
    </dependency>
    <dependency>
      <groupId>org.aspectj</groupId>
      <artifactId>aspectjweaver</artifactId>
      <version>1.9.24</version>
    </dependency>

    <!-- SLF4J 2.0 兼容 Java 8+，没问题 -->
    <dependency>
      <groupId>org.slf4j</groupId>
      <artifactId>slf4j-api</artifactId>
      <version>2.0.17</version>
    </dependency>

    <!-- ↓ 降级 Logback 到兼容 Java 8 的版本 -->
    <dependency>
      <groupId>ch.qos.logback</groupId>
      <artifactId>logback-classic</artifactId>
      <version>1.2.13</version>
    </dependency>

    <!-- ↓ 为 Spring 5.x + Jetty 9.4 使用 javax servlet -->
    <dependency>
      <groupId>javax.servlet</groupId>
      <artifactId>javax.servlet-api</artifactId>
      <version>4.0.1</version>
      <scope>provided</scope>
    </dependency>

    <dependency>
      <groupId>org.apache.commons</groupId>
      <artifactId>commons-lang3</artifactId>
      <version>3.17.0</version>
    </dependency>
  </dependencies>

  <build>
    <plugins>
      <!-- 如果需要 JavadocRemover，请保留 exec-maven-plugin -->
      <plugin>
        <groupId>org.codehaus.mojo</groupId>
        <artifactId>exec-maven-plugin</artifactId>
        <version>3.5.1</version>
        <executions>
          <execution>
            <id>remove-javadoc</id>
            <phase>compile</phase>
            <goals><goal>java</goal></goals>
            <configuration>
              <mainClass>org.lzw.JavadocRemover</mainClass>
              <arguments><argument>src/main</argument></arguments>
            </configuration>
          </execution>
        </executions>
      </plugin>

      <!-- ↓ 移除 Spotless 或将其限制在 Java 11+ 的 Profile 中。
           如果确实需要在 Java 8 上使用，请使用旧版 Spotless + JDK8，
           但最简单的做法是现在移除它。 -->
      <!-- (Spotless 插件块已移除) -->

      <!-- ↓ Checkstyle：选择兼容 Java 8 的引擎 -->
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-checkstyle-plugin</artifactId>
        <version>3.1.2</version>
        <dependencies>
          <dependency>
            <groupId>com.puppycrawl.tools</groupId>
            <artifactId>checkstyle</artifactId>
            <version>9.3</version>
          </dependency>
        </dependencies>
        <configuration>
          <configLocation>${project.basedir}/checks.xml</configLocation>
          <failOnViolation>true</failOnViolation>
        </configuration>
        <executions>
          <execution>
            <id>checkstyle-check</id>
            <phase>compile</phase>
            <goals><goal>check</goal></goals>
          </execution>
        </executions>
      </plugin>

      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-war-plugin</artifactId>
        <version>3.4.0</version>
        <configuration>
          <failOnMissingWebXml>true</failOnMissingWebXml>
        </configuration>
      </plugin>

      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-surefire-plugin</artifactId>
        <version>3.5.3</version>
      </plugin>

      <plugin>
        <groupId>org.jacoco</groupId>
        <artifactId>jacoco-maven-plugin</artifactId>
        <version>0.8.12</version>
        <executions>
          <execution>
            <id>prepare-agent</id>
            <goals><goal>prepare-agent</goal></goals>
          </execution>
          <execution>
            <id>report</id>
            <phase>verify</phase>
            <goals><goal>report</goal></goals>
          </execution>
        </executions>
      </plugin>

      <!-- Jetty 9.4 在 Java 8 + javax.servlet 环境下运行良好 -->
      <plugin>
        <groupId>org.eclipse.jetty</groupId>
        <artifactId>jetty-maven-plugin</artifactId>
        <version>9.4.54.v20240208</version>
        <configuration>
          <httpConnector><port>8080</port></httpConnector>
          <webApp><contextPath>/</contextPath></webApp>
        </configuration>
      </plugin>
    </plugins>
  </build>

  <!-- 保留您的 'python-integration-tests' Profile，
       但注意 spring-boot-maven-plugin 3.5.0 需要 Java 17+。
       在 Java 8 上构建时，请确保此 Profile 处于关闭状态。 -->
  <profiles>
    <profile>
      <id>python-integration-tests</id>
      <build>
        <plugins>
          <plugin>
            <groupId>org.jacoco</groupId>
            <artifactId>jacoco-maven-plugin</artifactId>
            <version>0.8.12</version>
            <executions>
              <execution>
                <id>prepare-agent-integration</id>
                <goals><goal>prepare-agent-integration</goal></goals>
                <configuration>
                  <destFile>${project.build.directory}/jacoco-it.exec</destFile>
                  <propertyName>jacoco.agent.it</propertyName>
                </configuration>
              </execution>
            </executions>
          </plugin>

          <!-- 将此 Boot 插件保留在此处，但不要在 Java 8 上激活此 Profile -->
          <plugin>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-maven-plugin</artifactId>
            <version>3.5.0</version>
          </plugin>

          <plugin>
            <groupId>org.codehaus.mojo</groupId>
            <artifactId>exec-maven-plugin</artifactId>
            <version>3.5.1</version>
            <executions>
              <execution>
                <id>python-integration-tests</id>
                <phase>integration-test</phase>
                <goals><goal>exec</goal></goals>
                <configuration>
                  <executable>python</executable>
                  <workingDirectory>${project.basedir}</workingDirectory>
                  <arguments>
                    <argument>-m</argument><argument>unittest</argument>
                    <argument>discover</argument><argument>tests/</argument>
                    <argument>-v</argument>
                  </arguments>
                </configuration>
              </execution>
            </executions>
          </plugin>
        </plugins>
      </build>
    </profile>
  </profiles>
</project>
```

然后运行：

```bash
mvn -v                # 确认使用 JDK 1.8.x
mvn clean package
# 或用于开发
mvn jetty:run
```

---

## 方案 B — 升级您的构建 JDK（Java 17 是一个理想选择）

* 将您的**构建**环境切换到 JDK 17+（`mvn -v` 应显示 Java 17）。
* 保持 Spotless 和 Checkstyle 10.x 不变。
* 您可以保留 `jakarta.servlet-api`，**前提是**您同时将运行时环境迁移到 Jetty 11+ 或 Tomcat 10+，并将您的代码迁移到 `jakarta.*` 命名空间（Spring 6 / Spring Boot 3 的世界）。如果您停留在 Spring 5.2.x，请使用 `javax.servlet-api:4.0.1` 和一个 Servlet 4 容器。

典型命令：

```bash
# 在 Ubuntu 上，安装 JDK 17 并选择它：
sudo apt install openjdk-17-jdk
sudo update-alternatives --config java
sudo update-alternatives --config javac

mvn -v             # 应打印 Java 版本 17
mvn clean package
```

如果您必须在 Java 17 上构建的同时生成 Java 8 字节码，请设置：

```xml
<properties>
  <maven.compiler.release>8</maven.compiler.release>
</properties>
```

（但请注意：像 Logback 1.5 这样的依赖项是 Java 11+ 的，因此如果包含它们，您的**运行时**环境必须是 11+。）

---

## 失败原因（简要说明）

* `UnsupportedClassVersionError ... class file version 55.0` = 插件/库使用 **Java 11** 编译，但 Maven 在 **Java 8** 下运行。
* 您在 Java 8 上遇到的具体问题来源：

  * Spotless 插件 2.44.5 (Java 11+)
  * Checkstyle 10.25.0 (Java 11+)
  * Logback 1.5.x (Java 11+)
  * `jakarta.servlet-api:5.0.0` 与 Spring 5 的 `javax.*` 和 Jetty 9.4 不匹配。

---

如果您告诉我您倾向于哪种方案（坚持 Java 8 还是迁移到 Java 17+），我将为您精确调整 POM 配置，并在必要时为您提供 `web.xml`/Spring 配置以及 Jetty/Tomcat 选择的最小差异修改。
