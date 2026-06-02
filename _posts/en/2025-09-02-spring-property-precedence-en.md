---
audio: false
generated: true
image: false
lang: en
layout: post
title: Spring Property Precedence Rules Explained
translated: false
type: note
---

In Spring, when you have **duplicate property keys** across your configuration sources (e.g., `application.properties`, `application.yml`, environment variables, command-line arguments, etc.), the **last one with the highest precedence wins**.

Here’s how it works in detail:

### 1. Property Source Ordering

Spring Boot applies a well-defined **property source order**. For example:

* Command line arguments
* `application.properties` / `application.yml` (profile-specific ones first, then default)
* Environment variables
* System properties
* Defaults in code (`@Value("${...:default}")`)

If the same property key appears in multiple sources, Spring picks the one from the **highest-priority source**.

### 2. Inside the Same File

If you have the same property key **repeated in a single file** (like `application.properties`), Spring uses the **last declared occurrence**.
Example (`application.properties`):

```properties
server.port=8080
server.port=9090
```

Here, `server.port=9090` takes effect.

### 3. Across Multiple Files

If you define the same property in `application.properties` and `application-dev.properties`, and you activate the `dev` profile, then the value from `application-dev.properties` will override the default one.

### 4. With `@PropertySource`

If you load multiple property files via `@PropertySource`, the order of declaration matters. The later one can override earlier values unless you mark it with `ignoreResourceNotFound` or explicitly control precedence.

---

✅ **Summary:**

* Spring resolves properties by **precedence of sources**.
* Within the **same file**, the **last key definition** wins.
* Across files/profiles, the **active profile’s or later-loaded file’s property** overrides the earlier ones.

Do you want me to also show you the **exact Spring Boot property precedence hierarchy (from highest to lowest)**? That gives a very clear picture of where overrides happen.
