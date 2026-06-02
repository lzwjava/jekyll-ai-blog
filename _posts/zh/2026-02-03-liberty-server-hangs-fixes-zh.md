---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: Liberty 服务器停止挂起及修复方法
translated: true
type: note
---

在 Windows 上的 IBM WebSphere Liberty Profile 中，有几种场景可能导致正常的 server stop 挂起或无法彻底完成：

## Cases Where Server Stop Can Hang

**不响应中断的 Background threads** - 忽略 interrupt 信号的 worker threads 或 executor services 将阻止优雅停机（graceful shutdown）。

**长时间运行的 scheduled tasks** - 通过 `@Schedule`、`ScheduledExecutorService` 或 Quartz jobs 调度且正在执行中的任务。

**活跃的数据库连接或事务** - 长时间运行的 transactions 或连接池清理问题。

**正在处理消息的 Message-driven beans (MDBs)** - 如果 JMS listeners 正在积极消费消息。

**Servlet async contexts** - 包含未完成请求的异步 servlets。

**Thread pool deadlocks** - 线程正在等待永远不会释放的资源。

**实现不当的 lifecycle listeners** - 在 `@PreDestroy` 或 shutdown hooks 执行期间阻塞的 ServletContextListeners 或 CDI observers。

## How to End the Server When Normal Stop Fails

**等待 shutdown timeout** - Liberty 有一个默认的 shutdown timeout（30 秒）。超时后，它将强制终止剩余线程。

**在 server.xml 中配置 shutdown timeout**：

```xml
<executor name="defaultExecutor"
          coreThreads="5"
          maxThreads="25"
          keepAlive="60s"
          stealPolicy="STRICT"
          rejectedWorkPolicy="CALLER_RUNS"/>

<applicationMonitor updateTrigger="mbean" dropinsEnabled="false" pollingRate="500ms"/>
```

**在 Windows 上强制杀死进程**：

```cmd
rem Find the Java process
tasklist | findstr java

rem Force kill by PID
taskkill /F /PID <process_id>

rem Or kill all java processes (use with caution)
taskkill /F /IM java.exe
```

**使用带有 force 选项的 server stop**：

```cmd
server stop myServer --force
```

**实现正确的 shutdown hooks** - 在应用程序代码中，确保 background tasks 可以被中断：

```java
@PreDestroy
public void cleanup() {
    if (scheduledExecutor != null) {
        scheduledExecutor.shutdown();
        try {
            if (!scheduledExecutor.awaitTermination(30, TimeUnit.SECONDS)) {
                scheduledExecutor.shutdownNow();
            }
        } catch (InterruptedException e) {
            scheduledExecutor.shutdownNow();
        }
    }
}
```

**对于 scheduled tasks，使其变为可中断的**：

```java
@Schedule(hour="*", minute="*/5", persistent=false)
public void scheduledTask() {
    if (Thread.currentThread().isInterrupted()) {
        return; // Exit gracefully
    }
    // Task logic
}
```

最可靠的方法是从一开始就在设计应用程序时考虑适当的 lifecycle management，确保所有 background tasks 都尊重 interrupt 信号，并实现能干净地关闭 executors 和 scheduled tasks 的 `@PreDestroy` 方法。
