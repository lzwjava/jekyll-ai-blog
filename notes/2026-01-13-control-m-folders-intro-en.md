---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Introduction to Control-M Folders
translated: false
type: note
---

**Question:** Give a comprehensive introduction to folders in Control-M.

**Answer:**

In **Control-M** (a workload automation and job scheduling tool from BMC), a **folder** is a fundamental organizational container used to group related **jobs**, **subfolders**, and **flows** (dependencies).

Folders help manage complex workflows by allowing logical grouping, centralized configuration, and inheritance of settings to child objects (jobs and subfolders).

### Main Purposes of Folders
- Group related jobs together (by application, department, business process, geography, customer, etc.)
- Define common settings once at the folder level instead of repeating them on every job
- Enable inheritance → jobs and subfolders automatically inherit many properties from their parent folder
- Support complex scheduling, prerequisites (events/resources), post-execution actions, and notifications for entire groups of jobs
- Improve visibility, maintainability, and understanding of workflows in large environments

### Main Folder Types

| Type              | Description                                                                 | Scheduling & Inheritance                          | Most Common Use Case                  |
|-------------------|-----------------------------------------------------------------------------|----------------------------------------------------|----------------------------------------|
| **SMART Folder**  | Full-featured folder (default and recommended type)                        | Supports full scheduling, events, resources, etc. at folder level → inherited by jobs/subfolders | Most production workflows             |
| **Regular Folder** | Basic grouping container                                                    | No inheritance of scheduling/prerequisites from folder level | Very simple static groupings          |
| **Simple Folder**  | Minimal container (mainly used in Automation API / JSON definitions)       | No folder-level configuration possible             | API/script-based simple deployments   |
| **Subfolder**      | Folder nested inside another folder or subfolder                           | Inherits most settings from parent SMART folder, but has some limitations | Hierarchical organization (e.g. Dept → Team → Process) |

**SMART folders** are used in the vast majority of real-world Control-M implementations.

### Key Properties and Settings (mainly SMART Folders)

- **General attributes**
  - Folder name (must be unique within Control-M/Server)
  - Description
  - Application / Sub-Application (logical tagging)
  - Priority
  - RunAs (default user/account)
  - Time Zone
  - Site Standard (compliance tagging)
  - Business fields (custom metadata)

- **Scheduling (When)**
  - Days of week, month days, months
  - Rule-based calendars (RBC), calendars
  - Specific dates, exceptions
  - Active retention policy (how long to keep non-ok jobs active)
  - Order method: Automatic (daily) or Manual

- **Prerequisites (controls whether folder can start)**
  - Events / Wait for events
  - Resources (quantitative, lock/mutex)
  - Host groups / Agents
  - Max days to wait, confirmation calendars

- **Post-execution Actions**
  - On OK / Not OK: shout messages, notifications, add/remove events, run corrective jobs, force OK, etc.

- **Flow / Dependencies**
  - Defined inside folder using Flow object (predecessor → successor relationships)
  - Can connect jobs across subfolders

- **Variables**
  - Folder-level variables that can be used in jobs

- **Other**
  - Notifications
  - Rerun settings
  - Adjust events behavior

### Folder → Job Inheritance Rules (SMART Folder)
Most folder-level definitions (scheduling, events, resources, notifications, RunAs, Application, variables, etc.) are **inherited** by:
- All jobs directly in the folder
- All subfolders
- All jobs inside subfolders

You can override any inherited setting at the job or subfolder level when needed.

### Practical Organization Examples
- Finance_EndOfMonth (SMART Folder)
  - Finance_US (subfolder)
    - Process_Raw_Data
    - Calculate_Salaries
    - Update_GL
  - Finance_Australia (subfolder)
    - Process_Raw_Data
    - Calculate_Payroll
    - Update_GL

All jobs can inherit the same "End of Month" calendar and "wait for EOM confirmation event" from the top-level folder.

### Summary – Why Folders Matter
- Reduce duplication → define schedule, events, notifications once
- Improve governance → consistent tagging (Application, Business fields)
- Enable hierarchy → complex business processes
- Make large environments understandable → grouping replaces chaos

Folders (especially SMART folders) are one of the most important concepts for building maintainable, scalable Control-M workflows.

**References:**

- [Introduction to Control-M - BMC Documentation](https://documents.bmc.com/supportu/9.0.21/en-US/Documentation/Introduction_to.htm)
- [Folders and Flows - Control-M SaaS Automation API](https://docs.bmc.com/docs/saas-api/folders-and-flows-941879023.html)
- [Creating a Folder - BMC Documentation](https://documents.bmc.com/supportu/controlm-saas/en-US/Documentation/Creating_a_Folder.htm)
- [Folder - Control-M Automation API Documentation](https://docs.bmc.com/docs/automation-api/9191/folder-869560598.html)