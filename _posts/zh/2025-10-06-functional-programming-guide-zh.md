---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: Java函数式编程指南
translated: true
type: note
---

自 Java 8 起，Java 开始拥抱函数式编程理念，引入了 lambda 表达式、流式处理等特性，使代码更简洁、可读且声明式。本指南涵盖从基础到进阶的概念，假定读者已熟悉 Java 核心知识。我们将使用 Java 8+ 语法，因为这些特性自此版本开始引入。示例代码均采用 Java 代码块形式，方便复制使用。

## 1. Java 函数式编程简介

函数式编程（FP）强调：

- **纯函数**：无副作用的函数（例如不改变可变状态）
- **不可变性**：数据创建后不可更改
- **高阶函数**：可接收或返回其他函数的函数
- **声明式风格**：关注"做什么"而非"如何做"（例如使用流替代循环）

Java 并非 Haskell 那样的纯函数式语言，而是将 FP 与面向对象特性融合。关键支撑技术：

- Lambda 表达式（匿名函数）
- 函数式接口（仅含单个抽象方法的接口）
- 用于集合函数式处理的 Streams API

优势：减少模板代码、更易实现并行化、更好的可组合性

## 2. Lambda 表达式

Lambda 是用于简短一次性实现的匿名函数，是 Java 中进入 FP 世界的入口。

### 基础语法

Lambda 格式：`(参数) -> { 函数体 }`

- 单参数时可省略括号
- 单表达式时可省略大括号（隐式返回）
- 通常支持类型推断，也可显式声明类型

```java
// 传统匿名内部类
Runnable r = new Runnable() {
    @Override
    public void run() {
        System.out.println("Hello, World!");
    }
};

// Lambda 等效写法
Runnable lambda = () -> System.out.println("Hello, World!");
lambda.run();
```

### 带参数示例

```java
// 二元运算符示例
BinaryOperator<Integer> add = (a, b) -> a + b;
System.out.println(add.apply(2, 3)); // 5

// 多行函数体
Comparator<String> comparator = (s1, s2) -> {
    int lenDiff = s1.length() - s2.length();
    return lenDiff != 0 ? lenDiff : s1.compareTo(s2);
};
```

### 变量捕获（实质最终）

Lambda 可访问外部变量，但变量必须是**实质最终**（未被重新赋值）

```java
int threshold = 10;
Predicate<Integer> isHigh = x -> x > threshold; // 正确
// threshold = 20; // 错误：非实质最终
```

## 3. 函数式接口

函数式接口是仅含一个抽象方法（SAM - Single Abstract Method）的接口。Java 在 `java.util.function` 包中提供了内置接口。

### 内置示例

- `Predicate<T>`：`boolean test(T t)`
- `Function<T, R>`：`R apply(T t)`
- `Consumer<T>`：`void accept(T t)`
- `Supplier<T>`：`T get()`
- `BiFunction<T, U, R>` 等双参数接口

自定义接口：

```java
@FunctionalInterface  // 可选标注，但推荐使用
interface Transformer {
    String transform(String input);
}

Transformer upper = s -> s.toUpperCase();
System.out.println(upper.transform("java")); // JAVA
```

使用 `@FunctionalInterface` 强制保证 SAM 规范。

### 默认与静态方法

函数式接口可包含默认方法（Java 8+），如 `Optional.orElse()`

```java
default int compare(String a, String b) { ... } // 允许
static void utility() { ... } // 允许
```

## 4. 方法引用

是调用现有方法的 lambda 简写形式。语法：`类名::方法名` 或 `实例::方法名`

类型：

- 静态方法：`类名::静态方法`
- 特定类型实例方法：`类名::实例方法`
- 任意对象实例方法：`对象::实例方法`
- 构造器：`类名::new`

示例：

```java
// Lambda: x -> System.out.println(x)
Consumer<String> printer = System.out::println;

// 静态方法
Function<String, Integer> length = String::length;

// 实例方法
List<String> list = Arrays.asList("a", "b");
list.forEach(System.out::println); // 逐个打印

// 构造器
Supplier<List<String>> listSupplier = ArrayList::new;
```

## 5. Streams API

流以声明式方式处理集合：创建 → 转换 → 收集。采用惰性求值（中间操作在终端操作触发前不执行）

### 创建流

```java
import java.util.*;
import java.util.stream.*;

List<String> names = Arrays.asList("Alice", "Bob", "Charlie");

// 从集合创建
Stream<String> stream = names.stream();

// 从数组创建
String[] arr = {"x", "y"};
Stream<String> arrStream = Arrays.stream(arr);

// 无限流
Stream<Integer> infinite = Stream.iterate(0, n -> n + 1);
```

### 中间操作（惰性）

可链式调用，终端操作前不执行计算

- `filter(Predicate)`：保留匹配元素
- `map(Function)`：转换每个元素
- `flatMap(Function<? super T, ? extends Stream<? extends R>>)`：展平嵌套流
- `distinct()`、`sorted()`、`limit(n)`、`skip(n)`

```java
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
List<Integer> evensSquared = numbers.stream()
    .filter(n -> n % 2 == 0)
    .map(n -> n * n)
    .collect(Collectors.toList()); // [4, 16]
```

### 终端操作（急切）

触发计算并返回结果

- `collect(Collector)`：收集到列表、集合、映射等
- `forEach(Consumer)`：副作用操作（尽量避免）
- `reduce()`：聚合操作（如求和）
- `anyMatch()`、`allMatch()`、`findFirst()`

