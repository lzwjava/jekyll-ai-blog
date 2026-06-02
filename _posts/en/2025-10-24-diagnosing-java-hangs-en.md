---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Diagnosing Java Hangs with jstack
translated: false
type: note
---

### Using jstack to Diagnose Java Application Hangs or Stucks

jstack is a command-line tool included in the JDK that generates thread dumps for a running Java Virtual Machine (JVM). Thread dumps capture the state of all threads at a given moment, which is crucial for identifying causes of hangs, such as deadlocks, infinite loops, blocked I/O, or CPU-intensive operations. It's especially useful on Linux/Unix systems or cross-platform environments.

#### Steps to Use jstack:
1. **Identify the Java Process ID (PID):**
   - Run `jps` (also part of JDK) to list all Java processes:
     ```
     jps -l
     ```
     This outputs something like `12345 MyApp.jar`. Note the PID (e.g., 12345).

   - Alternatively, use OS commands like `ps aux | grep java` on Linux/macOS.

2. **Generate a Thread Dump:**
   - Run jstack with the PID to output the dump to a file:
     ```
     jstack <PID> > thread-dump.txt
     ```
     - Replace `<PID>` with your process ID.
     - For a more detailed dump (including locks), use `jstack -l <PID> > thread-dump.txt`.
     - If the JVM is unresponsive to signals, use `jhsdb jstack --pid <PID>` (available in JDK 8+).

3. **Capture Multiple Dumps for Analysis:**
   - Hangs often require comparison over time. Take 3-5 dumps at 10-30 second intervals:
     ```
     jstack <PID> > dump1.txt
     sleep 10
     jstack <PID> > dump2.txt
     sleep 10
     jstack <PID> > dump3.txt
     ```
     - Script this in a loop if needed (e.g., using a bash script).

4. **Analyze the Dump:**
   - Open the text file in an editor or IDE.
   - Look for:
     - **Thread States:** Focus on threads in `RUNNABLE` (active), `BLOCKED` (waiting for lock, potential deadlock), `WAITING` (idle wait), or `TIMED_WAITING`.
     - **Deadlocks:** Search for "deadlock" or use tools like `jstack -l` which flags them.
     - **Stack Traces:** Identify repeating patterns or stuck in specific methods (e.g., infinite loop in a loop).
     - **Native Frames:** If threads are stuck in native code, it might indicate JNI issues or OS-level blocks.
   - Tools for deeper analysis: VisualVM, Eclipse MAT, or online parsers like fastThread.io. For example, in VisualVM, load the dump file under "Thread" tab to visualize locks and states.

If the JVM doesn't respond (e.g., no output from `kill -3 <PID>` on Unix), the hang might be at the OS level—consider full core dumps via `gcore <PID>`.

### Using ProcDump to Diagnose Process Hangs or Stucks

ProcDump is a free Sysinternals tool for Windows that creates memory or CPU dumps of processes. It's great for capturing snapshots of hangs in any application (including Java), especially when the process is unresponsive. Use it for full memory dumps to analyze with tools like WinDbg or Visual Studio.

#### Steps to Use ProcDump:
1. **Download and Setup:**
   - Get ProcDump from the Microsoft Sysinternals site (procdump.exe).
   - Run Command Prompt as Administrator.
   - Navigate to the folder containing procdump.exe.

2. **Identify the Process:**
   - Use Task Manager or `tasklist | findstr <process-name>` to get the PID or image name (e.g., `java.exe`).

3. **Capture a Hang Dump:**
   - For immediate full memory dump (useful for stuck processes):
     ```
     procdump -ma <process-name-or-PID>
     ```
     - `-ma`: Full memory dump (includes all threads and heap).
     - Example: `procdump -ma java.exe` or `procdump -ma 12345`.

   - For automatic hang detection (triggers on unresponsiveness):
     ```
     procdump -h <process-name-or-PID> -o
     ```
     - `-h`: Monitors for hangs (process unresponsive to window messages for 5+ seconds; for services without windows, use CPU thresholds like `-h 80` for 80% CPU).
     - `-o`: Overwrite existing dumps.
     - For services: Combine with `-e` for exceptions or monitor CPU: `procdump -c 80 -h <service-exe>`.

   - Take multiple dumps: Add `-n 3` for 3 dumps at intervals (e.g., `-t 10` for 10-second delay):
     ```
     procdump -ma -n 3 -t 10 <PID>
     ```

4. **Analyze the Dump:**
   - Dumps are saved as `.dmp` files in the current directory.
   - Open in WinDbg (free from Microsoft) or Visual Studio Debugger.
   - Key commands in WinDbg:
     - `!threads`: List threads and states (look for blocked/waiting).
     - `~<thread-id>s`: Switch to a thread and use `k` for stack trace.
     - `!analyze -v`: Auto-analyze for hangs/deadlocks.
   - For Java-specific analysis, load the dump into Eclipse MAT or use `jhat` on a heap dump (if captured with `-mh` flag).

ProcDump works well for non-interactive processes like services; if the hang is CPU-bound, use `-c` to trigger on high CPU.

### General Tips for Both Tools
- **Safety:** Dumps can be large (GBs for full memory); ensure disk space.
- **Combine Tools:** For Java on Windows, use jstack first (lighter), then ProcDump for deeper OS-level insight.
- **Prevention:** Enable JVM flags like `-XX:+PrintGCDetails` for logging, or use agents like JFR for profiling.
- If dumps show no clear issue, check system resources (CPU, memory, I/O) with tools like `top` or Performance Monitor.

[Oracle Java Troubleshooting Guide](https://docs.oracle.com/en/java/javase/17/troubleshoot/troubleshoot-process-hangs-and-loops.html)
[Taking a Hang Dump with ProcDump](https://www.poppastring.com/blog/taking-a-hang-dump-or-crash-dump-with-procdump)
[Java Thread Dump Analysis](https://www.baeldung.com/java-analyze-thread-dumps)
[ProcDump Usage for Hangs](https://learn.microsoft.com/en-us/sysinternals/downloads/procdump)
