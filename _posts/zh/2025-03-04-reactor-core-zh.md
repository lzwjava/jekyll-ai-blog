---
audio: false
generated: true
lang: zh
layout: post
title: Java中的响应式编程
translated: true
type: note
---

要使用 **reactor-core**（一个基于响应式流规范构建非阻塞、异步应用的Java库），请按照以下步骤操作：

---

### 1. 添加 reactor-core 依赖
首先在项目中引入 **reactor-core**。根据构建工具选择：

- **Maven**：在 `pom.xml` 中添加：
  ```xml
  <dependency>
    <groupId>io.projectreactor</groupId>
    <artifactId>reactor-core</artifactId>
    <version>3.7.3</version>
  </dependency>
  ```

- **Gradle**：在 `build.gradle` 中添加：
  ```groovy
  implementation 'io.projectreactor:reactor-core:3.7.3'
  ```

这能确保库在项目中可用。如需最新版本请查看 [Maven Central](https://central.sonatype.com/artifact/io.projectreactor/reactor-core)。

---

### 2. 理解核心组件
Reactor-core 提供两个响应式编程核心类：
- **`Flux`**：代表能发射 **0 到 N 个元素**的异步流
- **`Mono`**：代表发射 **0 或 1 个元素**的异步流

它们是实现响应式数据处理的基石。

---

### 3. 创建 Flux 或 Mono
通过创建 `Flux` 或 `Mono` 实例来表示数据流：

- **Flux 示例**（多元素）：
  ```java
  Flux<Integer> numbers = Flux.just(1, 2, 3, 4, 5);
  ```

- **Mono 示例**（单元素）：
  ```java
  Mono<String> greeting = Mono.just("Hello, World!");
  ```

`just` 方法是通过静态值创建流的简单方式，Reactor 还提供其他创建方式（如从数组、范围或自定义源创建）。

---

### 4. 订阅处理数据
需要通过**订阅** `Flux` 或 `Mono` 来消费发射的元素。订阅会触发数据流开始发射。

- **订阅 Flux**：
  ```java
  numbers.subscribe(System.out::println);  // 输出：1, 2, 3, 4, 5
  ```

- **订阅 Mono**：
  ```java
  greeting.subscribe(System.out::println); // 输出：Hello, World!
  ```

`subscribe` 方法还可接收错误处理器或完成回调等参数，实现更精细的控制。

---

### 5. 使用操作符转换数据
Reactor 提供丰富的操作符来操控数据流，如 `map`、`filter` 等：

- **Flux 与 map 示例**：
  ```java
  numbers.map(n -> n * 2).subscribe(System.out::println);  // 输出：2, 4, 6, 8, 10
  ```

- **Mono 与 map 示例**：
  ```java
  greeting.map(s -> s.toUpperCase()).subscribe(System.out::println); // 输出：HELLO, WORLD!
  ```

这些操作符支持以声明式方式转换、过滤或组合数据。

---

### 6. 处理错误与背压
Reactor-core 支持错误处理和背压管理：
- **错误处理**：使用带错误消费者的订阅方式：
  ```java
  Flux.error(new RuntimeException("出错啦！"))
      .subscribe(System.out::println, error -> System.err.println(error.getMessage()));
  // 输出：出错啦！
  ```
- **背压**：通过 `onBackpressureBuffer()` 或 `onBackpressureDrop()` 等操作符控制订阅者处理过载数据流。

---

### 7. 进阶探索
如需深入了解：
- 查阅 [官方 Reactor 文档](https://projectreactor.io/docs/core/release/reference/) 获取详细示例
- 访问 [reactor-core GitHub 仓库](https://github.com/reactor/reactor-core) 获取额外资源

---

### 总结
使用 **reactor-core** 只需：
1. 在项目中添加依赖
2. 多元素用 `Flux`，单元素用 `Mono`
3. 使用 `just` 等方法创建流
4. 通过订阅处理数据
5. 按需使用操作符转换数据流

这是入门 reactor-core 响应式编程的友好起点，建议通过小型示例熟悉其响应式范式！