```java
// Reduce：求和
int sum = numbers.stream().reduce(0, Integer::sum); // 15

// 收集到映射
Map<String, Integer> nameLengths = Stream.of("Alice", "Bob")
    .collect(Collectors.toMap(s -> s, String::length)); // {Alice=5, Bob=3}

// 分组
Map<Integer, List<String>> byLength = names.stream()
    .collect(Collectors.groupingBy(String::length)); // {5=[Alice, Charlie], 3=[Bob]}
```

### 并行流

使用 `parallelStream()` 或 `.parallel()` 实现并行处理。需谨慎使用（调试困难）

```java
long count = names.parallelStream().count(); // 3
```

## 6. 收集器

来自 `java.util.stream.Collectors`，用于构建复杂归约操作

常用收集器：

- `toList()`、`toSet()`、`toMap()`
- `joining()`：字符串拼接
- `summingInt()`、`averagingDouble()`
- `groupingBy()`、`partitioningBy()`
- `collectingAndThen()`：后处理

```java
// 按长度取最大值的自定义收集器
String longest = names.stream()
    .collect(Collectors.maxBy(Comparator.comparingInt(String::length)))
    .orElse(""); // "Charlie"

// 奇偶分区
Map<Boolean, List<Integer>> partitions = numbers.stream()
    .collect(Collectors.partitioningBy(n -> n % 2 == 0));
```

## 7. Optional 容器

通过包装可能为 null 的值避免 `NullPointerException`，鼓励显式空值处理

创建方式：

- `Optional.of(value)`：非空值
- `Optional.ofNullable(value)`：空值转为空容器
- `Optional.empty()`

操作：

- `isPresent()`、`ifPresent(Consumer)`
- `orElse(默认值)`、`orElseThrow()`
- `map()`、`flatMap()` 用于链式调用

```java
Optional<String> opt = Optional.ofNullable(getName()); // 假设可能返回 null

String name = opt.orElse("Unknown");
opt.ifPresent(System.out::println);

String upper = opt.map(String::toUpperCase).orElse("DEFAULT");
```

流操作常返回 `Optional`（如 `findFirst()`）

## 8. 进阶主题

### 可组合函数

`Function.andThen()`、`Function.compose()` 用于链式组合

```java
Function<String, Integer> len = String::length;
Function<Integer, String> toStr = i -> "长度: " + i;

Function<String, String> chain = len.andThen(toStr);
System.out.println(chain.apply("Java")); // 长度: 4
```

### 递归与尾调用

Java 缺乏尾调用优化，但可使用 `Stream.iterate()` 实现迭代式递归

### 不可变性辅助工具

使用 `Collections.unmodifiableList()` 或 Guava/Immutable Collections 等库（Java 10+ 内置 `List.of()`）

`List.of("a", "b")` 创建不可变列表（Java 9+）

### 模式匹配（Java 21+ 预览/稳定版）

通过 switch 中的解构增强 FP 能力

```java
// 预览特性：使用 --enable-preview 启用
String desc = switch (obj) {
    case Integer i -> "整数: " + i;
    case String s -> "字符串: " + s.length();
    default -> "未知";
};
```

### 虚拟线程（Java 21+）

FP 与轻量级线程结合，为并发流处理增色

## 9. 最佳实践

- **优先不可变性**：使用 final 字段，避免修改集合
- **避免副作用**：保持 lambda 纯净；仅在 `forEach` 或显式消费者中使用副作用
- **流与循环选择**：可读性优先用流；性能关键代码用循环
- **空值处理**：优先使用 `Optional` 替代空检查
- **测试**：使用 lambda 轻松模拟函数式接口
- **性能**：流存在开销；使用并行前先性能分析
- **可读性**：简单 lambda 可直接使用；复杂逻辑提取为方法

常见陷阱：

- 在 lambda 中修改外部状态
- 忘记终端操作（流不执行任何操作！）
- 过度使用并行流（并非总是更快）

## 10. 示例：函数式处理管道

以函数式风格处理员工列表

```java
import java.util.*;
import java.util.stream.Collectors;

class Employee {
    String name;
    int salary;
    Department dept;

    Employee(String name, int salary, Department dept) {
        this.name = name;
        this.salary = salary;
        this.dept = dept;
    }
}

enum Department { ENG, HR }

public class FunctionalExample {
    public static void main(String[] args) {
        List<Employee> employees = Arrays.asList(
            new Employee("Alice", 50000, Department.ENG),
            new Employee("Bob", 60000, Department.HR),
            new Employee("Charlie", 55000, Department.ENG)
        );

        // 获取高薪工程师姓名并排序
        List<String> result = employees.stream()
            .filter(e -> e.dept == Department.ENG)
            .filter(e -> e.salary > 52000)
            .map(Employee::getName)  // 假设有 getter 方法
            .sorted()
            .collect(Collectors.toList());

        System.out.println(result); // [Charlie]
    }
}
```

## 总结

Lambda 和函数式编程将 Java 从命令式转变为表达式风格。从简单替换开始（如用 `forEach` 替代循环），逐步构建处理管道。在实际项目中实践以达到精通水平。如需深入探索，可在 IDE 中实验各种特性。

### 参考资源

- [Oracle Java 教程：Lambda 表达式](https://docs.oracle.com/javase/tutorial/java/javaOO/lambdaexpressions.html)
- [Baeldung：Java 8 函数式接口](https://www.baeldung.com/java-functional-interfaces)
- [Java 流式处理指南](https://www.baeldung.com/java-8-streams)
- [Effective Java（第3版）- 关于 Lambda 的条款 42-45](https://www.oreilly.com/library/view/effective-java-3rd/9780134686097/)
