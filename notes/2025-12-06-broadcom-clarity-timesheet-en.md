---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Broadcom Clarity Timesheet System Overview
translated: false
type: note
---

### Question: Provide a comprehensive introduction to Broadcom's Clarity timesheet system

### Answer

#### Overview of Broadcom Clarity PPM

Broadcom's Clarity, formerly known as CA Project & Portfolio Management (CA PPM), is a comprehensive enterprise software platform designed for project and portfolio management (PPM). It enables organizations to align projects with business strategies, optimize resource allocation, and track financial performance across portfolios. Acquired by Broadcom in 2018, Clarity supports both on-premise and SaaS deployments, offering tools for roadmapping, financial planning, resource management, and demand fulfillment. At its core, Clarity integrates modular components that facilitate end-to-end project lifecycle management, with a focus on agility, scalability, and data-driven decision-making. As of 2025, the latest versions (e.g., 16.x) emphasize a modern user experience (New UX) with mobile accessibility and AI-enhanced features.

#### Introduction to the Timesheet System

The timesheet system in Clarity is a pivotal module within the Resource Management and Financial Management functionalities. It allows team members, project managers, and resources to accurately capture and report time spent on tasks, projects, or other investments (e.g., programs or non-project investments). This system goes beyond simple time logging by enabling granular tracking at the task level, supporting charge codes for billing, and integrating with cost calculations for budgeting and forecasting. Timesheets are essential for compliance, resource utilization analysis, and ensuring that actual effort aligns with planned estimates.

Key purposes include:

- **Time Tracking and Reporting**: Record daily or periodic hours worked on specific assignments to provide visibility into resource productivity.
- **Cost Management**: Feed time data into financial models for earned value management (EVM), actual cost of work performed (ACWP), and work-in-progress (WIP) postings.
- **Resource Optimization**: Help PMOs (Project Management Offices) assess allocation, identify bottlenecks, and adjust staffing based on real-time data.
- **Compliance and Auditing**: Enforce organizational policies (e.g., maximum weekly hours) and generate audit trails for regulatory needs.

Timesheets in Clarity are configurable, supporting both classic and modern interfaces, and are accessible via web, mobile apps, and integrations with tools like Microsoft Excel for bulk edits.

#### Key Features of the Timesheet System

Clarity's timesheet module is feature-rich, blending usability with enterprise-grade controls. Below is a breakdown of core capabilities:

| Feature | Description | Benefits |
| --------- | ------------- | ---------- |
| **Task-Level Time Entry** | Log hours against specific tasks, projects, or indirect/incident activities. Supports multi-day spreading (e.g., enter a total of 40 hours to auto-distribute 8 hours/day). | Ensures precise allocation; reduces manual errors in multi-task scenarios. |
| **Submission and Approval Workflow** | Users submit timesheets for manager review; includes notifications, reminders, and rejection/rework loops. Post-submission, jobs like "Post Timesheets" update actuals and ETC (Estimate to Complete). | Streamlines governance; maintains accountability with audit logs. |
| **Business Rules and Validation** | Admins define rules (e.g., no more than 50 hours/week) in hours or days, validated on submission. Integrates with "Timesheet Hook" for custom logic. | Enforces policies like overtime limits; prevents invalid data entry. |
| **Mobile and UI Flexibility** | New UX supports drag-and-drop grids, gauges for effort visualization, and mobile entry. Classic PPM offers customizable layouts and auto-population from prior periods. | Enhances accessibility for remote/field teams; user-friendly for all skill levels. |
| **Financial Integration** | Time posts to WIP for cost calculations using rate matrices (based on roles, charge codes, or input types). Supports EVM metrics like ACWP and ETC costs. | Accurate budgeting; handles variances from rate changes or task-specific rates. |
| **Reporting and Analytics** | View unsubmitted/submitted/posted timesheets; export to Excel. Portlets for PMO overviews show pending estimates and utilization trends. | Data-driven insights; supports portfolio-level dashboards. |
| **Advanced Options** | Track for inactive/terminated resources (with restrictions post-termination); indirect time for non-project work; multi-currency and multi-language support. | Adaptable to hybrid environments; compliant with global operations. |

