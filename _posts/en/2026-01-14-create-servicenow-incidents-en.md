---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: How to Create ServiceNow Incidents
translated: false
type: note
---

**Question:** How to raise an incident in ServiceNow?

**Answer:**

Here are the most common ways to **raise (create) an incident** in ServiceNow as of 2026. The exact steps and available options depend on your organization's configuration, role (end-user vs. agent), and whether you're using the Employee Center, Service Portal, ITSM Agent Workspace, or mobile app.

### 1. As an End User (Most Common for Employees/Requestors)

- Log in to your company's **ServiceNow portal** (usually called Employee Center, Service Portal, or a custom name like `yourcompany.service-now.com`).
- Look for options such as:
  - **Report an Issue** / **Create Incident** / **Report IT Problem** / **Something's broken**
- Click the button/tile to start a new incident.
- Fill in the main fields:
  - **Short description** — a clear, concise title (mandatory)
  - **Description** — detailed explanation of what happened
  - **Category** / **Subcategory** (if shown)
  - **Affected CI** / **Configuration item** (the computer, application, service, etc.)
  - **Urgency** / **Impact** (helps set priority)
  - **Location** / **Assignment group** (sometimes pre-filled or searchable)
  - Attachments (screenshots, error messages, logs — very helpful)
- (Optional) Link it to a service or add watch list users.
- Click **Submit** / **Create** / **Submit Incident**.

After submission, you'll usually receive a ticket number (e.g., INC0012345) and a confirmation.

### 2. As an IT Agent / Service Desk (using Agent Workspace or platform)

- Log in to the **ServiceNow platform** (navigate to `yourcompany.service-now.com/navpage.do` or directly to workspace).
- In **Agent Workspace** (most modern setups):
  - Click **+** (Create New) in the header → choose **Incident**
  - Or go to **Incidents → Create New**
- In classic UI:
  - Navigate to **Incident → Create New** in the application navigator.
- Fill in the form (similar fields as above, but agents usually see many more technical fields):
  - **Caller** — usually the affected user
  - **Short description** and **Description**
  - **Category**, **Subcategory**, **Cause**
  - **Configuration item** (CI)
  - **Priority** / **Urgency** / **Impact**
  - **Assignment group** and **Assigned to**
  - Business service, location, etc.
- Save or Submit.

### 3. Other Common Creation Methods

- **From email** — many organizations allow sending an email to `incident@yourcompany.service-now.com` (subject becomes short description, body becomes description).
- **From Virtual Agent / Now Assist chat** — type "create incident" or describe the issue → bot guides you through creation.
- **From an Interaction / CSM Case** — agents can convert or raise linked incidents.
- **Via API / Integration** — for monitoring tools (e.g., Splunk, SolarWinds, PagerDuty), alerts automatically create incidents.

**Tips for faster resolution:**

- Provide **clear reproduction steps**, business impact, and screenshots.
- Choose the **correct category** so it routes to the right team.
- Use **self-service knowledge articles** first — many companies require searching KB before creating an incident.

The user interface and mandatory fields vary between companies, so if the above steps don't match your instance, check your internal IT support page or ask your ServiceNow administrator for the exact process.

**References:**

- [Create an incident (ServiceNow Docs)](https://docs.servicenow.com/bundle/utah-it-service-management/page/product/incident-management/task/create-an-incident.html)
- [ServiceNow Community - Incident Creation Discussions](https://www.servicenow.com/community)
