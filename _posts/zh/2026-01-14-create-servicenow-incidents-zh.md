---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 如何创建 ServiceNow 事件
translated: true
type: note
---

**Question:** 如何在 ServiceNow 中提交 Incident？

**Answer:**

以下是截至 2026 年在 ServiceNow 中**提交（创建）Incident** 的最常用方法。具体步骤和可用选项取决于您所在组织的配置、角色（最终用户 vs Agent）以及您使用的是 Employee Center、Service Portal、ITSM Agent Workspace 还是移动端 App。

### 1. 作为最终用户（员工/请求者最常用的方式）

- 登录您公司的 **ServiceNow portal**（通常称为 Employee Center、Service Portal 或自定义名称，如 `yourcompany.service-now.com`）。
- 查找以下选项：
  - **Report an Issue** / **Create Incident** / **Report IT Problem** / **Something's broken**
- 点击该按钮或卡片以开始创建新的 Incident。
- 填写主要字段：
  - **Short description** — 清晰、简洁的标题（必填）
  - **Description** — 发生情况的详细说明
  - **Category** / **Subcategory**（如果显示）
  - **Affected CI** / **Configuration item**（受影响的电脑、Application、Service 等）
  - **Urgency** / **Impact**（有助于设定 Priority）
  - **Location** / **Assignment group**（有时会自动填充或支持搜索）
  - 附件（截图、错误信息、Logs — 非常有用）
- （可选）将其关联到某个 Service 或添加 watch list 用户。
- 点击 **Submit** / **Create** / **Submit Incident**。

提交后，您通常会收到一个 Ticket 编号（例如 INC0012345）和确认信息。

### 2. 作为 IT Agent / Service Desk（使用 Agent Workspace 或 Platform）

- 登录 **ServiceNow platform**（访问 `yourcompany.service-now.com/navpage.do` 或直接进入 Workspace）。
- 在 **Agent Workspace**（大多数现代配置）中：
  - 点击页眉中的 **+** (Create New) → 选择 **Incident**
  - 或者转到 **Incidents → Create New**
- 在经典 UI 中：
  - 在 Application Navigator 中导航至 **Incident → Create New**。
- 填写表单（字段与上述类似，但 Agent 通常会看到更多技术字段）：
  - **Caller** — 通常是受影响的用户
  - **Short description** 和 **Description**
  - **Category**、**Subcategory**、**Cause**
  - **Configuration item** (CI)
  - **Priority** / **Urgency** / **Impact**
  - **Assignment group** 和 **Assigned to**
  - Business service、Location 等
- 保存 (Save) 或提交 (Submit)。

### 3. 其他常用创建方式

- **通过 Email** — 许多组织允许发送邮件至 `incident@yourcompany.service-now.com`（邮件主题变为 Short description，正文变为 Description）。
- **通过 Virtual Agent / Now Assist chat** — 输入 "create incident" 或描述问题 → 机器人会引导您完成创建。
- **从 Interaction / CSM Case** — Agent 可以转换或提交关联的 Incident。
- **通过 API / Integration** — 对于监控工具（如 Splunk、SolarWinds、PagerDuty），Alerts 可以自动创建 Incident。

**快速解决问题的技巧：**
- 提供**清晰的复现步骤**、业务影响和截图。
- 选择**正确的 Category**，以便将其分配给正确的团队。
- 先查看 **Self-service knowledge articles** — 许多公司要求在创建 Incident 之前先搜索 KB。

用户界面和必填字段因公司而异，因此如果上述步骤与您的实例不符，请查看您的内部 IT Support 页面或咨询您的 ServiceNow 管理员以获取确切流程。

**References:**

- [Create an incident (ServiceNow Docs)](https://docs.servicenow.com/bundle/utah-it-service-management/page/product/incident-management/task/create-an-incident.html)
- [ServiceNow Community - Incident Creation Discussions](https://www.servicenow.com/community)