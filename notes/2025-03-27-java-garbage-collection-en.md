---
audio: false
generated: true
lang: en
layout: post
title: Garbage Collection in Java
translated: false
type: note
---

Okay, let's learn about Garbage Collection (GC) in Java! It's a crucial aspect of Java's memory management that helps developers avoid manual memory allocation and deallocation.

**What is Garbage Collection in Java?**

Garbage Collection is the automatic process of reclaiming memory occupied by objects that are no longer in use by a Java application. In essence, it's Java's way of cleaning up the "garbage" (unused objects) to make space for new objects.

**Why is Garbage Collection Needed?**

In many other programming languages (like C or C++), developers are responsible for explicitly allocating and deallocating memory using functions like `malloc` and `free`. This manual memory management can lead to several problems:

* **Memory Leaks:** If memory is allocated but never freed, the application can eventually run out of memory and crash.
* **Dangling Pointers:** If memory is freed but a pointer still refers to that memory location, using that pointer can lead to unpredictable behavior or crashes.
* **Increased Development Complexity:** Managing memory manually adds a significant layer of complexity to software development.

Java's Garbage Collection automates this process, freeing developers from the burden of manual memory management and making it easier to write safer and more reliable code.

**How Does Garbage Collection Work?**

The core idea behind garbage collection is to identify which objects in memory are still being used by the application and which are not. The garbage collector then reclaims the memory occupied by the unused objects.

Here's a simplified overview of the process:

1. **Identifying Live Objects (Marking):** The garbage collector starts by identifying the set of objects that are still reachable from the "root" objects. Root objects are typically objects that are directly accessible by the application, such as:
    * Local variables in currently executing methods.
    * Static variables.
    * Objects referenced by native code.
    * The Java Virtual Machine's (JVM) active threads.

    The garbage collector traverses the object graph starting from these roots, marking all the objects that are reachable.

2. **Reclaiming Memory (Sweeping and Compacting):** Once the live objects are marked, the garbage collector needs to reclaim the memory occupied by the unmarked (unreachable) objects. Different garbage collection algorithms employ different strategies for this:

    * **Mark and Sweep:** This algorithm identifies and marks the live objects, then sweeps through the memory, freeing the space occupied by the unmarked objects. This can lead to memory fragmentation (small, scattered blocks of free memory that are not large enough to allocate new objects).
    * **Mark and Compact:** This algorithm also marks live objects. After marking, it moves (compacts) the live objects together in memory, eliminating fragmentation and making it easier to allocate contiguous blocks of memory for new objects.
    * **Copying:** This algorithm divides the memory into two or more regions. Live objects are copied from one region to another, effectively reclaiming the space in the original region.

**Key Concepts in Java Garbage Collection:**

* **Heap:** The area of memory where objects are allocated in Java. The garbage collector primarily operates on the heap.
* **Young Generation (Nursery):** This is a portion of the heap where newly created objects are initially allocated. It's further divided into:
  * **Eden Space:** Where most new objects are created.
  * **Survivor Spaces (S0 and S1):** Used to hold objects that have survived a few minor garbage collection cycles.
* **Old Generation (Tenured Generation):** Objects that have survived multiple garbage collection cycles in the young generation are eventually moved to the old generation. Objects in the old generation are generally long-lived.
* **Permanent Generation (PermGen) / Metaspace:** In older versions of Java (before Java 8), the Permanent Generation stored metadata about classes and methods. In Java 8 and later, this has been replaced by Metaspace, which is part of native memory (not the Java heap).
* **Garbage Collection Algorithms:** Different algorithms are used for garbage collection, each with its own trade-offs in terms of performance and efficiency.

**Generational Garbage Collection:**

Java HotSpot JVM (the most common JVM) uses a generational approach to garbage collection. This is based on the observation that most objects in an application have short lifespans.

1. **Minor GC (Young Generation GC):** When the Eden space becomes full, a minor GC is triggered. Live objects from Eden and one of the Survivor spaces (say, S0) are copied to the other Survivor space (S1). Objects that have survived a certain number of minor GC cycles are moved to the old generation. Unreachable objects are discarded.

2. **Major GC (Old Generation GC) / Full GC:** When the old generation becomes full, a major GC (or sometimes a full GC, which can involve both young and old generations) is performed. This process is generally more time-consuming than a minor GC and can cause longer pauses in the application's execution.

