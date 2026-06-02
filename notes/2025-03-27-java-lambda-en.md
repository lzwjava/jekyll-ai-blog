---
audio: false
generated: true
lang: en
layout: post
title: Lambda Expressions and the Stream API in Java
translated: false
type: note
---

Okay, let's learn about Lambda Expressions and the Stream API in Java. These are powerful features introduced in Java 8 that enable a more functional programming style, leading to more concise and expressive code.

**1. Lambda Expressions**

**What is a Lambda Expression?**

A lambda expression is essentially an anonymous (unnamed) function. It allows you to define a function inline without explicitly declaring a separate method. Lambda expressions are particularly useful for passing behavior as data, making your code more flexible and readable, especially when working with functional interfaces.

**Syntax of a Lambda Expression:**

A lambda expression has the following basic syntax:

```java
(parameter list) -> expression body
```

* **Parameter List:** This is similar to the parameters of a method. It can be empty, contain one parameter, or multiple parameters. The types of the parameters can often be inferred by the compiler, so you don't always need to declare them explicitly.
* **Arrow Token (`->`):** This separates the parameter list from the expression body.
* **Expression Body:** This is the code that the lambda expression executes. It can be a single expression or a block of statements enclosed in curly braces `{}`.

**Functional Interfaces:**

Lambda expressions in Java are used to implement methods defined by **functional interfaces**. A functional interface is an interface that contains **only one abstract method**. It can have default methods and static methods, but only one abstract method.

Examples of built-in functional interfaces in Java include:

* `Runnable` (single abstract method: `void run()`)
* `Callable<V>` (single abstract method: `V call() throws Exception`)
* `Comparator<T>` (single abstract method: `int compare(T o1, T o2)`)
* `Consumer<T>` (single abstract method: `void accept(T t)`)
* `Function<T, R>` (single abstract method: `R apply(T t)`)
* `Predicate<T>` (single abstract method: `boolean test(T t)`)
* `Supplier<T>` (single abstract method: `T get()`)

**Examples of Lambda Expressions:**

Let's look at some examples to understand how lambda expressions work:

* **No parameters:**

    ```java
    Runnable myRunnable = () -> System.out.println("Hello from lambda!");
    myRunnable.run(); // Output: Hello from lambda!
    ```

* **One parameter (parentheses can be omitted):**

    ```java
    Consumer<String> printMessage = message -> System.out.println("Message: " + message);
    printMessage.accept("Lambda is cool!"); // Output: Message: Lambda is cool!
    ```

* **Multiple parameters:**

    ```java
    java.util.Comparator<Integer> compareTwoNumbers = (a, b) -> a.compareTo(b);
    int result = compareTwoNumbers.compare(5, 10); // result will be -1
    ```

* **Lambda expression with a block of statements:**

    ```java
    java.util.function.Function<Integer, String> checkEvenOdd = number -> {
        if (number % 2 == 0) {
            return "Even";
        } else {
            return "Odd";
        }
    };
    String output = checkEvenOdd.apply(7); // output will be "Odd"
    ```

**Method References:**

Method references are a shorthand syntax for lambda expressions that simply call an existing method. They make your code even more concise. There are four kinds of method references:

1.  **Reference to a static method:** `ClassName::staticMethodName`

    ```java
    java.util.function.Function<String, Integer> stringToInt = Integer::parseInt;
    int number = stringToInt.apply("123"); // number will be 123
    ```

2.  **Reference to an instance method of a particular object:** `instance::instanceMethodName`

    ```java
    String message = "Hello";
    java.util.function.Consumer<String> printLength = message::length; // Incorrect - Consumer takes one arg
    java.util.function.Supplier<Integer> getLength = message::length;
    int len = getLength.get(); // len will be 5
    ```
    **Correction:** The `Consumer` example should take an argument. Here's a better example:

    ```java
    String message = "Hello";
    java.util.function.Consumer<String> printContains = s -> message.contains(s);
    printContains.accept("ll"); // This will execute message.contains("ll")
    ```
    For a `Supplier`, it's more like:

    ```java
    String message = "Hello";
    java.util.function.Supplier<Integer> getLength = message::length;
    int len = getLength.get(); // len will be 5
    ```

