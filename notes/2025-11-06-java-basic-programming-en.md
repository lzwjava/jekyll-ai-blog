---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Java Basic Programming Guide
translated: false
type: note
---

Here’s a focused guide for **Part II: Basic Programming** of *08553 Introduction to Programming—Java*, tailored for the **National Higher Education Self-study Examination (自考)**. This section trains you to write small, correct Java programs and understand how Java handles data and expressions.

---

## 1. Reading Input from the Console

### 1.1 Using `Scanner`

Java reads input with the `Scanner` class in `java.util`.

```java
import java.util.Scanner;

public class InputExample {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter your name: ");
        String name = sc.nextLine();
        System.out.print("Enter your age: ");
        int age = sc.nextInt();
        System.out.println("Hello " + name + ", you are " + age + " years old.");
        sc.close();
    }
}
```

**Key points:**

* Always `import java.util.Scanner;`
* Use `nextInt()`, `nextDouble()`, `nextLine()` based on data type.
* Close the `Scanner` to free resources.
* Be careful: `nextLine()` reads the rest of a line, so mixing it with `nextInt()` may cause skipped input.

---

## 2. Identifiers, Variables, Expressions, Assignments, and Constants

### 2.1 Identifiers

Names you give to variables, methods, or classes.
**Rules:**

* Must start with a letter, `_`, or `$`.
* Cannot start with a number.
* Case-sensitive (`score` ≠ `Score`).
* Cannot be a keyword (`int`, `class`, `if`, etc.).

**Examples:**
`studentName`, `_total`, `$price`

### 2.2 Variables

A variable holds data of a certain **type**.
Declaration examples:

```java
int age = 20;
double price = 12.5;
char grade = 'A';
boolean passed = true;
```

### 2.3 Assignment Statements

Assign a value using `=` (right → left):

```java
x = 5;
y = x + 2;
```

### 2.4 Constants

Declared with `final`, cannot change later:

```java
final double PI = 3.14159;
```

Use uppercase names for constants.

---

## 3. Numeric Data Types and Operations

### 3.1 Common Numeric Types

* `byte` (8-bit integer)
* `short` (16-bit)
* `int` (32-bit, most common)
* `long` (64-bit)
* `float` (32-bit decimal)
* `double` (64-bit decimal, more precise)

**Example:**

```java
int count = 5;
double price = 19.99;
```

### 3.2 Basic Arithmetic Operators

`+`, `-`, `*`, `/`, `%`

Examples:

```java
int a = 10, b = 3;
System.out.println(a / b);  // 3 (integer division)
System.out.println(a % b);  // 1
System.out.println((double)a / b); // 3.3333 (type conversion)
```

---

## 4. Type Conversion (Casting)

### 4.1 Automatic Conversion (Widening)

Small → large type automatically:
`int` → `long` → `float` → `double`

Example:

```java
int i = 10;
double d = i;  // automatic conversion
```

### 4.2 Manual Conversion (Casting)

Explicitly convert larger → smaller type:

```java
double d = 9.7;
int i = (int) d; // i = 9 (fraction lost)
```

Be careful with **precision loss**.

---

## 5. Expression Evaluation and Operator Precedence

### 5.1 Order of Operations

Java follows a defined order:

1. Parentheses `( )`
2. Unary `+`, `-`, `++`, `--`
3. Multiplication, division, modulus `* / %`
4. Addition and subtraction `+ -`
5. Assignment `=`

Example:

```java
int x = 2 + 3 * 4;   // 14, not 20
int y = (2 + 3) * 4; // 20
```

### 5.2 Mixed Expressions

If one operand is `double`, the result becomes `double`:

```java
double result = 5 / 2;     // 2.0 (integer division first)
double result2 = 5.0 / 2;  // 2.5 (floating-point division)
```

---

## 6. Augmented Assignment and Increment/Decrement

### 6.1 Augmented Assignment

Shortcut operators:

```java
x += 3;  // same as x = x + 3
y *= 2;  // same as y = y * 2
```

### 6.2 Increment and Decrement

`++` increases by 1, `--` decreases by 1.
Two forms:

```java
int a = 5;
System.out.println(a++); // prints 5, then a = 6
System.out.println(++a); // a = 7, then prints 7
```

**Remember:**

* Postfix (`a++`) → use then increment
* Prefix (`++a`) → increment then use

---

## 7. Common Mistakes to Avoid

* Using `=` instead of `==` in comparisons.
* Integer division when you expect decimals.
* Forgetting to initialize a variable before use.
* Losing data in type conversion (e.g., `(int) 3.9` → 3).

---

## 8. Typical Exam Questions

**Example 1:**

> What is the output of the following code?
>
> ```java
> int x = 5, y = 2;
> double z = x / y;
> System.out.println(z);
> ```

**Answer:** `2.0` (integer division before assignment)

**Example 2:**

> Which operator has the highest precedence?
> A. `+`
> B. `*`
> C. `=`
> D. `++`
> **Answer:** D

**Example 3:**

> What is the output of this code?
>
> ```java
> int a = 3;
> int b = ++a + a++;
> System.out.println(b);
> ```

**Explanation:**
`++a` makes `a = 4`, adds `4`, then `a++` uses `4` and increments to `5`.
So `b = 8`.

---

Would you like me to continue with **Part III: Control Structures (Selection and Looping Statements)** next? It covers `if`, `switch`, `for`, `while`, and is the core of procedural logic in the Java exam.
