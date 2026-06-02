---
audio: false
date: 2025-09-08
generated: true
image: false
lang: en
layout: post
title: Single JVM Integration Coverage Strategy
translated: false
type: note
---

You don’t need to run Jetty twice or create a separate JaCoCo `.exec` per module. One agent on the single JVM that serves your WAR can record coverage for **all classes that JVM loads**—including `PlaygroundUtils`—into **one shared exec file**. Then every module can generate its own report by pointing at that same exec. For a big reactor (10+ modules), this scales cleanly.

Below is a concrete, minimal plan and drop-in edits for your repo.

---

## The strategy

1. **Use a single, shared IT exec file at the parent level.**
   Start Jetty **once**, instrumented with JaCoCo, writing to `../target/it-coverage/jacoco-it.exec` (a parent‐scoped path).
2. **Run your external Python tests once.**
   They hit the deployed app; the agent records hits for all loaded classes (web + libs).
3. **Generate per-module reports**, each module pointing to the shared `jacoco-it.exec`.
   `PlaygroundUtils` will get a report even though it has no tests—it maps the shared exec to its own `target/classes`.
4. (Optional) **Also generate an aggregate HTML** at the parent with `report-aggregate`, or just keep per-module reports.

Only when you truly have **multiple JVMs** (e.g., several microservices) do you need multiple exec files and a `jacoco:merge` step. For your current single JVM (Jetty) build, keep it to one exec.

---

## Exact edits

### 1) Parent `pom.xml` (PlaygroundLib)

Add shared properties so every module can reference the same exec file:

```xml
<properties>
  <!-- ... your existing versions ... -->
  <it.coverage.dir>${project.basedir}/target/it-coverage</it.coverage.dir>
  <jacoco.it.exec>${it.coverage.dir}/jacoco-it.exec</jacoco.it.exec>
  <!-- Toggle per-module IT report generation -->
  <it.report.skip>false</it.report.skip>
</properties>
```

(Optional) If you want a single **aggregate** HTML at the parent, add this execution:

```xml
<build>
  <pluginManagement>
    <!-- keep your existing blocks -->
  </pluginManagement>

  <plugins>
    <plugin>
      <groupId>org.jacoco</groupId>
      <artifactId>jacoco-maven-plugin</artifactId>
      <executions>
        <execution>
          <id>it-aggregate-report</id>
          <phase>verify</phase>
          <goals>
            <goal>report-aggregate</goal>
          </goals>
          <configuration>
            <!-- Use the shared IT exec produced by Jetty run -->
            <dataFile>${jacoco.it.exec}</dataFile>
            <outputDirectory>${project.reporting.outputDirectory}/jacoco-it</outputDirectory>
          </configuration>
        </execution>
      </executions>
    </plugin>
  </plugins>
</build>
```

> If your JaCoCo version rejects `<dataFile>` on `report-aggregate`, skip this optional block and rely on the per-module reports below. You can always add a tiny “coverage” aggregator module later to run `merge` + `report`.

---

### 2) `PlaygroundWeb/pom.xml`

Point the Jetty agent to the **parent-level** exec path and enable append:

```xml
<plugin>
  <groupId>org.eclipse.jetty</groupId>
  <artifactId>jetty-maven-plugin</artifactId>
  <executions>
    <execution>
      <id>start-jetty</id>
      <phase>pre-integration-test</phase>
      <goals><goal>start</goal></goals>
      <configuration>
        <daemon>true</daemon>
        <jvmArgs>
          -javaagent:${settings.localRepository}/org/jacoco/org.jacoco.agent/${jacoco.version}/org.jacoco.agent-${jacoco.version}-runtime.jar=destfile=${project.parent.basedir}/target/it-coverage/jacoco-it.exec,append=true,includes=org.lzw.*
        </jvmArgs>
        <httpConnector>
          <port>8080</port>
          <host>127.0.0.1</host>
        </httpConnector>
        <webApp><contextPath>/</contextPath></webApp>
        <stopHost>127.0.0.1</stopHost>
        <stopPort>8081</stopPort>
        <stopKey>stop</stopKey>
      </configuration>
    </execution>

    <execution>
      <id>stop-jetty</id>
      <phase>post-integration-test</phase>
      <goals><goal>stop</goal></goals>
      <configuration>
        <stopHost>127.0.0.1</stopHost>
        <stopPort>8081</stopPort>
        <stopKey>stop</stopKey>
        <stopWait>15</stopWait>
      </configuration>
    </execution>
  </executions>
</plugin>
```

