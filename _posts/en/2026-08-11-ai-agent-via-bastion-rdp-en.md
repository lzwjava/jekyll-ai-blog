---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI Agent via Bastion RDP
translated: false
type: note
---

Question: How do I use an AI coding agent against a Windows Server 2012 box that's only reachable through a 深信服 (Sangfor) 运维审计/bastion RDP session — no direct SSH, no way to just point Claude Code at it?

Answer:

Two real options. Pick based on whether the bastion lets you push files/clipboard through.

**Option A — drop a native PowerShell agent loop on the box (best if file transfer is allowed)**

WS2012 has no `curl.exe`, no Python by default, and TLS 1.2 isn't the *default* SecurityProtocol for `Invoke-WebRequest`/`Invoke-RestMethod` — you'll get `Could not create SSL/TLS secure channel` unless you force it. So the whole thing has to be pure PS 5.1, no installs:

```powershell
# agent.ps1 — self-contained, no deps, runs on WS2012 native PowerShell 5.1
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$ApiKey = "<ANTHROPIC_API_KEY>"
$History = @()

function Call-Claude($msg) {
    $History += @{ role = "user"; content = $msg }
    $body = @{
        model      = "claude-sonnet-5"
        max_tokens = 1024
        system     = "You are a Windows Server 2012 sysadmin agent. Reply ONLY with a single PowerShell command to run next, or DONE if finished. No prose."
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

Getting it onto the box: Sangfor's 运维审计 (EOM/AC bastion) usually disables clipboard *and* drive redirection by default for compliance recording. If clipboard is off, you can't paste this — you either (1) ask the admin to enable text clipboard for your session (common exception even when file-drive redirect stays off), or (2) base64-encode the script, split into chunks under whatever the RDP text buffer allows, and reconstruct with `[System.Convert]::FromBase64String()` typed manually. If drive redirection is enabled, just drag-and-drop the `.ps1` in.

Also confirm outbound 443 to `api.anthropic.com` isn't blocked by the bastion's egress policy — 深信服 AC devices commonly whitelist by domain/App-ID, so this may need a firewall exception request.

**Option B — computer-use agent driving the RDP client itself (works even with zero file transfer)**

If clipboard and drive redirection are both locked down, don't fight the bastion — treat the RDP window on *your* local machine as the "screen" and drive it with a vision-based computer-use loop, same idea as Anthropic's reference computer-use implementation, just aimed at the mstsc window instead of a VM:

```python
# local machine only — controls the RDP client window via screenshot + mouse/keyboard
import pyautogui, base64, io
import anthropic

client = anthropic.Anthropic()

def screenshot_b64():
    img = pyautogui.screenshot()
    buf = io.BytesIO(); img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()

messages = [{"role": "user", "content": [
    {"type": "text", "text": "Task: check disk space on the remote server via the open RDP window, report result."},
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
# handle tool_use blocks -> pyautogui.click(x,y) / .typewrite() / screenshot loop
```

This never touches the server's filesystem or clipboard policy at all — it's just mouse/keyboard automation on a window you already legitimately have open, so it's invisible to the bastion's file-transfer/clipboard auditing (though keystroke/session logging on the bastion side will still record it, same as your own typing would).

For your case I'd default to **A** — you already ship CLI agents (ww/iclaw/zz), and a native PS loop is far more reliable than vision-based clicking on RDP, which lags and misreads text at low DPI. Only fall back to B if the bastion truly blocks both clipboard and drive redirection with no exception process.

References:

- [Enable TLS 1.2 on Windows Server 2012 — BonGuides](https://bonguides.com/how-to-enable-tls-1-2-on-windows-server-2012/)
- [Enable TLS 1.2 on clients — Microsoft Learn](https://learn.microsoft.com/en-us/intune/configmgr/core/plan-design/security/enable-tls-1-2-client)
- [Anthropic Messages API](https://docs.claude.com/en/api/messages)
- [Anthropic computer-use tool docs](https://docs.claude.com/en/docs/agents-and-tools/tool-use/computer-use-tool)
