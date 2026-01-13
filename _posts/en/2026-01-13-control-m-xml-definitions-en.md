---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Understanding Classic Control-M XML Definitions
translated: false
type: note
---

**Question:** How to understand Control-M XML?

**Answer:**

Control-M XML files define **job scheduling definitions** (jobs, folders, SMART folders, calendars, etc.) in a structured format used by Control-M/Enterprise Manager (Control-M/EM) utilities like `defjob`, `exportdefjob`, `updatedef`, and others.

These files are **plain text XML** and follow Control-M's specific schema (historically validated against `.dtd` files in older versions).

### Two Main Contexts for Control-M XML (important to distinguish)

1. **Classic Control-M/EM XML** (older versions, pre ~9.0.20, still widely used)
   - Used with utilities: `emdef`, `defjob`, `exportdefjob`, `copydefjob`, etc.
   - Structure uses uppercase tags like `<JOB>`, `<FOLDER>`, `<INCOND>`, `<OUTCOND>`, `<AUTOEDIT2>`, `<DOMAIL>`, etc.
   - Attributes define parameters (e.g. `JOBNAME="MyJob"`, `NODEID="agent-host"`)

   Typical root elements:
   - `<JOB>`
   - `<FOLDER>` or `<SMART_FOLDER>`
   - `<CALENDAR>`

   Common child elements:
   - Scheduling: `<DAYS>`, `<WEEKDAYS>`, `<MONTHS>`, `<CAL rule-based calendars>`
   - Dependencies: `<INCOND>`, `<OUTCOND>`
   - Execution: `<CMDLINE>`, `<SCRIPTNAME>`, `<NODEID>`, `<CREATOR>`
   - On-do actions: `<ON CODE="COMPSTAT=0">`, `<DO MAIL>`, `<DO OK>`
   - Variables: `<AUTOEDIT2 NAME="%%VAR" VALUE="value"/>`

2. **Modern Control-M JSON / Automation API style** (Control-M 9.0.18+, SaaS, Automation API)
   - Uses **JSON**, not XML (although XML support existed earlier and is now deprecated in many places)
   - Structure: `"Type": "Job:Command"`, `"Command": "echo hello"`, `"RunAs": "user1"`, etc.
   - Folders/jobs defined as nested JSON objects

If your XML file starts with tags like `<JOB JOBNAME="..." ...>`, it's the **classic XML format**.

### How to Understand / Read Classic Control-M XML

**Step-by-step approach**

1. **Open in a good editor**
   - VS Code, Notepad++, IntelliJ, Oxygen XML Editor, etc.
   - Use XML syntax highlighting and folding

2. **Look at the top-level structure**
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

   or folder style:
   ```xml
   <FOLDER NAME="Finance_Daily">
       <JOB ...> ... </JOB>
       <JOB ...> ... </JOB>
   </FOLDER>
   ```

3. **Key sections to focus on**
   - **Identification** — JOBNAME, TABLENAME (table/dataset), APPLGROUP, APPLIC, DESC
   - **Agent / Execution** — NODEID (agent), CREATOR, RUN_AS, CMDLINE / SCRIPTNAME / TASKTYPE
   - **Scheduling** — DAYS, WEEKDAYS, MONTH, DATES, CAL rules
   - **Prerequisites** — INCOND (waits for these conditions)
   - **Outcome** — OUTCOND (sets these conditions when finished)
   - **On actions** — ON CODE="..." DO MAIL / SHOUT / OK / NOTOK / RERUN / ...
   - **AutoEdit variables** — `<AUTOEDIT2 NAME="%%MY_VAR" VALUE="xyz"/>`

4. **Practical ways to make it readable**
   - Load into Control-M/EM Planning domain → **File → Open** (or drag & drop XML) → view graphically
   - Use **Control-M Desktop** (older versions) or **Control-M Workbench**
   - Export from Planning domain to workspace XML → easier to read visually first
   - Apply an XSLT stylesheet (if you can find an old community one) to convert to HTML

### Quick Mapping Table (classic XML → meaning)

| XML Tag/Attribute       | Meaning / Equivalent in GUI                  |
|-------------------------|----------------------------------------------|
| JOBNAME                 | Job name                                     |
| TABLENAME               | Table / Data set name                        |
| APPLGROUP               | Group                                        |
| NODEID                  | Run on Agent / Host                          |
| INCOND NAME=... SIGN=DEL| Waits for condition (predecessor)            |
| OUTCOND NAME=... SIGN=ADD| Creates condition (successor trigger)       |
| AUTOEDIT2               | AutoEdit variable (%%VAR)                    |
| ON CODE="COMPSTAT≠0"    | If action: when job fails / specific code    |
| DOMAIL                  | Send email notification                      |

**Note:** Since ~2022–2024, BMC has been deprecating XML in many places (Automation API, exports, etc.) in favor of **JSON**. If you're starting new work, prefer JSON definitions via Automation API.

**References:**

- [XML File Rules (BMC documentation)](https://documents.bmc.com/supportu/9.0.21.000/en-US/Documentation/Utilities/XML_File_Rules.htm)
- [defjob utility (classic XML import)](https://controlm.wisconsin.gov/help/CTMHelp/en-US/Documentation/Utilities/defjob.htm)
- [Job Properties – Automation API (JSON style comparison)](https://docs.bmc.com/docs/automation-api/9191/job-properties-869560601.html)
- [XML Deprecation Notice](https://docs.bmc.com/xwiki/bin/view/Control-M-Orchestration/Control-M/Announcements/Deprecation-and-End-of-Support/XML-Format-Deprecation)