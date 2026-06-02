---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: PCF日志的Kibana配置
translated: true
type: note
---

看起来"kabana"很可能指的是**Kibana**——Elasticsearch的开源数据可视化仪表板。在**Pivotal Cloud Foundry (PCF)**（现已更名为VMware Tanzu Application Service）环境中，Kibana通常通过平台的日志系统（Loggregator）用于搜索、可视化和分析日志。PCF本身并不原生独立运行Kibana，而是通过**日志搜索**模块/服务进行集成，该服务将日志存储在Elasticsearch中并通过Kibana提供查询界面。

若您所指并非此意，欢迎进一步说明！接下来我将详细说明如何在PCF日志环境中配置和使用Kibana。本文假设您是具有PCF运维管理员访问权限的用户，且已部署运行中的PCF环境（2.0+版本）。请注意PCF日志系统已历经多次迭代，请根据您使用的版本查阅对应文档。

### 前置准备
- **PCF版本**：日志搜索服务（含Kibana）需PCF 2.2+版本。早期版本使用独立的"ELK"（Elasticsearch、Logstash、Kibana）模块
- **功能模块/服务**：确保已通过Pivotal Network（现Broadcom支持门户）安装**Elastic Runtime**模块（用于Loggregator）和**日志搜索**模块
- **访问权限**：需具备运维管理员控制台和PCF命令行工具的管理员权限
- **资源分配**：预留充足资源（根据日志量分配4-8GB内存给日志搜索服务）

### 步骤一：在运维管理员控制台安装配置日志搜索模块
该模块将PCF日志（来自应用、平台和系统组件）转发至Elasticsearch，使其可通过Kibana进行检索

1. **下载并导入模块**：
   - 登录Broadcom支持门户（原Pivotal Network）
   - 下载**PCF日志搜索**模块（版本需与PCF发行版匹配）
   - 在运维管理员控制台进入**目录** > **导入产品**并上传该模块

2. **配置模块**：
   - 在运维管理员中进入**Elastic Runtime**模块 > **Loggregator**标签页：
     - 启用**Loggregator转发至外部系统**（如需设置syslog或HTTP转发，但日志搜索服务采用内部转发）
     - 设置**Loggregator日志保留期**（建议5-30天）
   - 进入**日志搜索**模块：
     - **分配可用区**：选择至少一个可用区确保高可用
     - **Elasticsearch配置**：
       - 设置实例数量（生产环境建议从3个起步）
       - 配置存储空间（如100GB持久化磁盘）
       - 启用安全功能（如Elasticsearch的TLS加密）
     - **Kibana配置**：
       - 启用Kibana（默认捆绑安装）
       - 设置管理员凭据（用户名/密码）
     - **Loggregator集成**：
       - 设置每秒最大日志行数（根据负载设置1000-5000行）
       - 定义索引模式（设置7-30天的日志保留期）
     - **网络配置**：通过路由暴露Kibana访问地址（如`kibana.您的PCF域名.com`）
   - 点击**应用变更**进行部署（预计耗时30-60分钟）

3. **验证部署**：
   - 执行`cf tiles`命令或在运维管理员中确认部署状态
   - 通过BOSH命令行登录日志搜索虚拟机（`bosh ssh log-search/0`）确认Elasticsearch运行状态（`curl localhost:9200`）

### 步骤二：访问Kibana
部署完成后可通过以下方式访问：

1. **通过PCF应用管理器（图形界面）**：
   - 登录应用管理器（如`https://apps.您的PCF域名.com`）
   - 搜索"日志搜索"服务实例（系统会自动创建）
   - 点击服务实例 > **日志**标签页，即可打开嵌入式Kibana界面进行快速日志检索

2. **直接访问Kibana**：
   - 访问模块中配置的Kibana网址（如`https://kibana.您的PCF域名.com`）
   - 使用预设的管理员凭据登录
   - 若使用自定义域名，请确保DNS解析正确且路由已注册（可通过`cf routes`验证）

3. **命令行访问（可选）**：
   - 基础日志查看可使用`cf logs 应用名称`，但高级查询需使用Kibana界面或API
   - 将日志搜索服务绑定到应用：`cf create-service log-search standard my-log-search` 然后执行 `cf bind-service 应用名称 my-log-search`

### 步骤三：使用Kibana分析PCF日志
Kibana提供基于Web的界面，用于查询、筛选和可视化PCF组件日志（如应用日志、Diego容器、Gorouter等）

1. **基础导航**：
   - **发现标签页**：使用Lucene查询语法搜索日志
     - 示例：搜索特定应用错误：`source_id:APP:您的应用名称 AND json.message:ERROR`
     - 可用字段：`timestamp`、`source_id`（如`APP:应用名`、`RTR:router`）、`message`、`deployment`等
   - **可视化标签页**：创建统计图表（如时序日志量、错误率）
     - 示例可视化：按source_id分类的日志条形图
   - **仪表板标签页**：保存和分享预置仪表板（日志搜索服务包含PCF日志的默认仪表板）

2. **常用查询与技巧**：
   - **按应用筛选**：`source_id:APP:应用名称`（需替换为实际应用GUID或名称）
   - **按时间筛选**：使用时间选择器（如最近24小时）
   - **系统日志**：`source_id:DEA`（Diego容器）或`source_id:LOGGREGATOR`
   - **导出日志**：在发现页面下载CSV/JSON格式
   - **高级功能**：通过Kibana开发工具控制台直接查询Elasticsearch：
     ```
     GET /logstash-*/_search
     {
       "query": { "match": { "message": "error" } },
       "sort": [ { "timestamp": { "order": "desc" } } ]
     }
     ```
   - **保留策略与索引**：日志按日索引（如`logstash-YYYY.MM.DD`），可在模块中配置滚动策略管理存储空间

3. **日志问题排查**：
   - **无日志显示**：检查Loggregator转发规则（运维管理员 > Elastic Runtime > Loggregator），确保应用正在输出日志（如Node.js应用使用`console.log`）
   - **性能问题**：扩展Elasticsearch实例或调整日志速率限制
   - **安全配置**：在日志搜索服务中启用UAA集成实现Kibana单点登录
   - **错误排查**：通过`cf logs log-search`查看PCF日志或检查运维管理员任务日志

### 扩展资源
- **官方文档**：VMware Tanzu文档中心的[日志搜索指南](https://docs.vmware.com/en/VMware-Tanzu-Application-Service/10.0/tas/GUID-log-search-index.html)（请按版本搜索）
- **命令行工具**：如需UAA认证可安装`uaac`工具，或使用`cf curl`进行API访问
- **替代方案**：简单需求可使用PCF内置**日志缓存**（命令行：`cf tail 应用名称`），或通过syslog转发集成Splunk等外部工具
- **版本升级**：若使用旧版PCF，需迁移至ELK模块或联系Broadcom技术支持

如果您能提供更多细节（如PCF版本、错误信息或具体使用场景），我可以提供更精准的指导！
