---
audio: false
generated: true
image: false
lang: en
layout: post
title: JaCoCo for Liberty JVM Coverage
translated: false
type: note
---

You can do it—attach JaCoCo to the **Liberty JVM** that runs your EAR. The key is: JaCoCo must sit inside the same JVM as Liberty, not in your Python runner.

Here are reliable setups (pick one).

---

## 1) Simple & robust: write to file on JVM exit

**When to use:** you can stop the Liberty server after tests.

1. **Make the agent jar available** (one-time in your build)

```xml
<!-- copy jacoco agent into target/jacoco/jacocoagent.jar -->
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-dependency-plugin</artifactId>
  <version>3.6.1</version>
  <executions>
    <execution>
      <id>copy-jacoco-agent</id>
      <phase>prepare-package</phase>
      <goals><goal>copy</goal></goals>
      <configuration>
        <artifactItems>
          <artifactItem>
            <groupId>org.jacoco</groupId>
            <artifactId>org.jacoco.agent</artifactId>
            <version>0.8.12</version>
            <classifier>runtime</classifier>
            <destFileName>jacocoagent.jar</destFileName>
          </artifactItem>
        </artifactItems>
        <outputDirectory>${project.build.directory}/jacoco</outputDirectory>
      </configuration>
    </execution>
  </executions>
</plugin>
```

2. **Add a Liberty JVM option** (file: `wlp/usr/servers/<serverName>/jvm.options`)

```text
-javaagent:${server.config.dir}/jacoco/jacocoagent.jar=output=file,append=false,includes=com.myco.*,excludes=org.slf4j.*,destfile=${server.output.dir}/jacoco/jacoco-it.exec
```

* Put `jacocoagent.jar` into `wlp/usr/servers/<serverName>/jacoco/` (or any readable path).
* Adjust `includes`/`excludes` to your packages.

3. **Run flow**

* Start Liberty (`server start <serverName>`), deploy EAR.
* Run your Python `unittest` (they hit the endpoints).
* Stop Liberty (`server stop <serverName>`).
  → The agent writes `${server.output.dir}/jacoco/jacoco-it.exec`.

4. **Generate report**

* If your project is multi-module (EAR + EJB + WAR), use an aggregator pom and `report-aggregate`:

```xml
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.12</version>
  <executions>
    <execution>
      <id>report-it</id>
      <phase>verify</phase>
      <goals><goal>report-aggregate</goal></goals>
      <configuration>
        <dataFile>${env.SERVER_OUTPUT_DIR}/jacoco/jacoco-it.exec</dataFile>
        <includes>
          <include>com/myco/**</include>
        </includes>
      </configuration>
    </execution>
  </executions>
</plugin>
```

(Or use `jacococli`:)

```bash
java -jar jacococli.jar report /path/to/jacoco-it.exec \
  --classfiles module1/target/classes --classfiles module2/target/classes \
  --sourcefiles module1/src/main/java --sourcefiles module2/src/main/java \
  --html target/jacoco-it-report
```

---

## 2) Live dump without stopping Liberty (TCP server mode)

**When to use:** you want to keep Liberty running and pull coverage on demand.

1. `jvm.options`:

```text
-javaagent:${server.config.dir}/jacoco/jacocoagent.jar=output=tcpserver,address=*,port=6300,append=false,includes=com.myco.*
```

2. Run Liberty, execute Python tests, then **dump**:

```bash
# pulls coverage over TCP and writes a .exec locally
java -jar jacococli.jar dump --address 127.0.0.1 --port 6300 --destfile jacoco-it.exec --reset
```

Now generate the report as above.
Tip: `--reset` clears counters so you can take multiple snapshots during a long run.

---

## 3) Containers / CI (env-style)

* If you run Liberty in Docker/K8s, mount the agent and set:

  * `jvm.options` as above, **or**
  * `WLP_JAVA_OPTIONS` / `JAVA_TOOL_OPTIONS` env containing the same `-javaagent=...`.
* For clusters with multiple Liberty JVMs, give each a distinct TCP port or file path, then **merge**:

```bash
java -jar jacococli.jar merge node1.exec node2.exec --destfile merged.exec
```

---

## Notes & gotchas

* **EAR layout doesn’t matter** to JaCoCo; it instruments bytecode in memory. Reporting just needs the **original class files** from your modules (`target/classes`) and their sources for pretty HTML.
* Use **recent JaCoCo (0.8.12+)** for Java 17/21 compatibility (Liberty often runs on OpenJ9/HotSpot—both fine).
* Watch `includes/excludes` to avoid counting third-party libs.
* If the `.exec` is empty, you likely:

  * forgot to attach the agent,
  * filtered out your packages,
  * or pulled the dump before traffic hit the code.

---

If you share your EAR’s module layout (EJB/WAR modules and package roots), I can drop in an exact `report-aggregate` config and a tiny script to: start Liberty → run Python tests → fetch dump → build HTML report in one go.
