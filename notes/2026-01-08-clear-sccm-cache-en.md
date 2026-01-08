---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: How to Safely Clear SCCM Cache
translated: false
type: note
---

Question: In Software Center on Windows, some failed packages, how to delete ccmcache to reinstall again?

Answer: 

The **Software Center** on Windows is part of Microsoft Endpoint Configuration Manager (formerly SCCM/MECM), where deployed applications, updates, and packages appear. Failed installations often occur due to corrupted or incomplete files in the client cache folder (**ccmcache**, typically located at `C:\Windows\ccmcache`). Clearing this cache forces the client to re-download the content, allowing a fresh reinstall attempt.

### Important Warnings
- **Do not manually delete files or folders directly from `C:\Windows\ccmcache` using File Explorer or command line**. This can corrupt the client's tracking of content, leading to further issues.
- Always use supported methods to clear the cache.

### Recommended Method: Clear Cache via Configuration Manager Properties
This is the official, safest way:

1. Open the Run dialog (Win + R) and type: `control smscfgrc` (or search for "Configuration Manager" in Control Panel).
2. In the **Configuration Manager Properties** window, go to the **Cache** tab.
3. Click **Configure Settings** (if prompted, enter admin credentials).
4. Click **Delete Files**.
5. Check the box for **Delete persisted cache content** (if available and needed).
6. Confirm with **Yes**.

This properly removes cached items and updates the client's internal tracking.

### After Clearing the Cache
1. Close and reopen **Software Center**.
2. Navigate to the failed package/application/update.
3. Click **Retry** or **Install** again.
   - It may initially show quick failure or 0% download—try retrying a second time, as it often starts downloading properly on the next attempt.

### Alternative Method: Using PowerShell (Advanced)
If you need to automate or clear selectively, run this PowerShell script as Administrator (it uses the official COM object to safely delete all cache items):

```powershell
$UIResourceMgr = New-Object -ComObject UIResource.UIResourceMgr
$Cache = $UIResourceMgr.GetCacheInfo()
$Cache.GetCacheElements() | ForEach-Object {
    $Cache.DeleteCacheElement($_.CacheElementID)
}
```

- Run this on the affected machine.
- Then retry the installation in Software Center.

### Additional Tips
- If failures persist, trigger client policy refresh: In Actions tab of Configuration Manager Properties, run **Machine Policy Retrieval & Evaluation Cycle** and **Application Deployment Evaluation Cycle**.
- Check logs (e.g., `C:\Windows\CCM\Logs`) for details on failures.
- In enterprise environments, admins can handle this remotely via tools like Right Click Tools.

This should resolve most failed package issues by forcing a clean re-download.

References:  

- [https://learn.microsoft.com/en-us/mem/configmgr/core/clients/manage/configure-client-cache](https://learn.microsoft.com/en-us/mem/configmgr/core/clients/manage/configure-client-cache)  
- [https://areit.wordpress.ncsu.edu/software-center-troubleshooting/](https://areit.wordpress.ncsu.edu/software-center-troubleshooting/)  
- [https://www.reddit.com/r/SCCM/comments/4poj0i/force_software_center_to_redownload_appsupdates/](https://www.reddit.com/r/SCCM/comments/4poj0i/force_software_center_to_redownload_appsupdates/)  
- [https://learn.microsoft.com/en-us/answers/questions/1694202/how-to-cleanup-ccmcache](https://learn.microsoft.com/en-us/answers/questions/1694202/how-to-cleanup-ccmcache)