---
audio: false
date: 2025-09-11
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Understanding JaCoCo and Maven Integration
translated: false
type: note
---

Got it—here’s how the JaCoCo pieces in **your exact POM** work together, step-by-step, and why.

---

# The two coverage streams this POM creates

1. **Unit-test coverage (Surefire path)**

* You bind JaCoCo’s **`prepare-agent`** without any special config:

  ```xml
  <execution>
    <id>prepare-agent</id>
    <goals><goal>prepare-agent</goal></goals>
  </execution>
  ```

  This injects `-javaagent:...org.jacoco.agent-<ver>-runtime.jar` into the **Surefire** test JVM via the `argLine` property.
  • Default **destfile** is `${project.build.directory}/jacoco.exec`.
  • Default **append** is `true` (JaCoCo agent appends when the file already exists).
  • Effect: when you run unit tests (if any) during `test`, coverage goes into `target/jacoco.exec`.

2. **Integration-test coverage (Jetty path)**

* You define a **separate file** for IT coverage:

  ```xml
  <properties>
    <jacoco.it.exec>${project.build.directory}/jacoco-it.exec</jacoco.it.exec>
  </properties>
  ```

* You start Jetty **with its own JaCoCo agent** pointing to that file:

  ```xml
  <plugin>
    <artifactId>jetty-maven-plugin</artifactId>
    ...
    <execution>
      <id>start-jetty</id>
      <phase>pre-integration-test</phase>
      <goals><goal>start</goal></goals>
      <configuration>
        <daemon>true</daemon>
        <jvmArgs>
          -javaagent:${settings.localRepository}/org/jacoco/org.jacoco.agent/${jacoco.version}/org.jacoco.agent-${jacoco.version}-runtime.jar=destfile=${jacoco.it.exec}
        </jvmArgs>
        ...
      </configuration>
    </execution>
  </plugin>
  ```

  • Jetty runs as a **separate JVM**; its agent writes to `target/jacoco-it.exec`.
  • Because `append` isn’t specified, JaCoCo’s default `append=true` applies—so multiple Jetty launches append to the same file unless you clean or set `append=false`.

---

# Lifecycle flow (what happens on `mvn verify`)

1. **compile**

   * Spotless formats (`spotless-maven-plugin`) and Checkstyle runs (`maven-checkstyle-plugin`).
   * Your WAR is prepared (`maven-war-plugin`).

2. **test (Surefire)**

   * If you have unit tests, they run under the **`prepare-agent`** injected argLine → coverage goes to `target/jacoco.exec`.

3. **pre-integration-test**

   * Jetty is started **in daemon mode**:

     ```xml
     <daemon>true</daemon>
     ```

     Maven immediately regains control; Jetty keeps running with the JaCoCo agent attached, writing to `jacoco-it.exec`.

4. **integration-test**

   * Your Python tests hit the running app:

     ```xml
     <plugin>
       <artifactId>exec-maven-plugin</artifactId>
       <execution>
         <id>python-integration-tests</id>
         <phase>integration-test</phase>
         <goals><goal>exec</goal></goals>
         <configuration>
           <executable>python3</executable>
           <workingDirectory>${project.parent.basedir}</workingDirectory>
           <arguments>
             <argument>-m</argument><argument>unittest</argument>
             <argument>discover</argument><argument>tests/</argument>
             <argument>-v</argument>
           </arguments>
         </configuration>
       </execution>
     </plugin>
     ```

     These tests exercise Jetty, so coverage accumulates in **`target/jacoco-it.exec`** via the Jetty JVM’s agent.

5. **post-integration-test**

   * Jetty is cleanly stopped:

     ```xml
     <execution>
       <id>stop-jetty</id>
       <phase>post-integration-test</phase>
       <goals><goal>stop</goal></goals>
       ...
     </execution>
     ```

6. **verify**

   * You generate a **separate IT report** using the IT data file and a custom output directory:

     ```xml
     <execution>
       <id>report-it</id>
       <phase>verify</phase>
       <goals><goal>report</goal></goals>
       <configuration>
         <dataFile>${jacoco.it.exec}</dataFile>
         <outputDirectory>${project.reporting.outputDirectory}/jacoco-it
         </outputDirectory>
       </configuration>
     </execution>
     ```

   * Result: HTML goes to `target/site/jacoco-it/index.html` summarizing only **integration** coverage (from Jetty).

