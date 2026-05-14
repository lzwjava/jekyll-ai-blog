---
audio: false
generated: true
image: false
lang: en
layout: post
title: Skipping Unchanged Maven Modules
translated: false
type: note
---

Question: How can I skip or opt out of a Maven module during a build to speed up the build process, especially if the module hasn’t changed? Suppose I have a project like PAUWeb with Angular frontend, Java 8 backend, and 10 modules, and one module contributes 2 minutes to a 6-minute build.

Answer:

Yes, skipping modules that haven’t changed can speed up your Maven build significantly. There are several strategies you can use in Maven to “opt out” or skip certain modules:

---

### 1. **Use the `-pl` (projects) and `-am` (also make) flags**

Maven allows you to build only specific modules with `-pl` (projects list). For example:

```bash
# Build only moduleA and moduleB
mvn clean install -pl moduleA,moduleB
```

* `-pl` specifies which modules to include.
* `-am` (also make) tells Maven to also build dependencies of the specified modules.

**Example skipping a module:**

If `moduleX` takes 2 minutes and hasn’t changed:

```bash
mvn clean install -pl !moduleX
```

* The `!` excludes the module.

---

### 2. **Use `maven.test.skip` or `skipTests`**

If your build is slow because of tests in a module, you can skip tests:

```bash
mvn install -DskipTests
```

* Saves time if the module code hasn’t changed but tests take long.

---

### 3. **Use `-am` with selective builds**

If modules are interdependent, building only changed modules with `-pl` + `-am` ensures dependencies are also built:

```bash
mvn install -pl moduleA -am
```

This builds `moduleA` and any modules it depends on, skipping unrelated modules.

---

### 4. **Incremental Builds / `mvn reactor`**

Maven doesn’t automatically skip unchanged modules by default. To handle that:

* Use **`takari-lifecycle-plugin`** or **`maven-incremental-build`** tools.
* Some CI/CD systems (like Jenkins) can track which modules changed using Git and trigger Maven builds only for those modules.

Example with incremental plugin:

```xml
<plugin>
  <groupId>io.takari.maven.plugins</groupId>
  <artifactId>takari-lifecycle-plugin</artifactId>
  <version>1.13.6</version>
</plugin>
```

This allows building only changed modules.

---

### 5. **Angular frontend optimization**

If Angular build is part of the module:

* Consider **building Angular separately** and only trigger Maven when Java code changes.
* Use `ng build --watch` or incremental builds to avoid rebuilding every time.

---

### 6. **Profile-based skipping**

You can define Maven profiles to skip certain modules:

```xml
<profiles>
  <profile>
    <id>skip-moduleX</id>
    <modules>
      <module>module1</module>
      <module>module2</module>
      <!-- do not include moduleX -->
    </modules>
  </profile>
</profiles>
```

Then:

```bash
mvn clean install -Pskip-moduleX
```

---

**Recommendation for your case:**

* Identify slow module (`moduleX`) → check if code changed.
* Use:

```bash
mvn install -pl !moduleX
```

* Combine with `-DskipTests` if tests are slow.
* For Angular parts, consider building separately to avoid full rebuild.

This can reduce your build from 6 minutes to ~4 minutes if `moduleX` hasn’t changed.

---

References:

* [Maven Reactor Options (`-pl` and `-am`)](https://maven.apache.org/ref/3.6.3/maven-embedder/cli.html)
* [Skipping Tests in Maven](https://maven.apache.org/surefire/maven-surefire-plugin/examples/skipping-tests.html)
* [Maven Multi-module Build Tips](https://www.baeldung.com/maven-multi-module-build)

---

If you want, I can show a **ready-to-use Maven command** for PAUWeb that skips unchanged modules automatically based on Git diffs. That can save you several minutes per build. Do you want me to do that?