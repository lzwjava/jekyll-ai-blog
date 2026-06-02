---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Java Programming Fundamentals Study Guide
translated: false
type: note
---

## National Higher Education Self-study Examination

This guide covers the fundamental concepts you need to master for the first part of your Java programming course.

---

## 1. Java Language Specifications, API, JDK, and IDE Tools

### **Java Language Specifications**
The Java Language Specification defines the syntax and semantics of Java. Key concepts to understand:

- **Platform Independence**: "Write Once, Run Anywhere" (WORA) - Java code compiles to bytecode that runs on any platform with a JVM (Java Virtual Machine)
- **Object-Oriented**: Everything in Java is organized around objects and classes
- **Strongly Typed**: Variables must be declared with specific data types
- **Automatic Memory Management**: Garbage collection handles memory deallocation

### **Java API (Application Programming Interface)**
The Java API is a large collection of pre-written classes organized into packages:

- **Core packages**: `java.lang` (automatically imported), `java.util`, `java.io`
- **Purpose**: Provides ready-to-use functionality (collections, file I/O, networking, etc.)
- **Documentation**: Available at Oracle's official Java documentation site
- **How to use**: Import packages using `import` statements

### **JDK (Java Development Kit)**
Essential components of the JDK:

- **javac**: Java compiler (converts .java files to .class bytecode files)
- **java**: Java runtime environment launcher
- **javadoc**: Documentation generator
- **jar**: Java archive tool
- **JRE included**: Java Runtime Environment for executing programs
- **Standard libraries**: Complete Java API implementation

**Installation and Setup**:
- Download from Oracle or use OpenJDK
- Set JAVA_HOME environment variable
- Add JDK bin directory to system PATH

### **IDE (Integrated Development Environment) Tools**
Popular IDEs for Java development:

1. **Eclipse** - Free, open-source, widely used in education
2. **IntelliJ IDEA** - Powerful features, both free and paid versions
3. **NetBeans** - Official Oracle-supported IDE
4. **VS Code** - Lightweight with Java extensions

**IDE Benefits**:
- Syntax highlighting and error detection
- Code completion and suggestions
- Integrated debugging tools
- Project management
- Version control integration

---

## 2. Creating, Compiling, and Running Java Programs

### **Basic Java Program Structure**

```java
// Every Java application needs a main class
public class HelloWorld {
    // main method - entry point of the program
    public static void main(String[] args) {
        // Your code goes here
        System.out.println("Hello, World!");
    }
}
```

### **Step-by-Step Process**

**Step 1: Creating a Java Program**
- Create a text file with `.java` extension
- Filename MUST match the public class name (case-sensitive)
- Example: `HelloWorld.java` for class `HelloWorld`

**Step 2: Compiling**
```bash
javac HelloWorld.java
```
- This creates `HelloWorld.class` (bytecode file)
- Compiler checks for syntax errors
- If errors exist, compilation fails with error messages

**Step 3: Running**
```bash
java HelloWorld
```
- Note: Use class name WITHOUT `.class` extension
- JVM loads the class and executes the main method

### **Command Line vs IDE Workflow**

**Command Line**:
- Open terminal/command prompt
- Navigate to the directory containing your .java file
- Use `javac` to compile, `java` to run
- Good for understanding the underlying process

**IDE Workflow**:
- Create a new Java project
- Create a new class
- Write code in the editor
- Click "Run" button (IDE handles compilation automatically)
- More convenient for larger projects

---

## 3. Programming Style Guidelines

Good programming style makes code readable and maintainable. Follow these conventions:

### **Naming Conventions**

- **Classes**: PascalCase (capitalize first letter of each word)
  - Examples: `StudentRecord`, `BankAccount`, `HelloWorld`

- **Methods and Variables**: camelCase (first word lowercase, capitalize subsequent words)
  - Examples: `calculateTotal()`, `firstName`, `studentAge`

- **Constants**: ALL_CAPS with underscores
  - Examples: `MAX_SIZE`, `PI`, `DEFAULT_VALUE`

- **Packages**: all lowercase, often reverse domain name
  - Examples: `com.company.project`, `java.util`

### **Code Formatting**

**Indentation**:
```java
public class Example {
    public static void main(String[] args) {
        if (condition) {
            // Indent 4 spaces or 1 tab
            statement;
        }
    }
}
```

**Braces**:
- Opening brace on same line (Java convention)
- Closing brace on its own line, aligned with statement

**Spacing**:
```java
// Good spacing
int sum = a + b;
if (x > 0) {

// Poor spacing
int sum=a+b;
if(x>0){
```

### **Comments**

**Single-line comments**:
```java
// This is a single-line comment
int age = 20; // Comment after code
```

**Multi-line comments**:
```java
/*
 * This is a multi-line comment
 * Used for longer explanations
 */
```

**Javadoc comments** (for documentation):
```java
/**
 * Calculates the sum of two numbers.
 * @param a the first number
 * @param b the second number
 * @return the sum of a and b
 */
public int add(int a, int b) {
    return a + b;
}
```

### **Best Practices**

