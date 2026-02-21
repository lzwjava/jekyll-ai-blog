---
audio: false
generated: true
image: false
lang: en
layout: post
title: Distribution Groups in Windows Server
translated: false
type: note
---

Question: In a Windows Server 2003 environment, which group type is used exclusively for distributing email and does not have security enabled?

Answer: 

The correct answer is **C. Distribution Group** (通信组).

### Detailed Explanation:

In Windows Server 2003 (and subsequent versions), there are two primary types of groups based on their usage:

1.  **Security Groups (安全组)**:
    *   **Purpose**: Used to assign permissions to resources (files, folders, printers) and to grant user rights.
    *   **Security Enabled**: Yes. They have a Security Identifier (SID) and can be used in Access Control Lists (ACLs).
    *   **Email Capability**: They *can* be used for email distribution if the environment includes Microsoft Exchange Server, but their primary definition is security-related.

2.  **Distribution Groups (通信组)**:
    *   **Purpose**: Used **exclusively** for sending emails to a collection of users.
    *   **Security Enabled**: **No**. They do not have a SID and cannot be used to assign permissions or user rights. Using them for security purposes is impossible.
    *   **Email Capability**: This is their sole function.

### Analysis of Other Options:
*   **A. Security Group**: Incorrect because it is security-enabled.
*   **B. Global Group**: Incorrect. "Global" refers to the **scope** of the group (where the members can come from and where the group can be used), not its **type**. A Global Group can be either a Security Group or a Distribution Group. Therefore, being "Global" does not inherently mean it lacks security capabilities.
*   **D. Local Group**: Incorrect. Similar to "Global," "Local" (usually referred to as Domain Local in Active Directory) is a **scope**, not a type. It can also be security-enabled.

### Conclusion:
The question specifically asks for the group **type** that is used *only* for email and has *no* security enabled. That definition matches **Distribution Groups** perfectly.

References:
- [Microsoft Learn: Groups](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/understand-groups)