---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 博通Clarity工时表系统概述
translated: true
type: note
---

### 问题：全面介绍 Broadcom 的 Clarity 工时表系统

### 回答

#### Broadcom Clarity PPM 概览

Broadcom 的 Clarity，前身为 CA Project & Portfolio Management (CA PPM)，是一个全面的企业软件平台，专为项目与服务组合管理 (PPM) 而设计。它使组织能够将项目与业务战略对齐，优化资源分配，并跟踪跨组合的财务绩效。Clarity 于 2018 年被 Broadcom 收购，支持本地部署和 SaaS 部署，提供路线图、财务规划、资源管理和需求履行工具。Clarity 的核心是整合了模块化组件，以促进端到端项目生命周期管理，重点关注敏捷性、可扩展性和数据驱动的决策。截至 2025 年，最新版本（例如 16.x）强调现代用户体验 (New UX) 与移动可访问性和 AI 增强功能。

#### 工时表系统简介

Clarity 中的工时表系统是资源管理和财务管理功能中的一个关键模块。它允许团队成员、项目经理和资源准确地捕获和报告在任务、项目或其他投资（例如，计划或非项目投资）上花费的时间。该系统超越了简单的工时记录，通过在任务级别实现精细跟踪、支持用于计费的费用代码以及与成本计算（用于预算和预测）集成，从而实现更强大的功能。工时表对于合规性、资源利用率分析以及确保实际工作量与计划估计相符至关重要。

主要目的包括：

- **时间跟踪和报告**：记录每天或定期在特定任务上花费的小时数，以提供资源生产力的可见性。
- **成本管理**：将时间数据输入财务模型，用于挣值管理 (EVM)、已完成工作实际成本 (ACWP) 和在制品 (WIP) 过账。
- **资源优化**：帮助 PMO (Project Management Offices) 评估分配、识别瓶颈，并根据实时数据调整人员配置。
- **合规性和审计**：强制执行组织政策（例如，每周最大工时）并生成用于监管需求的审计跟踪。

Clarity 中的工时表是可配置的，支持经典和现代界面，可通过网络、移动应用程序以及与 Microsoft Excel 等工具的集成（用于批量编辑）进行访问。

#### 工时表系统的主要功能

Clarity 的工时表模块功能丰富，将可用性与企业级控制融为一体。以下是核心功能的细分：

| 功能 | 描述 | 优势 |
|---------|-------------|----------|
| **任务级时间输入** | 根据特定任务、项目或间接/事件活动记录小时数。支持多日分布（例如，输入总计 40 小时可自动分配每天 8 小时）。 | 确保精确分配；减少多任务场景中的手动错误。 |
| **提交和审批工作流** | 用户提交工时表供经理审核；包括通知、提醒和拒绝/返工循环。提交后，像“过账工时表”这样的作业会更新实际值和 ETC (Estimate to Complete)。 | 简化治理；通过审计日志保持问责制。 |
| **业务规则和验证** | 管理员以小时或天定义规则（例如，每周不超过 50 小时），并在提交时进行验证。与“工时表 Hook”集成以实现自定义逻辑。 | 强制执行加班限制等政策；防止无效数据输入。 |
| **移动和 UI 灵活性** | New UX 支持拖放网格、用于工作量可视化的仪表，以及移动输入。经典 PPM 提供可自定义的布局和从前期自动填充。 | 增强远程/现场团队的可访问性；对所有技能水平的用户都友好。 |
| **财务集成** | 时间过账到 WIP 进行成本计算，使用费率矩阵（基于角色、费用代码或输入类型）。支持 EVM 指标，如 ACWP 和 ETC 成本。 | 准确预算；处理费率变化或任务特定费率的差异。 |
| **报告和分析** | 查看未提交/已提交/已过账的工时表；导出到 Excel。PMO 概览的 Portlet 显示待定估计和利用率趋势。 | 数据驱动的洞察；支持组合级仪表板。 |
| **高级选项** | 跟踪非活动/已终止资源（终止后有限制）；非项目工作的间接时间；多币种和多语言支持。 | 适应混合环境；符合全球运营。 |