These features are governed by access rights, with admins configuring defaults via the Administration > Timesheets workspace.

#### How the Timesheet System Works

The timesheet process follows a structured workflow:

1. **Access and Setup**: Log in to Clarity (via web or mobile). If granted timesheet access, navigate to the Timesheets page from the main menu. Admins enable "New Timesheets" for modern UX, resetting custom layouts if needed.

2. **Create/Open Timesheet**: Select a period (e.g., weekly). Use the "Select Tasks" grid to pull assigned tasks automatically. Enter hours manually or via totals that spread across days.

3. **Enter and Review Data**: Update task status, add notes, and validate against rules (e.g., total hours cap). Notifications alert for deadlines or issues.

4. **Submit for Approval**: Submit to manager; they review, approve, or return for corrections. Approved timesheets trigger automated jobs.

5. **Posting and Integration**: "Post Timesheets" job processes data, updating assignment actuals, costs, and ETC. "Post to WIP" handles financial postings, factoring in rate matrices.

6. **Adjustments and Reporting**: Post-period edits allowed for open tasks/projects. Generate reports for audits or forecasts.

For example, a developer logs 8 hours daily on a task; upon approval, this updates project costs and resource utilization dashboards in real-time.

#### Benefits and Use Cases

- **For Teams**: Simplifies tracking, saving hours on manual spreadsheets; mobile entry boosts compliance rates.
- **For Managers/PMOs**: Provides accurate data for forecasting, reducing overruns by 20-30% (based on Broadcom case studies).
- **Enterprise-Wide**: Integrates with roadmaps and financials for holistic PPM; supports agile transformations by linking time to value delivery.
Use cases span IT services (chargeback billing), consulting (client invoicing), and R&D (portfolio prioritization).

#### Recent Developments (as of 2025)

Clarity's timesheets have evolved with New UX enhancements, including beta workspaces for rules and improved hooks for custom integrations. Version 16.x introduces better termination handling (e.g., blocking post-termination entries) and Excel-like expense tracking. Future roadmaps hint at AI-driven anomaly detection for time entries.

In summary, Broadcom Clarity's timesheet system is a robust, integrated tool that transforms raw time data into actionable insights, empowering organizations to deliver projects efficiently and profitably.

### References

- [Getting Started with Clarity](https://techdocs.broadcom.com/us/en/ca-enterprise-software/business-management/clarity-project-and-portfolio-management-ppm-on-premise/16-1-3/Getting-Started.html)
- [Enter Hours and Submit a Timesheet](https://techdocs.broadcom.com/us/en/ca-enterprise-software/business-management/clarity-project-and-portfolio-management-ppm-on-premise/16-3-0/using/new-user-experience-enter-hours-and-submit-a-timesheet.html)
- [Setting Up Rules for Timesheets](https://techdocs.broadcom.com/us/en/ca-enterprise-software/business-management/clarity-project-and-portfolio-management-ppm-on-premise/16-2-1/using/Getting-Started-with-Clarity-Administration/setting-up-rules-for-timesheets.html)
- [PMO Resource Management Timesheet Overview](https://techdocs.broadcom.com/us/en/ca-enterprise-software/business-management/clarity-project-and-portfolio-management-ppm-on-premise/16-3-0/add-ins-and-integrations/add-in-pmo-accelerator/pmo-resource-management-timesheet-overview-and-pending-estimates-review.html)
- [Submit a Timesheet (Classic PPM)](https://techdocs.broadcom.com/us/en/ca-enterprise-software/business-management/clarity-project-and-portfolio-management-ppm-on-premise/16-2-1/Using-Classic-Clarity-PPM/submit-a-timesheet.html)
- [How are costs calculated?](https://knowledge.broadcom.com/external/article/189329/how-are-costs-calculated.html)
- [Clarity timesheet features accessible post resource termination](https://knowledge.broadcom.com/external/article/370964/clarity-timesheet-features-accessible-po.html)