3.  **Reference to an instance method of an arbitrary object of a particular type:** `ClassName::instanceMethodName`

    ```java
    java.util.function.BiPredicate<String, String> checkStartsWith = String::startsWith;
    boolean starts = checkStartsWith.test("Java", "Ja"); // starts will be true
    ```

4.  **Reference to a constructor:** `ClassName::new`

    ```java
    java.util.function.Supplier<String> createString = String::new;
    String emptyString = createString.get(); // emptyString will be ""

    java.util.function.Function<Integer, int[]> createIntArray = int[]::new;
    int[] myArray = createIntArray.apply(5); // myArray will be an int array of size 5
    ```

**2. Stream API**

**What is the Stream API?**

The Stream API, introduced in Java 8, provides a powerful and elegant way to process collections of data. A stream represents a sequence of elements that supports various aggregate operations. Streams are different from collections; collections are about storing data, while streams are about processing data.

**Key Concepts of the Stream API:**

* **Stream:** A sequence of elements supporting sequential and parallel aggregate operations.
* **Source:** The origin of the stream (e.g., a collection, an array, an I/O channel).
* **Intermediate Operations:** Operations that transform or filter the stream and return a new stream. These operations are lazy, meaning they are not executed until a terminal operation is invoked.
* **Terminal Operations:** Operations that produce a result or a side effect and consume the stream (the stream is no longer usable after a terminal operation).

**Creating Streams:**

You can create streams in various ways:

* **From a Collection:**

    ```java
    java.util.List<String> names = java.util.Arrays.asList("Alice", "Bob", "Charlie");
    java.util.stream.Stream<String> sequentialStream = names.stream();
    java.util.stream.Stream<String> parallelStream = names.parallelStream();
    ```

* **From an Array:**

    ```java
    int[] numbers = {1, 2, 3, 4, 5};
    java.util.stream.IntStream intStream = java.util.Arrays.stream(numbers);
    ```

* **Using `Stream.of()`:**

    ```java
    java.util.stream.Stream<String> stringStream = java.util.stream.Stream.of("apple", "banana", "cherry");
    ```

* **Using `Stream.iterate()`:** (Creates an infinite sequential ordered stream)

    ```java
    java.util.stream.Stream<Integer> evenNumbers = java.util.stream.Stream.iterate(0, n -> n + 2).limit(5); // 0, 2, 4, 6, 8
    ```

* **Using `Stream.generate()`:** (Creates an infinite sequential unordered stream)

    ```java
    java.util.stream.Stream<Double> randomNumbers = java.util.stream.Stream.generate(Math::random).limit(3);
    ```

**Intermediate Operations:**

These operations transform or filter the stream and return a new stream. Common intermediate operations include:

* **`filter(Predicate<T> predicate)`:** Returns a stream consisting of the elements that match the given predicate.

    ```java
    java.util.List<Integer> numbers = java.util.Arrays.asList(1, 2, 3, 4, 5, 6);
    java.util.stream.Stream<Integer> evenNumbersStream = numbers.stream().filter(n -> n % 2 == 0); // 2, 4, 6
    ```

* **`map(Function<T, R> mapper)`:** Returns a stream consisting of the results of applying the given function to the elements of this stream.

    ```java
    java.util.List<String> names = java.util.Arrays.asList("Alice", "Bob", "Charlie");
    java.util.stream.Stream<Integer> nameLengths = names.stream().map(String::length); // 5, 3, 7
    ```

* **`flatMap(Function<T, Stream<R>> mapper)`:** Returns a stream consisting of the results of replacing each element of this stream with the contents of a mapped stream produced by applying the provided mapping function to each element. Useful for flattening nested collections.

    ```java
    java.util.List<java.util.List<Integer>> listOfLists = java.util.Arrays.asList(
            java.util.Arrays.asList(1, 2),
            java.util.Arrays.asList(3, 4, 5)
    );
    java.util.stream.Stream<Integer> singleStream = listOfLists.stream().flatMap(java.util.List::stream); // 1, 2, 3, 4, 5
    ```

