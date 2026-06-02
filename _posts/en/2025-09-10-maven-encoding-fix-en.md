---
audio: false
date: 2025-09-10
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Fixing Maven Platform Encoding Warnings
translated: false
type: note
---

That Maven warning means your project build process depends on the **default platform encoding** (e.g., GBK on a Chinese Windows system). If other developers or CI servers use a different encoding (like UTF-8 on Linux), text resources (Java source, properties, XML, etc.) may be misread or miscompiled.

Here’s how you can fix it:

---

### 1. Set the Source Encoding in `pom.xml`

In your project’s `<properties>` section, explicitly declare the encoding:

```xml
<properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
    <maven.compiler.encoding>UTF-8</maven.compiler.encoding>
</properties>
```

This ensures Maven compiles sources and generates reports consistently in UTF-8, regardless of your OS default.

---

### 2. Configure the Compiler Plugin (if not already)

Some older Maven setups require encoding under the compiler plugin:

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <version>3.11.0</version>
            <configuration>
                <source>1.8</source>
                <target>1.8</target>
                <encoding>UTF-8</encoding>
            </configuration>
        </plugin>
    </plugins>
</build>
```

---

### 3. Check File Encodings

* Make sure your `.java`, `.properties`, `.yml`, etc. are saved in UTF-8, not GBK.
* In IntelliJ IDEA or VS Code, set **File Encoding = UTF-8** in project settings.
* For Git, you can enforce consistent encoding with `.gitattributes` if needed.

---

### 4. Run Maven with Explicit Encoding (Optional)

You can also override encoding when running Maven:

```bash
mvn clean install -Dfile.encoding=UTF-8
```

But best practice is to fix it inside `pom.xml`, so it’s consistent for everyone.

---

✅ After these changes, the “platform dependent encoding GBK” warning should disappear, and your Spring + Maven project will be encoding-safe across machines.

Do you want me to also show you how to **convert existing GBK source files to UTF-8** safely (so your repo is clean and consistent)?
