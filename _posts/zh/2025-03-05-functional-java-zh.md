---
audio: false
generated: true
lang: zh
layout: post
title: Java函数式接口
translated: true
type: note
---

Java 8 引入的 `java.util.function` 包提供了一系列函数式接口，旨在支持函数式编程。这些接口均包含单个抽象方法，因此可与 lambda 表达式和方法引用兼容。本文将通过实际示例说明如何使用该包中最常用的函数式接口——`Function<T, R>`、`Predicate<T>`、`Consumer<T>` 和 `Supplier<T>`。

---

### 什么是函数式接口？
函数式接口是指仅包含一个抽象方法的接口。`java.util.function` 包为常见任务提供了预定义的函数式接口，无需自行创建。这些接口广泛配合 lambda 表达式、方法引用和 Stream API 使用，能帮助编写简洁且富有表达力的代码。

以下是核心接口的使用方法：

---

### 1. `Function<T, R>`：将输入转换为输出
`Function<T, R>` 接口表示接收类型 `T` 的输入并返回类型 `R` 结果的函数。其抽象方法为 `apply`。

#### 示例：获取字符串长度
```java
import java.util.function.Function;

public class Main {
    public static void main(String[] args) {
        Function<String, Integer> stringLength = s -> s.length();
        System.out.println(stringLength.apply("Hello")); // 输出：5
    }
}
```
- **说明**：lambda 表达式 `s -> s.length()` 定义了一个接收 `String`（`T`）并返回 `Integer`（`R`）的 `Function`。`apply` 方法用于执行该逻辑。

---

### 2. `Predicate<T>`：条件判断
`Predicate<T>` 接口表示接收类型 `T` 输入并返回布尔值的函数。其抽象方法为 `test`。

#### 示例：判断数字是否为偶数
```java
import java.util.function.Predicate;

public class Main {
    public static void main(String[] args) {
        Predicate<Integer> isEven = n -> n % 2 == 0;
        System.out.println(isEven.test(4)); // 输出：true
        System.out.println(isEven.test(5)); // 输出：false
    }
}
```
- **说明**：lambda 表达式 `n -> n % 2 == 0` 定义了一个当输入为偶数时返回 `true` 的 `Predicate`。`test` 方法用于执行条件判断。

---

### 3. `Consumer<T>`：执行操作
`Consumer<T>` 接口表示接收类型 `T` 输入但不返回结果的操作。其抽象方法为 `accept`。

#### 示例：打印字符串
```java
import java.util.function.Consumer;

public class Main {
    public static void main(String[] args) {
        Consumer<String> printer = s -> System.out.println(s);
        printer.accept("Hello, World!"); // 输出：Hello, World!
    }
}
```
- **说明**：lambda 表达式 `s -> System.out.println(s)` 定义了一个打印输入内容的 `Consumer`。`accept` 方法用于执行该操作。

---

### 4. `Supplier<T>`：生成结果
`Supplier<T>` 接口表示结果提供者，无需输入但返回类型 `T` 的值。其抽象方法为 `get`。

#### 示例：生成随机数
```java
import java.util.function.Supplier;
import java.util.Random;

public class Main {
    public static void main(String[] args) {
        Supplier<Integer> randomInt = () -> new Random().nextInt(100);
        System.out.println(randomInt.get()); // 输出 0 到 99 的随机整数
    }
}
```
- **说明**：lambda 表达式 `() -> new Random().nextInt(100)` 定义了一个生成随机整数的 `Supplier`。`get` 方法用于获取该值。

---

### 在 Stream 中使用函数式接口
这些接口在 Java Stream API 中尤为强大，能实现简洁的数据处理。以下示例演示如何过滤、转换并打印字符串列表：

#### 示例：处理字符串列表
```java
import java.util.Arrays;
import java.util.List;
import java.util.function.Consumer;
import java.util.function.Function;
import java.util.function.Predicate;

public class Main {
    public static void main(String[] args) {
        List<String> strings = Arrays.asList("a", "bb", "ccc", "dddd");

        Predicate<String> longerThanTwo = s -> s.length() > 2;       // 过滤长度大于 2 的字符串
        Function<String, String> toUpperCase = s -> s.toUpperCase(); // 转换为大写
        Consumer<String> printer = s -> System.out.println(s);       // 打印结果

        strings.stream()
               .filter(longerThanTwo)   // 保留 "ccc" 和 "dddd"
               .map(toUpperCase)        // 转换为 "CCC" 和 "DDDD"
               .forEach(printer);       // 输出：CCC, DDDD（分行显示）
    }
}
```
- **说明**：
  - `filter` 使用 `Predicate` 保留长度大于 2 的字符串。
  - `map` 使用 `Function` 将字符串转换为大写。
  - `forEach` 使用 `Consumer` 打印每个结果。

#### 使用方法引用
通过方法引用可进一步简化代码：
```java
strings.stream()
       .filter(s -> s.length() > 2)
       .map(String::toUpperCase)      // Function 的方法引用
       .forEach(System.out::println); // Consumer 的方法引用
```

---

### 组合函数式接口
部分接口支持组合以构建复杂操作：
- **Function 组合**：使用 `andThen` 或 `compose`。
  ```java
  Function<String, Integer> toLength = s -> s.length();
  Function<Integer, String> toString = i -> "Length is " + i;
  Function<String, String> combined = toLength.andThen(toString);
  System.out.println(combined.apply("Hello")); // 输出：Length is 5
  ```
- **Predicate 组合**：使用 `and`、`or` 或 `negate`。
  ```java
  Predicate<String> isLong = s -> s.length() > 5;
  Predicate<String> startsWithA = s -> s.startsWith("A");
  Predicate<String> isLongAndStartsWithA = isLong.and(startsWithA);
  System.out.println(isLongAndStartsWithA.test("Avocado")); // 输出：true
  ```

---

### 总结
以下是各接口的使用场景与方法：
- **`Function<T, R>`**：将输入转换为输出（例如 `apply`）。
- **`Predicate<T>`**：执行条件判断（例如 `test`）。
- **`Consumer<T>`**：对输入执行操作（例如 `accept`）。
- **`Supplier<T>`**：无输入生成值（例如 `get`）。
- **结合 Stream**：组合使用以实现强大的数据处理。
- **组合操作**：通过链式调用构建复杂逻辑。

可通过 lambda 表达式（如 `s -> s.length()`）或方法引用（如 `String::toUpperCase`）实现这些接口。它们使 Java 支持函数式编程风格，尤其在 Stream API 配合下，能让代码更简洁、可读且可复用。