**Common Garbage Collectors in Java HotSpot JVM:**

The Java HotSpot JVM offers several garbage collection algorithms that can be chosen based on the application's requirements (e.g., low latency, high throughput). Some common ones include:

* **Serial Collector:** Uses a single thread for garbage collection. Suitable for small applications with limited resources.
* **Parallel Collector:** Uses multiple threads for garbage collection, improving throughput. Suitable for applications with moderate to large data sets running on multi-core processors.
* **CMS (Concurrent Mark Sweep) Collector:** Tries to minimize pause times by performing most of the garbage collection work concurrently with the application threads. However, it can lead to fragmentation and might require a full GC eventually.
* **G1 (Garbage-First) Collector:** Aims to provide a good balance between throughput and low latency. It divides the heap into regions and prioritizes collecting garbage from regions with the most garbage. It's the default collector in Java 9 and later.
* **ZGC (Z Garbage Collector):** A low-latency garbage collector designed for large heaps. It aims for pause times of less than 10ms.
* **Shenandoah:** Another low-latency garbage collector with similar goals to ZGC.

You can specify which garbage collector to use via JVM command-line options.

**When Does Garbage Collection Run?**

Garbage collection is mostly an automatic process driven by the JVM. It typically runs when:

* The young generation (Eden space) becomes full.
* The old generation becomes full.
* The system is low on memory.

While you cannot directly control *when* garbage collection will run, you can suggest to the JVM that it might be a good time to perform garbage collection using `System.gc()`. However, there's no guarantee that the JVM will actually run the garbage collector immediately or at all when you call this method. It's generally better to rely on the JVM's automatic garbage collection mechanism.

**`System.gc()` and Finalization:**

* **`System.gc()`:** As mentioned, this is a request to the JVM to run the garbage collector. It's often advised to avoid relying on this method for critical memory management, as the JVM is usually better at deciding when to perform GC.
* **`finalize()` Method:** Before an object is garbage collected, the JVM gives it a chance to perform any cleanup operations by calling its `finalize()` method (if it's implemented). However, `finalize()` has several drawbacks and is generally discouraged in modern Java development. It can introduce performance issues and make garbage collection less predictable. Consider using other mechanisms like try-with-resources for resource management.

**Impact of Garbage Collection on Application Performance:**

While garbage collection is essential for memory management, it can also impact the performance of an application due to the "stop-the-world" pauses. During these pauses, all application threads are stopped while the garbage collector performs its work. The duration and frequency of these pauses depend on the garbage collection algorithm being used and the size and characteristics of the heap.

Low-latency garbage collectors like G1, ZGC, and Shenandoah aim to minimize these pause times to make applications more responsive.

**Tuning Garbage Collection:**

For applications with specific performance requirements, garbage collection can be tuned by adjusting JVM parameters such as:

* Heap size (`-Xms`, `-Xmx`)
* Young generation size (`-Xmn`)
* Survivor ratios (`-XX:SurvivorRatio`)
* Choosing a specific garbage collector (`-XX:+UseG1GC`, `-XX:+UseZGC`, etc.)
* Setting garbage collection flags for more fine-grained control.

GC tuning is an advanced topic and usually requires careful analysis of the application's behavior and performance.

**Best Practices for Writing Garbage Collector-Friendly Code:**

While Java handles memory management automatically, writing code with the garbage collector in mind can lead to better performance:

* **Minimize Object Creation:** Creating a large number of short-lived objects can put pressure on the garbage collector. Try to reuse objects when appropriate.
* **Release Object References:** If you have a reference to an object that you no longer need, set the reference to `null`. This makes the object eligible for garbage collection sooner.
* **Use Data Structures Wisely:** Choose data structures that are appropriate for your needs. For example, using a large `ArrayList` and then discarding most of its elements can be inefficient.
* **Avoid Finalizers:** As mentioned earlier, avoid relying on the `finalize()` method for resource cleanup. Use try-with-resources for resources like files and network connections.
* **Be Mindful of Static Variables:** Objects referenced by static variables will live for the entire duration of the application, so be cautious about storing large or unnecessary objects in static fields.

**In Summary:**

Garbage Collection in Java is an automatic memory management process that reclaims memory occupied by unused objects. It simplifies development by freeing developers from manual memory management. Understanding how it works, the different generations of the heap, and the available garbage collection algorithms can help you write more efficient and performant Java applications.
