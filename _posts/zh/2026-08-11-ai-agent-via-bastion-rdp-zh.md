---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过堡垒机RDP的AI代理
translated: true
type: note
---

问题：如何对一台只能通过深信服（Sangfor）运维审计/堡垒机RDP会话访问的Windows Server 2012机器使用AI编码代理——没有直接的SSH，也无法直接将Claude Code指向它？

答案：

有两种实际可行的方案。根据堡垒机是否允许推送文件/剪贴板来选择。

**方案 A — 在目标机器上部署原生PowerShell代理循环（如果允许文件传输，此为最佳方案）**

WS2012默认没有`curl.exe`或Python，而且TLS 1.2并非`Invoke-WebRequest`/`Invoke-RestMethod`的默认SecurityProtocol——除非强制指定，否则会遇到`Could not create SSL/TLS secure channel`错误。因此整个过程必须纯使用PS 5.1，无需额外安装：

```powershell
# agent.ps1 — 独立脚本，无依赖，运行于WS2012原生PowerShell 5.1
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$ApiKey = "<ANTHROPIC_API_KEY>"
$History = @()

function Call-Claude($msg) {
    $History += @{ role = "user"; content = $msg }
    $body = @{
        model      = "claude-sonnet-5"
        max_tokens = 1024
        system     = "你是一个Windows Server 2012系统管理员代理。请仅回复下一步要运行的单个PowerShell命令，如果已完成则回复DONE。不要添加任何说明性文字。"
        messages   = $History
    } | ConvertTo-Json -Depth 10

    $resp = Invoke-RestMethod -Uri "https://api.anthropic.com/v1/messages" `
        -Method Post -Headers @{
            "x-api-key"         = $ApiKey
            "anthropic-version" = "2023-06-01"
            "content-type"      = "application/json"
        } -Body $body

    $reply = $resp.content[0].text
    $History += @{ role = "assistant"; content = $reply }
    return $reply
}

$task = Read-Host "Task"
$cmd = Call-Claude $task
while ($cmd -ne "DONE") {
    Write-Host "> $cmd" -ForegroundColor Yellow
    try   { $out = Invoke-Expression $cmd 2>&1 | Out-String }
    catch { $out = $_.Exception.Message }
    Write-Host $out
    $cmd = Call-Claude "Output:`n$out`nNext command?"
}
```

将脚本放入目标机器：深信服的运维审计（EOM/AC堡垒机）出于合规审计需要，通常默认禁用剪贴板和驱动器重定向。如果剪贴板被禁用，你将无法粘贴此脚本——你可以：(1) 请求管理员为你的会话启用文本剪贴板（即使文件和驱动器重定向仍保持禁用，这也是常见例外）；或 (2) 将脚本进行Base64编码，拆分成符合RDP文本缓冲区限制的块，然后手动输入`[System.Convert]::FromBase64String()`命令进行重建。如果启用了驱动器重定向，直接将`.ps1`文件拖放进去即可。

另外，确认目标机器到`api.anthropic.com`的443端口出站流量未被堡垒机的出站策略阻止——深信服AC设备通常按域名/应用ID进行白名单控制，因此可能需要申请防火墙例外。

**方案 B — 使用计算机操控代理驱动RDP客户端本身（即使零文件传输也能工作）**

如果剪贴板和驱动器重定向都被锁定，不要与堡垒机硬抗——将你本地机器上的RDP窗口视为"屏幕"，并使用基于视觉的计算机操控循环来驱动它，原理与Anthropic的参考计算机操控实现相同，只是目标对准的是mstsc窗口而非虚拟机：

```python
# 仅在本地机器上运行——通过截图+鼠标/键盘控制RDP客户端窗口
import pyautogui, base64, io
import anthropic

client = anthropic.Anthropic()

def screenshot_b64():
    img = pyautogui.screenshot()
    buf = io.BytesIO(); img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()

messages = [{"role": "user", "content": [
    {"type": "text", "text": "任务：通过打开的RDP窗口检查远程服务器上的磁盘空间，并报告结果。"},
    {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": screenshot_b64()}}
]}]

resp = client.beta.messages.create(
    model="claude-sonnet-5",
    tools=[{"type": "computer_20250124", "name": "computer",
            "display_width_px": 1280, "display_height_px": 800}],
    betas=["computer-use-2025-01-24"],
    messages=messages,
    max_tokens=1024,
)
# 处理tool_use块 -> pyautogui.click(x,y) / .typewrite() / 截图循环
```

这种方法完全不会触及服务器的文件系统或剪贴板策略——它仅在你已经合法打开的窗口上进行鼠标/键盘自动化操作，因此对堡垒机的文件传输/剪贴板审计完全不可见（不过堡垒机侧的按键/会话日志仍然会记录，和你自己打字的效果一样）。

针对你的情况，我建议默认使用**方案A**——你已经熟悉CLI代理（ww/iclaw/zz），原生PowerShell循环远比基于视觉的RDP点击操作更可靠，因为后者存在延迟且在低DPI下会误读文本。只有当堡垒机确实同时阻止了剪贴板和驱动器重定向且无例外流程时，才退而求其次使用方案B。

参考资料：
- [在Windows Server 2012上启用TLS 1.2 — BonGuides](https://bonguides.com/how-to-enable-tls-1-2-on-windows-server-2012/)
- [在客户端启用TLS 1.2 — Microsoft Learn](https://learn.microsoft.com/en-us/intune/configmgr/core/plan-design/security/enable-tls-1-2-client)
- [Anthropic Messages API](https://docs.claude.com/en/api/messages)
- [Anthropic计算机操控工具文档](https://docs.claude.com/en/docs/agents-and-tools/tool-use/computer-use-tool)