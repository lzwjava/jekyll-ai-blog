---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Windows Server 中的分发组
translated: true
type: note
---

问题：在 Windows Server 2003 环境中，哪种组类型专门用于分发电子邮件且不启用安全功能？

答案：

正确答案是 **C. Distribution Group**（通信组）。

### 详细说明：

在 Windows Server 2003（及后续版本）中，根据用途可将组分为两种主要类型：

1. **Security Groups（安全组）**：
   * **用途**：用于分配资源（文件、文件夹、打印机）的权限，并授予用户权利。
   * **启用安全功能**：是。它们具有安全标识符（SID），可用于访问控制列表（ACL）。
   * **电子邮件功能**：在包含 Microsoft Exchange Server 的环境中*可以*用于电子邮件分发，但其主要定义与安全相关。

2. **Distribution Groups（通信组）**：
   * **用途**：**专门**用于向一组用户发送电子邮件。
   * **启用安全功能**：**否**。它们没有 SID，无法用于分配权限或用户权利，也无法用于安全目的。
   * **电子邮件功能**：这是其唯一功能。

### 其他选项分析：
* **A. Security Group**：错误，因为它启用了安全功能。
* **B. Global Group**：错误。“Global”指的是组的**范围**（成员来源和组使用范围），而非**类型**。Global Group 可以是 Security Group 或 Distribution Group。因此，“Global”并不意味着其本身不具备安全功能。
* **D. Local Group**：错误。类似“Global”，“Local”（在 Active Directory 中通常称为 Domain Local）是**范围**而非类型，且可启用安全功能。

### 结论：
题目特别询问**类型**为仅用于电子邮件且**不启用安全功能**的组，其定义与 **Distribution Groups** 完全匹配。

参考：
- [Microsoft Learn: Groups](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/understand-groups)