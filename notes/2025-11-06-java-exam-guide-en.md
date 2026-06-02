---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Java Programming Exam Study Guide
translated: false
type: note
---

Here’s a practical, exam-oriented guide for the **first part of “08553 Introduction to Programming—Java”**, based on the *National Higher Education Self-study Examination in China* syllabus. It focuses on concepts, examples, and key points that beginners must master.

---

## 1. Java Language Overview

### 1.1 Java Characteristics

* **Platform Independence:** Java code compiles into *bytecode*, which runs on any device with a *Java Virtual Machine (JVM)* — “Write once, run anywhere.”
* **Object-Oriented:** Supports *encapsulation, inheritance,* and *polymorphism.*
* **Secure and Robust:** Automatic memory management (garbage collection) and strong type checking reduce errors.
* **Multithreading:** Supports concurrent execution of multiple tasks.
* **Rich Standard Library (API):** Includes ready-made classes for math, strings, files, networking, etc.

### 1.2 Java Versions and Components

* **JDK (Java Development Kit):** For developers — includes compiler (`javac`), JVM, and development tools.
* **JRE (Java Runtime Environment):** For end-users — includes JVM + core libraries.
* **API (Application Programming Interface):** Java’s built-in class libraries, such as `java.lang`, `java.util`, `java.io`, etc.

---

## 2. Java Development Tools (IDE and CLI)

### 2.1 Common IDEs

For the exam, you just need to know their purpose:

* **Eclipse, IntelliJ IDEA, NetBeans:** Used to write, compile, and run Java code easily.

### 2.2 Command-Line Workflow

Typical compilation and execution steps:

1. **Write** your code in a `.java` file, e.g. `Hello.java`
2. **Compile** it:

   ```bash
   javac Hello.java
   ```

   → Produces `Hello.class` (bytecode file)
3. **Run** it:

   ```bash
   java Hello
   ```

   (No `.class` extension when running)

### 2.3 Simple Example

```java
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello, Java!");
    }
}
```

---

## 3. Programming Style Guidelines

### 3.1 Naming Conventions

* **Classes:** `CamelCase`, first letter capitalized → `StudentInfo`
* **Variables & Methods:** `camelCase`, start lowercase → `studentName`, `calculateScore()`
* **Constants:** All uppercase with underscores → `MAX_SIZE`

### 3.2 Indentation and Comments

* Use **consistent indentation** (4 spaces typical).
* Write clear **comments**:

  ```java
  // This is a single-line comment
  /* This is a multi-line comment */
  ```

### 3.3 Code Structure

Follow logical grouping and readability:

* Each file contains **one public class** with the **same name** as the file.
* Keep lines short and meaningful; one statement per line.

---

## 4. Common Programming Errors and Debugging Basics

### 4.1 Syntax Errors

Detected by the compiler:

* Missing semicolon `;`
* Mismatched braces `{ }`
* Wrong capitalization (Java is **case-sensitive**)

  ```java
  System.out.println("Hi"); // correct
  system.out.println("Hi"); // error
  ```

### 4.2 Runtime Errors

Occur while running the program:

* Dividing by zero
* Array index out of bounds
* Null pointer exceptions

### 4.3 Logic Errors

Program runs but gives incorrect output.
→ Use **print statements** or **debugger tools** in IDEs to trace variable values step-by-step.

---

## 5. Key Points for the Exam

* Understand **JDK, JRE, JVM** roles and differences.
* Know how to **compile and run** Java from both IDE and command line.
* Remember **basic syntax rules** and **style standards**.
* Be able to **identify common errors** and explain their causes.
* Practice writing small programs that:

  * Print messages
  * Use variables and expressions
  * Follow correct structure and naming

---

## 6. Sample Exam-style Question

**Example 1:**

> Which of the following statements about Java is *incorrect*?
> A. Java supports platform independence through bytecode
> B. Java programs must always be compiled into native machine code
> C. The JVM executes compiled bytecode
> D. Java programs can be run on any system with a JVM installed

**Answer:** B

**Example 2:**

> What command compiles a Java source file named `Test.java`?
> A. java Test
> B. javac Test.java
> C. run Test
> D. compile Test

**Answer:** B

---

Would you like me to continue with **Part II: Basic Syntax and Data Types** next (the next major section in this course)? It will follow the same clear, exam-oriented structure.
