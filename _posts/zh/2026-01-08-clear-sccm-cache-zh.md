---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 如何安全地清理 SCCM 缓存
translated: true
type: note
---

Question: In Windows 的 Software Center 中，有些 Package 安装失败，如何删除 ccmcache 以重新安装？

Answer: 

Windows 上的 **Software Center** 是 Microsoft Endpoint Configuration Manager (原 SCCM/MECM) 的一部分，用于显示部署的任务、更新和 Package。安装失败通常是由于 Client Cache 文件夹 (**ccmcache**，通常位于 `C:\Windows\ccmcache`) 中的文件损坏或不完整导致的。清理此 Cache 会强制 Client 重新下载内容，从而允许重新尝试安装。

### 重要警告
- **不要直接使用 File Explorer 或命令行手动删除 `C:\Windows\ccmcache` 中的文件或文件夹**。这会破坏 Client 对内容的跟踪记录，导致进一步的问题。
- 请务必使用受支持的方法来清理 Cache。

### 推荐方法：通过 Configuration Manager Properties 清理 Cache
这是官方且最安全的方法：

1. 打开运行对话框 (Win + R) 并输入：`control smscfgrc`（或在 Control Panel 中搜索 "Configuration Manager"）。
2. 在 **Configuration Manager Properties** 窗口中，转到 **Cache** 选项卡。
3. 点击 **Configure Settings**（如果弹出提示，请输入管理员凭据）。
4. 点击 **Delete Files**。
5. 勾选 **Delete persisted cache content** 复选框（如果可用且需要）。
6. 点击 **Yes** 确认。

此操作会正确删除缓存项并更新 Client 的内部跟踪信息。

### 清理 Cache 之后
1. 关闭并重新打开 **Software Center**。
2. 导航到失败的 Package/Application/Update。
3. 再次点击 **Retry** 或 **Install**。
   - 初始可能会显示快速失败或下载进度为 0% —— 请尝试第二次点击 Retry，通常在下一次尝试时会开始正常下载。

### 替代方法：使用 PowerShell（高级）
如果您需要自动化或有选择地清理，请以 Administrator 身份运行此 PowerShell 脚本（它使用官方 COM object 安全地删除所有缓存项）：

```powershell
$UIResourceMgr = New-Object -ComObject UIResource.UIResourceMgr
$Cache = $UIResourceMgr.GetCacheInfo()
$Cache.GetCacheElements() | ForEach-Object {
    $Cache.DeleteCacheElement($_.CacheElementID)
}
```

- 在受影响的机器上运行此脚本。
- 然后在 Software Center 中重试安装。

### 其他提示
- 如果故障仍然存在，请触发 Client Policy 刷新：在 Configuration Manager Properties 的 Actions 选项卡中，运行 **Machine Policy Retrieval & Evaluation Cycle** 和 **Application Deployment Evaluation Cycle**。
- 检查 Logs（例如 `C:\Windows\CCM\Logs`）以获取失败的详细信息。
- 在企业环境中，管理员可以使用 Right Click Tools 等工具远程处理此问题。

通过强制进行全新的重新下载，这些步骤应能解决大多数 Package 安装失败的问题。

References:  

- [https://learn.microsoft.com/en-us/mem/configmgr/core/clients/manage/configure-client-cache](https://learn.microsoft.com/en-us/mem/configmgr/core/clients/manage/configure-client-cache)  
- [https://areit.wordpress.ncsu.edu/software-center-troubleshooting/](https://areit.wordpress.ncsu.edu/software-center-troubleshooting/)  
- [https://www.reddit.com/r/SCCM/comments/4poj0i/force_software_center_to_redownload_appsupdates/](https://www.reddit.com/r/SCCM/comments/4poj0i/force_software_center_to_redownload_appsupdates/)  
- [https://learn.microsoft.com/en-us/answers/questions/1694202/how-to-cleanup-ccmcache](https://learn.microsoft.com/en-us/answers/questions/1694202/how-to-cleanup-ccmcache)