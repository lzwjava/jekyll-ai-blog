---
audio: false
generated: true
lang: zh
layout: post
title: Java中的Lambda表达式与Stream API
translated: true
type: note
---

好的，让我们来学习 Java 中的 Lambda 表达式和 Stream API。这些是 Java 8 引入的强大特性，支持更具函数式的编程风格，从而使代码更简洁、更具表达力。

**1. Lambda 表达式**

**什么是 Lambda 表达式？**

Lambda 表达式本质上是一个匿名（未命名）函数。它允许您内联定义一个函数，而无需显式声明一个单独的方法。Lambda 表达式在将行为作为数据传递时特别有用，使您的代码更加灵活和可读，尤其是在使用函数式接口时。

**Lambda 表达式的语法：**

Lambda 表达式具有以下基本语法：

```java
(参数列表) -> 表达式主体
```

* **参数列表：** 这类似于方法的参数。它可以是空的、包含一个参数或多个参数。参数的类型通常可以由编译器推断，因此您并不总是需要显式声明它们。
* **箭头标记 (`->`):** 这将参数列表与表达式主体分开。
* **表达式主体：** 这是 Lambda 表达式执行的代码。它可以是一个单独的表达式，也可以是用花括号 `{}` 括起来的语句块。

**函数式接口：**

Java 中的 Lambda 表达式用于实现由**函数式接口**定义的方法。函数式接口是**仅包含一个抽象方法**的接口。它可以有默认方法和静态方法，但只能有一个抽象方法。

Java 中内置的函数式接口示例包括：

* `Runnable` (单一抽象方法: `void run()`)
* `Callable<V>` (单一抽象方法: `V call() throws Exception`)
* `Comparator<T>` (单一抽象方法: `int compare(T o1, T o2)`)
* `Consumer<T>` (单一抽象方法: `void accept(T t)`)
* `Function<T, R>` (单一抽象方法: `R apply(T t)`)
* `Predicate<T>` (单一抽象方法: `boolean test(T t)`)
* `Supplier<T>` (单一抽象方法: `T get()`)

**Lambda 表达式示例：**

让我们看一些例子来理解 Lambda 表达式是如何工作的：

* **无参数：**

    ```java
    Runnable myRunnable = () -> System.out.println("Hello from lambda!");
    myRunnable.run(); // 输出: Hello from lambda!
    ```

* **一个参数（括号可以省略）：**

    ```java
    Consumer<String> printMessage = message -> System.out.println("Message: " + message);
    printMessage.accept("Lambda is cool!"); // 输出: Message: Lambda is cool!
    ```

* **多个参数：**

    ```java
    java.util.Comparator<Integer> compareTwoNumbers = (a, b) -> a.compareTo(b);
    int result = compareTwoNumbers.compare(5, 10); // result 将为 -1
    ```

* **包含语句块的 Lambda 表达式：**

    ```java
    java.util.function.Function<Integer, String> checkEvenOdd = number -> {
        if (number % 2 == 0) {
            return "Even";
        } else {
            return "Odd";
        }
    };
    String output = checkEvenOdd.apply(7); // output 将为 "Odd"
    ```

**方法引用：**

方法引用是 Lambda 表达式的一种简写语法，它只是调用一个现有的方法。它们使您的代码更加简洁。方法引用有四种：

1. **引用静态方法：** `ClassName::staticMethodName`

    ```java
    java.util.function.Function<String, Integer> stringToInt = Integer::parseInt;
    int number = stringToInt.apply("123"); // number 将为 123
    ```

2. **引用特定对象的实例方法：** `instance::instanceMethodName`

    ```java
    String message = "Hello";
    java.util.function.Consumer<String> printLength = message::length; // 错误 - Consumer 接受一个参数
    java.util.function.Supplier<Integer> getLength = message::length;
    int len = getLength.get(); // len 将为 5
    ```

    **更正：** `Consumer` 示例应该接受一个参数。这里是一个更好的例子：

    ```java
    String message = "Hello";
    java.util.function.Consumer<String> printContains = s -> message.contains(s);
    printContains.accept("ll"); // 这将执行 message.contains("ll")
    ```

    对于 `Supplier`，它更像是：

    ```java
    String message = "Hello";
    java.util.function.Supplier<Integer> getLength = message::length;
    int len = getLength.get(); // len 将为 5
    ```

