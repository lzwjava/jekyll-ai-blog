---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Set Teams Status via PowerShell
translated: false
type: note
---

No, Microsoft Teams does not have an official standalone command-line utility (like a simple `teams --status offline` executable) for setting your presence status. The built-in slash commands (e.g., `/away` or `/offline`) only work within the Teams app interface, not from a terminal.

However, you can achieve this via command line using PowerShell and the Microsoft Graph API. This requires installing the Microsoft Graph PowerShell SDK, authenticating with your Microsoft account, and running a cmdlet to update your presence. Here's a step-by-step guide:

### Prerequisites

1. Install PowerShell (if not already available; it's built into Windows 10+).
2. Open PowerShell as an administrator and install the module:

   ```
   Install-Module Microsoft.Graph -Scope CurrentUser
   ```

### Set Your Status

1. Connect to Microsoft Graph (this will prompt for authentication via browser):

   ```
   Connect-MgGraph -Scopes "Presence.ReadWrite"
   ```

2. Run the cmdlet to set your status. Replace `YourUserId` with your Microsoft Entra ID (Azure AD) user ID (you can get it via `Get-MgUser -UserId your.email@domain.com`). Common status values include:
   - `Available`
   - `Away`
   - `Busy`
   - `DoNotDisturb`
   - `Offline` (appears offline to others)

   Example to set to offline:

   ```
   Set-MgUserPresence -UserId "YourUserId" -Presence "Offline"
   ```

   Example to set to away:

   ```
   Set-MgUserPresence -UserId "YourUserId" -Presence "Away"
   ```

3. To disconnect when done:

   ```
   Disconnect-MgGraph
   ```

### Notes

- This updates your presence immediately, but it may reset based on your activity (e.g., idle time triggers "Away").
- For automation (e.g., scripts to toggle status on schedule), wrap the above in a `.ps1` file and run it via Task Scheduler.
- If you want to set a custom status message too (e.g., "Out for lunch"), use `Set-MgUserPresenceStatusMessage`.
- This works for personal use but requires appropriate permissions; admins might need to enable Graph API access.

For keeping your status "Available" during idle periods (common workaround), scripts exist that simulate activity (e.g., toggling Num Lock every few minutes), but they're not true status setters.

References:
[Manage Presence Status in Microsoft Teams Using MS Graph PowerShell](https://m365scripts.com/microsoft-teams/manage-presence-status-in-microsoft-teams-using-ms-graph-powershell/)
[Set-MgUserPresence PowerShell Cmdlet Docs](https://learn.microsoft.com/en-us/powershell/module/microsoft.graph.users.actions/set-mguserpresence)
[Reddit Thread on Teams Status via API/CLI](https://www.reddit.com/r/teams/comments/1h5wee9/teams_status_with_api_command_line/)
