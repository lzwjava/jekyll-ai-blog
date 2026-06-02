---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Java 执行器：不受欢迎的观点和陷阱
translated: true
type: note
---

问题：关于 Java executor 有哪些不受欢迎的观点？

回答：

Java 的 Executor 框架（包括 Executor、ExecutorService 和 ThreadPoolExecutor 等实现）在管理并发方面广受好评，但在开发者中也存在一些不太受欢迎或批判性的观点。这些观点通常源于实际使用中的陷阱、不断发展的替代方案，或该框架在某些特定用例中表现不足：

- **Executors 中的工厂方法很危险，应避免使用**：像 `newCachedThreadPool()` 或 `newFixedThreadPool()` 这种带有无界队列的方法可能导致资源耗尽（例如，无限的线程创建或队列增长导致 OutOfMemoryError）。许多经验丰富的开发者建议直接实例化 `ThreadPoolExecutor`，以便对线程限制、队列和拒绝策略进行细粒度控制。

- **ExecutorService 对于现代异步编程来说已经过时了**：它在 Java 5 中引入，依赖于 `Future`，而 `Future` 是阻塞且有限的。自 Java 8 以来，`CompletableFuture` 提供了更好的组合性、非阻塞操作和链式调用，使得原始的 ExecutorService 在复杂工作流中显得冗长且功能不足。

- **频繁创建 ExecutorService 是一个常见错误**：Executors 旨在用于长期运行的线程池。为每个请求或短期任务实例化和关闭它们会引入开销，并违背了池化的目的，但初学者却经常这样做。

- **并非总是优于原始线程**：对于简单的、长期运行的单线程（例如，监视端口的守护线程），直接创建 `Thread` 可以更简单、足够。在某些情况下，“永远不要直接创建线程，总是使用 executor”的建议被认为是过于教条的。

- **非结构化并发导致错误**：经典的 ExecutorService 允许跨线程无限制地提交任务，使得生命周期管理、取消传播和错误处理容易出错。新的 API，如结构化并发（Structured Concurrency，在最近的 Java 版本中作为预览功能），通过强制执行有范围的、分层的任务关系来解决这个问题。

- **对于微小任务，开销可能超过收益**：将非常短期的任务提交给 executor 会引入排队和调度开销，这可能使其比按顺序或单线程执行更慢，特别是对于 CPU 密集型微任务。

- **使用 invokeAll() 强制排序效率低下**：即便后面的任务先完成，以提交顺序检索结果也会阻塞在前面的任务上——最好使用 `ExecutorCompletionService` 进行完成顺序处理，但许多人仍然坚持使用更简单（但次优）的方法。

这些观点强调，尽管 Executors 是基础性的，但它们需要仔细使用，并且在现代 Java 中并非总是最佳选择。

参考：

- https://dzone.com/articles/the-challenges-and-pitfalls-of-using-executors-in
- https://www.baeldung.com/java-executor-service-tutorial
- https://dzone.com/articles/executorservice-10-tips-and
- https://www.baeldung.com/java-executorservice-vs-completablefuture
- https://openjdk.org/jeps/505
- https://stackoverflow.com/questions/1647990/executorservices-surprising-performance-break-even-point-rules-of-thumb
- https://stackoverflow.com/questions/70547255/when-should-i-use-executor-over-executorservice
- https://javanexus.com/blog/understanding-java-executor-service-pitfalls
