---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Control-M 文件夹简介
translated: true
type: note
---

**Question:** 请对 Control-M 中的 folder 进行全面介绍。

**Answer:**

在 **Control-M**（来自 BMC 的 workload automation 和 job scheduling 工具）中，**folder** 是一个基础的组织容器，用于对相关的 **jobs**、**subfolders** 和 **flows**（依赖关系）进行分组。

Folder 通过逻辑分组、集中配置以及将设置继承给子对象（jobs 和 subfolders），帮助管理复杂的 workflows。

### Folder 的主要用途
- 将相关的 jobs 分组（按 application、部门、业务流程、地理位置、客户等）
- 在 folder 级别定义一次通用设置，而无需在每个 job 上重复定义
- 支持继承机制 → jobs 和 subfolders 会自动从其父级 folder 继承许多属性
- 为整个作业组支持复杂的 scheduling、prerequisites（events/resources）、执行后操作（post-execution actions）和 notifications
- 提高在大型环境中 workflows 的可见性、可维护性和理解度

### 主要 Folder 类型

| 类型 | 描述 | Scheduling & Inheritance | 最常见用例 |
|-------------------|-----------------------------------------------------------------------------|----------------------------------------------------|----------------------------------------|
| **SMART Folder** | 功能全备的 folder（默认且推荐的类型） | 在 folder 级别支持完整的 scheduling, events, resources 等 → 由 jobs/subfolders 继承 | 绝大多数生产环境 workflows |
| **Regular Folder** | 基础分组容器 | folder 级别不支持 scheduling/prerequisites 的继承 | 非常简单的静态分组 |
| **Simple Folder** | 极简容器（主要用于 Automation API / JSON 定义） | 不支持 folder 级别的配置 | 基于 API/脚本的简单部署 |
| **Subfolder** | 嵌套在另一个 folder 或 subfolder 内部的 folder | 继承父级 SMART folder 的大部分设置，但有一些限制 | 分层组织（例如：部门 → 团队 → 流程） |

在实际的 Control-M 实施中，绝大多数情况下都使用 **SMART folders**。

### 关键属性和设置（主要是 SMART Folders）

- **通用属性 (General attributes)**
  - Folder 名称（在 Control-M/Server 内必须唯一）
  - Description (描述)
  - Application / Sub-Application (逻辑标签)
  - Priority (优先级)
  - RunAs (默认用户/账号)
  - Time Zone (时区)
  - Site Standard (合规性标签)
  - Business fields (自定义元数据)

- **调度控制 (Scheduling / When)**
  - 星期、日期、月份
  - Rule-based calendars (RBC)，calendars
  - 特定日期、例外日期
  - Active retention 策略（非 OK 状态的 jobs 保留多长时间）
  - Order method：Automatic (daily) 或 Manual

- **前置条件 (Prerequisites - 控制 folder 是否可以启动)**
  - Events / Wait for events
  - Resources (quantitative, lock/mutex)
  - Host groups / Agents
  - 最大等待天数，确认日历 (confirmation calendars)

- **执行后操作 (Post-execution Actions)**
  - On OK / Not OK：shout messages, notifications, add/remove events, 运行纠正性 jobs, force OK 等

- **Flow / 依赖关系**
  - 在 folder 内部使用 Flow 对象定义（前续/后续关系）
  - 可以跨 subfolders 连接 jobs

- **Variables (变量)**
  - 可在 jobs 中使用的 folder 级别变量

- **其他**
  - Notifications
  - Rerun 设置
  - 调整 events 行为

### Folder → Job 继承规则 (SMART Folder)
大多数 folder 级别的定义（scheduling, events, resources, notifications, RunAs, Application, variables 等）会被以下对象**继承**：
- 直接位于该 folder 下的所有 jobs
- 所有 subfolders
- subfolders 内部的所有 jobs

需要时，你可以在 job 或 subfolder 级别覆盖任何继承的设置。

### 实际组织示例
- Finance_EndOfMonth (SMART Folder)
  - Finance_US (subfolder)
    - Process_Raw_Data
    - Calculate_Salaries
    - Update_GL
  - Finance_Australia (subfolder)
    - Process_Raw_Data
    - Calculate_Payroll
    - Update_GL

所有 jobs 都可以从顶级 folder 继承相同的 "End of Month" calendar 和 "wait for EOM confirmation event"。

### 总结 – 为什么 Folder 很重要
- 减少重复工作 → 只需定义一次 schedule, events, notifications
- 加强治理 → 统一的标签（Application, Business fields）
- 实现层级化 → 处理复杂的业务流程
- 使大型环境易于理解 → 用分组取代混乱

Folder（尤其是 SMART folder）是构建可维护、可扩展的 Control-M workflows 最重要的概念之一。

**References:**

- [Introduction to Control-M - BMC Documentation](https://documents.bmc.com/supportu/9.0.21/en-US/Documentation/Introduction_to.htm)
- [Folders and Flows - Control-M SaaS Automation API](https://docs.bmc.com/docs/saas-api/folders-and-flows-941879023.html)
- [Creating a Folder - BMC Documentation](https://documents.bmc.com/supportu/controlm-saas/en-US/Documentation/Creating_a_Folder.htm)
- [Folder - Control-M Automation API Documentation](https://docs.bmc.com/docs/automation-api/9191/folder-869560598.html)
