---
audio: false
generated: true
image: false
lang: en
layout: post
title: Comparing Liberty Agent and JaCoCo Agent
translated: false
type: note
---

In WebSphere Liberty (WLP), the `ws-javaagent.jar` is IBM’s own Java instrumentation agent. It’s used mainly for runtime monitoring, diagnostics, and integration with tools like Application Performance Management (APM), Health Center, or Liberty’s own monitoring capabilities. When you enable it, Liberty can collect profiling, garbage collection, thread, and other JVM-level metrics automatically.

JaCoCo’s `jacocoagent.jar`, on the other hand, is specifically a **code coverage agent**. Its purpose is to instrument bytecode at runtime so that test runs or application executions produce coverage data (e.g., which classes, methods, and branches were executed).

So the distinction is:

* **`ws-javaagent.jar`** → general monitoring, profiling, diagnostics for Liberty and IBM tooling.
* **`jacocoagent.jar`** → test/code coverage reporting, independent of Liberty.

You shouldn’t replace JaCoCo’s agent with Liberty’s one. If your goal is **test coverage reporting** (for CI pipelines, SonarQube, Maven/Gradle reports, etc.), you must keep using the **JaCoCo agent**. The Liberty agent won’t generate JaCoCo `.exec` coverage files.

But you *can* run both at the same time if needed — Java supports multiple `-javaagent` arguments. For example:

```bash
-javaagent:/path/to/ws-javaagent.jar
-javaagent:/path/to/jacocoagent.jar=destfile=jacoco.exec,output=file
```

👉 In short:
Use **`jacocoagent.jar`** for coverage.
Use **`ws-javaagent.jar`** if you need Liberty diagnostics/profiling.
They serve different purposes and are not interchangeable.

Do you want me to also show you how to configure them together in a Liberty server JVM options file?