* **`sorted()`:** Returns a stream consisting of the elements of this stream, sorted according to natural order.

    ```java
    java.util.List<String> fruits = java.util.Arrays.asList("banana", "apple", "cherry");
    java.util.stream.Stream<String> sortedFruits = fruits.stream().sorted(); // apple, banana, cherry
    ```

* **`distinct()`:** Returns a stream consisting of the distinct elements (according to `equals()`) of this stream.

    ```java
    java.util.List<Integer> numbersWithDuplicates = java.util.Arrays.asList(1, 2, 2, 3, 3, 3);
    java.util.stream.Stream<Integer> distinctNumbers = numbersWithDuplicates.stream().distinct(); // 1, 2, 3
    ```

* **`peek(Consumer<T> action)`:** Returns a stream consisting of the elements of this stream, additionally performing the provided action on each element as the elements are consumed from the resulting stream. Primarily for debugging or side effects.

    ```java
    java.util.List<String> names = java.util.Arrays.asList("Alice", "Bob");
    java.util.stream.Stream<String> peekedNames = names.stream().peek(name -> System.out.println("Processing: " + name));
    peekedNames.forEach(System.out::println);
    // Output:
    // Processing: Alice
    // Alice
    // Processing: Bob
    // Bob
    ```

* **`limit(long maxSize)`:** Returns a stream consisting of the elements of this stream, truncated to be no longer than `maxSize` in length.

    ```java
    java.util.stream.Stream<Integer> firstThree = java.util.stream.Stream.iterate(1, n -> n + 1).limit(3); // 1, 2, 3
    ```

* **`skip(long n)`:** Returns a stream consisting of the remaining elements of this stream after discarding the first `n` elements.

    ```java
    java.util.stream.Stream<Integer> afterSkipping = java.util.stream.Stream.iterate(1, n -> n + 1).skip(2).limit(3); // 3, 4, 5
    ```

**Terminal Operations:**

These operations produce a result or a side effect and consume the stream. Common terminal operations include:

* **`forEach(Consumer<T> action)`:** Performs an action for each element of this stream.

    ```java
    java.util.List<String> colors = java.util.Arrays.asList("red", "green", "blue");
    colors.stream().forEach(System.out::println);
    ```

* **`count()`:** Returns the count of elements in this stream.

    ```java
    long numberOfFruits = java.util.Arrays.asList("apple", "banana", "cherry").stream().count(); // 3
    ```

* **`collect(Collector<T, A, R> collector)`:** Performs a mutable reduction operation on the elements of this stream using a `Collector`. Common collectors include `toList()`, `toSet()`, `toMap()`, `joining()`, `groupingBy()`, `summarizingInt()`, etc.

    ```java
    java.util.List<String> fruits = java.util.Arrays.asList("apple", "banana", "cherry");
    java.util.List<String> fruitList = fruits.stream().collect(java.util.stream.Collectors.toList());
    java.util.Set<String> fruitSet = fruits.stream().collect(java.util.stream.Collectors.toSet());
    String joinedFruits = fruits.stream().collect(java.util.stream.Collectors.joining(", ")); // "apple, banana, cherry"
    ```

* **`reduce(T identity, BinaryOperator<T> accumulator)`:** Performs a reduction on the elements of this stream, using the provided identity value and an associative accumulation function.

    ```java
    java.util.List<Integer> numbers = java.util.Arrays.asList(1, 2, 3, 4);
    int sum = numbers.stream().reduce(0, (a, b) -> a + b); // sum will be 10
    ```

* **`min(Comparator<T> comparator)`:** Returns an `Optional` describing the minimum element of this stream according to the provided comparator.

    ```java
    java.util.List<Integer> numbers = java.util.Arrays.asList(3, 1, 4, 1, 5, 9);
    java.util.Optional<Integer> minNumber = numbers.stream().min(Integer::compareTo); // Optional[1]
    ```

* **`max(Comparator<T> comparator)`:** Returns an `Optional` describing the maximum element of this stream according to the provided comparator.

    ```java
    java.util.List<Integer> numbers = java.util.Arrays.asList(3, 1, 4, 1, 5, 9);
    java.util.Optional<Integer> maxNumber = numbers.stream().max(Integer::compareTo); // Optional[9]
    ```

