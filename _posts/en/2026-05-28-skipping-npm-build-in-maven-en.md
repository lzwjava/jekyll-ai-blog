---
audio: false
generated: true
image: false
lang: en
layout: post
title: Skipping npm build in Maven
translated: false
type: note
---

**Question:** Can we use `exec.skip` to skip the npm build in a Maven exec plugin configuration for a Java + Angular full-stack app?

**Answer:**

Yes — but the property name depends on which Maven plugin is running your npm build.

## Common setups

### 1. `frontend-maven-plugin` (most common for Angular)

This is `com.github.eirslett:frontend-maven-plugin`. It doesn't use `exec.skip`. It has its own skip property:

```xml
<plugin>
  <groupId>com.github.eirslett</groupId>
  <artifactId>frontend-maven-plugin</artifactId>
  <configuration>
    <skip>${skipFrontend}</skip>
  </configuration>
</plugin>
```

Then skip at build time:

```bash
mvn install -DskipFrontend=true
```

Or hardcode it in a profile:

```xml
<profiles>
  <profile>
    <id>skip-ui</id>
    <properties>
      <skipFrontend>true</skipFrontend>
    </properties>
  </profile>
</profiles>
```

```bash
mvn install -P skip-ui
```

### 2. `maven-exec-plugin` (if npm is called via `exec:exec` or `exec:java`)

Here `exec.skip` **does work**:

```bash
mvn install -Dexec.skip=true
```

This skips all `exec-maven-plugin` executions. Check your `pom.xml` — if you see:

```xml
<groupId>org.codehaus.mojo</groupId>
<artifactId>exec-maven-plugin</artifactId>
```

...then `-Dexec.skip=true` is the right flag.

### 3. Per-execution skip with `<skip>` + custom property

If you want fine-grained control (skip npm but not other exec goals):

```xml
<execution>
  <id>npm-build</id>
  <goals><goal>exec</goal></goals>
  <configuration>
    <executable>npm</executable>
    <arguments><argument>run build</argument></arguments>
    <skip>${skipNpmBuild}</skip>
  </configuration>
</execution>
```

```bash
mvn install -DskipNpmBuild=true
```

## Quick diagnosis

```bash
grep -r "exec-maven-plugin\|frontend-maven-plugin" pom.xml */pom.xml
```

That tells you which plugin to target. Then:

| Plugin | Skip flag |
|---|---|
| `frontend-maven-plugin` | `-DskipFrontend=true` (or whatever `<skip>${...}</skip>` is bound to) |
| `exec-maven-plugin` | `-Dexec.skip=true` |
| Custom property | `-DskipNpmBuild=true` |

The `exec.skip` flag is real and works, but only if the npm step is wired through `exec-maven-plugin` — not `frontend-maven-plugin`.
