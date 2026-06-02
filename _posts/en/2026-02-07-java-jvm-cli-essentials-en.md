---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Java JVM Command Line Essentials
translated: false
type: note
---

Java provides extensive command-line options to control the JVM's behavior. Here's a practical guide to the most important categories.

## System Properties (-D)

The `-D` flag sets system properties that your application can access at runtime.

**Syntax:**
```bash
java -Dkey=value -Dkey2=value2 YourClass
```

**Common examples:**
```bash
# Set custom application properties
java -Dapp.environment=production -Dapp.port=8080 MyApp

# Configure file encoding
java -Dfile.encoding=UTF-8 MyApp

# Set HTTP proxy
java -Dhttp.proxyHost=proxy.example.com -Dhttp.proxyPort=8080 MyApp

# Configure temp directory
java -Djava.io.tmpdir=/custom/temp MyApp
```

**Accessing in code:**
```java
String env = System.getProperty("app.environment");
String port = System.getProperty("app.port", "8080"); // with default
```

## JVM Memory Settings

Memory settings control heap and non-heap memory allocation.

**Heap Memory:**
```bash
# Initial heap size
-Xms512m          # Start with 512 MB
-Xms2g            # Start with 2 GB

# Maximum heap size
-Xmx2g            # Maximum 2 GB
-Xmx4096m         # Maximum 4 GB

# Combined example
java -Xms1g -Xmx4g MyApp
```

**Other Memory Options:**
```bash
# Metaspace (class metadata, replaced PermGen in Java 8+)
-XX:MetaspaceSize=128m
-XX:MaxMetaspaceSize=512m

# Thread stack size
-Xss1m            # 1 MB per thread stack

# Direct memory (NIO buffers)
-XX:MaxDirectMemorySize=512m
```

**Practical example:**
```bash
java -Xms2g -Xmx8g -XX:MetaspaceSize=256m -XX:MaxMetaspaceSize=512m \
     -Xss1m MyLargeApplication
```

## Garbage Collection Options

Control GC behavior and logging.

**GC Algorithm Selection:**
```bash
# G1 GC (default in Java 9+, good general purpose)
-XX:+UseG1GC

# Parallel GC (throughput-focused)
-XX:+UseParallelGC

# ZGC (low-latency, Java 11+)
-XX:+UseZGC

# Shenandoah (low-latency, Java 12+)
-XX:+UseShenandoahGC
```

**GC Tuning:**
```bash
# G1 GC specific
-XX:MaxGCPauseMillis=200        # Target pause time
-XX:G1HeapRegionSize=16m        # Region size

# General
-XX:+UseStringDeduplication      # Reduce String memory usage
```

## Debug and Logging Options

### GC Logging

**Java 8 and earlier:**
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

**Java 9+ (Unified Logging):**
```bash
java -Xlog:gc*:file=/path/to/gc.log:time,level,tags \
     -Xlog:gc*=info:file=/path/to/gc.log:time,uptimemillis:filecount=10,filesize=100m \
     MyApp
```

### Class Loading Debug

```bash
# See which classes are loaded
-verbose:class
# or
-XX:+TraceClassLoading
-XX:+TraceClassUnloading

# Java 9+ unified logging
-Xlog:class+load=info
```

### JIT Compilation Debug

```bash
# Print compilation
-XX:+PrintCompilation

# Detailed compilation log
-XX:+UnlockDiagnosticVMOptions
-XX:+LogCompilation
-XX:LogFile=/path/to/hotspot.log
```

### Remote Debugging (JDWP)

```bash
# Java 8 and earlier
java -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5005 MyApp

# Java 9+ (bind to all interfaces - be careful!)
java -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005 MyApp

# Suspend until debugger attaches
java -agentlib:jdwp=transport=dt_socket,server=y,suspend=y,address=5005 MyApp
```

### General Verbose Options

```bash
-verbose:gc        # GC activity
-verbose:class     # Class loading
-verbose:jni       # JNI calls
```

## JVM Information and Diagnostics

```bash
# Print JVM version and exit
java -version

# Print detailed version
java -XshowSettings:all -version

# Print VM settings
java -XX:+PrintFlagsFinal -version | grep -i <flag>

# Heap dump on OutOfMemoryError
-XX:+HeapDumpOnOutOfMemoryError
-XX:HeapDumpPath=/path/to/dumps/

# Print crash logs
-XX:ErrorFile=/path/to/hs_err_pid%p.log
```

## Performance Monitoring

```bash
# Enable JMX for monitoring
-Dcom.sun.management.jmxremote
-Dcom.sun.management.jmxremote.port=9010
-Dcom.sun.management.jmxremote.authenticate=false
-Dcom.sun.management.jmxremote.ssl=false
-Dcom.sun.management.jmxremote.local.only=false

# Flight Recorder (Java 11+, free)
-XX:+FlightRecorder
-XX:StartFlightRecording=duration=60s,filename=/path/to/recording.jfr
```

## Complete Real-World Example

Here's a production-ready command combining multiple options:

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

## Finding Available Options

```bash
# Standard options (start with -)
java -help

# Extended options (start with -X)
java -X

# Advanced options (start with -XX)
java -XX:+PrintFlagsFinal -version
```

This covers the essential Java command-line options you'll use for configuring memory, debugging, logging, and monitoring your applications.
