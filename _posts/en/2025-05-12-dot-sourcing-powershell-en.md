---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast:free
title: Dot Sourcing PowerShell Scripts
translated: false
type: note
---

### Dot Sourcing PowerShell Functions in .ps1 Files

Dot sourcing (using the `.` operator) loads a PowerShell script (.ps1 file) into the current session's memory, making its functions and variables available for use without executing the script's top-level code. It's useful for importing modules or reusable code.

#### Basic Syntax

Run this command in your PowerShell session:

```
. Path\To\YourScript.ps1
```

- Replace `Path\To\YourScript.ps1` with the actual file path (use absolute paths for reliability).
- Example: `. C:\Scripts\MyFunctions.ps1` – This loads functions from that file into your session.

#### How It Works

- Functions defined in the script become callable in your current session.
- Variables are also imported, but only if they're not scoped locally.
- Avoid dot sourcing in production scripts; use modules for better organization.
- Tip: If the path has spaces, wrap it in quotes: `. "C:\My Scripts\Functions.ps1"`

Common issue: If the script has syntax errors, dot sourcing will fail with an error. Test by running `PowerShell -Command ". .\YourScript.ps1"` from a command prompt.

### Using PowerShell Execution Policy

Execution policies are security settings that restrict which scripts PowerShell can run, preventing malicious code execution. They're per-scope (e.g., machine-wide, user-specific).

#### Checking Current Policy

Run this in PowerShell:

```
Get-ExecutionPolicy
```

- Output examples: `Restricted` (blocks all scripts), `AllSigned` (only signed scripts), `RemoteSigned` (signed remote scripts, local allowed), or `Unrestricted`.

#### Setting or Changing Policy

Use `Set-ExecutionPolicy` (requires admin rights for machine-level changes):

- Example to allow locally written scripts: `Set-ExecutionPolicy RemoteSigned`
- Force without prompts: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Force`
- Per-scope: `Set-ExecutionPolicy -ExecutionPolicy AllSigned -Scope CurrentUser` (affects only your user account).

#### Common Policies

- `Restricted`: Default; no scripts run.
- `AllSigned`: Requires digital signatures (secure but inconvenient).
- `RemoteSigned`: Balances security—allows local scripts, signs remote ones.
- `Unrestricted`: Runs all scripts (risky; use cautiously).
- `Bypass`: Fully unrestricted, for automation.

Tip: Policies apply to console sessions, but not ISE or VS Code unless set. Test changes by running a sample script like `Write-Host "Hello"`. For more, see Microsoft's docs: `help about_Execution_Policies`. If in an enterprise, Group Policy might override local settings.
