---
audio: false
date: 2025-09-11
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Understanding Maven Lifecycles and JaCoCo
translated: false
type: note
---

Good question — this comes down to Maven’s *lifecycle phases* and how plugins bind to them.

### Lifecycle basics

Maven has three standard lifecycles: `clean`, `default` (sometimes called *build*), and `site`.
Inside the *default* lifecycle, the important phases go in order like this:

* `validate`
* `compile`
* `test`
* `package`
* `verify`
* `install`
* `deploy`

Each phase includes all the previous ones (if you run `mvn verify`, Maven executes everything from `validate` through `verify`). Running `mvn package` will stop after creating the artifact (JAR/WAR), and it will not run `verify`.

### Why JaCoCo is involved

The JaCoCo Maven plugin typically binds its **`prepare-agent`** goal to the `initialize` or `verify` phase depending on configuration.

* If it’s bound to `verify` (the common setup for coverage reports), then `mvn verify` will trigger it.
* `mvn package` does not go that far in the lifecycle, so the `verify` phase (and thus JaCoCo’s step) is skipped.

That’s why you see JaCoCo executed when you run `mvn verify` but not when you run `mvn package`.

### Practical takeaway

* Use **`mvn package`** when you just want the build artifact (fast, no extra checks).
* Use **`mvn verify`** when you want to run *integration tests, checks, coverage reports, or QA plugins* that are bound to later phases.

👉 If you want JaCoCo to always run even with `mvn package`, you can rebind the `prepare-agent` goal to an earlier phase like `test` or `package` in your `pom.xml`.

Would you like me to show you a concrete `pom.xml` snippet that makes JaCoCo’s `prepare-agent` run already at `test` instead of `verify`?
