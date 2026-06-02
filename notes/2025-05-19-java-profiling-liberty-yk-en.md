---
audio: false
generated: true
image: false
lang: en
layout: post
title: Profiling Liberty With YourKit Java Profiler
translated: false
type: note
---

WebSphere Liberty can be integrated with YourKit Java Profiler quite smoothly, since Liberty is just another JVM-based runtime. Here’s how it typically works:

---

### 1. How the Integration Works

YourKit Java Profiler doesn’t need Liberty-specific plugins; it works by attaching to the JVM process that Liberty runs in. Once attached, it intercepts method calls, memory allocations, thread activity, and other runtime events.
Liberty runs on the OpenJ9 (or HotSpot) JVM, so you can enable profiling by adding the YourKit agent to Liberty’s startup.

---

### 2. Attaching the YourKit Agent

There are two main ways:

* **Startup attachment (preferred for servers)**
  Add the YourKit agent options to Liberty’s `jvm.options` file (in `<wlp_home>/usr/servers/<server_name>/`).
  Example:

  ```
  -agentpath:/path/to/yourkit/bin/linux-x86-64/libyjpagent.so=port=10001,listen=all
  ```

  This loads the profiler agent as soon as the server starts.

* **On-demand (dynamic) attach**
  If Liberty is already running, you can attach YourKit via the GUI. It scans for running JVMs and lets you connect without restarting. Useful for production debugging, but requires permissions (same user / JDK tools.jar).

---

### 3. Profiling in Liberty Context

When running on Liberty, you may want to:

* **Filter by application packages** so you don’t drown in Liberty’s internal code.
* **Use call tree / hotspots view** to analyze slow servlets, JAX-RS endpoints, or CDI beans.
* **Monitor JDBC and thread pools** since Liberty applications often rely on container-managed resources. YourKit can trace JDBC calls and measure wait times.
* **Handle multiple apps** – if Liberty hosts several apps, use YourKit’s thread and class filters to narrow down profiling to the one you care about.

---

### 4. Performance Considerations

* Profiling always adds overhead. For development it’s fine to use full CPU/memory profiling; in production use *sampling* mode instead of instrumentation.
* Liberty’s modular classloading can sometimes cause duplicate class names; YourKit generally handles this but be mindful when filtering.
* If you use IBM JDK with Liberty, make sure you download the YourKit agent built for IBM J9/OpenJ9, not just HotSpot.

---

### 5. Typical Workflow

1. Install YourKit on your dev machine.
2. Modify Liberty’s `jvm.options` with the agent path.
3. Start Liberty.
4. Connect from the YourKit GUI to the Liberty JVM (via socket or attach).
5. Profile your endpoints, memory usage, or thread locks.
6. Save snapshots for offline analysis.

---

👉 Do you want me to give you a **step-by-step config example** for Liberty on **OpenJ9** (the default Liberty JVM) with YourKit, including sample `jvm.options` settings for CPU vs memory profiling?
