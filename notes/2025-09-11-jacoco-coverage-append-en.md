---
audio: false
date: 2025-09-11
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: JaCoCo Coverage File and Append Mode
translated: false
type: note
---

That’s a subtle but important detail in how JaCoCo works.

### Behavior of `jacoco:prepare-agent`

* When Maven runs the **`prepare-agent`** goal, it doesn’t actually generate the coverage file immediately.
* Instead, it **configures the JVM** (usually via a `-javaagent:jacocoagent.jar` argument) so that coverage data will be collected while your tests or app run.
* The location of the `.exec` file is controlled by the property `jacoco.destFile` (default is `target/jacoco.exec`, but often customized, e.g. `target/jacoco-it.exec`).

### What happens if the file already exists?

* By default, **JaCoCo will overwrite the file** when the JVM starts with the agent.
* This means every run of `prepare-agent` → test execution will produce a *fresh* `.exec` file.
* It doesn’t append automatically — old data is lost unless you configure it otherwise.

### How to append instead

If you want multiple runs to accumulate into the same exec file, you must explicitly enable append mode:

```xml
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.12</version>
  <configuration>
    <destFile>${project.build.directory}/jacoco-it.exec</destFile>
    <append>true</append>   <!-- ✅ append coverage data -->
  </configuration>
</plugin>
```

With `<append>true>`, if the file exists, the new coverage data will be merged into it.

### So in short

* **Default:** Every run replaces the old `.exec`.
* **With `append=true`:** Coverage from multiple JVM runs (or multiple modules/tests) gets merged into the same file.

---

Do you want me to also explain how this interacts with **multi-module Maven builds** (where each module may try to write its own JaCoCo exec), since that’s often why people hit overwrite vs append issues?
