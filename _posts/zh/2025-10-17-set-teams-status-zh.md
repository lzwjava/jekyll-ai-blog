---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 通过PowerShell设置Teams状态
translated: true
type: note
---

不，Microsoft Teams 并没有官方的独立命令行工具（比如简单的 `teams --status offline` 可执行文件）来设置您的在线状态。内置的斜杠命令（例如 `/away` 或 `/offline`）仅在 Teams 应用界面内有效，无法在终端中使用。

不过，您可以通过 PowerShell 和 Microsoft Graph API 在命令行中实现此功能。这需要安装 Microsoft Graph PowerShell SDK、使用您的 Microsoft 账户进行身份验证，并运行一个 cmdlet 来更新您的状态。以下是详细步骤：

### 前提条件

1. 安装 PowerShell（如果尚未安装；Windows 10 及以上版本已内置）。
2. 以管理员身份打开 PowerShell 并安装模块：

   ```
   Install-Module Microsoft.Graph -Scope CurrentUser
   ```

### 设置您的状态

1. 连接到 Microsoft Graph（这将通过浏览器提示进行身份验证）：

   ```
   Connect-MgGraph -Scopes "Presence.ReadWrite"
   ```

2. 运行 cmdlet 来设置您的状态。将 `YourUserId` 替换为您的 Microsoft Entra ID（Azure AD）用户 ID（您可以通过 `Get-MgUser -UserId your.email@domain.com` 获取）。常见的状态值包括：
   - `Available`（在线）
   - `Away`（离开）
   - `Busy`（忙碌）
   - `DoNotDisturb`（请勿打扰）
   - `Offline`（对他人显示为离线）

   设置为离线的示例：

   ```
   Set-MgUserPresence -UserId "YourUserId" -Presence "Offline"
   ```

   设置为离开的示例：

   ```
   Set-MgUserPresence -UserId "YourUserId" -Presence "Away"
   ```

3. 完成后断开连接：

   ```
   Disconnect-MgGraph
   ```

### 注意事项

- 这会立即更新您的状态，但可能会根据您的活动重置（例如，空闲时间会触发“离开”状态）。
- 对于自动化需求（例如，按计划切换状态的脚本），可以将上述命令包装在 `.ps1` 文件中，并通过任务计划程序运行。
- 如果您还想设置自定义状态消息（例如，“外出午餐”），请使用 `Set-MgUserPresenceStatusMessage`。
- 此方法适用于个人使用，但需要适当的权限；管理员可能需要启用 Graph API 访问。

若要在空闲期间保持“在线”状态（常见的变通方法），存在一些模拟活动的脚本（例如，每隔几分钟切换一次 Num Lock 键），但它们并非真正的状态设置工具。

参考资料：
[使用 MS Graph PowerShell 管理 Microsoft Teams 中的在线状态](https://m365scripts.com/microsoft-teams/manage-presence-status-in-microsoft-teams-using-ms-graph-powershell/)
[Set-MgUserPresence PowerShell Cmdlet 文档](https://learn.microsoft.com/en-us/powershell/module/microsoft.graph.users.actions/set-mguserpresence)
[关于通过 API/命令行设置 Teams 状态的 Reddit 讨论](https://www.reddit.com/r/teams/comments/1h5wee9/teams_status_with_api_command_line/)
