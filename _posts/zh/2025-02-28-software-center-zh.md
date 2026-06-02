---
audio: false
generated: true
lang: zh
layout: post
title: 软件中心下载问题
translated: true
type: note
---

### 关键要点

- services.msc 似乎是用于管理 Windows 服务的工具，在此处检查 SMS 代理主机服务对解决下载问题至关重要。
- 研究表明 adaptiveclient 很可能是 Adaptiva 客户端服务，属于系统管理工具的一部分，可能与 Configuration Manager 冲突，从而影响下载。
- 证据倾向于认为 wmi 性能适配器是提供性能数据的 Windows 服务，Configuration Manager 会使用该服务，应保持运行以确保功能正常。
- sms 代理主机很可能是 Configuration Manager 客户端服务，对软件中心操作至关重要，必须保持运行才能继续下载。

---

### 这些服务及其作用是什么？

**services.msc 概述**
services.msc 是用于服务的 Microsoft 管理控制台，允许您查看和管理 Windows 计算机上的所有服务。要修复软件中心下载问题，您应使用它来确保 sms 代理主机服务正在运行。如果未运行，启动它可能会解决问题。

**adaptiveclient 说明**
adaptiveclient 可能指的是 Adaptiva 客户端服务，属于 Adaptiva 系统管理软件的一部分，该软件与 Configuration Manager 集成 ([Adaptiva 官方网站](https://adaptiva.com))。如果此服务导致资源冲突或网络干扰，则可能会影响 Configuration Manager 客户端下载软件的能力。您可能需要管理或暂时停止此服务，以查看是否解决了问题。

**wmi 性能适配器详细信息**
wmi 性能适配器是一项 Windows 服务，通过 Windows Management Instrumentation (WMI) 提供性能数据 ([排查 WMI 性能问题](https://learn.microsoft.com/en-us/troubleshoot/windows-server/system-management-components/scenario-guide-troubleshoot-wmi-performance-issues))。Configuration Manager 使用 WMI 执行各种管理任务，因此确保此服务正在运行对于 Configuration Manager 正常运行是必需的。

**sms 代理主机角色**
sms 代理主机是在计算机上运行 Configuration Manager 客户端的服务 ([关于 Configuration Manager 客户端管理的 Microsoft 文档](https://learn.microsoft.com/en-us/mem/configmgr/core/clients/manage/manage-clients))。它对于软件中心和部署至关重要。如果它未运行，下载将无法进行。

### 它们与修复下载问题的关系

要修复软件中心下载卡在 0% 的问题，请按照以下步骤操作：

- 打开 services.msc 并确保 sms 代理主机服务正在运行。如果未运行，请启动它。
- 检查 wmi 性能适配器服务是否正在运行，因为某些 Configuration Manager 功能可能需要它。
- 如果 adaptiveclient 正在运行并可能产生干扰，请考虑停止它或向 Adaptiva 的支持寻求进一步帮助。
- 如果问题仍然存在，请检查 Configuration Manager 日志中是否存在与下载相关的错误，并确保与分发点的网络连接没有问题。验证边界和分发点配置，并考虑清除 CCM 缓存或执行客户端修复。

---

### 调查说明：服务及其对软件中心下载影响的全面分析

本节详细检查了提到的服务——services.msc、adaptiveclient、wmi 性能适配器和 sms 代理主机——以及它们在解决 Microsoft Configuration Manager (SCCM) 环境中软件中心下载卡在 0% 问题中的潜在作用。该分析基于广泛的研究，旨在为 IT 专业人士和非专业用户提供透彻的理解，确保包含调查中的所有相关细节。

#### 理解每项服务

**services.msc：服务管理控制台**
services.msc 本身不是服务，而是用于管理 Windows 服务的 Microsoft 管理控制台管理单元。它提供了一个图形界面来查看、启动、停止和配置服务，这些服务是系统和应用程序功能所必需的后台进程。在修复软件中心下载问题的背景下，services.msc 是用户用来检查关键服务（如 sms 代理主机和 wmi 性能适配器）状态的工具。确保这些服务正在运行是基本的故障排除步骤，因为任何服务故障都可能停止 Configuration Manager 操作，包括软件部署。

**adaptiveclient：很可能是 Adaptiva 客户端服务**
术语 "adaptiveclient" 并不直接对应于任何本机 Configuration Manager 服务，因此得出的结论是它很可能指的是 Adaptiva 客户端服务，属于 Adaptiva 系统管理套件的一部分 ([Adaptiva 官方网站](https://adaptiva.com))。Adaptiva 的软件（例如 OneSite）旨在增强 SCCM 的内容分发和管理能力，特别是补丁管理和端点健康。Adaptiva 客户端服务 (AdaptivaClientService.exe) 负责执行健康检查和内容交付优化等任务。鉴于其与 SCCM 的集成，如果此服务消耗过多的网络资源或与 SCCM 客户端操作冲突，则可能间接导致下载问题。例如，论坛讨论表明可能存在资源争用，例如用于缓存的磁盘空间使用，这可能会影响 SCCM 的性能 ([r/SCCM on Reddit: Adaptiva - Anyone have an Experience?](https://www.reddit.com/r/SCCM/comments/pb7325/adaptiva_anyone_have_an_experience/))。

**wmi 性能适配器：用于性能数据的 Windows 服务**
wmi 性能适配器，或称 WMI 性能适配器 (wmiApSrv)，是一项 Windows 服务，它通过网络向客户端提供来自 WMI 高性能提供程序的性能库信息 ([WMI 性能适配器 | Windows 安全百科全书](https://www.windows-security.org/windows-service/wmi-performance-adapter-0))。它仅在性能数据帮助程序 (PDH) 激活时运行，并且对于通过 WMI 或 PDH API 提供系统性能计数器至关重要。Configuration Manager 严重依赖 WMI 执行清单收集和客户端健康监控等任务 ([排查 WMI 性能问题](https://learn.microsoft.com/en-us/troubleshoot/windows-server/system-management-components/scenario-guide-troubleshoot-wmi-performance-issues))。如果此服务未运行，则可能会破坏 SCCM 收集必要数据的能力，这可能会间接影响软件中心下载，特别是在部署决策需要性能数据时。

**sms 代理主机：Configuration Manager 客户端服务**
sms 代理主机服务，也称为 CcmExec.exe，是安装在受管设备上的 Configuration Manager 客户端的核心服务 ([关于 Configuration Manager 客户端管理的 Microsoft 文档](https://learn.microsoft.com/en-us/mem/configmgr/core/clients/manage/manage-clients))。它处理与 SCCM 服务器的通信，管理软件部署，收集清单，并通过软件中心促进用户交互。此服务对于任何部署活动都至关重要，包括下载和安装应用程序或更新。如果它未运行或遇到问题，例如由于计时问题而停止响应 ([Systems Management Server (SMS) Agent Host service (Ccmexec.exe) stops responding on a System Center Configuration Manager 2007 SP2 client computer](https://support.microsoft.com/en-us/topic/the-systems-management-server-sms-agent-host-service-ccmexec-exe-stops-responding-on-a-system-center-configuration-manager-2007-sp2-client-computer-6bd93824-d9ac-611f-62fc-eabc1ba20d47))，它会直接阻止下载进行，导致卡在 0% 的状态。

#### 将这些服务与修复软件中心下载卡在 0% 的问题联系起来

软件中心下载卡在 0% 表明下载过程尚未启动或在开始时失败，这是 SCCM 环境中常见的问题，通常与客户端、网络或服务器端问题有关。以下是每项服务与故障排除及潜在解决此问题的关系：

- **services.msc 的作用**：作为管理控制台，services.msc 是检查 sms 代理主机和 wmi 性能适配器状态的第一个工具。如果 sms 代理主机已停止，通过 services.msc 重新启动它是直接解决问题的潜在操作。同样，确保 wmi 性能适配器正在运行支持 SCCM 依赖 WMI 的操作。此步骤至关重要，因为论坛帖子和故障排除指南经常建议验证服务状态 ([SCCM Application Download Stuck at 0% in Software Center](https://www.prajwaldesai.com/sccm-application-download-stuck/))。

- **adaptiveclient 的潜在影响**：鉴于 Adaptiva 与 SCCM 的集成，如果 adaptiveclient 服务消耗网络带宽或磁盘空间，可能与 SCCM 的内容下载过程冲突，从而成为一个因素。例如，如果配置不正确，Adaptiva 的点对点内容分发可能会产生干扰，正如用户经验中所指出的，通过 Adaptiva 的内容传输可能会失败并需要清理 ([r/SCCM on Reddit: Adaptiva - Anyone have an Experience?](https://www.reddit.com/r/SCCM/comments/pb7325/adaptiva_anyone_have_an_experience/))。如果下载卡住，暂时停止或管理此服务可能有助于隔离问题，但用户应查阅 Adaptiva 文档以了解安全的管理实践。

- **wmi 性能适配器的相关性**：虽然在大多数下载卡在 0% 的故障排除指南中未直接提及，但 wmi 性能适配器在提供性能数据方面的作用对于 SCCM 至关重要。如果它未运行，SCCM 可能在监控客户端健康或性能方面遇到困难，这可能会间接影响部署过程。确保将其设置为自动启动并正在运行可以防止日志膨胀和系统压力，正如 SCCM 等监控工具触发的频繁启动/停止周期报告中所见 ([Why is my System event log full of WMI Performance Adapter messages?](https://serverfault.com/questions/108829/why-is-my-system-event-log-full-of-wmi-performance-adapter-messages))。

- **sms 代理主机的关键作用**：此服务是问题的核心。如果它未运行，软件中心无法启动下载，导致卡在 0% 的状态。故障排除步骤通常包括重新启动此服务、检查 CcmExec.log 等日志中的错误，以及确保与分发点的网络连接 ([How To Restart SMS Agent Host Service | Restart SCCM Client](https://www.prajwaldesai.com/restart-sms-agent-host-service-sccm-client/))。高 CPU 使用率或由于 WMI 问题导致启动失败等问题也可能导致此情况，需要进一步调查客户端设置和日志。

#### 详细的故障排除步骤

要系统地解决下载卡在 0% 的问题，请考虑以下步骤，并纳入提到的服务：

1. **通过 services.msc 验证服务状态**：
   - 打开 services.msc 并检查 sms 代理主机 (CcmExec.exe) 是否正在运行。如果已停止，请启动它并监控下载是否继续进行。
   - 确保 wmi 性能适配器正在运行或设置为自动启动，以避免 WMI 依赖的 SCCM 操作中断。

2. **如果怀疑 adaptiveclient，则进行管理**：
   - 如果 adaptiveclient 正在运行，请通过任务管理器检查资源使用情况（CPU、内存、网络）。如果很高，请考虑暂时停止它并再次测试下载。参考 Adaptiva 的文档以了解安全程序 ([Adaptiva | FAQ](https://adaptiva.com/faq))。

3. **检查 Configuration Manager 日志**：
   - 查看 DataTransferService.log、ContentTransferManager.log 和 LocationServices.log 等日志，查找指示下载未启动原因的错误。查找诸如 DP 连接失败或边界配置错误等问题 ([Application Installation stuck at Downloading 0% in Software Center](https://learn.microsoft.com/en-us/answers/questions/264523/application-installation-stuck-at-downloading-0-in))。

4. **确保网络和分发点连接**：
   - 验证客户端是否在正确的边界内并且可以访问分发点。检查防火墙设置和网络策略，特别是当 adaptiveclient 影响网络使用时。

5. **执行客户端维护**：
   - 清除 CCM 缓存 (C:\Windows\CCMCache) 并重新启动 sms 代理主机服务。如果问题仍然存在，请考虑客户端修复或重新安装，如论坛讨论中所建议 ([r/SCCM on Reddit: Software Center Apps Downloading Stuck At 0% Complete](https://www.reddit.com/r/SCCM/comments/14z25vp/software_center_apps_downloading_stuck_at_0/))。

#### 表格说明

下表总结了服务及其对下载问题的潜在影响：

| 服务                  | 描述                                                                 | 对下载问题的潜在影响                                   | 采取的措施                                          |
|-----------------------|---------------------------------------------------------------------|-------------------------------------------------------|----------------------------------------------------|
| services.msc          | Windows 服务的管理控制台                                            | 用于检查和启动关键服务，如 sms 代理主机                 | 打开并验证 sms 代理主机和 wmi 性能适配器状态         |
| adaptiveclient        | 很可能是 Adaptiva 客户端服务，属于 Adaptiva 的 SCCM 集成软件的一部分 | 可能导致资源或网络冲突                                | 检查使用情况，考虑暂时停止                          |
| wmi 性能适配器        | 通过 WMI 提供性能数据，供 SCCM 使用                                | 如果未运行，可能会破坏 SCCM 操作                      | 确保正在运行，如果需要则设置为自动启动              |
| sms 代理主机          | Configuration Manager 客户端服务，处理部署                         | 必须运行才能进行下载                                  | 如果停止则启动，检查日志中的错误                    |

另一个用于故障排除步骤的表格：

| 步骤编号 | 操作                                          | 目的                                                  |
|-------------|---------------------------------------------|------------------------------------------------------|
| 1           | 通过 services.msc 检查 sms 代理主机状态        | 确保核心 SCCM 客户端服务正在运行                      |
| 2           | 验证 wmi 性能适配器是否正在运行              | 支持依赖 WMI 的 SCCM 操作                             |
| 3           | 如果资源使用率高，则管理 adaptiveclient      | 隔离与 SCCM 下载的潜在冲突                            |
| 4           | 查看 Configuration Manager 日志              | 识别特定错误，例如 DP 连接问题                        |
| 5           | 检查网络和边界                              | 确保客户端可以访问分发点                              |
| 6           | 清除 CCM 缓存，重新启动客户端                | 解决潜在的缓存或客户端配置问题                        |

#### 意外细节：Adaptiva 的作用

一个意外的细节是 Adaptiva 软件的潜在作用，这在标准 SCCM 故障排除中不常讨论，但如果安装则可能很重要。其与 SCCM 在内容分发和健康检查方面的集成可能会引入复杂性，特别是在两个系统都存在的环境中，可能导致资源争用或影响下载的网络问题。

#### 结论

这项全面分析强调了确保 sms 代理主机和 wmi 性能适配器服务正在运行的重要性，并使用 services.msc 作为管理工具。adaptiveclient（很可能是 Adaptiva 的服务）可能通过资源或网络冲突间接影响下载，需要仔细管理。通过遵循详细的故障排除步骤并利用提供的表格，用户可以系统地解决软件中心下载卡在 0% 的问题，确保彻底的解决过程。

---

### 关键引用

- [Adaptiva 官方网站，全面的端点管理解决方案](https://adaptiva.com)
- [关于 Configuration Manager 客户端管理的 Microsoft 文档，在 ConfigMgr 中管理客户端](https://learn.microsoft.com/en-us/mem/configmgr/core/clients/manage/manage-clients)
- [排查 WMI 性能问题，解决 WMI 性能问题的指南](https://learn.microsoft.com/en-us/troubleshoot/windows-server/system-management-components/scenario-guide-troubleshoot-wmi-performance-issues)
- [WMI 性能适配器，Windows 服务百科全书条目](https://www.windows-security.org/windows-service/wmi-performance-adapter-0)
- [SCCM Application Download Stuck at 0% in Software Center，故障排除指南](https://www.prajwaldesai.com/sccm-application-download-stuck/)
- [r/SCCM on Reddit: Adaptiva - Anyone have an Experience?，用户使用 Adaptiva 的经验](https://www.reddit.com/r/SCCM/comments/pb7325/adaptiva_anyone_have_an_experience/)
- [How To Restart SMS Agent Host Service | Restart SCCM Client，分步指南](https://www.prajwaldesai.com/restart-sms-agent-host-service-sccm-client/)
- [Systems Management Server (SMS) Agent Host service (Ccmexec.exe) stops responding on a System Center Configuration Manager 2007 SP2 client computer，已知问题和修复](https://support.microsoft.com/en-us/topic/the-systems-management-server-sms-agent-host-service-ccmexec-exe-stops-responding-on-a-system-center-configuration-manager-2007-sp2-client-computer-6bd93824-d9ac-611f-62fc-eabc1ba20d47)
- [Why is my System event log full of WMI Performance Adapter messages?，关于 WMI 服务行为的讨论](https://serverfault.com/questions/108829/why-is-my-system-event-log-full-of-wmi-performance-adapter-messages)
- [Application Installation stuck at Downloading 0% in Software Center，Microsoft Q&A 论坛讨论](https://learn.microsoft.com/en-us/answers/questions/264523/application-installation-stuck-at-downloading-0-in)
- [r/SCCM on Reddit: Software Center Apps Downloading Stuck At 0% Complete，社区故障排除技巧](https://www.reddit.com/r/SCCM/comments/14z25vp/software_center_apps_downloading_stuck_at_0/)