3. **引用特定类型的任意对象的实例方法：** `ClassName::instanceMethodName`

    ```java
    java.util.function.BiPredicate<String, String> checkStartsWith = String::startsWith;
    boolean starts = checkStartsWith.test("Java", "Ja"); // starts 将为 true
    ```

4. **引用构造函数：** `ClassName::new`

    ```java
    java.util.function.Supplier<String> createString = String::new;
    String emptyString = createString.get(); // emptyString 将为 ""

    java.util.function.Function<Integer, int[]> createIntArray = int[]::new;
    int[] myArray = createIntArray.apply(5); // myArray 将是一个大小为 5 的 int 数组
    ```

**2. Stream API**

**什么是 Stream API？**

Stream API 在 Java 8 中引入，提供了一种强大而优雅的方式来处理数据集合。流代表一个支持各种聚合操作的元素序列。流与集合不同；集合是关于存储数据的，而流是关于处理数据的。

**Stream API 的关键概念：**

* **流：** 一个支持顺序和并行聚合操作的元素序列。
* **源：** 流的来源（例如，集合、数组、I/O 通道）。
* **中间操作：** 转换或过滤流并返回一个新流的操作。这些操作是惰性的，意味着在调用终止操作之前它们不会被执行。
* **终止操作：** 产生结果或副作用并消费流的操作（在终止操作之后，流不再可用）。

**创建流：**

您可以通过多种方式创建流：

* **从集合创建：**

    ```java
    java.util.List<String> names = java.util.Arrays.asList("Alice", "Bob", "Charlie");
    java.util.stream.Stream<String> sequentialStream = names.stream();
    java.util.stream.Stream<String> parallelStream = names.parallelStream();
    ```

* **从数组创建：**

    ```java
    int[] numbers = {1, 2, 3, 4, 5};
    java.util.stream.IntStream intStream = java.util.Arrays.stream(numbers);
    ```

* **使用 `Stream.of()`：**

    ```java
    java.util.stream.Stream<String> stringStream = java.util.stream.Stream.of("apple", "banana", "cherry");
    ```

* **使用 `Stream.iterate()`：**（创建一个无限顺序有序流）

    ```java
    java.util.stream.Stream<Integer> evenNumbers = java.util.stream.Stream.iterate(0, n -> n + 2).limit(5); // 0, 2, 4, 6, 8
    ```

* **使用 `Stream.generate()`：**（创建一个无限顺序无序流）

    ```java
    java.util.stream.Stream<Double> randomNumbers = java.util.stream.Stream.generate(Math::random).limit(3);
    ```

**中间操作：**

这些操作转换或过滤流并返回一个新流。常见的中间操作包括：

* **`filter(Predicate<T> predicate)`：** 返回一个由匹配给定谓词的元素组成的流。

    ```java
    java.util.List<Integer> numbers = java.util.Arrays.asList(1, 2, 3, 4, 5, 6);
    java.util.stream.Stream<Integer> evenNumbersStream = numbers.stream().filter(n -> n % 2 == 0); // 2, 4, 6
    ```

* **`map(Function<T, R> mapper)`：** 返回一个由将给定函数应用于此流元素的结果组成的流。

    ```java
    java.util.List<String> names = java.util.Arrays.asList("Alice", "Bob", "Charlie");
    java.util.stream.Stream<Integer> nameLengths = names.stream().map(String::length); // 5, 3, 7
    ```

* **`flatMap(Function<T, Stream<R>> mapper)`：** 返回一个由将提供的映射函数应用于每个元素所产生的映射流的内容替换此流的每个元素的结果组成的流。对于扁平化嵌套集合很有用。

    ```java
    java.util.List<java.util.List<Integer>> listOfLists = java.util.Arrays.asList(
            java.util.Arrays.asList(1, 2),
            java.util.Arrays.asList(3, 4, 5)
    );
    java.util.stream.Stream<Integer> singleStream = listOfLists.stream().flatMap(java.util.List::stream); // 1, 2, 3, 4, 5
    ```

* **`sorted()`：** 返回一个由此流的元素组成的流，按自然顺序排序。

    ```java
    java.util.List<String> fruits = java.util.Arrays.asList("banana", "apple", "cherry");
    java.util.stream.Stream<String> sortedFruits = fruits.stream().sorted(); // apple, banana, cherry
    ```