> Note: If you also want a **unit-test** report, you could add another `jacoco:report` execution that points at the default `target/jacoco.exec` and outputs to `target/site/jacoco`—keeping unit and IT reports separate.

---

# About “create new or replace?” for the `.exec` files

* **JaCoCo agent default is `append=true`**.

  * For **unit tests**, the file is `target/jacoco.exec`. When you run `mvn verify` repeatedly **without `clean`**, data may append across runs.
  * For **Jetty IT**, your `jvmArgs` don’t override `append`, so `target/jacoco-it.exec` also **appends** by default.

**Best practice** (to avoid mixing old data):

* Run `mvn clean verify`, **or** add `append=false` in the Jetty agent line:

  ```xml
  -javaagent:...org.jacoco.agent-...-runtime.jar=destfile=${jacoco.it.exec},append=false
  ```

* If you ever want to merge multiple `.exec` files on purpose, use `jacoco:merge` before `jacoco:report`.

---

# What each relevant block in your original XML is doing (by reference)

* **IT file location**

  ```xml
  <properties>
    <jacoco.it.exec>${project.build.directory}/jacoco-it.exec</jacoco.it.exec>
    <it.report.skip>false</it.report.skip>
  </properties>
  ```

  Defines where integration coverage is stored. `it.report.skip` is declared but not yet wired into the report execution (see tip below).

* **Unit test agent (Surefire path)**

  ```xml
  <plugin>
    <artifactId>jacoco-maven-plugin</artifactId>
    <executions>
      <execution>
        <id>prepare-agent</id>
        <goals><goal>prepare-agent</goal></goals>
      </execution>
      ...
    </executions>
  </plugin>
  ```

* **Jetty with JaCoCo for IT**

  ```xml
  <plugin>
    <artifactId>jetty-maven-plugin</artifactId>
    ...
    <jvmArgs>
      -javaagent:${settings.localRepository}/org/jacoco/org.jacoco.agent/${jacoco.version}/org.jacoco.agent-${jacoco.version}-runtime.jar=destfile=${jacoco.it.exec}
    </jvmArgs>
    ...
  </plugin>
  ```

* **Python integration tests while Jetty runs**

  ```xml
  <plugin>
    <artifactId>exec-maven-plugin</artifactId>
    <execution>
      <id>python-integration-tests</id>
      <phase>integration-test</phase>
      <goals><goal>exec</goal></goals>
      ...
    </execution>
  </plugin>
  ```

* **Generate the IT coverage report at verify**

  ```xml
  <execution>
    <id>report-it</id>
    <phase>verify</phase>
    <goals><goal>report</goal></goals>
    <configuration>
      <dataFile>${jacoco.it.exec}</dataFile>
      <outputDirectory>${project.reporting.outputDirectory}/jacoco-it</outputDirectory>
    </configuration>
  </execution>
  ```

---

# Practical tips / small improvements

* **Avoid stale IT data**
  Add `append=false` to the Jetty agent (shown above), or always run `mvn clean verify`.

* **Wire your `it.report.skip` switch**
  If you want to skip generating the IT report via a property:

  ```xml
  <execution>
    <id>report-it</id>
    <phase>verify</phase>
    <goals><goal>report</goal></goals>
    <configuration>
      <skip>${it.report.skip}</skip>
      <dataFile>${jacoco.it.exec}</dataFile>
      <outputDirectory>${project.reporting.outputDirectory}/jacoco-it</outputDirectory>
    </configuration>
  </execution>
  ```

* **Keep unit vs IT reports separate**
  You’ve already separated the IT report to `site/jacoco-it`. If you also need the unit report, add another `jacoco:report` (no `dataFile` override) writing to `site/jacoco`.

* **Multi-module note**
  This module-local setup reports coverage for **PlaygroundWeb** only. If you later want a **combined** view, use `jacoco:merge` (to combine `.exec` files) and/or `report-aggregate` from a parent `pom` with `packaging=pom` (JaCoCo 0.8.8+).

---

# TL;DR

* **Unit tests** → `prepare-agent` injects JaCoCo into Surefire JVM → `target/jacoco.exec`.
* **Integration tests** → Jetty starts with its own JaCoCo agent → `target/jacoco-it.exec`.
* **Report** → At `verify`, `jacoco:report` renders **only the IT** coverage to `target/site/jacoco-it`.
* **File behavior** → JaCoCo **appends by default**; prefer `mvn clean verify` or `append=false` to avoid mixing runs.
