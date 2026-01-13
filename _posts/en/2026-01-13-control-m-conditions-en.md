---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Understanding Control-M IN and OUT Conditions
translated: false
type: note
---

**Question:** How do conditions work in Control-M, including what IN and OUT conditions are?

**Answer:**

In Control-M (a workload automation/scheduling tool from BMC), **conditions** (also called **prerequisite conditions** or **events**) are the primary way to create dependencies between jobs. They act as flags or signals in the system to control job execution order.

### Core Concept
- A job will not run until **all** of its **IN conditions** are satisfied (i.e., they exist in the active environment).
- When a job completes (usually successfully), it can create or remove conditions via its **OUT conditions**.

### IN Conditions (Prerequisites / "wait for")
- These are the conditions a job **requires** before it can be submitted for execution.
- Defined in the job's definition (Conditions tab or IN conditions section).
- A job waits in **Wait Condition** status if any IN condition is missing.
- Common format: `JOB1-OK` or `DAILY-START-OK`.
- Date handling: Often use `ODAT` (Original Scheduling Date) or specific dates like `PREV`, `NEXT`, or explicit YYMMDD.
- Special types:
  - **Maybe conditions** (prefixed with `#-` or similar in some versions) — optional dependencies; Control-M can "fake" them if the predecessor isn't scheduled.
- Multiple IN conditions act as AND logic (all must be present).

### OUT Conditions (Signals / "post")
- These are the conditions a job **adds** or **removes** when it finishes.
- Defined with a **sign**:
  - **+** (ADD / plus sign): Adds/creates the condition (most common for signaling success).
  - **-** (DELETE / minus sign): Removes/deletes the condition (often used to clean up after a downstream job finishes).
- Typically placed in post-processing rules or directly in the OUT conditions section.
- Common pattern:
  - Job A: OUT condition `JOB-A-OK +` (adds it on success).
  - Job B: IN condition `JOB-A-OK` → waits for Job A to succeed.
  - Job B: OUT condition `JOB-A-OK -` → removes it after Job B finishes (prevents stale conditions).

### Typical Flow Example
1. Job A runs and ends OK → adds `JOB-A-OK` (OUT +).
2. Job B has IN condition `JOB-A-OK` → now becomes eligible and runs.
3. Job B ends OK → deletes `JOB-A-OK` (OUT -) to clean up.

### Related Concepts
- **Global Conditions**: Static or long-lived conditions not tied to specific jobs (managed via Tools → Global Conditions).
- **Resources** (separate from conditions):
  - **Quantitative Resources** (now often called Resource Pools): Limit concurrent usage (e.g., 5 database connections → jobs require 1 unit each).
  - **Control Resources**: Exclusive or shared access (e.g., lock a file/table).
- Conditions are stored in the Control-M server's Conditions table/database.
- You can view/add/delete conditions manually in Control-M/EM (Planning or Monitoring domain) or via utilities like `ctmcontb`.
- In flows, conditions appear as arrows/links in the graphic view.

This mechanism enables complex workflows like job chaining, fan-in/fan-out, and conditional paths without needing scripts in many cases.

**References:**

- [Introduction to Control-M - BMC Documentation](https://documents.bmc.com/supportu/INC/9.0.21/en-US/Control-M_for_zOS_Getting_Started_Guide/Introduction_to_Control-M.htm)
- [Prerequisite Conditions explanation](http://www.ctmguru.com/2012/02/prerequisite-conditions.html)
- [Stack Overflow discussions on Control-M conditions](https://stackoverflow.com/questions/66812246/control-m-out-condition-added-with-number-at-the-end)