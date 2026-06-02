---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 更新WebSphere上下文根路径
translated: true
type: note
---

### 在 IBM WebSphere Application Server (WAS) 中更新 Web 上下文根路径

Web 上下文根路径定义了 Web 应用程序的基础 URL 路径（例如 `/myapp`）。在 IBM WebSphere Application Server 中，您可以通过管理控制台在初始部署时或为现有应用程序更新该路径。以下是针对现有应用程序的操作步骤，请确保您拥有 WAS 控制台的管理员访问权限。

#### 前提条件
- 可访问 WebSphere 管理控制台（通常位于 `https://your-server:9043/ibm/console`）
- 应用程序必须已安装并处于停止状态（建议），以避免修改时产生冲突

#### 更新上下文根路径步骤
1. **登录管理控制台**：
   - 打开浏览器访问 WAS 控制台 URL
   - 输入管理员凭据

2. **定位应用程序**：
   - 在左侧导航栏展开 **应用程序** > **应用程序类型** > **WebSphere 企业应用程序**
   - 从列表中找到并选择已部署的应用程序

3. **访问上下文根设置**：
   - 在应用程序详情页面，滚动至 **Web 模块属性** 部分
   - 点击 **Web 模块的上下文根**

4. **编辑上下文根**：
   - 在出现的表格中找到对应 Web 模块（如 WAR 文件名）
   - 在 **上下文根** 字段中输入新值（例如从 `/oldapp` 改为 `/newapp`）。若非必需请勿使用前导斜杠，但类似 `/myapp` 的路径需保留斜杠
   - 点击 **确定** 保存更改

5. **保存并同步配置**：
   - 在控制台点击 **保存**（若提示则选择 **直接保存到主配置**）
   - 若处于集群或网络部署环境：
     - 转至 **系统管理** > **节点**
     - 选择所有相关节点并点击 **完全重新同步**

6. **重启应用程序**：
   - 返回 **应用程序** > **WebSphere 企业应用程序**
   - 选择目标应用程序，依次点击 **停止** 与 **启动**
   - 或通过 **服务器** > **服务器类型** > **WebSphere 应用服务器** > 选择服务器 > **重新启动** 重启整个服务器

7. **验证更改**：
   - 在浏览器访问应用程序新 URL（如 `http://your-server:9080/newapp`）
   - 检查服务器日志（如 `SystemOut.log`）中是否存在部署相关错误

#### 补充说明
- **初始部署期间**：若部署新应用，可在 **选择安装选项** 步骤中为每个 Web 模块指定上下文根
- **EAR 文件**：对于 EAR 格式的应用程序，请确保 `application.xml` 未硬编码上下文根，控制台中的设置具有更高优先级
- **常见问题**：
  - 若应用程序正在运行，更改可能无法生效——请务必先停止应用
  - 在 WebSphere Liberty 或 Open Liberty 中需改用 `server.xml` 配置
  - 若涉及虚拟主机或插件，请在更改后更新 Web 服务器插件配置
- 若应用程序使用了安全模块或共享库，请在更新后进行全面测试

更多细节请参考 IBM 官方文档或技术社区指南。

#### 参考资源
- [Web 模块的上下文根设置](https://www.ibm.com/docs/SSEQTP_9.0.5/com.ibm.websphere.base.doc/ae/uweb_contextroot.html)
- [IBM WebSphere - 应用程序上下文根](https://www.freekb.net/Article?id=1647)
- [WebSphere 8.5 上下文根更改未应用于 WAR 文件](https://stackoverflow.com/questions/24472790/websphere-8-5-context-root-change-not-applying-to-war-file)
