---
audio: false
date: 2025-09-07
generated: true
image: false
lang: en
layout: post
title: Fixing Forked Jetty Stop Issues
translated: false
type: note
---

You actually did most things right—the hang is almost always because the **stop goal can’t reach the forked Jetty** (wrong stopHost/port/key scope) or because **`run-forked` keeps Maven attached** unexpectedly. Two solid fixes below; pick one.

### Option A — Reliable pattern: `jetty:start` (daemon) + `jetty:stop`

This avoids `run-forked` entirely and is the most stable for IT lifecycles.

**What to change**

1. Pin the plugin version and use `start` with `daemon=true` in `pre-integration-test`.
2. Keep your Python ITs in `integration-test`.
3. Use `stop` in `post-integration-test`.
4. Provide the *same* `stopHost/stopPort/stopKey` in **both** executions.

```xml
<plugin>
  <groupId>org.eclipse.jetty</groupId>
  <artifactId>jetty-maven-plugin</artifactId>
  <version>9.4.54.v20240208</version>

  <configuration>
    <httpConnector>
      <port>8080</port>
      <host>127.0.0.1</host>
    </httpConnector>
  </configuration>

  <executions>
    <execution>
      <id>start-jetty</id>
      <phase>pre-integration-test</phase>
      <goals>
        <goal>start</goal>
      </goals>
      <configuration>
        <daemon>true</daemon>
        <stopHost>127.0.0.1</stopHost>
        <stopPort>8081</stopPort>
        <stopKey>stop</stopKey>
        <jvmArgs>
          -javaagent:${settings.localRepository}/org/jacoco/org.jacoco.agent/${jacoco.version}/org.jacoco.agent-${jacoco.version}-runtime.jar=destfile=${jacoco.it.exec},append=true
        </jvmArgs>
        <webApp>
          <contextPath>/</contextPath>
        </webApp>
      </configuration>
    </execution>

    <execution>
      <id>stop-jetty</id>
      <phase>post-integration-test</phase>
      <goals>
        <goal>stop</goal>
      </goals>
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

**Why this fixes the “stuck”**

* `daemon=true` makes `start` return control to Maven immediately, so your ITs can run.
* Matching `stopHost/stopPort/stopKey` guarantees the `stop` mojo reaches the same Jetty.
* No reliance on `run-forked`’s monitor thread behavior.

---

### Option B — Keep `run-forked`, but make stop actually work

If you prefer `run-forked`, the common pitfalls are:

* `stopHost` defaults can differ from how the child binds (IPv6 vs IPv4).
* `stopPort/stopKey` only set on the start execution but **not** mirrored on the stop execution.
* Child not exposing a stop handler if config is misplaced.

**Tighten config like this:**

```xml
<plugin>
  <groupId>org.eclipse.jetty</groupId>
  <artifactId>jetty-maven-plugin</artifactId>
  <version>9.4.54.v20240208</version>

  <executions>
    <execution>
      <id>start-jetty</id>
      <phase>pre-integration-test</phase>
      <goals>
        <goal>run-forked</goal>
      </goals>
      <configuration>
        <stopHost>127.0.0.1</stopHost>
        <stopPort>8081</stopPort>
        <stopKey>stop</stopKey>
        <stopWait>15</stopWait>

        <httpConnector>
          <host>127.0.0.1</host>
          <port>8080</port>
        </httpConnector>

        <jvmArgs>
          -javaagent:${settings.localRepository}/org/jacoco/org.jacoco.agent/${jacoco.version}/org.jacoco.agent-${jacoco.version}-runtime.jar=destfile=${jacoco.it.exec},append=true
        </jvmArgs>
        <webApp>
          <contextPath>/</contextPath>
        </webApp>
      </configuration>
    </execution>

    <execution>
      <id>stop-jetty</id>
      <phase>post-integration-test</phase>
      <goals>
        <goal>stop</goal>
      </goals>
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

**Extra guardrails**

* Add `-Djava.net.preferIPv4Stack=true` to the child `jvmArgs` if your macOS/Java picks IPv6 and the stop goal uses IPv4:

  ```
  <jvmArgs>
    -Djava.net.preferIPv4Stack=true
    -javaagent:...
  </jvmArgs>
  ```

* Ensure nothing else is on `8081`. If it is, change both start+stop to another free port.
* If your ITs crash or hang, `post-integration-test` may never run; in that case, add a `verify`-phase kill fallback (see below).

---

### Optional safety net — kill the child if `stop` fails

Add a tiny helper to forcibly kill the forked Jetty by PID written to a file:

1. In `run-forked`/`start` config:

```
<pidFile>${project.build.directory}/jetty.pid</pidFile>
```

2. After `post-integration-test`, add an `exec-maven-plugin` in `verify` that checks the pid file and nukes the process if it’s still alive.

---

### A couple of minor notes from your log

* `No Spring WebApplicationInitializer types detected` is normal if you use `web.xml` + DispatcherServlet; not related to the stop hang.
* Consider moving ITs to **maven-failsafe-plugin** (binds to `integration-test`/`verify`) and keep unit tests on surefire. Your current `exec-maven-plugin` approach works, but failsafe integrates better with the IT lifecycle.

---

If you want, paste your **full** Jetty plugin block + any `settings.xml` mirrors (for local repo path) and I’ll tailor the exact minimal diff for your repo.
