---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix Double Maven Deploy
translated: false
type: note
---

Question:
Can we fix the double deployment by setting the execution id of the custom Maven deploy plugin to `default-deploy`?

Answer:

Yes — **this is actually a clean Maven-native solution.**
If you name your execution **`default-deploy`**, it **overrides the default lifecycle binding** of `maven-deploy-plugin`, preventing Maven from running it twice.

Maven lifecycle internally defines:

```text
phase: deploy
execution id: default-deploy
plugin: maven-deploy-plugin
```

So if you define the same execution id, Maven **replaces** the default one instead of adding another.

---

## Correct way

```xml
<plugin>
  <artifactId>maven-deploy-plugin</artifactId>
  <executions>
    <execution>
      <id>default-deploy</id>   <!-- override default -->
      <phase>deploy</phase>
      <goals>
        <goal>deploy</goal>
      </goals>
    </execution>
  </executions>
</plugin>
```

Now Maven runs **only once**.

---

## Why this works

Maven merges executions by:

```text
plugin + execution id
```

So:

Before:

```text
default lifecycle:
  maven-deploy-plugin (id=default-deploy)

your pom:
  maven-deploy-plugin (id=custom-deploy)
```

Result → TWO executions

After:

```text
default lifecycle:
  maven-deploy-plugin (id=default-deploy)

your pom:
  maven-deploy-plugin (id=default-deploy)
```

Result → ONE execution (overridden)

---

## This is actually better than skip=true

Because:

* keeps lifecycle clean
* avoids disabling plugin globally
* works well with parent POM
* more maintainable in multi-module builds

---

## Important caveat

This only works when you're overriding **maven-deploy-plugin** itself.

If you're using **another custom plugin** like:

```xml
com.company:custom-deploy-plugin
```

then naming it `default-deploy` **does NOT override** Maven default —
you will still get **two deploys**.

Because Maven matches by:

```text
groupId + artifactId + executionId
```

So different plugin ≠ override.

---

## Summary

✔ Same plugin + `id=default-deploy` → overrides default
✔ Different plugin + `id=default-deploy` → still double deploy
✔ safest: override or skip default plugin

So your idea is **correct and commonly used**.