* **`findFirst()`:** Returns an `Optional` describing the first element of this stream.

    ```java
    java.util.Optional<String> firstFruit = java.util.Arrays.asList("apple", "banana", "cherry").stream().findFirst(); // Optional[apple]
    ```

* **`findAny()`:** Returns an `Optional` describing some element of the stream. This operation might not always return the same result when the stream is parallel.

    ```java
    java.util.Optional<String> anyFruit = java.util.Arrays.asList("apple", "banana", "cherry").stream().findAny(); // Might return Optional[apple], Optional[banana], or Optional[cherry]
    ```

* **`anyMatch(Predicate<T> predicate)`:** Returns whether any element of this stream matches the provided predicate.

    ```java
    boolean hasEven = java.util.Arrays.asList(1, 3, 5, 2, 7).stream().anyMatch(n -> n % 2 == 0); // true
    ```

* **`allMatch(Predicate<T> predicate)`:** Returns whether all elements of this stream match the provided predicate.

    ```java
    boolean allPositive = java.util.Arrays.asList(2, 4, 6, 8).stream().allMatch(n -> n > 0); // true
    ```

* **`noneMatch(Predicate<T> predicate)`:** Returns whether no elements of this stream match the provided predicate.

    ```java
    boolean noNegatives = java.util.Arrays.asList(1, 2, 3, 4).stream().noneMatch(n -> n < 0); // true
    ```

**3. Relationship Between Lambdas and Streams**

Lambda expressions are heavily used with the Stream API. They provide a concise way to define the behavior for many of the intermediate and terminal operations. For example, the `Predicate` in `filter()`, the `Function` in `map()`, and the `Consumer` in `forEach()` are often implemented using lambda expressions.

**Examples Combining Lambdas and Streams:**

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class LambdaStreamExample {
    public static void main(String[] args) {
        List<String> names = Arrays.asList("Alice", "Bob", "Charlie", "David", "Eve");

        // Filter names starting with 'A' and convert them to uppercase
        List<String> aNamesUppercase = names.stream()
                .filter(name -> name.startsWith("A")) // Lambda for filtering
                .map(String::toUpperCase)             // Method reference for mapping
                .collect(Collectors.toList());

        System.out.println("Names starting with 'A' in uppercase: " + aNamesUppercase);
        // Output: Names starting with 'A' in uppercase: [ALICE]

        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

        // Find the sum of squares of even numbers
        int sumOfSquaresOfEvens = numbers.stream()
                .filter(n -> n % 2 == 0)       // Lambda for filtering even numbers
                .map(n -> n * n)              // Lambda for squaring
                .reduce(0, Integer::sum);     // Method reference for summing

        System.out.println("Sum of squares of even numbers: " + sumOfSquaresOfEvens);
        // Output: Sum of squares of even numbers: 220

        List<Person> people = Arrays.asList(
                new Person("Alice", 30),
                new Person("Bob", 25),
                new Person("Charlie", 35)
        );

        // Get a list of names of people older than 28
        List<String> olderPeopleNames = people.stream()
                .filter(person -> person.getAge() > 28) // Lambda for filtering
                .map(Person::getName)                 // Method reference for getting name
                .collect(Collectors.toList());

        System.out.println("Names of people older than 28: " + olderPeopleNames);
        // Output: Names of people older than 28: [Alice, Charlie]
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

**4. Parallel Streams**

The Stream API also supports parallel processing. You can easily process elements of a stream in parallel using the `parallelStream()` method on a collection or by calling the `parallel()` method on a sequential stream. This can significantly improve performance for certain operations on large datasets.

```java
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

// Calculate the sum of squares in parallel
int sumOfSquaresParallel = numbers.parallelStream()
        .map(n -> n * n)
        .reduce(0, Integer::sum);

System.out.println("Sum of squares (parallel): " + sumOfSquaresParallel);
```

**Conclusion**

Lambda expressions and the Stream API are powerful additions to Java that enable a more functional and concise way of writing code, especially when dealing with collections of data. By using lambdas with streams, you can perform complex data processing operations in a declarative and readable manner. Understanding these features is essential for modern Java development. Remember to practice using them to become more comfortable and proficient.
