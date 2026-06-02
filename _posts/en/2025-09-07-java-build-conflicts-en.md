---
audio: false
date: 2025-09-07
generated: true
image: false
lang: en
layout: post
title: Resolving Java Build Version Conflicts
translated: false
type: note
---

You’re building with **Java 8** (class file 52.0), but some build plugins/libs in your POM were compiled for newer Javas. The first one blowing up is **Spotless** (class file 55.0 = Java 11). You also have a few other Java-11+ items that will bite even if Spotless is removed (Checkstyle 10.x, Logback 1.5, and the Jakarta Servlet 5 vs Spring 5’s javax namespace).

Below are two clean ways to fix it. Pick one and you’ll be good.

---

## Option A — Stay on Java 8 (works with Spring 5.2.x and Jetty 9.4)

* Remove/roll back Java-11+ plugins and libs.
* Use **javax.servlet-api 4.0.1** (Spring 5 uses `javax.*`, not `jakarta.*`).
* Keep Jetty 9.4 (Servlet 3.1/4 era).

Paste this POM (only the parts below differ from yours):

```xml
<project>
  ...
  <properties>
    <maven.compiler.source>8</maven.compiler.source>
    <maven.compiler.target>8</maven.compiler.target>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
  </properties>

  <dependencies>
    <!-- Spring 5.x is fine -->
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

    <!-- Test deps unchanged -->
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

    <!-- AOP ok -->
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

    <!-- SLF4J 2.0 is Java 8+, OK -->
    <dependency>
      <groupId>org.slf4j</groupId>
      <artifactId>slf4j-api</artifactId>
      <version>2.0.17</version>
    </dependency>

    <!-- ↓ Downgrade Logback to Java 8-compatible line -->
    <dependency>
      <groupId>ch.qos.logback</groupId>
      <artifactId>logback-classic</artifactId>
      <version>1.2.13</version>
    </dependency>

    <!-- ↓ Use javax servlet for Spring 5.x + Jetty 9.4 -->
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
      <!-- Keep your exec-maven-plugin if you need JavadocRemover -->
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

      <!-- ↓ REMOVE Spotless or gate it behind a Java 11+ profile.
           If you really want it on Java 8, use an old Spotless + JDK8,
           but simplest is to remove it now. -->
      <!-- (Spotless plugin block removed) -->

      <!-- ↓ Checkstyle: pick Java 8–compatible engine -->
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

      <!-- Jetty 9.4 is fine on Java 8 + javax.servlet -->
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

  <!-- Keep your 'python-integration-tests' profile,
       but note spring-boot-maven-plugin 3.5.0 needs Java 17+.
       Leave this profile OFF when building on Java 8. -->
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

          <!-- Leave this Boot plugin here but DO NOT activate this profile on Java 8 -->
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

Then run:

```bash
mvn -v                # confirm using a JDK 1.8.x
mvn clean package
# or for dev
mvn jetty:run
```

---

## Option B — Upgrade your build JDK (Java 17 is a sweet spot)

* Switch your **build** to JDK 17+ (and `mvn -v` should show Java 17).
* Keep Spotless and Checkstyle 10.x as-is.
* You can keep `jakarta.servlet-api` **only if** you also move the runtime to Jetty 11+ or Tomcat 10+ and migrate your code to `jakarta.*` namespaces (Spring 6 / Spring Boot 3 world). If you stay on Spring 5.2.x, use `javax.servlet-api:4.0.1` and a Servlet 4 container instead.

Typical commands:

```bash
# On Ubuntu, install a JDK 17 and select it:
sudo apt install openjdk-17-jdk
sudo update-alternatives --config java
sudo update-alternatives --config javac

mvn -v             # should print Java version 17
mvn clean package
```

If you must still generate Java 8 bytecode while building on Java 17, set:

```xml
<properties>
  <maven.compiler.release>8</maven.compiler.release>
</properties>
```

(But note: dependencies like Logback 1.5 are Java 11+ anyway, so your **runtime** must be 11+ if you include them.)

---

## Why it failed (short version)

* `UnsupportedClassVersionError ... class file version 55.0` = plugin/library compiled with **Java 11**, but Maven ran under **Java 8**.
* Your specific offenders on Java 8:

  * Spotless plugin 2.44.5 (Java 11+)
  * Checkstyle 10.25.0 (Java 11+)
  * Logback 1.5.x (Java 11+)
  * `jakarta.servlet-api:5.0.0` mismatches Spring 5’s `javax.*` and Jetty 9.4.

---

If you tell me which path you prefer (stick to Java 8 vs move to Java 17+), I’ll tighten the POM exactly for that setup and, if needed, give you the minimal diffs for your `web.xml`/Spring config and Jetty/Tomcat choice.
