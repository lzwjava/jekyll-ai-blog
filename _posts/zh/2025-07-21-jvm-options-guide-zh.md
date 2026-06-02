---
audio: false
generated: true
image: false
lang: zh
layout: post
title: JVM 选项分类速查指南
translated: true
type: note
---

在 JVM 生态中，存在**众多可配置选项**，具体选项集取决于 JVM 实现（HotSpot、OpenJ9、GraalVM 等）及版本。总体而言，JVM 选项可分为以下几类：

---

## 1. 标准选项

这些是稳定且跨版本的官方文档化选项，保证可用。例如：

* `-classpath` / `-cp` → 指定类路径
* `-Dproperty=value` → 设置系统属性
* `-version` → 输出 JVM 版本信息
* `-Xms` / `-Xmx` → 初始堆大小与最大堆大小
* `-ea` → 启用断言检查

---

## 2. 非标准选项（`-X`前缀）

这些是 JVM 特定实现选项，不保证长期稳定性。示例（HotSpot）：

* `-Xint` → 纯解释模式（禁用 JIT）
* `-Xcomp` → 首次使用时编译所有方法
* `-Xbatch` → 禁用后台编译
* `-Xss512k` → 设置线程栈大小

---

## 3. 高级选项（`-XX`前缀）

这些选项提供针对垃圾回收、即时编译与运行时行为的细粒度调优。示例：

* `-XX:+UseG1GC` → 启用 G1 垃圾收集器
* `-XX:+PrintGCDetails` → 记录垃圾回收活动详情
* `-XX:MaxMetaspaceSize=256m` → 设置元空间容量上限
* `-XX:+HeapDumpOnOutOfMemoryError` → 发生内存溢出时生成堆转储
* `-XX:+UnlockExperimentalVMOptions` → 启用实验性参数
* `-XX:+UseStringDeduplication` → 通过字符串去重降低内存占用

---

## 4. 诊断与实验性选项

部分参数需要解锁才能使用：

* `-XX:+UnlockDiagnosticVMOptions` → 启用诊断参数
* `-XX:+UnlockExperimentalVMOptions` → 允许实验性调优

解锁后可使用的选项示例：

* `-XX:+PrintFlagsFinal` → 列出所有 JVM 参数及其取值
* `-XX:+LogCompilation` → 记录即时编译活动

---

## 5. JVM 参数管理工具

* **`java -X`** → 列出当前 JVM 版本支持的非标准选项
* **`java -XX:+PrintFlagsFinal`** → 输出所有可识别参数及其默认值与当前值
* **`jcmd <pid> VM.flags`** → 查看运行中进程的 JVM 参数
* **`jcmd <pid> VM.uptime`**、`jcmd <pid> VM.system_properties` → 运行时状态检查
* **`jps` + `jinfo`** → 列出 Java 进程并查看 JVM 参数
* **VisualVM / JConsole** → 监控堆内存、垃圾回收及运行时参数

---

👉 探索当前环境的实用方法：

```bash
java -XX:+PrintFlagsFinal | grep GC
```

查看所有垃圾回收相关选项，或直接执行：

```bash
java -X
```

查看可用的非标准参数。

---

是否需要我为您整理**最实用 JVM 参数分类速查表**（涵盖垃圾回收、内存管理、调试与性能调优），避免您手动解析冗长的 `PrintFlagsFinal` 输出列表？
