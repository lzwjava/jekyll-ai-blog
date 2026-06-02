---
audio: false
generated: true
lang: en
layout: post
title: Java Package Names Cannot Start with Numbers
translated: false
type: note
---

In Java, a package name **cannot start with a number**. According to the Java Naming Conventions and the Java Language Specification:

- Package names must be valid identifiers.
- A valid identifier in Java must start with a letter (A-Z or a-z), an underscore (`_`), or a dollar sign (`$`).
- Numbers (0-9) are allowed in identifiers, but only **after** the first character.

For example:

- Valid package names: `com.example`, `my_package`, `a123`
- Invalid package names: `123example`, `1package`

If you try to use a package name starting with a number, the Java compiler will throw a syntax error. To work around this, you can:

- Start the package name with a letter or underscore, e.g., `a123.example` or `_123.example`.
- Use a descriptive name that follows conventions, like `com.example.project123`.

This rule ensures consistency and compatibility across Java's naming system.
