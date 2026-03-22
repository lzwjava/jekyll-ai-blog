---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 日常生活最佳自托管工具清单
translated: true
type: note
---

问题：除了开发工具之外，有哪些最适合日常生活的 self-hosted 工具——例如待办事项任务管理、资产/库存追踪、个人理财和家庭组织？

回答：

根据 lzwjava.github.io 的文章和更广泛的研究，以下是涵盖 **日常生活** 需求（而非仅限于软件工程）的最佳 self-hosted 工具综合概述。以下所有工具均为开源、Docker 友好，且可免费 self-hosted。

---

## 📋 待办事项与任务管理

### Vikunja
Vikunja 是一款可以 self-hosted 的开源任务管理工具，具有列表、Kanban 广告牌、Gantt 图等功能。它支持子任务、团队协作，以及支持离线使用的移动端和桌面端 Client。它还提供用于集成的 REST API，并可以从 Todoist、Trello 和 JSON 导入数据。可以将其视为 self-hosted 版的 Todoist/ClickUp。

### Super Productivity
Super Productivity 专为个人和开发者打造，专注于深度工作和简单的任务组织。它支持 WebDAV、Nextcloud 和 Dropbox 同步，且不需要中央服务器。

### OpenProject
OpenProject 是历史最悠久的开源项目管理产品之一，其 Community Edition 下载量超过 2000 万次，在欧盟拥有极高的普及率。它的特点是包含 Agile 画板、Gantt 图和时间追踪。最适合团队或更具结构化的项目工作流。

### Plane
安装 Plane 只需不到五分钟，其 CLI 包含健康检查、监控和版本更新选项。它可以在 Docker Hub 和 Coolify 的一键服务中找到。Community Edition 采用 AGPL 3.0 许可。

---

## 🏠 家庭库存与资产管理

### Homebox
Homebox 是为家庭用户构建的库存和组织系统。它部署简单（单个 Docker 容器），使用 Go 编写以最小化资源占用（闲置状态低于 50MB），并使用带有嵌入式 Web UI 的 SQLite。Homebox 的核心是将资产分配到位置。每个页面都有唯一的 URL 和自动生成的 QR code。您可以为物品添加附件，如照片、用户手册、保修文档和发票。非常适合追踪家用物品、电器、电子产品和保修期。

### Shelf (由 awesome-selfhosted 提供)
Shelf 是一款资产和设备追踪工具，适用于重视清晰度的团队。它是一个资产数据库和 QR 资产标签生成器，让您可以跨地点创建、管理和概览您的资产。资产数量不受限制，永久免费。

### Snipe-IT
Snipe-IT 是一个免费的开源 IT 资产管理系统。它不仅是替代 Excel 的库存软件，更是一套引导您管理 IT 资产的完整方法论。它比 Homebox 更强大，如果您有许多设备或需要更严格的追踪，它会更合适。

---

## 💰 个人理财

### Firefly III
Firefly III 是一款个人财务管理器和复式记账工具，旨在帮助个人和小型组织追踪预算、投资、债务和支出。用户可以导入银行对账单（CSV、OFX、QIF）或通过 API 进行集成。系统支持预算计划、重复交易、自动分类规则和用于分析长期趋势的报表 Dashboard。

### Actual Budget
Actual Budget 是一款快速、注重隐私的个人理财应用，围绕信封预算方法论构建。它完全是 local-first 的，支持离线工作，并在设备之间安静地同步。可选的端到端加密可确保您的财务信息即使在使用 self-hosted 同步服务器时也能保持私密。

---

## 📄 文档与知识管理

### Paperless-ngx
Paperless-ngx 会监视一个特定的 "consume" 文件夹；一旦您将扫描件或电子发票放入其中，它就会使用 OCR 读取每个单词，然后利用机器学习自动为文档添加标签、分配类别（如“房东”或“税务局”）并归档。全文本搜索让您可以立即找到任何文档。对于管理合同、税务文件、收据和发票至关重要。

### Joplin
Joplin 是一款注重隐私、使用 Markdown 的开源笔记应用，支持跨设备同步、加密、附件和 self-hosting，以便完全控制个人知识管理工作流。

### AFFiNE Community Edition
AFFiNE 是下一代知识库，将规划、排序和创作融合在一起。隐私优先、可定制，是替代 Notion 和 Miro 的理想选择。

---

## 📸 照片与媒体

### Immich
一个 self-hosted 的 Google Photos 替代品，具有手机自动备份、人脸识别和相册共享功能。界面非常精美且开发活跃。

### Jellyfin
您的个人 Netflix——用于电影、电视、音乐的 self-hosted 流媒体平台，无需订阅。可推送到任何设备。

---

## 🔐 密码与安全

### Vaultwarden
一个轻量级的、与 Bitwarden 兼容的 self-hosted 密码管理器。适用于所有 Bitwarden 浏览器扩展和移动端 App。可以完全替代 1Password/LastPass。

---

## 🌐 网络与隐私

### AdGuard Home / Pi-hole
为整个家庭提供网络层级的广告和追踪器拦截，充当本地 DNS 服务器。

### SearXNG
一个注重隐私的元搜索引擎，您可以将其设置为浏览器默认搜索，它会聚合来自多个引擎的结果而不会进行追踪。

---

## 🤖 自动化与监控

### n8n
Self-hosted 工作流自动化工具（类似于 Zapier）。连接 API、webhooks、日历和文件以自动执行重复任务——非常适合工程师。

### Uptime Kuma
一个美观的监控 Dashboard，用于检查您的网站、服务器和 API 是否在线，并支持通过 Telegram/Discord/Email 发送警报。

---

## 🗂️ 杂货与家庭管理

### Grocy
Grocy 被描述为“冰箱之外的 ERP”——一套用于家庭的杂货和家庭管理解决方案。追踪库存、购物清单、食谱、餐食计划和家务。

---

## 入门建议

上述所有工具都可以通过 Docker 安装。一个适合日常生活的入门方案如下：

1. **Paperless-ngx** — 取代您的文件柜
2. **Firefly III** 或 **Actual Budget** — 取代电子表格理财
3. **Homebox** — 取代关于家庭库存的便签贴
4. **Vikunja** — 取代 Todoist/TickTick
5. **Vaultwarden** — 取代您的密码管理器订阅服务

参考资料：

- [lzwjava.github.io - 为软件工程师准备的 Self-Hosted 工具](https://lzwjava.github.io/self-hosted-tools-software-engineers-en)
- [awesome-selfhosted GitHub](https://github.com/awesome-selfhosted/awesome-selfhosted)
- [awesome-selfhosted.net - 任务管理](https://awesome-selfhosted.net/tags/task-management--to-do-lists.html)
- [awesome-selfhosted.net - 库存管理](https://awesome-selfhosted.net/tags/inventory-management.html)
- [Vikunja - Self-Hosted 任务管理器](https://vikunja.io/)
- [Homebox - 家庭库存](https://hay-kot.github.io/homebox/)
- [Firefly III - 个人理财](https://www.firefly-iii.org/)
- [XDA Developers - 2026 年 Self-Hosted 生产力技术栈](https://www.xda-developers.com/non-negotiable-self-hosted-productivity-stack-for-2026/)
- [Super Productivity - 开源任务应用对比](https://super-productivity.com/blog/open-source-productivity-apps-comparison/)