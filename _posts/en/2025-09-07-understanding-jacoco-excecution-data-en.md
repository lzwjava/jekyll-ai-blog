---
audio: false
date: 2025-09-07
generated: true
image: false
lang: en
layout: post
title: Understanding JaCoCo Execution Data Files
translated: false
type: note
---

Here’s a practical, everything-you-need rundown.

# What is `jacoco-it.exec`?

* It’s a **JaCoCo execution data file** produced during **integration tests**.
* The “`-it`” is just a **convention** (from `jacoco-maven-plugin`’s *report-integration* goal and the Failsafe phase). Unit tests often dump to `jacoco.exec`, while integration tests dump to `jacoco-it.exec`.
* You can have many `.exec` files (per module, per phase, per run) and **merge** them later to produce a single coverage report.

Typical Maven setup:

```xml
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.12</version>
  <executions>
    <!-- for unit tests -->
    <execution>
      <id>prepare-agent</id>
      <goals><goal>prepare-agent</goal></goals>
    </execution>
    <!-- for integration tests -->
    <execution>
      <id>prepare-agent-integration</id>
      <goals><goal>prepare-agent-integration</goal></goals>
    </execution>
    <execution>
      <id>report</id>
      <phase>verify</phase>
      <goals><goal>report</goal></goals>
    </execution>
    <execution>
      <id>report-it</id>
      <phase>verify</phase>
      <goals><goal>report-integration</goal></goals>
    </execution>
  </executions>
</plugin>
```

This usually writes `target/jacoco.exec` (unit) and `target/jacoco-it.exec` (integration).

# What’s inside an `.exec` file?

* **Only probe hits**, keyed by class.
* Concretely: for each loaded class, JaCoCo calculates an **ID** (based on the bytecode) and stores a **boolean array of probes** (which instructions/branches were executed).
* It also stores a **session id** and timestamps.
* **It does *not* contain class bytecode, method names, line numbers, or source**. That structural info comes later from your **class files** and **sources** when you run `jacoco:report` to render HTML/XML.

Implications:

* If your classes change after producing the `.exec`, the file may no longer match (IDs won’t line up). Always generate the report against **the exact same build** of class files that produced the exec.

# Does it contain class structure information?

* **No.** No methods, no line numbers, no source.
* It’s a compact, binary **hit-map** per class. The reporting step reads your **compiled classes** (and optionally sources) to map those hits to packages, classes, methods, lines, and branches.

# Will it be updated when you attach via `-javaagent`?

Short answer: **Yes**, with details:

* When you start your JVM with the agent, it instruments classes **on the fly** and records probe hits **in memory**.
* The agent **writes** to `destfile`:

  * **On JVM exit** (for `output=file`, the default), or
  * When you explicitly **dump** (TCP/JMX/API), or
  * When `append=true` is set, it will **append/merge** to an existing file instead of overwriting.

Common agent options:

```bash
-javaagent:/path/to/org.jacoco.agent.jar=\
destfile=/path/to/jacoco-it.exec,\
append=true,\
output=file
```

Other useful modes:

* `output=tcpserver` (listen on a port; you can connect and trigger a dump)
* `output=tcpclient` (push to a server)
* `jmx=true` (expose a JMX MBean to dump/reset)
* Programmatic: `org.jacoco.agent.rt.RT.getAgent().dump(/*reset*/ true|false)`

Notes on “updated”:

* With `output=file` **and** `append=true`, **each dump** merges probe arrays into the existing file (logical OR of hits).
* Without `append=true`, the next write **overwrites** the file at dump/exit.
* If you have **multiple JVMs** (microservices, forked tests), point each to **different files**, or use TCP/JMX to collect centrally, then merge.

# Typical workflows

**Integration test phase (Failsafe):**

* Maven attaches the agent to the integration-test JVM(s) with `destfile=target/jacoco-it.exec`.
* At the end, run `jacoco:report-integration` which reads:

  * `target/jacoco-it.exec` (hits)
  * `target/classes` (structure)
  * `src/main/java` (optional for source lines)
* Output: HTML/XML/CSV coverage for *integration tests only*.

**Merging multiple runs:**

```bash
# via Maven
mvn jacoco:merge -Djacoco.destFile=target/merged.exec \
  -Djacoco.dataFileList="target/jacoco.exec,target/jacoco-it.exec,other.exec"
# then
mvn jacoco:report -Djacoco.dataFile=target/merged.exec
```

# Practical gotchas and tips

* **Match builds**: generate reports against the **same compiled classes** that produced the `.exec`.
* **Parallel forks**: when running tests in parallel or multiple JVMs, avoid many writers to the same file unless `append=true` and you’re okay with concurrent appends (safer is one file per JVM and then merge).
* **Long-running services**: enable **TCP/JMX** or call the runtime API to **dump periodically**; don’t wait for process exit.
* **Classloader isolation**: some app servers load the same class twice; JaCoCo de-duplicates by class id, but be aware in complex containers.
* **Offline instrumentation** exists, but the **javaagent** approach is usually simpler and more robust.

---

## Direct answers to your questions

* **“What is `jacoco-it.exec`?”**
  The execution data file (probe hits) captured during **integration tests**. It’s just a naming convention; functionally it’s the same format as `jacoco.exec`.

* **“Does it contain class structure information?”**
  **No.** It only stores per-class **probe hit arrays** and session metadata. Class/method/line info comes from your compiled classes/sources during the reporting step.

* **“Will it be updated when attached via `-javaagent`?”**
  **Yes.** With `output=file`, the agent writes on **JVM exit** or **on demand** (TCP/JMX/API). With `append=true`, it **merges** with any existing file; without it, it **overwrites**. For multi-JVM runs, use separate files or a remote dump and **merge** later.
