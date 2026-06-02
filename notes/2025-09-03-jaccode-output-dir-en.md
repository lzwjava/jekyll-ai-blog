---
audio: false
generated: true
image: false
lang: en
layout: post
title: Configuring JaCoCo Agent Output Directory
translated: false
type: note
---

Yes — exactly 👍.

By default, if you write

```bash
-javaagent:/path/to/jacocoagent.jar=destfile=jacoco.exec,output=file
```

then `jacoco.exec` is created in the **current working directory** of the JVM process (often the server root or wherever you launched Liberty from).

If you want to control where it goes, you give it an **absolute or relative path**, for example:

```bash
-javaagent:/path/to/jacocoagent.jar=destfile=/opt/coverage-data/jacoco.exec,output=file
```

or

```bash
-javaagent:/path/to/jacocoagent.jar=destfile=target/jacoco.exec,output=file
```

(where `target/` is relative to the startup directory).

So yes, if you want to guarantee where the `.exec` ends up, use the full path.

👉 Tip: It’s common in Maven/Gradle projects to point it into `target/` (Maven) or `build/` (Gradle), so later the reporting plugins can pick it up automatically.

Do you want me to show you a Liberty `jvm.options` example with the full path configured?