Update your `jacoco:report` in `PlaygroundWeb` to read the **same** shared exec:

```xml
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <executions>
    <execution>
      <id>report-it</id>
      <phase>verify</phase>
      <goals><goal>report</goal></goals>
      <configuration>
        <dataFile>${project.parent.basedir}/target/it-coverage/jacoco-it.exec</dataFile>
        <outputDirectory>${project.reporting.outputDirectory}/jacoco-it</outputDirectory>
      </configuration>
    </execution>
  </executions>
</plugin>
```

Your existing Exec Maven Plugin that runs `python -m unittest discover tests -v` is perfect—leave it as is.

---

### 3) `PlaygroundUtils/pom.xml`

Add a **report-only** execution so it can map the shared exec to its own classes:

```xml
<build>
  <plugins>
    <!-- keep your existing plugins -->

    <plugin>
      <groupId>org.jacoco</groupId>
      <artifactId>jacoco-maven-plugin</artifactId>
      <executions>
        <execution>
          <id>report-it</id>
          <phase>verify</phase>
          <goals><goal>report</goal></goals>
          <configuration>
            <dataFile>${project.parent.basedir}/target/it-coverage/jacoco-it.exec</dataFile>
            <outputDirectory>${project.reporting.outputDirectory}/jacoco-it</outputDirectory>
            <skip>${it.report.skip}</skip>
          </configuration>
        </execution>
      </executions>
    </plugin>
  </plugins>
</build>
```

This module never starts Jetty or runs Python; it only consumes the shared exec and its own `target/classes`. If any `PlaygroundUtils` classes are used by the web app during tests, they’ll show up with coverage. If they aren’t exercised, they’ll be 0%—which is the correct signal.

---

## How you run it

From the repo root:

```bash
mvn -pl PlaygroundWeb -am clean verify
```

The build order compiles both modules, starts Jetty once with the agent, runs your Python tests, stops Jetty, then generates:

* `PlaygroundWeb/target/site/jacoco-it/index.html`
* `PlaygroundUtils/target/site/jacoco-it/index.html`
* Optionally, an aggregate report under the parent if you enabled `report-aggregate`.

---

## When you have 10 modules

* If all 10 end up inside the **same WAR/JVM**, keep the **single shared exec** pattern. Every module adds a `report` execution that points to the shared exec. You still start Jetty once and run Python once.

* If you have **multiple JVMs** (e.g., separate services), give each JVM its own `destfile` (e.g., `it-coverage/serviceA.exec`, `serviceB.exec`), then in the parent run:

  ```xml
  <plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <executions>
      <execution>
        <id>merge-it</id>
        <phase>post-integration-test</phase>
        <goals><goal>merge</goal></goals>
        <configuration>
          <destFile>${project.basedir}/target/it-coverage/jacoco-merged.exec</destFile>
          <files>
            <file>${project.basedir}/target/it-coverage/serviceA.exec</file>
            <file>${project.basedir}/target/it-coverage/serviceB.exec</file>
            <!-- add more as needed -->
          </files>
        </configuration>
      </execution>

      <execution>
        <id>aggregate-report</id>
        <phase>verify</phase>
        <goals><goal>report-aggregate</goal></goals>
        <configuration>
          <dataFile>${project.basedir}/target/it-coverage/jacoco-merged.exec</dataFile>
          <outputDirectory>${project.reporting.outputDirectory}/jacoco-it</outputDirectory>
        </configuration>
      </execution>
    </executions>
  </plugin>
  ```

* If you want to limit noise, set `includes=org.lzw.*` (already shown) or add `excludes` to the agent line to filter third-party libs.

---

## Why your current pain happens

* You were creating **per-module exec files**, so you felt forced to re-run Jetty with different agents to populate each one. That’s unnecessary. The agent doesn’t care which module a class “belongs” to—it records any loaded class. Centralize the exec and point each module’s `report` to it.

---

## Quick checklist

* One **shared** `${jacoco.it.exec}` under the parent.
* Jetty started **once** with `append=true` and `includes=org.lzw.*`.
* Python tests run **once**.
* Each module has a `jacoco:report` that reads the shared exec.
* Optional parent `report-aggregate` for a single top-level HTML.

That should make your setup both simpler and scalable. If you want, I can produce exact diffs for your current POMs with these changes applied.
