---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast:free
title: JavaCC Source and Class Locations
translated: false
type: note
---

### JavaCC Overview

JavaCC (Java Compiler Compiler) is a tool that generates Java source code (e.g., parser classes) from grammar specification files (.jj files). It does **not** directly compile code into bytecode (.class files)—that's handled by a standard Java compiler like `javac`. If you're using JavaCC programmatically (e.g., in an IDE or runtime environment) to generate and compile dynamic code, the output locations depend on how you configure it. I'll break this down step by step, based on standard JavaCC behavior and common usage patterns.

### Where JavaCC Generates Source Files

- **Default Output Location**: JavaCC outputs generated `.java` files to the **current working directory** (or a subdirectory called "output" if not specified). You can override this with command-line options like `-OUTPUT_DIRECTORY=<path>` or programmatically via the `JavaCCOptions` class if invoking it in code.
- **Example Command-Line Usage**:

  ```
  javacc -OUTPUT_DIRECTORY=/path/to/generated MyGrammar.jj
  ```

  This would create `.java` files (e.g., `Token\` 0, `Parser`, `ParseException`) in `/path/to/generated`.
- **Programmatic Usage**: If you're calling JavaCC from within your Java application (e.g., using `org.javacc.JavaCC.main()` or similar APIs), you can set options to specify the output path. The source files are just plain `.java` files that need further compilation.

This aligns with official JavaCC documentation (e.g., from the legacy JavaCC project on SourceForge or Maven-based distributions), which states that generated classes are output to the specified directory as source code, not bytecode.

### Where Compiled Classes Are Stored If You Compile the Generated Code

JavaCC itself doesn't compile to `.class` files—you must do this manually or automate it in your code. Here's what happens next:

- **Manual Compilation**: Use `javac` on the generated `.java` files:

  ```
  javac -d /path/to/classes MyGeneratedParser.java
  ```

  - The `-d` flag specifies the output directory for `.class` files, often a `classes/` folder or your project's build target (e.g., `target/classes/` in Maven/Gradle).
  - Common locations: `bin/`, `build/classes/`, or `target/classes/` depending on your build system (e.g., Ant, Maven).

- **Dynamic Compilation in Code**: If you're using JavaCC at runtime to generate parsers for dynamic code (e.g., for script interpretation or on-the-fly parsing), you'd typically:
  1. Generate the `.java` files programmatically (e.g., writing to a temp directory like `System.getProperty("java.io.tmpdir")`).
  2. Compile them using the Java Compiler API (javax.tools.JavaCompiler) or a library like Janino.
     - Example: Set the compilation output to a custom directory, such as `new File("generated/classes")`.
     - The compiled `.class` files are stored in that directory. At runtime, use a custom ClassLoader to load them from there or in-memory buffers.
  - **JVM Default**: Without custom paths, classes might go to the default `target/classes` if using build tools, or to any directory you specify in the compilation task.

- **Common Dynamic Scenarios**:
  - **In-Memory Compilation**: Libraries like the Compiler API allow compiling without writing to disk, storing bytecode in memory via `ClassLoader.defineClass()`. No physical storage occurs.
  - **Temporary Storage**: If the generated code is compiled and persisted, it often goes to `/tmp/` on Unix-like systems or temporary folders. For production apps, use a dedicated `generated/` or `cache/` directory in your project's file system.
  - **Frameworks**: Tools like ANTLR (alternative to JavaCC) or custom runners might automate this, storing classes in RAM or a classpath folder (e.g., `CLASSPATH` entries).

### Key Considerations and Best Practices

- **Runtime Safety**: Dynamically compiling code carries risks (e.g., security issues). Ensure user-generated grammars are sandboxed.
- **Build Tools Integration**: If using Maven or Gradle, JavaCC plugins (e.g., `javacc-maven-plugin`) output to `target/generated-sources/javacc/` for sources and `target/classes/` for compiled classes, configurable in your `pom.xml` or `build.gradle`.
- **Debugging**: If compilation fails, check JavaCC's error output or logs. Generated files are typically stored where your app runs, not globally.
- **Evidence from Docs**: Per JavaCC's official guide (javacc.github.io or legacy docs), output is directory-based and post-compilation handling is user-managed. Real-world examples in GitHub repos (e.g., search for JavaCC usage) show custom output dirs like `src/main/generated/`.

If this doesn't match your setup (e.g., a specific framework or IDE), provide more details like your code snippet or environment, and I can refine the answer!