1. **Meaningful names**: Use descriptive variable and method names
   - Good: `studentCount`, `calculateAverage()`
   - Bad: `x`, `doStuff()`

2. **One statement per line**: Avoid cramming multiple statements on one line

3. **Consistent style**: Follow the same conventions throughout your code

4. **White space**: Use blank lines to separate logical sections

5. **Keep methods short**: Each method should do one thing well

---

## 4. Common Programming Errors and Debugging Basics

### **Types of Errors**

#### **A. Syntax Errors (Compile-Time Errors)**
These prevent compilation and must be fixed before running:

**Common syntax errors**:
```java
// Missing semicolon
int x = 5  // ERROR: missing ;

// Mismatched braces
public class Test {
    public static void main(String[] args) {
        System.out.println("Hello");
    // Missing closing brace }

// Case sensitivity
String name = "John";
system.out.println(name); // ERROR: should be 'System'

// Filename mismatch
// File: Test.java
public class MyClass { // ERROR: class name must match filename
```

#### **B. Runtime Errors**
Program compiles but crashes during execution:

```java
// Division by zero
int result = 10 / 0; // ArithmeticException

// Null pointer
String str = null;
int length = str.length(); // NullPointerException

// Array index out of bounds
int[] arr = {1, 2, 3};
int value = arr[5]; // ArrayIndexOutOfBoundsException
```

#### **C. Logic Errors**
Program runs but produces incorrect results:

```java
// Wrong operator
int average = (a + b) * 2; // Should be / not *

// Off-by-one error
for (int i = 0; i <= arr.length; i++) { // Should be i < arr.length

// Wrong condition
if (age > 18) { // Should be >= for "18 and older"
```

### **Debugging Techniques**

#### **1. Read Error Messages Carefully**
```
HelloWorld.java:5: error: ';' expected
        int x = 5
                 ^
1 error
```
- **Line number**: Shows where error occurred (line 5)
- **Error type**: Tells you what's wrong (missing semicolon)
- **Pointer**: Shows exact location

#### **2. Print Statement Debugging**
```java
public static int calculateSum(int a, int b) {
    System.out.println("Debug: a = " + a + ", b = " + b);
    int sum = a + b;
    System.out.println("Debug: sum = " + sum);
    return sum;
}
```

#### **3. Use IDE Debugger**
- **Breakpoints**: Pause execution at specific lines
- **Step Over**: Execute current line and move to next
- **Step Into**: Enter method calls to see internal execution
- **Watch Variables**: Monitor variable values in real-time
- **Call Stack**: See the sequence of method calls

#### **4. Divide and Conquer**
- Comment out sections of code to isolate the problem
- Test small parts independently
- Gradually add code back until error reappears

#### **5. Rubber Duck Debugging**
- Explain your code line-by-line to someone (or something)
- Often helps you spot the problem yourself

### **Common Beginner Mistakes**

1. **Forgetting to compile after changes**
   - Always recompile before running

2. **Class name doesn't match filename**
   - `public class Student` must be in `Student.java`

3. **Missing main method signature**
   - Must be exactly: `public static void main(String[] args)`

4. **Forgetting to import packages**
   ```java
   import java.util.Scanner; // Don't forget this!
   ```

5. **Incorrect capitalization**
   - `String` not `string`, `System` not `system`

6. **Using = instead of == in conditions**
   ```java
   if (x = 5) { // ERROR: assignment, not comparison
   if (x == 5) { // CORRECT
   ```

---

## Exam Preparation Tips

### **What to Study**

1. **Memorize**:
   - Main method signature
   - Basic program structure
   - Naming conventions
   - Common error types

2. **Understand**:
   - Difference between JDK, JRE, and JVM
   - Compilation vs execution process
   - Why Java is platform-independent

3. **Practice**:
   - Write simple programs by hand
   - Identify errors in code samples
   - Trace program execution

### **Common Exam Question Types**

1. **Multiple choice**: "What is the correct main method signature?"
2. **Error identification**: "Find the syntax errors in this code"
3. **Code tracing**: "What is the output of this program?"
4. **Short answer**: "Explain the difference between JDK and JRE"
5. **Code writing**: "Write a program that prints 'Hello, China!'"

### **Practice Exercise**

Try to identify and fix all errors in this code:

```java
public class test {
    Public Static Void Main(string[] args) {
        int x = 5
        int y = 10;
        System.Out.Println(x + y)
    }
}
```

**Answers**:
- Class name should be `Test` (capital T) and match filename
- `Public` → `public`, `Static` → `static`, `Void` → `void`
- `string` → `String`
- Missing semicolon after `int x = 5`
- `System.Out` → `System.out`
- Missing semicolon after println statement

---

## Summary Checklist

Before the exam, make sure you can:

- ☐ Explain what JDK, JRE, JVM, and API are
- ☐ Write a basic Java program with proper structure
- ☐ Compile and run a program using command line
- ☐ Follow Java naming conventions
- ☐ Identify syntax, runtime, and logic errors
- ☐ Use basic debugging techniques
- ☐ Write properly formatted and commented code

Good luck with your examination! 加油！
