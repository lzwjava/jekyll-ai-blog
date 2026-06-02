---
audio: false
generated: true
lang: en
layout: post
title: Stream API in Java
translated: false
type: note
---

To use `java.util.stream` in Java, you can leverage the Stream API introduced in Java 8 to process collections of data in a functional and declarative way. Streams allow you to perform operations such as filtering, mapping, and reducing on sequences of elements (like lists or arrays) efficiently and concisely. Below, I'll explain how to use `java.util.stream` by walking through a specific example: finding the average of even numbers greater than 10 from a list of integers. This will demonstrate key stream operations and concepts.

---

### **Overview of `java.util.stream`**

The `java.util.stream` package provides the `Stream` interface and related classes (like `IntStream`, `DoubleStream`, etc.) to process data. A stream is a sequence of elements that supports operations executed in a pipeline. These operations are:

- **Intermediate operations**: Transform or filter the stream (e.g., `filter`, `map`), returning a new stream. These are lazy and only executed when a terminal operation is invoked.
- **Terminal operations**: Produce a result or side effect (e.g., `average`, `collect`), triggering the pipeline to process the data.

To use streams, you typically:

1. Create a stream from a data source (e.g., a list).
2. Apply intermediate operations to transform or filter the data.
3. Use a terminal operation to produce a result.

---

### **Example Problem**

Let's solve this problem: Given a `List<Integer>`, compute the average of all even numbers greater than 10. If no such numbers exist, return 0.0. Here's how to do it using `java.util.stream`.

#### **Step-by-Step Solution**

1. **Create a Stream**
   - Start with a `List<Integer>` (e.g., `List.of(1, 2, 12, 15, 20, 25, 30)`).
   - Use the `stream()` method to create a `Stream<Integer>`:

     ```java
     list.stream()
     ```

2. **Filter the Stream**
   - Use the `filter` method to keep only numbers that are even and greater than 10.
   - The `filter` method takes a `Predicate` (a function returning a boolean) as a lambda expression:

     ```java
     .filter(number -> number % 2 == 0 && number > 10)
     ```

     - `number % 2 == 0` checks if a number is even.
     - `number > 10` ensures the number is greater than 10.
     - For the example list `[1, 2, 12, 15, 20, 25, 30]`, this keeps `[12, 20, 30]`.

3. **Convert to an `IntStream`**
   - Since `average()` is available on primitive streams like `IntStream` (not `Stream<Integer>`), convert the `Stream<Integer>` to an `IntStream` using `mapToInt`:

     ```java
     .mapToInt(i -> i)
     ```

     - `i -> i` unboxes each `Integer` to an `int`. Alternatively, you could use `Integer::intValue`.
     - This gives an `IntStream` of `[12, 20, 30]`.

4. **Compute the Average**
   - Use the `average()` method on `IntStream`, which returns an `OptionalDouble` (since the stream might be empty):

     ```java
     .average()
     ```

     - For `[12, 20, 30]`, this computes `(12 + 20 + 30) / 3 = 20.666...`.
     - If the stream is empty, it returns an empty `OptionalDouble`.

5. **Handle the Empty Case**
   - Use `orElse(0.0)` on the `OptionalDouble` to return 0.0 if no numbers satisfy the filter:

     ```java
     .orElse(0.0)
     ```

     - For `[12, 20, 30]`, this returns `20.666...`.
     - For a list like `[1, 3, 5]` (no even numbers > 10), it returns `0.0`.

#### **Complete Code**

Here’s the full solution as a method:

```java
import java.util.List;

public class Main {
    public static double averageOfEvenGreaterThanTen(List<Integer> list) {
        return list.stream()
                   .filter(number -> number % 2 == 0 && number > 10)
                   .mapToInt(i -> i)
                   .average()
                   .orElse(0.0);
    }

    public static void main(String[] args) {
        // Test cases
        System.out.println(averageOfEvenGreaterThanTen(List.of(1, 2, 12, 15, 20, 25, 30)));  // ~20.666
        System.out.println(averageOfEvenGreaterThanTen(List.of(1, 3, 5)));                    // 0.0
        System.out.println(averageOfEvenGreaterThanTen(List.of(12)));                         // 12.0
        System.out.println(averageOfEvenGreaterThanTen(List.of()));                           // 0.0
        System.out.println(averageOfEvenGreaterThanTen(List.of(10, 8, 6)));                   // 0.0
        System.out.println(averageOfEvenGreaterThanTen(List.of(11, 13, 14, 16)));             // 15.0
    }
}
```

---

### **Key Features of `java.util.stream` Demonstrated**

- **Chaining**: Operations are chained in a fluent style (e.g., `.filter().mapToInt().average()`).
- **Laziness**: Intermediate operations (like `filter` and `mapToInt`) are only executed when the terminal operation (`average`) is called.
- **Primitive Streams**: `IntStream` provides methods like `average()` tailored for numeric operations, avoiding boxing overhead.
- **Optional Handling**: `OptionalDouble` handles cases where no result exists, with `orElse` providing a default value.

---

### **Alternative Approach**

You could also use the `Collectors` class:

```java
import java.util.stream.Collectors;

double average = list.stream()
                     .filter(number -> number % 2 == 0 && number > 10)
                     .collect(Collectors.averagingInt(i -> i));
```

- This returns a `Double` directly and returns `0.0` for an empty stream. However, `mapToInt().average()` is more direct for this simple case and aligns with primitive stream usage.

---

### **When to Use Streams**

- Use `java.util.stream` for concise, readable code when processing collections.
- For large datasets, consider `parallelStream()` instead of `stream()` to leverage parallelism, though this is overkill for small lists due to overhead.

---

This example shows how to use `java.util.stream` to solve a practical problem. You can adapt these steps—creating a stream, filtering, mapping, and reducing—to other scenarios as needed!
