---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 使用jstack诊断Java程序卡死问题
translated: true
type: note
---

### 使用 jstack 诊断 Java 应用卡顿或假死问题

jstack 是 JDK 内置的命令行工具，可为正在运行的 Java 虚拟机（JVM）生成线程转储。线程转储能捕获特定时刻所有线程的执行状态，对于定位卡顿原因（如死锁、无限循环、阻塞式 I/O 或 CPU 密集型操作）至关重要。该工具在 Linux/Unix 系统或跨平台环境中尤为实用。

#### jstack 使用步骤：
1. **定位 Java 进程 ID（PID）：**
   - 运行 `jps`（同属 JDK 工具）列出所有 Java 进程：
     ```
     jps -l
     ```
     输出示例：`12345 MyApp.jar`。记录 PID（如 12345）。
   - 在 Linux/macOS 系统中也可使用 `ps aux | grep java` 等系统命令。

2. **生成线程转储：**
   - 通过 jstack 将转储内容输出至文件：
     ```
     jstack <PID> > thread-dump.txt
     ```
     - 将 `<PID>` 替换为实际进程 ID
     - 需获取更详细转储（含锁信息）时使用 `jstack -l <PID> > thread-dump.txt`
     - 若 JVM 对信号无响应，可使用 `jhsdb jstack --pid <PID>`（适用于 JDK 8+）

3. **采集多份转储用于对比分析：**
   - 卡顿问题常需通过时间维度对比，建议按 10-30 秒间隔采集 3-5 份转储：
     ```
     jstack <PID> > dump1.txt
     sleep 10
     jstack <PID> > dump2.txt
     sleep 10
     jstack <PID> > dump3.txt
     ```
     - 如需批量操作可通过 bash 脚本循环执行

4. **分析转储文件：**
   - 在文本编辑器或 IDE 中打开转储文件
   - 重点关注：
     - **线程状态：** 聚焦于 `RUNNABLE`（运行中）、`BLOCKED`（等待锁，可能死锁）、`WAITING`（空闲等待）或 `TIMED_WAITING` 状态的线程
     - **死锁检测：** 搜索 "deadlock" 关键词，或使用 `jstack -l` 自动标记死锁
     - **堆栈轨迹：** 识别重复模式或卡在特定方法（如循环中的无限迭代）
     - **本地帧：** 若线程卡在本地代码，可能预示 JNI 问题或系统级阻塞
   - 推荐使用 VisualVM、Eclipse MAT 或 fastThread.io 等在线解析工具进行深度分析。例如在 VisualVM 中通过"线程"标签页加载转储文件，可可视化锁状态

若 JVM 完全无响应（如 Unix 系统执行 `kill -3 <PID>` 无输出），可能为系统级卡顿，此时建议通过 `gcore <PID>` 获取完整核心转储

### 使用 ProcDump 诊断进程卡顿或假死问题

ProcDump 是 Windows 平台免费的 Sysinternals 工具，可创建进程的内存或 CPU 转储。该工具特别适用于捕获应用程序（包括 Java 程序）卡顿时的运行快照，尤其当进程失去响应时。通过生成完整内存转储，可结合 WinDbg 或 Visual Studio 进行深度分析

#### ProcDump 使用步骤：
1. **下载配置：**
   - 从微软 Sysinternals 官网获取 procdump.exe
   - 以管理员身份运行命令提示符
   - 进入 procdump.exe 所在目录

2. **定位目标进程：**
   - 使用任务管理器或 `tasklist | findstr <进程名>` 获取 PID 或镜像名称（如 `java.exe`）

3. **捕获卡顿转储：**
   - 立即生成完整内存转储（适用于僵死进程）：
     ```
     procdump -ma <进程名或PID>
     ```
     - `-ma`：生成完整内存转储（包含所有线程和堆数据）
     - 示例：`procdump -ma java.exe` 或 `procdump -ma 12345`

   - 自动检测卡顿（在无响应时触发）：
     ```
     procdump -h <进程名或PID> -o
     ```
     - `-h`：监控窗口消息无响应超 5 秒的卡顿（对无窗口服务需配合 CPU 阈值，如 `-h 80` 表示 80% CPU 使用率）
     - `-o`：覆盖现有转储文件
     - 针对服务程序：可结合 `-e` 异常监控或 CPU 监控：`procdump -c 80 -h <服务程序>`

   - 采集多份转储：通过 `-n 3` 指定采集次数，`-t 10` 设置间隔（单位：秒）：
     ```
     procdump -ma -n 3 -t 10 <PID>
     ```

4. **分析转储文件：**
   - 转储文件默认保存为当前目录下的 `.dmp` 文件
   - 使用 WinDbg（微软免费工具）或 Visual Studio 调试器打开
   - WinDbg 关键命令：
     - `!threads`：列出线程状态（重点关注阻塞/等待线程）
     - `~<线程ID>s`：切换至指定线程后使用 `k` 查看堆栈轨迹
     - `!analyze -v`：自动分析卡顿/死锁
   - 针对 Java 应用分析，可将转储载入 Eclipse MAT，或对堆转储（通过 `-mh` 参数捕获）使用 `jhat` 分析

ProcDump 尤其适合非交互式进程（如服务程序）；若卡顿为 CPU 密集型，可通过 `-c` 参数设置高 CPU 阈值触发

### 通用建议
- **注意事项：** 转储文件可能占用 GB 级存储空间，需确保磁盘容量充足
- **工具组合：** Windows 平台的 Java 应用建议先使用 jstack（轻量级），再通过 ProcDump 获取系统级深度信息
- **预防措施：** 启用 `-XX:+PrintGCDetails` 等 JVM 参数记录日志，或使用 JFR 等分析工具进行性能剖析
- 若转储未显示明确问题，请使用 `top` 或性能监视器等工具检查系统资源（CPU、内存、I/O）状态

[Oracle Java 故障排除指南](https://docs.oracle.com/en/java/javase/17/troubleshoot/troubleshoot-process-hangs-and-loops.html)
[使用 ProcDump 捕获卡顿转储](https://www.poppastring.com/blog/taking-a-hang-dump-or-crash-dump-with-procdump)
[Java 线程转储分析指南](https://www.baeldung.com/java-analyze-thread-dumps)
[ProcDump 卡顿分析应用](https://learn.microsoft.com/en-us/sysinternals/downloads/procdump)