这些功能受访问权限控制，管理员通过 Administration > Timesheets 工作区配置默认值。

#### 工时表系统如何运作

工时表流程遵循结构化的工作流：

1. **访问和设置**：登录 Clarity（通过网络或移动设备）。如果获得工时表访问权限，从主菜单导航到工时表页面。管理员为现代 UX 启用“新工时表”，如果需要，重置自定义布局。

2. **创建/打开工时表**：选择一个期间（例如，每周）。使用“选择任务”网格自动拉取分配的任务。手动输入小时数或通过跨天分布的总数输入。

3. **输入和审查数据**：更新任务状态、添加注释，并根据规则（例如，总小时数上限）进行验证。通知会在截止日期或出现问题时提醒。

4. **提交审批**：提交给经理；他们审查、批准或退回进行修改。已批准的工时表会触发自动化作业。

5. **过账和集成**：“过账工时表”作业处理数据，更新任务实际值、成本和 ETC。“过账到 WIP”处理财务过账，考虑费率矩阵。

6. **调整和报告**：允许对开放任务/项目进行后期编辑。生成用于审计或预测的报告。

例如，一名开发人员每天在一个任务上记录 8 小时；经批准后，这会实时更新项目成本和资源利用率仪表板。

#### 优势和用例

- **对于团队**：简化跟踪，节省手动电子表格的时间；移动输入提高了合规率。
- **对于经理/PMO**：提供准确的数据进行预测，根据 Broadcom 案例研究，减少 20-30% 的超支。
- **企业级**：与路线图和财务集成，实现全面的 PPM；通过将时间与价值交付联系起来，支持敏捷转型。
用例涵盖 IT 服务（收费计费）、咨询（客户开票）和研发（组合优先级）。

#### 最新发展（截至 2025 年）

Clarity 的工时表随着 New UX 的增强而发展，包括用于规则的 Beta 工作区和用于自定义集成的改进 Hook。版本 16.x 引入了更好的终止处理（例如，阻止终止后输入）和类似 Excel 的费用跟踪。未来的路线图暗示了 AI 驱动的时间输入异常检测。

总而言之，Broadcom Clarity 的工时表系统是一个强大、集成的工具，它将原始时间数据转换为可操作的见解，使组织能够高效、盈利地交付项目。

### 参考文献

- [Clarity 入门](https://techdocs.broadcom.com/us/en/ca-enterprise-software/business-management/clarity-project-and-portfolio-management-ppm-on-premise/16-1-3/Getting-Started.html)
- [输入工时并提交工时表](https://techdocs.broadcom.com/us/en/ca-enterprise-software/business-management/clarity-project-and-portfolio-management-ppm-on-premise/16-3-0/using/new-user-experience-enter-hours-and-submit-a-timesheet.html)
- [设置工时表规则](https://techdocs.broadcom.com/us/en/ca-enterprise-software/business-management/clarity-project-and-portfolio-management-ppm-on-premise/16-2-1/using/Getting-Started-with-Clarity-Administration/setting-up-rules-for-timesheets.html)
- [PMO 资源管理工时表概览](https://techdocs.broadcom.com/us/en/ca-enterprise-software/business-management/clarity-project-and-portfolio-management-ppm-on-premise/16-3-0/add-ins-and-integrations/add-in-pmo-accelerator/pmo-resource-management-timesheet-overview-and-pending-estimates-review.html)
- [提交工时表 (经典 PPM)](https://techdocs.broadcom.com/us/en/ca-enterprise-software/business-management/clarity-project-and-portfolio-management-ppm-on-premise/16-2-1/Using-Classic-Clarity-PPM/submit-a-timesheet.html)
- [成本如何计算？](https://knowledge.broadcom.com/external/article/189329/how-are-costs-calculated.html)
- [资源终止后可访问的 Clarity 工时表功能](https://knowledge.broadcom.com/external/article/370964/clarity-timesheet-features-accessible-po.html)
