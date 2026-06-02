---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Control-M Client 9.20 vs 9.21 Differences
translated: false
type: note
---

**Question:** What is the difference between v9.20 and v9.21 in Control-M client on Windows?

**Answer:**

Control-M (by BMC) uses versioning like 9.0.20 (often abbreviated as 9.20) and 9.0.21 (9.21) for the entire suite, including **Control-M/Enterprise Manager (EM)**, Server, Agent, and the **desktop client** (Control-M GUI client on Windows).

The **Control-M client** on Windows is primarily the desktop application from the Control-M/EM installation package. It connects to the EM/Server and provides tools like the Configuration Control Manager (CCM) and job definition/monitoring interfaces.

### Key Differences Between 9.0.20 and 9.0.21 (Relevant to the Windows Client)
- **Users and Roles Management**: In 9.0.21, user authorizations and roles are now managed exclusively in **Control-M Web** (the browser-based interface). The classic Authorizations tool in the Control-M Configuration Manager (CCM, part of the desktop client) is no longer available. This is a significant change for administrators who previously used the desktop client for privilege management.
- **Compatibility and Connectivity**: The client from 9.0.21 can connect to older EM/Server versions (down to 9.0.19 in compatibility mode), but to access new 9.0.21 features (e.g., enhanced role-based access), the EM/Server must also be upgraded. Older clients (9.0.20) can connect to 9.0.21 EM but with limited functionality for new features.
- **Installation Changes**: Control-M/EM installation in 9.0.21 now includes additional components like SLA Management, Control-M/Forecast, and Self Service by default. The client installation on Windows may bundle more features or updated dependencies.
- **Other Client-Related Enhancements**:
  - Improved integration with **Control-M Automation API** (secrets protection, new token types).
  - Updated terminology alignment with Helix Control-M.
  - General bug fixes and security improvements (e.g., password encryption changes that prevent downgrading after upgrade).
- **No Major UI Overhaul Specific to the Desktop Client**: The core desktop client interface remains similar, but many new features (e.g., Workflow Insights dashboards, new plug-ins like Control-M for Airflow) are primarily in Control-M Web, encouraging a shift away from the desktop client for day-to-day operations.
- **Windows-Specific Notes**: No unique differences mentioned for the Windows client beyond general platform support. Both versions support Windows, with agents running as 64-bit only.

Overall, upgrading from 9.0.20 to 9.0.21 introduces **modernized authorization management** (moving to web-based) and encourages use of Control-M Web over the traditional desktop client, while adding backend enhancements in security, API, and plug-ins.

For detailed lists of all changes (including fixed issues and new features across the suite), refer to the official BMC release notes.

**References:**

- [What's New in Control-M 9.0.21](https://docs.bmc.com/docs/controlm/90201/what-s-new-in-control-m-9-0-21-1044383595.html)
- [Introducing Control-M 9.0.21 (Blog Summary)](https://www.dbi-services.com/blog/introducing-control-m-9-0-21/)
- [Control-M Compatibility for Version 9.0.21](https://docs.bmc.com/docs/controlm/90201/control-m-compatibility-for-version-9-0-21-1044383593.html)
- [What's New in Control-M 9.0.20](https://docs.bmc.com/docs/controlm/9020/what-s-new-in-control-m-9-0-20-900847340.html)
