---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: Java JVM 命令行核心指南
translated: true
type: note
---

Java 提供了丰富的命令行选项来控制 JVM 的行为。以下是针对最重要分类的实用指南。

## System Properties (-D)

`-D` 标志用于设置应用程序在运行时可以访问的系统属性。

**语法：**
```bash
java -Dkey=value -Dkey2=value2 YourClass
```

**常见示例：**
```bash
# 设置自定义应用程序属性
java -Dapp.environment=production -Dapp.port=8080 MyApp

# 配置文件编码
java -Dfile.encoding=UTF-8 MyApp

# 设置 HTTP 代理
java -Dhttp.proxyHost=proxy.example.com -Dhttp.proxyPort=8080 MyApp

# 配置临时目录
java -Djava.io.tmpdir=/custom/temp MyApp
```

**在代码中访问：**
```java
String env = System.getProperty("app.environment");
String port = System.getProperty("app.port", "8080"); // 带有默认值
```

## JVM Memory Settings

内存设置用于控制 Heap 和非堆内存的分配。

**Heap Memory：**
```bash
# 初始 Heap 大小
-Xms512m          # 以 512 MB 启动
-Xms2g            # 以 2 GB 启动

# 最大 Heap 大小
-Xmx2g            # 最大 2 GB
-Xmx4096m         # 最大 4 GB

# 组合示例
java -Xms1g -Xmx4g MyApp
```

**其他内存选项：**
```bash
# Metaspace (类元数据，在 Java 8+ 中取代了 PermGen)
-XX:MetaspaceSize=128m
-XX:MaxMetaspaceSize=512m

# 线程栈大小
-Xss1m            # 每个线程栈 1 MB

# 直接内存 (NIO buffers)
-XX:MaxDirectMemorySize=512m
```

**实用示例：**
```bash
java -Xms2g -Xmx8g -XX:MetaspaceSize=256m -XX:MaxMetaspaceSize=512m \
     -Xss1m MyLargeApplication
```

## Garbage Collection Options

控制 GC 行为和日志。

**GC 算法选择：**
```bash
# G1 GC (Java 9+ 的默认选择，良好的通用型 GC)
-XX:+UseG1GC

# Parallel GC (专注于吞吐量)
-XX:+UseParallelGC

# ZGC (低延迟，Java 11+)
-XX:+UseZGC

# Shenandoah (低延迟，Java 12+)
-XX:+UseShenandoahGC
```

**GC 调优：**
```bash
# G1 GC 特定选项
-XX:MaxGCPauseMillis=200        # 目标停顿时间
-XX:G1HeapRegionSize=16m        # Region 大小

# 通用选项
-XX:+UseStringDeduplication      # 减少 String 内存占用
```

## Debug and Logging Options

### GC Logging

**Java 8 及更早版本：**
```bash
java -Xloggc:/path/to/gc.log \
     -XX:+PrintGCDetails \
     -XX:+PrintGCDateStamps \
     -XX:+PrintGCTimeStamps \
     -XX:+UseGCLogFileRotation \
     -XX:NumberOfGCLogFiles=10 \
     -XX:GCLogFileSize=100m \
     MyApp
```

**Java 9+ (Unified Logging)：**
```bash
java -Xlog:gc*:file=/path/to/gc.log:time,level,tags \
     -Xlog:gc*=info:file=/path/to/gc.log:time,uptimemillis:filecount=10,filesize=100m \
     MyApp
```

### Class Loading Debug

```bash
# 查看加载了哪些类
-verbose:class
# 或
-XX:+TraceClassLoading
-XX:+TraceClassUnloading

# Java 9+ 统一日志
-Xlog:class+load=info
```

### JIT Compilation Debug

```bash
# 打印编译信息
-XX:+PrintCompilation

# 详细编译日志
-XX:+UnlockDiagnosticVMOptions
-XX:+LogCompilation
-XX:LogFile=/path/to/hotspot.log
```

### Remote Debugging (JDWP)

```bash
# Java 8 及更早版本
java -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5005 MyApp

# Java 9+ (绑定到所有接口 - 请谨慎使用！)
java -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005 MyApp

# 挂起直到调试器连接
java -agentlib:jdwp=transport=dt_socket,server=y,suspend=y,address=5005 MyApp
```

### 通用 Verbose 选项

```bash
-verbose:gc        # GC 活动
-verbose:class     # 类加载
-verbose:jni       # JNI 调用
```

## JVM Information and Diagnostics

```bash
# 打印 JVM 版本并退出
java -version

# 打印详细版本信息
java -XshowSettings:all -version

# 打印 VM 设置
java -XX:+PrintFlagsFinal -version | grep -i <flag>

# 发生 OutOfMemoryError 时自动 Dump Heap
-XX:+HeapDumpOnOutOfMemoryError
-XX:HeapDumpPath=/path/to/dumps/

# 打印崩溃日志
-XX:ErrorFile=/path/to/hs_err_pid%p.log
```

## Performance Monitoring

```bash
# 启用 JMX 进行监控
-Dcom.sun.management.jmxremote
-Dcom.sun.management.jmxremote.port=9010
-Dcom.sun.management.jmxremote.authenticate=false
-Dcom.sun.management.jmxremote.ssl=false
-Dcom.sun.management.jmxremote.local.only=false

# Flight Recorder (Java 11+，免费)
-XX:+FlightRecorder
-XX:StartFlightRecording=duration=60s,filename=/path/to/recording.jfr
```

## 完整实战示例

这是一个结合了多个选项的生产环境就绪命令：

```bash
java \
  -Xms4g -Xmx8g \
  -XX:+UseG1GC \
  -XX:MaxGCPauseMillis=200 \
  -XX:MetaspaceSize=256m \
  -XX:MaxMetaspaceSize=512m \
  -XX:+HeapDumpOnOutOfMemoryError \
  -XX:HeapDumpPath=/var/logs/heapdumps/ \
  -XX:+UseStringDeduplication \
  -Xlog:gc*:file=/var/logs/gc.log:time,uptime:filecount=10,filesize=100m \
  -Dapp.environment=production \
  -Dfile.encoding=UTF-8 \
  -Dcom.sun.management.jmxremote \
  -Dcom.sun.management.jmxremote.port=9010 \
  -Dcom.sun.management.jmxremote.authenticate=false \
  -Dcom.sun.management.jmxremote.ssl=false \
  -jar myapplication.jar
```

## 查找可用选项

```bash
# 标准选项 (以 - 开头)
java -help

# 扩展选项 (以 -X 开头)
java -X

# 高级选项 (以 -XX 开头)
java -XX:+PrintFlagsFinal -version
```

以上涵盖了在配置内存、调试、日志记录和监控应用程序时会用到的核心 Java 命令行选项。
