---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 创建 Azure API 管理实例
translated: true
type: note
---

### 在 Azure 中使用 API 管理创建 API 网关

Azure API 管理（APIM）是全托管服务，可作为 API 网关使用，提供 API 发布、安全防护、分析统计和开发者门户等功能。以下是通过 Azure 门户创建 APIM 实例的逐步指南。

#### 先决条件

- 有效的 Azure 订阅。若尚未拥有，可创建 [免费 Azure 账户](https://azure.microsoft.com/free/)。

#### 创建 API 管理实例步骤

1. **登录 Azure 门户**
   访问 [Azure 门户](https://portal.azure.com) 并使用 Azure 账户登录。

2. **创建新资源**
   - 在 Azure 门户菜单中选择 **创建资源**（或从 Azure 主页选择 **创建资源**）
   - 在 **创建资源** 页面，搜索并选择 **集成** 类别下的 **API 管理**
   - 点击 **创建**

3. **配置基础设置**
   在 **创建 API 管理** 页面切换至 **基础** 选项卡并填写详细信息：

   | 设置项             | 说明                                                                         |
   |--------------------|-----------------------------------------------------------------------------|
   | 订阅               | 选择此实例的 Azure 订阅                                                      |
   | 资源组             | 选择现有资源组或新建（例如 "APIM-RG"）                                        |
   | 区域               | 选择靠近用户或后端服务的区域（例如 "美国东部"）                                |
   | 资源名称           | 输入唯一名称（例如 "my-apim-instance"），将作为默认域名的一部分：`<名称>.azure-api.net`。创建后不可修改 |
   | 组织名称           | 您的组织名称（用于开发者门户和邮件通知）                                       |
   | 管理员邮箱         | 接收系统通知的邮箱地址                                                        |
   | 定价层             | 开发/测试建议选择 **Basic v2**（快速部署，约需30-40分钟）。Developer 或 Standard 层级提供更多功能 |
   | 单元数             | 评估环境默认设为 1                                                           |
   检查无误后继续

4. **可选：配置监控与安全**
   在 **监控 + 安全** 选项卡：
   - 启用可选附加功能如 Log Analytics 进行日志记录（可能产生额外费用）
   - 初学者可暂不配置

5. **审阅并创建**
   - 在 **审阅 + 创建** 选项卡验证配置
   - 点击 **创建**。部署过程需要30-40分钟或更长时间
   - 提示：创建完成后可将资源固定到仪表板方便后续访问

6. **验证实例**
   - 在 Azure 门户搜索 **API 管理服务**
   - 选择新建的实例
   - 在 **概览** 页面确认状态为 "在线"。现在即可开始导入 API、配置策略或设置开发者门户

#### 后续步骤

- 导入首个 API：参照 [导入并发布 API 的教程](https://learn.microsoft.com/en-us/azure/api-management/import-and-publish)
- 安全加固：添加身份验证、速率限制等策略
- 清理资源：测试完成后可通过门户删除资源组避免产生费用（搜索 **资源组** > 选择组 > **删除资源组**）

如需自定义域名或高级配置，请参阅 [APIM 文档](https://learn.microsoft.com/en-us/azure/api-management/)。

[快速入门：通过门户创建 Azure API 管理实例](https://learn.microsoft.com/en-us/azure/api-management/get-started-create-service-instance)
[Azure API 管理概述](https://learn.microsoft.com/en-us/azure/api-management/api-management-key-concepts)
