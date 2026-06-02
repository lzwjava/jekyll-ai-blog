---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 解决WebSphere大型EAR文件上传错误
translated: true
type: note
---

### 问题分析
"多部分文件上传错误"（通常表现为`org.apache.commons.fileupload.FileUploadException: Processing of multipart/form-data request failed. File too large (errno:27)`）常见于通过IBM WebSphere应用服务器管理控制台更新EAR文件时。对于较大体积的EAR文件（如>20MB），由于文件上传限制、临时存储限制、堆内存限制或操作系统资源限制，常会触发此问题。这并非EAR文件本身的问题，而是控制台处理HTTP多部分上传的方式导致的。

### 快速解决方案
1. **将EAR文件复制到服务器进行本地部署**：
   - 使用FTP/SCP将新EAR文件传输至WAS服务器目录（如`/opt/IBM/WebSphere/AppServer/installableApps/`）
   - 在管理控制台中：进入**应用程序 > 应用程序类型 > WebSphere企业应用程序**
   - 选择现有应用 > **更新**
   - 选择**替换或添加单个模块**或**替换整个应用程序**，然后选择**本地文件系统**并指向已复制的EAR路径
   - 该方法可绕过HTTP多部分上传过程

2. **提高操作系统文件大小限制（UNIX/Linux服务器）**：
   - `errno:27`错误通常表示文件超出进程的ulimit限制
   - 以WAS用户身份（如`webadmin`）运行`ulimit -f`检查当前限制
   - 设置为无限制：在用户shell配置文件（如`~/.bash_profile`）或服务器启动脚本中添加`ulimit -f unlimited`
   - 重启部署管理器后重试上传

### WAS配置调整
1. **增加部署管理器堆内存大小**：
   - 大型EAR文件处理时可能引发内存不足
   - 在管理控制台：**服务器 > 服务器类型 > 管理服务器 > 部署管理器**
   - 在**Java和进程管理 > 进程定义 > Java虚拟机**下：
     - 将**初始堆大小**设为1024（或更高，如针对特大型EAR设为2048）
     - 将**最大堆大小**设为2048（或更高）
   - 保存配置后重启部署管理器并重试

2. **调整HTTP会话或POST大小限制（如适用）**：
   - 针对Web容器限制：**服务器 > 服务器类型 > WebSphere应用服务器 > [您的服务器] > Web容器 > HTTP传输**
   - 如设置值过低，可增加**最大POST大小**（字节单位）
   - 注意：这会间接影响管理控制台的Web应用

### 推荐长期解决方案：使用wsadmin进行更新
针对大型或频繁的更新操作，建议完全避免使用控制台——其对大文件处理不可靠。使用wsadmin脚本工具（Jython或JACL）来更新应用程序。

#### 操作步骤：
1. 将新EAR文件复制至服务器可访问路径（如`/tmp/myapp.ear`）
2. 启动wsadmin：
   ```
   /opt/IBM/WebSphere/AppServer/bin/wsadmin.sh -lang jython -user admin -password pass
   ```
3. 运行以下Jython脚本进行更新：
   ```python
   AdminApp.update('MyAppName', 'app', [-Map ModulesToApps, '[-MapWebModToVH [[default_host MyContext virtual_host]] ]'], [-Operation update], [-appname MyAppName], [-MapModulesToServers [[MyModule MyServer]]], [-nodefaultoptions], [-preCompileJSPs false], [-contextroot MyContext], [-noTxImport], [-connType SERVER], [ -contenturi /tmp/myapp.ear ])
   AdminConfig.save()
   ```
   - 将`MyAppName`替换为应用名称，`MyContext`替换为上下文根，`MyServer`替换为目标服务器/集群，`/tmp/myapp.ear`替换为EAR实际路径
4. 集群环境中同步节点：`AdminControl.invoke(AdminControl.completeServers(), 'sync')`
5. 重启应用：**应用程序 > [应用] > 重启**

该方法效率更高，可规避上传限制，且支持通过脚本实现自动化（如通过Jenkins）

### 补充建议
- **检查日志**：查看dmgr配置文件的`SystemOut.log`和`SystemErr.log`获取详细信息（路径如`/opt/IBM/WebSphere/AppServer/profiles/Dmgr01/logs/dmgr/`）
- **使用精简版EAR测试**：通过压缩最小版本来验证是否与文件大小相关
- **WAS版本**：确保使用受支持版本（如8.5、9.0），必要时安装最新补丁
- 若错误持续出现（如超时），可在**环境 > Web应用服务器 > [服务器] > 容器设置 > Web容器设置 > Web容器 > 会话管理 > 配置 > 超时**中增加HTTP超时设置

若以上方案均未解决问题，请提供具体错误信息和WAS版本以便获取针对性建议。

### 参考文档
- [WebSphere应用服务器7.0部署war文件时出错](https://coderanch.com/t/459530/application-servers/Error-deploy-war-file-Websphere)
- [WebSphere应用服务器部署应用时出现内存不足错误](https://www.ibm.com/support/pages/outofmemory-errors-while-deploying-applications-websphere-application-server)
- [WAS中可部署EAR文件的最大尺寸限制](https://stackoverflow.com/questions/58748076/maximum-size-limit-of-an-ear-that-can-be-deployed-in-was)
- [使用WebSphere管理控制台部署企业归档文件](https://www.ibm.com/docs/en/configurepricequote/9.5.0?topic=cwaso-deploying-enterprise-archive-ear-using-websphere-admin-console)