* **`distinct()`：** 返回一个由此流的不同元素（根据 `equals()`）组成的流。

    ```java
    java.util.List<Integer> numbersWithDuplicates = java.util.Arrays.asList(1, 2, 2, 3, 3, 3);
    java.util.stream.Stream<Integer> distinctNumbers = numbersWithDuplicates.stream().distinct(); // 1, 2, 3
    ```

* **`peek(Consumer<T> action)`：** 返回一个由此流的元素组成的流，并在从结果流中消耗元素时对每个元素执行提供的操作。主要用于调试或副作用。

    ```java
    java.util.List<String> names = java.util.Arrays.asList("Alice", "Bob");
    java.util.stream.Stream<String> peekedNames = names.stream().peek(name -> System.out.println("Processing: " + name));
    peekedNames.forEach(System.out::println);
    // 输出:
    // Processing: Alice
    // Alice
    // Processing: Bob
    // Bob
    ```

* **`limit(long maxSize)`：** 返回一个由此流的元素组成的流，截断后的长度不超过 `maxSize`。

    ```java
    java.util.stream.Stream<Integer> firstThree = java.util.stream.Stream.iterate(1, n -> n + 1).limit(3); // 1, 2, 3
    ```

* **`skip(long n)`：** 在丢弃此流的前 `n` 个元素后，返回由该流的剩余元素组成的流。

    ```java
    java.util.stream.Stream<Integer> afterSkipping = java.util.stream.Stream.iterate(1, n -> n + 1).skip(2).limit(3); // 3, 4, 5
    ```

**终止操作：**

这些操作产生结果或副作用并消费流。常见的终止操作包括：

* **`forEach(Consumer<T> action)`：** 对此流的每个元素执行一个操作。

    ```java
    java.util.List<String> colors = java.util.Arrays.asList("red", "green", "blue");
    colors.stream().forEach(System.out::println);
    ```

* **`count()`：** 返回此流中元素的数量。

    ```java
    long numberOfFruits = java.util.Arrays.asList("apple", "banana", "cherry").stream().count(); // 3
    ```

* **`collect(Collector<T, A, R> collector)`：** 使用 `Collector` 对此流的元素执行可变的归约操作。常见的收集器包括 `toList()`, `toSet()`, `toMap()`, `joining()`, `groupingBy()`, `summarizingInt()` 等。

    ```java
    java.util.List<String> fruits = java.util.Arrays.asList("apple", "banana", "cherry");
    java.util.List<String> fruitList = fruits.stream().collect(java.util.stream.Collectors.toList());
    java.util.Set<String> fruitSet = fruits.stream().collect(java.util.stream.Collectors.toSet());
    String joinedFruits = fruits.stream().collect(java.util.stream.Collectors.joining(", ")); // "apple, banana, cherry"
    ```

* **`reduce(T identity, BinaryOperator<T> accumulator)`：** 使用提供的标识值和关联的累积函数，对此流的元素执行归约。

    ```java
    java.util.List<Integer> numbers = java.util.Arrays.asList(1, 2, 3, 4);
    int sum = numbers.stream().reduce(0, (a, b) -> a + b); // sum 将为 10
    ```

* **`min(Comparator<T> comparator)`：** 根据提供的比较器返回描述此流中最小元素的 `Optional`。

    ```java
    java.util.List<Integer> numbers = java.util.Arrays.asList(3, 1, 4, 1, 5, 9);
    java.util.Optional<Integer> minNumber = numbers.stream().min(Integer::compareTo); // Optional[1]
    ```

* **`max(Comparator<T> comparator)`：** 根据提供的比较器返回描述此流中最大元素的 `Optional`。

    ```java
    java.util.List<Integer> numbers = java.util.Arrays.asList(3, 1, 4, 1, 5, 9);
    java.util.Optional<Integer> maxNumber = numbers.stream().max(Integer::compareTo); // Optional[9]
    ```

* **`findFirst()`：** 返回描述此流第一个元素的 `Optional`。

    ```java
    java.util.Optional<String> firstFruit = java.util.Arrays.asList("apple", "banana", "cherry").stream().findFirst(); // Optional[apple]
    ```

