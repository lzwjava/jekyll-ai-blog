---
audio: false
generated: true
lang: en
layout: post
title: Reactive Programming in Java
translated: false
type: note
---

To use **reactor-core**, a Java library for building non-blocking, asynchronous applications based on the Reactive Streams specification, follow these steps:

---

### 1. Add reactor-core as a Dependency
First, include **reactor-core** in your project. Depending on your build tool:

- **Maven**: Add this to your `pom.xml`:
  ```xml
  <dependency>
    <groupId>io.projectreactor</groupId>
    <artifactId>reactor-core</artifactId>
    <version>3.7.3</version>
  </dependency>
  ```

- **Gradle**: Add this to your `build.gradle`:
  ```groovy
  implementation 'io.projectreactor:reactor-core:3.7.3'
  ```

This ensures the library is available in your project. Check for the latest version on [Maven Central](https://central.sonatype.com/artifact/io.projectreactor/reactor-core) if needed.

---

### 2. Understand the Core Components
Reactor-core provides two main classes for reactive programming:
- **`Flux`**: Represents an asynchronous stream that can emit **0 to N items**.
- **`Mono`**: Represents an asynchronous stream that emits **0 or 1 item**.

These are the building blocks you'll use to handle data reactively.

---

### 3. Create a Flux or Mono
You can create instances of `Flux` or `Mono` to represent your data streams.

- **Example with Flux** (multiple items):
  ```java
  Flux<Integer> numbers = Flux.just(1, 2, 3, 4, 5);
  ```

- **Example with Mono** (single item):
  ```java
  Mono<String> greeting = Mono.just("Hello, World!");
  ```

The `just` method is a simple way to create a stream from static values, but Reactor offers many other creation methods (e.g., from arrays, ranges, or custom sources).

---

### 4. Subscribe to Process the Data
To consume the emitted items, you need to **subscribe** to the `Flux` or `Mono`. Subscribing triggers the stream to start emitting data.

- **Subscribe to Flux**:
  ```java
  numbers.subscribe(System.out::println);  // Prints: 1, 2, 3, 4, 5
  ```

- **Subscribe to Mono**:
  ```java
  greeting.subscribe(System.out::println); // Prints: Hello, World!
  ```

The `subscribe` method can also take additional arguments, like error handlers or completion callbacks, for more control.

---

### 5. Transform Data with Operators
Reactor provides a rich set of operators to manipulate streams, such as `map`, `filter`, and more.

- **Example with Flux and map**:
  ```java
  numbers.map(n -> n * 2).subscribe(System.out::println);  // Prints: 2, 4, 6, 8, 10
  ```

- **Example with Mono and map**:
  ```java
  greeting.map(s -> s.toUpperCase()).subscribe(System.out::println); // Prints: HELLO, WORLD!
  ```

These operators allow you to transform, filter, or combine data in a declarative way.

---

### 6. Handle Errors and Backpressure
Reactor-core supports error handling and backpressure management:
- **Error Handling**: Use `subscribe` with an error consumer:
  ```java
  Flux.error(new RuntimeException("Oops!"))
      .subscribe(System.out::println, error -> System.err.println(error.getMessage()));
  // Prints: Oops!
  ```
- **Backpressure**: Control how subscribers handle overwhelming data streams using operators like `onBackpressureBuffer()` or `onBackpressureDrop()`.

---

### 7. Explore Further
For more advanced usage:
- Check the [official Reactor documentation](https://projectreactor.io/docs/core/release/reference/) for detailed examples and tutorials.
- Look at the [reactor-core GitHub repository](https://github.com/reactor/reactor-core) for additional resources.

---

### Summary
To use **reactor-core**:
1. Add it as a dependency in your project.
2. Use `Flux` for multiple items or `Mono` for a single item.
3. Create streams with methods like `just`.
4. Subscribe to process the data.
5. Apply operators to transform the streams as needed.

This is a beginner-friendly starting point for reactive programming with reactor-core. Experiment with small examples to get comfortable with its reactive paradigm!
