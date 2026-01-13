---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 理解经典的 Control-M XML 定义
translated: true
type: note
---

**Question:** 如何理解 Control-M XML？

**Answer:**

Control-M XML 文件是以结构化格式定义的 **job scheduling definitions**（包括 jobs、folders、SMART folders、calendars 等），供 Control-M/Enterprise Manager (Control-M/EM) 的实用程序（如 `defjob`、`exportdefjob`、`updatedef` 等）使用。

这些文件是 **plain text XML**，并遵循 Control-M 的特定 schema（在旧版本中通常通过 `.dtd` 文件进行验证）。

### Control-M XML 的两种主要上下文（注意区分）

1. **Classic Control-M/EM XML**（较旧版本，9.0.20 之前，目前仍广泛使用）
   - 与以下实用程序配合使用：`emdef`、`defjob`、`exportdefjob`、`copydefjob` 等。
   - 结构使用大写标签，如 `<JOB>`、`<FOLDER>`、`<INCOND>`、`<OUTCOND>`、`<AUTOEDIT2>`、`<DOMAIL>` 等。
   - 通过属性（Attributes）定义参数（例如 `JOBNAME="MyJob"`、`NODEID="agent-host"`）。

   典型的根元素：
   - `<JOB>`
   - `<FOLDER>` 或 `<SMART_FOLDER>`
   - `<CALENDAR>`

   常见的子元素：
   - Scheduling（调度）：`<DAYS>`、`<WEEKDAYS>`、`<MONTHS>`、`<CAL rule-based calendars>`
   - Dependencies（依赖）：`<INCOND>`、`<OUTCOND>`
   - Execution（执行）：`<CMDLINE>`、`<SCRIPTNAME>`、`<NODEID>`、`<CREATOR>`
   - On-do actions（后续操作）：`<ON CODE="COMPSTAT=0">`、`<DO MAIL>`、`<DO OK>`
   - Variables（变量）：`<AUTOEDIT2 NAME="%%VAR" VALUE="value"/>`

2. **Modern Control-M JSON / Automation API 风格**（Control-M 9.0.18+、SaaS、Automation API）
   - 使用 **JSON** 而非 XML（尽管早期存在 XML 支持，但现在多处已废弃）。
   - 结构：`"Type": "Job:Command"`、`"Command": "echo hello"`、`"RunAs": "user1"` 等。
   - Folders/jobs 被定义为嵌套的 JSON 对象。

如果你的 XML 文件以 `<JOB JOBNAME="..." ...>` 这样的标签开头，那么它属于 **classic XML format**。

### 如何理解/读取 Classic Control-M XML

**分步操作方法**

1. **使用优秀的编辑器打开**
   - 如 VS Code、Notepad++、IntelliJ、Oxygen XML Editor 等。
   - 开启 XML 语法高亮和折叠功能。

2. **查看顶级结构**
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <JOB
       JOBNAME="MyApp_Daily_Report"
       TABLENAME="DAILY"
       APPLGROUP="Finance"
       APPLIC="Reporting"
       NODEID="server-prod-01"
       ...
   >
       <CMDLINE>run_report.sh</CMDLINE>
       ...
   </JOB>
   ```

   或者 Folder 样式：
   ```xml
   <FOLDER NAME="Finance_Daily">
       <JOB ...> ... </JOB>
       <JOB ...> ... </JOB>
   </FOLDER>
   ```

3. **需关注的核心部分**
   - **Identification（识别）** — JOBNAME、TABLENAME (table/dataset)、APPLGROUP、APPLIC、DESC
   - **Agent / Execution（执行）** — NODEID (agent)、CREATOR、RUN_AS、CMDLINE / SCRIPTNAME / TASKTYPE
   - **Scheduling（调度）** — DAYS、WEEKDAYS、MONTH、DATES、CAL rules
   - **Prerequisites（前置条件）** — INCOND（等待这些 condition）
   - **Outcome（输出结果）** — OUTCOND（完成后设置这些 condition）
   - **On actions（触发操作）** — ON CODE="..." DO MAIL / SHOUT / OK / NOTOK / RERUN / ...
   - **AutoEdit 变量** — `<AUTOEDIT2 NAME="%%MY_VAR" VALUE="xyz"/>`

4. **使其更具可读性的实用方法**
   - 导入到 Control-M/EM Planning 域 → **File → Open**（或拖拽 XML）→ 以图形化界面查看。
   - 使用 **Control-M Desktop**（旧版本）或 **Control-M Workbench**。
   - 从 Planning 域导出到 workspace XML → 先通过视觉直观读取。
   - 套用 XSLT 样式表（如果能找到旧的社区版本）将其转换为 HTML。

### 快速映射表（Classic XML → 含义）

| XML 标签/属性 | 含义 / 对应 GUI 术语 |
|-------------------------|----------------------------------------------|
| JOBNAME                 | Job 名称                                     |
| TABLENAME               | Table / Data set 名称                        |
| APPLGROUP               | Group                                        |
| NODEID                  | 在 Agent / Host 上运行                       |
| INCOND NAME=... SIGN=DEL| 等待 Condition（前置任务）                   |
| OUTCOND NAME=... SIGN=ADD| 创建 Condition（后继任务触发器）             |
| AUTOEDIT2               | AutoEdit 变量 (%%VAR)                        |
| ON CODE="COMPSTAT≠0"    | If 操作：当任务失败 / 特定返回码时           |
| DOMAIL                  | 发送邮件通知                                 |

**注意：** 自 2022–2024 年起，BMC 已在多处（Automation API、导出等）逐步废弃 XML，转而采用 **JSON**。如果你正在开展新工作，建议优先通过 Automation API 使用 JSON 定义。

**参考资料：**

- [XML File Rules (BMC 文档)](https://documents.bmc.com/supportu/9.0.21.000/en-US/Documentation/Utilities/XML_File_Rules.htm)
- [defjob 实用程序 (classic XML 导入)](https://controlm.wisconsin.gov/help/CTMHelp/en-US/Documentation/Utilities/defjob.htm)
- [Job Properties – Automation API (JSON 风格对比)](https://docs.bmc.com/docs/automation-api/9191/job-properties-869560601.html)
- [XML 废弃通知](https://docs.bmc.com/xwiki/bin/view/Control-M-Orchestration/Control-M/Announcements/Deprecation-and-End-of-Support/XML-Format-Deprecation)