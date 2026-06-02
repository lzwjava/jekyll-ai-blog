---
audio: false
generated: true
lang: en
layout: post
title: Functional Interfaces in Java
translated: false
type: note
---

The `java.util.function` package in Java provides a collection of functional interfaces that are designed to support functional programming, introduced in Java 8. These interfaces each have a single abstract method, making them compatible with lambda expressions and method references. This response explains how to use some of the most common functional interfaces in this package—`Function<T, R>`, `Predicate<T>`, `Consumer<T>`, and `Supplier<T>`—with practical examples.

---

### What Are Functional Interfaces?

A functional interface is an interface with exactly one abstract method. The `java.util.function` package offers predefined functional interfaces for common tasks, so you don’t need to create your own. These interfaces are widely used with lambda expressions, method references, and the Stream API to write concise and expressive code.

Here’s how to use the key interfaces:

---

### 1. `Function<T, R>`: Transforming Input to Output

The `Function<T, R>` interface represents a function that takes an input of type `T` and produces an output of type `R`. Its abstract method is `apply`.

#### Example: Get the Length of a String

```java
import java.util.function.Function;

public class Main {
    public static void main(String[] args) {
        Function<String, Integer> stringLength = s -> s.length();
        System.out.println(stringLength.apply("Hello")); // Outputs: 5
    }
}
```

- **Explanation**: The lambda expression `s -> s.length()` defines a `Function` that takes a `String` (`T`) and returns an `Integer` (`R`). The `apply` method executes this logic.

---

### 2. `Predicate<T>`: Testing a Condition

The `Predicate<T>` interface represents a boolean-valued function that takes an input of type `T`. Its abstract method is `test`.

#### Example: Check if a Number is Even

```java
import java.util.function.Predicate;

public class Main {
    public static void main(String[] args) {
        Predicate<Integer> isEven = n -> n % 2 == 0;
        System.out.println(isEven.test(4)); // Outputs: true
        System.out.println(isEven.test(5)); // Outputs: false
    }
}
```

- **Explanation**: The lambda `n -> n % 2 == 0` defines a `Predicate` that returns `true` if the input is even. The `test` method evaluates this condition.

---

### 3. `Consumer<T>`: Performing an Action

The `Consumer<T>` interface represents an operation that takes an input of type `T` and returns no result. Its abstract method is `accept`.

#### Example: Print a String

```java
import java.util.function.Consumer;

public class Main {
    public static void main(String[] args) {
        Consumer<String> printer = s -> System.out.println(s);
        printer.accept("Hello, World!"); // Outputs: Hello, World!
    }
}
```

- **Explanation**: The lambda `s -> System.out.println(s)` defines a `Consumer` that prints its input. The `accept` method performs the action.

---

### 4. `Supplier<T>`: Generating a Result

The `Supplier<T>` interface represents a supplier of results, taking no input and returning a value of type `T`. Its abstract method is `get`.

#### Example: Generate a Random Number

```java
import java.util.function.Supplier;
import java.util.Random;

public class Main {
    public static void main(String[] args) {
        Supplier<Integer> randomInt = () -> new Random().nextInt(100);
        System.out.println(randomInt.get()); // Outputs a random integer between 0 and 99
    }
}
```

- **Explanation**: The lambda `() -> new Random().nextInt(100)` defines a `Supplier` that generates a random integer. The `get` method retrieves the value.

---

### Using Functional Interfaces with Streams

These interfaces shine in the Java Stream API, where they enable concise data processing. Here’s an example that filters, transforms, and prints a list of strings:

#### Example: Process a List of Strings

```java
import java.util.Arrays;
import java.util.List;
import java.util.function.Consumer;
import java.util.function.Function;
import java.util.function.Predicate;

public class Main {
    public static void main(String[] args) {
        List<String> strings = Arrays.asList("a", "bb", "ccc", "dddd");

        Predicate<String> longerThanTwo = s -> s.length() > 2;       // Filter strings longer than 2
        Function<String, String> toUpperCase = s -> s.toUpperCase(); // Convert to uppercase
        Consumer<String> printer = s -> System.out.println(s);       // Print each result

        strings.stream()
               .filter(longerThanTwo)   // Keeps "ccc" and "dddd"
               .map(toUpperCase)        // Converts to "CCC" and "DDDD"
               .forEach(printer);       // Outputs: CCC, DDDD (on separate lines)
    }
}
```

- **Explanation**:
  - `filter` uses a `Predicate` to keep strings with length > 2.
  - `map` uses a `Function` to transform strings to uppercase.
  - `forEach` uses a `Consumer` to print each result.

#### Using Method References

You can make this even shorter with method references:

```java
strings.stream()
       .filter(s -> s.length() > 2)
       .map(String::toUpperCase)      // Method reference for Function
       .forEach(System.out::println); // Method reference for Consumer
```

---

### Composing Functional Interfaces

Some interfaces allow composition for more complex operations:

- **Function Composition**: Use `andThen` or `compose`.

  ```java
  Function<String, Integer> toLength = s -> s.length();
  Function<Integer, String> toString = i -> "Length is " + i;
  Function<String, String> combined = toLength.andThen(toString);
  System.out.println(combined.apply("Hello")); // Outputs: Length is 5
  ```

- **Predicate Combination**: Use `and`, `or`, or `negate`.

  ```java
  Predicate<String> isLong = s -> s.length() > 5;
  Predicate<String> startsWithA = s -> s.startsWith("A");
  Predicate<String> isLongAndStartsWithA = isLong.and(startsWithA);
  System.out.println(isLongAndStartsWithA.test("Avocado")); // Outputs: true
  ```

---

### Summary

Here’s when and how to use these interfaces:

- **`Function<T, R>`**: Transform an input into an output (e.g., `apply`).
- **`Predicate<T>`**: Test a condition (e.g., `test`).
- **`Consumer<T>`**: Perform an action on an input (e.g., `accept`).
- **`Supplier<T>`**: Generate a value without input (e.g., `get`).
- **With Streams**: Combine them for powerful data processing.
- **Composition**: Chain or combine them for complex logic.

You can implement these interfaces using lambda expressions (e.g., `s -> s.length()`) or method references (e.g., `String::toUpperCase`). They enable a functional programming style in Java, making your code more concise, readable, and reusable, especially with the Stream API.
