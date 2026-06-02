---
audio: false
generated: true
image: false
lang: en
layout: post
title: Java EE Container Managed Task Scheduler
translated: false
type: note
---

A **ManagedScheduledExecutorService** is a Java EE (Jakarta EE) resource provided by the application server (for example WebSphere, WebLogic, WildFly) that allows you to schedule tasks to run in the future or periodically, similar to `ScheduledExecutorService` in standard Java SE, but with **container-managed benefits**:

---

### How it Works

* **Integration with the container**
  It’s managed by the application server, which means tasks execute with the application’s security context, classloader, and transaction boundaries. This avoids common problems of unmanaged threads in Java EE.

* **Scheduling capabilities**
  You can schedule tasks to:

  * Run once after a delay.
  * Run at a fixed rate (e.g., every 5 seconds).
  * Run with a fixed delay between executions.

* **Lifecycle management**
  The container takes care of thread pool lifecycle, cleanup, and resource management. You don’t need to shut it down manually like a plain `ExecutorService`.

---

### Timeout

* There’s no single "timeout" setting for the pool itself, but two things are relevant:

  * **Task execution timeout**: You can wrap tasks with `ManagedTaskListener` and specify properties like `ManagedTask.TIMEOUT` (depending on vendor support). Some servers let you configure default task timeouts so tasks that hang are canceled by the container.
  * **Future get() timeout**: As with regular `ScheduledExecutorService`, you can use `future.get(timeout, unit)` to limit how long you wait for results.

So “timeout” is usually per-task, not at the pool level.

---

### Pool Size Configuration

* Each application server has its own configuration for the backing thread pool.
  Examples:

  * **WebSphere Liberty / Traditional**: you configure the pool in `server.xml` under `<managedScheduledExecutorService>` with attributes like `corePoolSize` and `maximumPoolSize`.
  * **WebLogic**: you configure it via the Admin Console or `weblogic-managed-executor`.
  * **WildFly / JBoss EAP**: configured under the EE subsystem.

* Typical pool configs include:

  * **Core pool size**: minimum number of threads kept alive.
  * **Maximum pool size**: maximum number of concurrent threads.
  * **Queue size / rejection policy**: what happens when all threads are busy.
  * **Keep-alive time**: how long idle threads are kept before being released.

---

✅ **In summary**:
`ManagedScheduledExecutorService` works like Java SE’s scheduler but is container-aware, so you get safe threading in Java EE apps. Timeout is usually applied per-task (either via API or server config), while pool size (core/max threads) is configured at the container level, not in your application code.

---

Do you want me to show you a **WebSphere Liberty example config snippet** for pool size and timeout?
