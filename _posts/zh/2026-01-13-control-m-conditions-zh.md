---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 理解 Control-M 入口和出口条件
translated: true
type: note
---

**Question:** How do conditions work in Control-M, including what IN and OUT conditions are?

**Answer:**

在 Control-M（由 BMC 开发的 workload automation/scheduling 调度工具）中，**conditions**（也称为 **prerequisite conditions** 或 **events**）是创建 Job 之间依赖关系的主要方式。它们在系统中充当标记或信号，用以控制 Job 的执行顺序。

### Core Concept

- 只有在其 **IN conditions** 全部满足（即存在于当前活动环境中）时，Job 才会运行。
- 当 Job 完成（通常是成功完成）时，它可以通过其 **OUT conditions** 创建或删除 conditions。

### IN Conditions (Prerequisites / "wait for")

- 这些是 Job 在被提交执行之前**必须具备**的 conditions。
- 在 Job 定义中定义（Conditions 选项卡或 IN conditions 部分）。
- 如果任何 IN condition 缺失，Job 将保持 **Wait Condition** 状态。
- 常见格式：`JOB1-OK` 或 `DAILY-START-OK`。
- 日期处理：通常使用 `ODAT` (Original Scheduling Date) 或特定日期如 `PREV`, `NEXT` 或明确的 YYMMDD。
- 特殊类型：
    - **Maybe conditions**（在某些版本中以前缀 `#-` 或类似符号表示）—— 可选依赖项；如果前置 Job 未被调度，Control-M 可以“模拟”它们。
- 多个 IN conditions 遵循 AND 逻辑（必须全部存在）。

### OUT Conditions (Signals / "post")

- 这些是 Job 结束时**添加**或**删除**的 conditions。
- 定义时带有符号（**sign**）：
    - **+** (ADD / 加号)：添加/创建 condition（最常用于传递成功信号）。
    - **-** (DELETE / 减号)：移除/删除 condition（通常用于在下游 Job 完成后进行清理）。
- 通常放置在 post-processing 规则或直接定义在 OUT conditions 部分中。
- 常见模式：
    - Job A：OUT condition `JOB-A-OK +`（成功后添加）。
    - Job B：IN condition `JOB-A-OK` → 等待 Job A 成功。
    - Job B：OUT condition `JOB-A-OK -` → 在 Job B 完成后将其删除（防止过时的 conditions 留存）。

### Typical Flow Example

1. Job A 运行并以 OK 结束 → 添加 `JOB-A-OK` (OUT +)。
2. Job B 拥有 IN condition `JOB-A-OK` → 现在符合条件并运行。
3. Job B 以 OK 结束 → 删除 `JOB-A-OK` (OUT -) 以进行清理。

### Related Concepts

- **Global Conditions**：不与特定 Job 绑定的静态或长效 conditions（通过 Tools → Global Conditions 管理）。
- **Resources**（与 conditions 不同）：
    - **Quantitative Resources**（现在常称为 Resource Pools）：限制并发使用（例如，5 个 database connections → 每个 Job 需要 1 个单位）。
    - **Control Resources**：独占或共享访问（例如，锁定文件或表）。
- Conditions 存储在 Control-M server 的 Conditions table/database 中。
- 可以在 Control-M/EM (Planning 或 Monitoring 域) 手动查看/添加/删除 conditions，或通过 `ctmcontb` 等 utility 进行操作。
- 在流程图中，conditions 在图形视图中显示为箭头/连线。

这种机制使得复杂的 workflow（如 job chaining、fan-in/fan-out 和 conditional paths）在许多情况下无需编写脚本即可实现。

**References:**

- [Introduction to Control-M - BMC Documentation](https://documents.bmc.com/supportu/INC/9.0.21/en-US/Control-M_for_zOS_Getting_Started_Guide/Introduction_to_Control-M.htm)
- [Prerequisite Conditions explanation](http://www.ctmguru.com/2012/02/prerequisite-conditions.html)
- [Stack Overflow discussions on Control-M conditions](https://stackoverflow.com/questions/66812246/control-m-out-condition-added-with-number-at-the-end)
