---
audio: false
generated: true
lang: en
layout: post
title: 'Getting Started with JShell: A Quick Guide'
translated: false
type: note
---

JShell is an interactive REPL (Read-Eval-Print Loop) tool included with the Java Development Kit (JDK) starting from JDK 9. It allows you to execute Java code snippets interactively without needing to write a full program. Below is a concise guide on how to use JShell:

### 1. **Starting JShell**
- **Ensure JDK is installed**: Make sure you have JDK 9 or later installed. You can check by running `java -version` in your terminal or command prompt.
- **Launch JShell**:
  - Open a terminal or command prompt.
  - Type `jshell` and press Enter.
  - You’ll see a prompt like `jshell>` indicating JShell is ready.

### 2. **Basic Usage**
- **Running Java Code**:
  - Type Java expressions, statements, or declarations directly at the prompt.
  - Example:
    ```java
    jshell> System.out.println("Hello, JShell!")
    Hello, JShell!
    ```
  - JShell evaluates the input and displays the result immediately.

- **Variables and Expressions**:
  - Declare variables or evaluate expressions:
    ```java
    jshell> int x = 10
    x ==> 10
    jshell> x * 2
    $2 ==> 20
    ```
  - JShell automatically assigns temporary names (e.g., `$2`) to expression results.

- **Defining Methods and Classes**:
  - You can define methods or classes:
    ```java
    jshell> void sayHello() { System.out.println("Hello!"); }
    |  created method sayHello()
    jshell> sayHello()
    Hello!
    ```
    ```java
    jshell> class Test { int x = 5; }
    |  created class Test
    jshell> Test t = new Test()
    t ==> Test@7c417213
    jshell> t.x
    $5 ==> 5
    ```

### 3. **Key Commands**
JShell provides built-in commands starting with `/`. Here are some essential ones:
- **List all code**: `/list` – Shows all snippets entered in the session.
  ```java
  jshell> /list
  ```
- **Edit code**: `/edit <id>` – Opens a GUI editor for the snippet with the given ID (from `/list`).
- **Save session**: `/save myfile.java` – Saves all snippets to a file.
- **Load file**: `/open myfile.java` – Loads and executes code from a file.
- **View variables**: `/vars` – Lists all declared variables.
  ```java
  jshell> /vars
  |    int x = 10
  ```
- **View methods**: `/methods` – Lists all defined methods.
- **Exit JShell**: `/exit` – Closes the JShell session.
- **Help**: `/help` – Displays all available commands.

### 4. **Importing Packages**
- JShell automatically imports common packages (e.g., `java.util`, `java.io`). To use others, import them manually:
  ```java
  jshell> import java.time.LocalDate
  jshell> LocalDate.now()
  $3 ==> 2025-06-27
  ```

### 5. **Editing and Correcting Code**
- **Modify existing code**:
  - Use `/list` to find the ID of a snippet.
  - Redefine it by typing a new version. JShell overwrites the old definition.
    ```java
    jshell> int x = 5
    x ==> 5
    jshell> int x = 10
    x ==> 10
    ```
- **Drop a snippet**: `/drop <id>` – Removes a specific snippet by its ID.

### 6. **Tab Completion**
- Press `Tab` to auto-complete class names, methods, or commands.
- Example:
  ```java
  jshell> System.out.pr<tab>
  ```
  This suggests `println`, `print`, etc.

### 7. **Running External Scripts**
- Load and run a Java file:
  ```java
  jshell> /open MyScript.java
  ```
- You can also start JShell with a script:
  ```bash
  jshell MyScript.java
  ```

### 8. **Customizing JShell**
- **Startup scripts**: Create a file (e.g., `startup.jsh`) with imports or common code, then load it with `/open startup.jsh` or set it as the default startup script:
  ```bash
  jshell --start startup.jsh
  ```
- **Feedback modes**: Adjust output verbosity with `/set feedback <mode>` (e.g., `normal`, `concise`, `verbose`).

### 9. **Tips**
- **Quick prototyping**: Use JShell to test small code snippets, experiment with APIs, or learn Java syntax.
- **Error handling**: JShell provides clear error messages and lets you correct mistakes on the fly.
- **Multi-line input**: For complex code, JShell supports multi-line editing. End a line with a backslash (`\`) to continue:
  ```java
  jshell> int sum(int a, int b) { \
      ...> return a + b; \
      ...> }
  ```

### 10. **Troubleshooting**
- **JShell not found**: Ensure the JDK `bin` directory is in your system’s PATH.
- **Slow startup**: On some systems, JShell may take a moment to initialize. Ensure your JDK is up to date.
- **Reset session**: Use `/reset` to clear all snippets and start fresh.

For more details, check the official JDK documentation or run `/help` in JShell. If you have specific tasks or code you want to try in JShell, let me know, and I can guide you further!