* **`findAny()`：** 返回描述流中某个元素的 `Optional`。当流是并行时，此操作可能不总是返回相同的结果。

    ```java
    java.util.Optional<String> anyFruit = java.util.Arrays.asList("apple", "banana", "cherry").stream().findAny(); // 可能返回 Optional[apple], Optional[banana], 或 Optional[cherry]
    ```

* **`anyMatch(Predicate<T> predicate)`：** 返回此流中是否有任何元素匹配提供的谓词。

    ```java
    boolean hasEven = java.util.Arrays.asList(1, 3, 5, 2, 7).stream().anyMatch(n -> n % 2 == 0); // true
    ```

* **`allMatch(Predicate<T> predicate)`：** 返回此流中是否所有元素都匹配提供的谓词。

    ```java
    boolean allPositive = java.util.Arrays.asList(2, 4, 6, 8).stream().allMatch(n -> n > 0); // true
    ```

* **`noneMatch(Predicate<T> predicate)`：** 返回此流中是否没有元素匹配提供的谓词。

    ```java
    boolean noNegatives = java.util.Arrays.asList(1, 2, 3, 4).stream().noneMatch(n -> n < 0); // true
    ```

**3. Lambda 表达式与 Stream 的关系**

Lambda 表达式大量用于 Stream API。它们为许多中间操作和终止操作定义行为提供了一种简洁的方式。例如，`filter()` 中的 `Predicate`、`map()` 中的 `Function` 和 `forEach()` 中的 `Consumer` 通常使用 Lambda 表达式来实现。

**结合使用 Lambda 表达式和 Stream 的示例：**

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class LambdaStreamExample {
    public static void main(String[] args) {
        List<String> names = Arrays.asList("Alice", "Bob", "Charlie", "David", "Eve");

        // 过滤以 'A' 开头的名字并将它们转换为大写
        List<String> aNamesUppercase = names.stream()
                .filter(name -> name.startsWith("A")) // 用于过滤的 Lambda 表达式
                .map(String::toUpperCase)             // 用于映射的方法引用
                .collect(Collectors.toList());

        System.out.println("Names starting with 'A' in uppercase: " + aNamesUppercase);
        // 输出: Names starting with 'A' in uppercase: [ALICE]

        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

        // 查找偶数的平方和
        int sumOfSquaresOfEvens = numbers.stream()
                .filter(n -> n % 2 == 0)       // 用于过滤偶数的 Lambda 表达式
                .map(n -> n * n)              // 用于平方的 Lambda 表达式
                .reduce(0, Integer::sum);     // 用于求和的方法引用

        System.out.println("Sum of squares of even numbers: " + sumOfSquaresOfEvens);
        // 输出: Sum of squares of even numbers: 220

        List<Person> people = Arrays.asList(
                new Person("Alice", 30),
                new Person("Bob", 25),
                new Person("Charlie", 35)
        );

        // 获取年龄大于 28 岁的人员姓名列表
        List<String> olderPeopleNames = people.stream()
                .filter(person -> person.getAge() > 28) // 用于过滤的 Lambda 表达式
                .map(Person::getName)                 // 用于获取姓名的方法引用
                .collect(Collectors.toList());

        System.out.println("Names of people older than 28: " + olderPeopleNames);
        // 输出: Names of people older than 28: [Alice, Charlie]
    }
}

class Person {
    private String name;
    private int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public String getName() {
        return name;
    }

    public int getAge() {
        return age;
    }
}
```

**4. 并行流**

Stream API 还支持并行处理。您可以使用集合上的 `parallelStream()` 方法，或者通过在顺序流上调用 `parallel()` 方法，轻松地并行处理流的元素。对于大型数据集上的某些操作，这可以显著提高性能。

```java
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

// 并行计算平方和
int sumOfSquaresParallel = numbers.parallelStream()
        .map(n -> n * n)
        .reduce(0, Integer::sum);

System.out.println("Sum of squares (parallel): " + sumOfSquaresParallel);
```

**结论**

Lambda 表达式和 Stream API 是 Java 的强大补充，支持一种更具函数式风格且更简洁的编码方式，尤其是在处理数据集合时。通过将 Lambda 表达式与 Stream 结合使用，您可以以声明性和可读性强的方式执行复杂的数据处理操作。理解这些特性对于现代 Java 开发至关重要。记住要多加练习使用它们，以变得更加熟练和精通。
