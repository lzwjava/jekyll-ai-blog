---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Liberty Server Stop Hangs and Fixes
translated: false
type: note
---

In IBM WebSphere Liberty Profile on Windows, there are several scenarios where a normal server stop might hang or fail to complete cleanly:

## Cases Where Server Stop Can Hang

**Background threads that don't respond to interrupts** - Worker threads or executor services that ignore interrupt signals will prevent graceful shutdown.

**Long-running scheduled tasks** - Tasks scheduled via `@Schedule`, `ScheduledExecutorService`, or Quartz jobs that are in the middle of execution.

**Active database connections or transactions** - Long-running transactions or connection pool cleanup issues.

**Message-driven beans (MDBs) processing messages** - If JMS listeners are actively consuming messages.

**Servlet async contexts** - Asynchronous servlets with requests that haven't completed.

**Thread pool deadlocks** - Threads waiting on resources that will never become available.

**Poorly implemented lifecycle listeners** - ServletContextListeners or CDI observers that block during `@PreDestroy` or shutdown hooks.

## How to End the Server When Normal Stop Fails

**Wait for shutdown timeout** - Liberty has a default shutdown timeout (30 seconds). After this, it will forcibly terminate remaining threads.

**Configure shutdown timeout in server.xml**:
```xml
<executor name="defaultExecutor" 
          coreThreads="5" 
          maxThreads="25"
          keepAlive="60s"
          stealPolicy="STRICT"
          rejectedWorkPolicy="CALLER_RUNS"/>

<applicationMonitor updateTrigger="mbean" dropinsEnabled="false" pollingRate="500ms"/>
```

**Force kill the process on Windows**:
```cmd
rem Find the Java process
tasklist | findstr java

rem Force kill by PID
taskkill /F /PID <process_id>

rem Or kill all java processes (use with caution)
taskkill /F /IM java.exe
```

**Use server stop with force option**:
```cmd
server stop myServer --force
```

**Implement proper shutdown hooks** - In your application code, ensure background tasks can be interrupted:
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

**For scheduled tasks, make them interruptible**:
```java
@Schedule(hour="*", minute="*/5", persistent=false)
public void scheduledTask() {
    if (Thread.currentThread().isInterrupted()) {
        return; // Exit gracefully
    }
    // Task logic
}
```

The most reliable approach is to design your application with proper lifecycle management from the start, ensuring all background tasks respect interrupt signals and implement `@PreDestroy` methods that cleanly shut down executors and scheduled tasks.