---
audio: false
generated: true
lang: zh
layout: post
title: Java Stream API详解
translated: true
type: note
---

要在 Java 中使用 `java.util.stream`，您可以利用 Java 8 引入的 Stream API 以函数式和声明式的方式处理数据集合。流允许您高效简洁地对元素序列（如列表或数组）执行过滤、映射和归约等操作。下面我将通过一个具体示例来讲解如何使用 `java.util.stream`：从整数列表中找出大于 10 的偶数的平均值。这将展示关键的流操作和概念。

---

### **`java.util.stream` 概述**

`java.util.stream` 包提供了 `Stream` 接口及相关类（如 `IntStream`、`DoubleStream` 等）来处理数据。流是一个支持管道操作的元素序列。这些操作包括：

- **中间操作**：转换或过滤流（例如 `filter`、`map`），返回一个新流。这些操作是惰性的，只有在调用终端操作时才会执行。
- **终端操作**：产生结果或副作用（例如 `average`、`collect`），触发管道处理数据。

使用流的典型步骤：

1. 从数据源（如列表）创建流。
2. 应用中间操作来转换或过滤数据。
3. 使用终端操作产生结果。

---

### **示例问题**

我们来解决这个问题：给定一个 `List<Integer>`，计算所有大于 10 的偶数的平均值。如果不存在这样的数字，则返回 0.0。以下是使用 `java.util.stream` 的实现方法。

#### **分步解决方案**

1. **创建流**
   - 从一个 `List<Integer>` 开始（例如 `List.of(1, 2, 12, 15, 20, 25, 30)`）。
   - 使用 `stream()` 方法创建 `Stream<Integer>`：

     ```java
     list.stream()
     ```

2. **过滤流**
   - 使用 `filter` 方法仅保留偶数和大于 10 的数字。
   - `filter` 方法接受一个 `Predicate`（返回布尔值的函数）作为 lambda 表达式：

     ```java
     .filter(number -> number % 2 == 0 && number > 10)
     ```

     - `number % 2 == 0` 检查数字是否为偶数。
     - `number > 10` 确保数字大于 10。
     - 对于示例列表 `[1, 2, 12, 15, 20, 25, 30]`，这将保留 `[12, 20, 30]`。

3. **转换为 `IntStream`**
   - 由于 `average()` 方法在原始流（如 `IntStream`）上可用，而在 `Stream<Integer>` 上不可用，因此使用 `mapToInt` 将 `Stream<Integer>` 转换为 `IntStream`：

     ```java
     .mapToInt(i -> i)
     ```

     - `i -> i` 将每个 `Integer` 拆箱为 `int`。或者，您可以使用 `Integer::intValue`。
     - 这将得到一个 `IntStream`，包含 `[12, 20, 30]`。

4. **计算平均值**
   - 在 `IntStream` 上使用 `average()` 方法，该方法返回一个 `OptionalDouble`（因为流可能为空）：

     ```java
     .average()
     ```

     - 对于 `[12, 20, 30]`，这将计算 `(12 + 20 + 30) / 3 = 20.666...`。
     - 如果流为空，则返回一个空的 `OptionalDouble`。

5. **处理空流情况**
   - 在 `OptionalDouble` 上使用 `orElse(0.0)`，如果没有数字满足过滤条件，则返回 0.0：

     ```java
     .orElse(0.0)
     ```

     - 对于 `[12, 20, 30]`，这将返回 `20.666...`。
     - 对于像 `[1, 3, 5]` 这样的列表（没有大于 10 的偶数），它将返回 `0.0`。

#### **完整代码**

以下是作为一个方法的完整解决方案：

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
        // 测试用例
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

### **`java.util.stream` 的关键特性展示**

- **链式调用**：操作以流畅的风格链式调用（例如 `.filter().mapToInt().average()`）。
- **惰性求值**：中间操作（如 `filter` 和 `mapToInt`）只有在调用终端操作（`average`）时才会执行。
- **原始流**：`IntStream` 提供了像 `average()` 这样的方法，专为数值操作设计，避免了装箱开销。
- **Optional 处理**：`OptionalDouble` 处理不存在结果的情况，`orElse` 提供了默认值。

---

### **替代方法**

您也可以使用 `Collectors` 类：

```java
import java.util.stream.Collectors;

double average = list.stream()
                     .filter(number -> number % 2 == 0 && number > 10)
                     .collect(Collectors.averagingInt(i -> i));
```

- 这会直接返回一个 `Double`，并在流为空时返回 `0.0`。然而，对于这种简单情况，`mapToInt().average()` 更直接，并且符合原始流的用法。

---

### **何时使用流**

- 在处理集合时，使用 `java.util.stream` 可以使代码简洁易读。
- 对于大型数据集，可以考虑使用 `parallelStream()` 而不是 `stream()` 来利用并行处理，但对于小列表来说，由于开销问题，这可能有些过度。

---

这个示例展示了如何使用 `java.util.stream` 解决一个实际问题。您可以根据需要调整这些步骤——创建流、过滤、映射和归约——以适应其他场景！
