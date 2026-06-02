---
audio: false
generated: true
lang: en
layout: post
title: 'Comprehensive Guide to VisualVM: Java Profiling and Monitoring'
translated: false
type: note
---

# Comprehensive Guide to VisualVM

VisualVM is a powerful, open-source Java profiling and monitoring tool that provides a graphical interface for analyzing the performance of Java applications. It is included with the Java Development Kit (JDK) and is particularly useful for diagnosing performance issues, memory leaks, and thread-related problems. This guide covers VisualVM’s features, setup, usage, and best practices for developers and system administrators.

## Table of Contents

1. [What is VisualVM?](#what-is-visualvm)
2. [Key Features of VisualVM](#key-features-of-visualvm)
3. [System Requirements](#system-requirements)
4. [Installing VisualVM](#installing-visualvm)
5. [Launching VisualVM](#launching-visualvm)
6. [Connecting to Java Applications](#connecting-to-java-applications)
7. [Using VisualVM for Monitoring and Profiling](#using-visualvm-for-monitoring-and-profiling)
   - [Overview Tab](#overview-tab)
   - [Monitor Tab](#monitor-tab)
   - [Threads Tab](#threads-tab)
   - [Sampler](#sampler)
   - [Profiler](#profiler)
   - [Heap Dump Analysis](#heap-dump-analysis)
   - [Thread Dump Analysis](#thread-dump-analysis)
   - [MBeans](#mbeans)
8. [Remote Monitoring](#remote-monitoring)
9. [Extending VisualVM with Plugins](#extending-visualvm-with-plugins)
10. [Best Practices](#best-practices)
11. [Troubleshooting Common Issues](#troubleshooting-common-issues)
12. [Additional Resources](#additional-resources)

## What is VisualVM?

VisualVM is a Java-based tool that integrates several JDK utilities (like `jstack`, `jmap`, and `jconsole`) into a single, user-friendly interface. It allows developers to monitor Java applications in real-time, profile CPU and memory usage, analyze heap dumps, and manage threads. VisualVM is particularly valuable for identifying performance bottlenecks, memory leaks, and threading issues in both local and remote Java applications.

Originally developed by Sun Microsystems, VisualVM is now part of the Oracle JDK and is actively maintained as an open-source project. It supports Java applications running on JDK 6 and later.

## Key Features of VisualVM

- **Real-time Monitoring**: Tracks CPU usage, memory consumption, thread activity, and garbage collection.
- **Profiling**: Offers CPU and memory profiling to identify performance bottlenecks and memory allocation patterns.
- **Heap Dump Analysis**: Allows inspection of memory contents to diagnose memory leaks.
- **Thread Dump Analysis**: Helps analyze thread states and detect deadlocks.
- **MBean Management**: Provides access to Java Management Extensions (JMX) for monitoring and managing applications.
- **Remote Monitoring**: Supports monitoring of Java applications running on remote machines.
- **Extensibility**: Supports plugins to extend functionality, such as integration with specific frameworks or additional profiling tools.
- **Lightweight and Easy to Use**: Minimal setup with an intuitive graphical interface.

## System Requirements

To use VisualVM, ensure the following:

- **Operating System**: Windows, macOS, Linux, or any OS supporting喧騒with a JVM.
- **Java Version**: JDK 6 or later (VisualVM is bundled with JDK 8 and later).
- **Memory**: At least 512 MB of free RAM for lightweight monitoring; 1 GB or more for heap dump analysis.
- **Disk Space**: Approximately 50 MB for VisualVM installation.
- **Permissions**: Administrative privileges may be required for certain features (e.g., accessing system processes).

## Installing VisualVM

VisualVM is included with Oracle JDK 8 and later, located in the `bin` directory of the JDK installation (`jvisualvm` executable). Alternatively, you can download it as a standalone application:

1. **From JDK**:
   - If you have JDK 8 or later installed, VisualVM is already available in the `JAVA_HOME/bin` directory as `jvisualvm`.
   - Run the `jvisualvm` executable to launch the tool.

2. **Standalone Download**:
   - Visit the [VisualVM website](https://visualvm.github.io/) to download the latest standalone version.
   - Extract the ZIP file to a directory of your choice.
   - Run the `visualvm` executable (e.g., `visualvm.exe` on Windows).

3. **Verify Installation**:
   - Ensure the `JRE_HOME` or `JAVA_HOME` environment variable points to a compatible JDK/JRE.
   - Test by launching VisualVM.

## Launching VisualVM

To start VisualVM:

- **On Windows**: Double-click `jvisualvm.exe` in the JDK’s `bin` folder or the standalone installation directory.
- **On macOS/Linux**: Run `./jvisualvm` from the terminal in the `bin` directory.
- The VisualVM interface will open, displaying a list of local Java applications on the left panel.

## Connecting to Java Applications

VisualVM can monitor both local and remote Java applications.

### Local Applications

- Upon launching, VisualVM automatically detects running Java applications on the local machine.
- Double-click an application in the left panel to open its monitoring dashboard.
- If an application is not listed, ensure it is running under a compatible JVM.

### Remote Applications

To monitor a remote Java application:

1. Enable JMX on the remote application by adding JVM arguments (e.g., `-Dcom.sun.management.jmxremote`).
2. In VisualVM, go to **File > Add JMX Connection**.
3. Enter the remote host’s IP address and port (e.g., `hostname:port`).
4. Provide credentials if authentication is enabled.
5. Connect and monitor the application.

**Note**: For secure connections, configure SSL and authentication as needed (see [Remote Monitoring](#remote-monitoring)).

## Using VisualVM for Monitoring and Profiling

VisualVM provides several tabs and tools for analyzing Java applications. Below is a detailed breakdown of each feature.

### Overview Tab

- Displays general information about the application, including:
  - JVM arguments
  - System properties
  - Application classpath
  - PID (Process ID)
- Useful for verifying the application’s configuration.

### Monitor Tab

- Provides real-time graphs for:
  - **CPU Usage**: Tracks application and system CPU usage.
  - **Heap Memory**: Monitors heap usage (Eden, Old Gen, PermGen/Metaspace) and garbage collection activity.
  - **Classes**: Shows the number of loaded classes.
  - **Threads**: Displays the number of live and daemon threads.
- Allows triggering garbage collection or heap dumps manually.

### Threads Tab

- Visualizes thread states (Running, Sleeping, Waiting, etc.) over time.
- Provides thread dump functionality to capture the current state of all threads.
- Useful for identifying deadlocks, blocked threads, or excessive thread usage.

### Sampler

- Offers lightweight CPU and memory sampling for performance analysis.
- **CPU Sampling**:
  - Captures method-level execution time.
  - Identifies hot methods consuming the most CPU time.
- **Memory Sampling**:
  - Tracks object allocations and memory usage.
  - Helps identify objects consuming excessive memory.
- Sampling has lower overhead than profiling but provides less detailed data.

### Profiler

- Provides in-depth CPU and memory profiling.
- **CPU Profiling**:
  - Measures the execution time of methods.
  - Identifies performance bottlenecks at the method level.
- **Memory Profiling**:
  - Tracks object allocations and references.
  - Helps detect memory leaks by identifying objects that persist unexpectedly.
- **Note**: Profiling has higher overhead than sampling and may slow down the application.

### Heap Dump Analysis

- A heap dump is a snapshot of the application’s memory.
- To generate a heap dump:
  1. Go to the **Monitor** tab.
  2. Click **Heap Dump**.
  3. Save the dump to a `.hprof` file or analyze it directly in VisualVM.
- Features:
  - View class instances, sizes, and references.
  - Identify objects with high memory usage.
  - Detect memory leaks by analyzing object retention paths.
- Use the **OQL (Object Query Language)** console for advanced heap queries.

### Thread Dump Analysis

- Captures the state of all threads at a specific moment.
- To generate a thread dump:
  1. Go to the **Threads** tab.
  2. Click **Thread Dump**.
  3. Analyze the dump in VisualVM or export it for external tools.
- Useful for diagnosing:
  - Deadlocks
  - Blocked threads
  - Thread contention issues

### MBeans

- Accesses JMX MBeans for managing and monitoring the application.
- Features:
  - View and modify MBean attributes.
  - Invoke MBean operations.
  - Monitor MBean notifications.
- Useful for applications with custom JMX instrumentation.

## Remote Monitoring

To monitor remote Java applications:

1. **Configure the Remote JVM**:
   - Add the following JVM arguments to the remote application:

     ```bash
     -Dcom.sun.management.jmxremote
     -Dcom.sun.management.jmxremote.port=<port>
     -Dcom.sun.management.jmxremote.ssl=false
     -Dcom.sun.management.jmxremote.authenticate=false
     ```

   - For secure connections, enable SSL and authentication:

     ```bash
     -Dcom.sun.management.jmxremote.ssl=true
     -Dcom.sun.management.jmxremote.authenticate=true
     -Dcom.sun.management.jmxremote.password.file=<password_file>
     ```

2. **Set Up VisualVM**:
   - Add a JMX connection in VisualVM using the remote host’s IP and port.
   - Provide credentials if required.
3. **Firewall Configuration**:
   - Ensure the JMX port is open on the remote host.
   - Use SSH tunneling for secure remote access if needed:

     ```bash
     ssh -L <local_port>:<remote_host>:<remote_port> user@remote_host
     ```

## Extending VisualVM with Plugins

VisualVM supports plugins to enhance its functionality:

1. **Install Plugins**:
   - Go to **Tools > Plugins**.
   - Browse the Plugin Center for available plugins (e.g., Visual GC, BTrace, JConsole plugins).
   - Install and restart VisualVM.
2. **Popular Plugins**:
   - **Visual GC**: Visualizes garbage collection activity.
   - **BTrace**: Provides dynamic tracing for Java applications.
   - **JConsole Plugins**: Adds JConsole-compatible features.
3. **Custom Plugins**:
   - Download plugins from the VisualVM website or third-party sources.
   - Place plugin files in the `plugins` directory and restart VisualVM.

## Best Practices

- **Start with Sampling**: Use sampling before profiling to minimize performance impact.
- **Limit Profiling Scope**: Profile specific packages or classes to reduce overhead.
- **Regular Heap Dumps**: Schedule periodic heap dumps for long-running applications to track memory trends.
- **Monitor Garbage Collection**: Use the Visual GC plugin to analyze GC performance.
- **Secure Remote Connections**: Always use SSL and authentication for remote monitoring.
- **Save Snapshots**: Save heap and thread dumps for later analysis or collaboration.
- **Use OQL for Advanced Analysis**: Learn OQL for efficient heap dump queries.
- **Monitor Resource Usage**: Ensure VisualVM has sufficient memory for large heap dumps.

## Troubleshooting Common Issues

- **Application Not Detected**:
  - Ensure the application is running on a compatible JVM.
  - Check if the JVM is configured to allow JMX connections.
- **High Overhead During Profiling**:
  - Switch to sampling for lower overhead.
  - Profile specific classes or methods.
- **Connection Issues for Remote Monitoring**:
  - Verify the JMX port and firewall settings.
  - Test connectivity using `telnet <host> <port>`.
- **OutOfMemoryError in VisualVM**:
  - Increase VisualVM’s heap size by editing the `visualvm.conf` file:

    ```bash
    -J-Xmx<memory_size>m
    ```

- **Heap Dump Analysis is Slow**:
  - Use a machine with more RAM.
  - Filter classes to reduce the scope of analysis.

## Additional Resources

- **Official Website**: [visualvm.github.io](https://visualvm.github.io/)
- **Documentation**: [VisualVM Documentation](https://visualvm.github.io/documentation.html)
- **Tutorials**:
  - Oracle’s [VisualVM Guide](https://www.oracle.com/java/technologies/visualvm.html)
  - [Java Performance Tuning with VisualVM](https://www.baeldung.com/java-visualvm)
- **Community**:
  - [VisualVM GitHub Issues](https://github.com/visualvm/visualvm.github.io/issues)
  - [Stack Overflow VisualVM Tag](https://stackoverflow.com/questions/tagged/visualvm)
